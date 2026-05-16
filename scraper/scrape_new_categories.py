#!/usr/bin/env python3
"""
Scrape Solar Heating and One-Stop-Shop (Project Coordinator) categories
from the SEAI contractor register and merge into data/providers.json.
"""

import requests
import json
import time
import re
import os
from bs4 import BeautifulSoup
from datetime import datetime

BASE_URL = 'https://hes.seai.ie/GrantProcess/ContractorSearch.aspx'
OUTPUT   = os.path.join(os.path.dirname(__file__), '..', 'data', 'providers.json')
DELAY    = 1.0
TIMEOUT  = 40

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml',
    'Accept-Language': 'en-IE,en;q=0.9',
}

SEARCH_CONFIGS = [
    {
        'category': 'Solar Thermal',
        'checkboxes': [
            'ctl00$DefaultContent$ContractorSearch1$dfSearch$SolarHeating$ctl02$0',
        ],
    },
    {
        'category': 'One-Stop-Shop Retrofit',
        'checkboxes': [
            'ctl00$DefaultContent$ContractorSearch1$dfSearch$ProjectCoordinator$ctl02$0',
        ],
    },
]

GRID_PAGER_TARGET = 'ctl00$DefaultContent$ContractorSearch1$gridContractor$grid_pager'


def get_hidden_fields(soup):
    fields = {}
    for name in ['__VIEWSTATE', '__VIEWSTATEGENERATOR', '__EVENTVALIDATION',
                  '__VIEWSTATEENCRYPTED', 'ctl00$forgeryToken']:
        el = soup.find('input', {'name': name})
        fields[name] = el['value'] if el and el.get('value') else ''
    return fields


def get_total_pages(soup):
    m = re.search(r'Total items:\s*(\d+)', soup.get_text())
    if m:
        total = int(m.group(1))
        return max(1, (total + 9) // 10), total
    return 1, 0


def parse_results_table(soup):
    rows = []
    for table in soup.find_all('table'):
        headers = [th.get_text(strip=True) for th in table.find_all('th')]
        if 'Company/Trading Name' not in headers:
            continue
        col = {h: i for i, h in enumerate(headers)}
        for tr in table.find_all('tr')[1:]:
            cells = [td.get_text(' ', strip=True) for td in tr.find_all('td')]
            if len(cells) < 6:
                continue
            rows.append({
                'seai_id':        cells[col.get('Contractor ID', 0)],
                'name':           cells[col.get('Company/Trading Name', 1)],
                'phone':          cells[col.get('Phone', 2)],
                'mobile':         cells[col.get('Mobile', 3)],
                'email':          cells[col.get('Email', 4)],
                'raw_county':     cells[col.get('County', 5)],
                'serviced_areas': cells[col.get('Serviced Areas', 6)] if len(cells) > 6 else '',
            })
        break
    return rows


def normalise_county(raw):
    raw = raw.strip()
    if raw.lower().startswith('dublin') or raw.lower() == 'co dublin':
        return 'Dublin'
    return raw


def format_phone(raw):
    digits = re.sub(r'\D', '', raw)
    if not digits:
        return ''
    if digits.startswith('08') and len(digits) == 10:
        return f'{digits[:3]} {digits[3:6]} {digits[6:]}'
    if digits.startswith('01') and len(digits) == 9:
        return f'{digits[:2]} {digits[2:5]} {digits[5:]}'
    if digits.startswith('0') and len(digits) == 10:
        return f'{digits[:3]} {digits[3:6]} {digits[6:]}'
    return raw.strip()


def make_description(name, county, categories, serviced_areas):
    cats = ' and '.join(categories)
    area = serviced_areas if serviced_areas else county
    return (
        f'SEAI registered {cats.lower()} contractor based in {county}. '
        f'Listed on the SEAI Better Energy Homes scheme register. '
        f'Serving: {area}.'
    )


def scrape_category(session, config):
    category   = config['category']
    checkboxes = config['checkboxes']
    print(f'\n{"="*60}\nCategory: {category}\n{"="*60}')

    r = session.get(BASE_URL, headers=HEADERS, timeout=TIMEOUT)
    soup = BeautifulSoup(r.text, 'html.parser')

    base_data = {
        '__EVENTTARGET': '', '__EVENTARGUMENT': '',
        '__SCROLLPOSITIONX': '0', '__SCROLLPOSITIONY': '0',
        **get_hidden_fields(soup),
    }
    for cb in checkboxes:
        base_data[cb] = 'on'
    base_data['ctl00$DefaultContent$ContractorSearch1$dfSearch$search'] = 'Search'

    r2 = session.post(BASE_URL, data=base_data, headers=HEADERS, timeout=TIMEOUT)
    soup = BeautifulSoup(r2.text, 'html.parser')

    all_rows = parse_results_table(soup)
    total_pages, total_items = get_total_pages(soup)
    print(f'  Page 1/{total_pages} — {len(all_rows)} rows (total: {total_items})')

    if total_items == 0:
        print('  No results.')
        return []

    for page_num in range(2, total_pages + 1):
        time.sleep(DELAY)
        page_data = {
            '__EVENTTARGET': GRID_PAGER_TARGET,
            '__EVENTARGUMENT': f'1${page_num}',
            '__SCROLLPOSITIONX': '0', '__SCROLLPOSITIONY': '0',
            **get_hidden_fields(soup),
        }
        for cb in checkboxes:
            page_data[cb] = 'on'

        for attempt in range(1, 4):
            try:
                rp = session.post(BASE_URL, data=page_data, headers=HEADERS, timeout=TIMEOUT)
                soup = BeautifulSoup(rp.text, 'html.parser')
                rows = parse_results_table(soup)
                if not rows:
                    print(f'  Page {page_num}: empty — stopping')
                    break
                all_rows.extend(rows)
                if page_num % 10 == 0 or page_num == total_pages:
                    print(f'  Page {page_num}/{total_pages} — running total: {len(all_rows)}')
                break
            except Exception as e:
                if attempt < 3:
                    print(f'  Page {page_num} attempt {attempt} failed ({e}) — retrying...')
                    time.sleep(5)
                else:
                    print(f'  ERROR page {page_num}: {e} — stopping')
                    return all_rows

    print(f'  Done: {len(all_rows)} rows')
    return all_rows


def main():
    print(f'SEAI new category scrape — {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')

    session = requests.Session()

    # Collect all new rows keyed by (name, county)
    new_rows_by_category = {}
    for config in SEARCH_CONFIGS:
        rows = scrape_category(session, config)
        new_rows_by_category[config['category']] = rows
        time.sleep(DELAY)

    # Load existing providers
    with open(OUTPUT, 'r', encoding='utf-8') as f:
        existing = json.load(f)

    existing_by_key = {}
    for p in existing:
        key = (p['name'].strip().lower(), p['county'].strip().lower())
        existing_by_key[key] = p

    for category, rows in new_rows_by_category.items():
        added_new = added_cat = already_had = 0
        for row in rows:
            if not row['seai_id']:
                continue
            county = normalise_county(row['raw_county'])
            key = (row['name'].strip().lower(), county.strip().lower())

            if key in existing_by_key:
                p = existing_by_key[key]
                if category not in p['categories']:
                    p['categories'].append(category)
                    p['description'] = make_description(p['name'], p['county'], p['categories'], row['serviced_areas'])
                    added_cat += 1
                else:
                    already_had += 1
            else:
                phone  = format_phone(row['phone'])
                mobile = format_phone(row['mobile'])
                new_p = {
                    'id':          0,
                    'name':        row['name'],
                    'county':      county,
                    'categories':  [category],
                    'phone':       phone if phone else mobile,
                    'email':       row['email'].lower().strip(),
                    'website':     '',
                    'description': make_description(row['name'], county, [category], row['serviced_areas']),
                    'featured':    False,
                }
                existing.append(new_p)
                existing_by_key[key] = new_p
                added_new += 1

        print(f'\n{category}: {added_new} new providers, {added_cat} existing gained category, {already_had} already had it')

    # Re-sort and reassign IDs
    existing.sort(key=lambda x: (x['county'], x['name']))
    for i, p in enumerate(existing, start=1):
        p['id'] = i

    with open(OUTPUT, 'w', encoding='utf-8') as f:
        json.dump(existing, f, indent=2, ensure_ascii=False)

    print(f'\nDone. {len(existing)} total providers in providers.json.')


if __name__ == '__main__':
    main()
