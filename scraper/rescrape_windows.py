#!/usr/bin/env python3
"""
Targeted re-scrape for Windows & Doors category only.
Merges results into the existing data/providers.json.
Uses a longer timeout (40s) to handle slow SEAI responses.
"""

import requests
import json
import time
import re
import os
from bs4 import BeautifulSoup
from datetime import datetime

BASE_URL  = 'https://hes.seai.ie/GrantProcess/ContractorSearch.aspx'
OUTPUT    = os.path.join(os.path.dirname(__file__), '..', 'data', 'providers.json')
DELAY     = 1.0   # slightly more polite this time
TIMEOUT   = 40    # was 20 — doubled to handle slow server

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml',
    'Accept-Language': 'en-IE,en;q=0.9',
}

CATEGORY   = 'Windows & Doors'
CHECKBOXES = [
    'ctl00$DefaultContent$ContractorSearch1$dfSearch$ExternalWindowsAndDoors$ctl02$0',
]
GRID_PAGER_TARGET = 'ctl00$DefaultContent$ContractorSearch1$gridContractor$grid_pager'


def get_hidden_fields(soup):
    fields = {}
    for name in [
        '__VIEWSTATE', '__VIEWSTATEGENERATOR', '__EVENTVALIDATION',
        '__VIEWSTATEENCRYPTED', 'ctl00$forgeryToken',
    ]:
        el = soup.find('input', {'name': name})
        fields[name] = el['value'] if el and el.get('value') else ''
    return fields


def get_total_pages(soup):
    m = re.search(r'Total items:\s*(\d+)', soup.get_text())
    if m:
        total_items = int(m.group(1))
        return max(1, (total_items + 9) // 10), total_items
    return 1, 0


def parse_results_table(soup):
    rows = []
    total = 0
    total_m = re.search(r'Total items:\s*(\d+)', soup.get_text())
    if total_m:
        total = int(total_m.group(1))

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
    return rows, total


def normalise_county(raw):
    raw = raw.strip()
    if raw.lower().startswith('dublin'):
        return 'Dublin'
    if raw.lower() == 'co dublin':
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


def main():
    print(f'Windows & Doors re-scrape — {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')

    session = requests.Session()

    # --- Page 1 ---
    print('Fetching page 1...')
    r = session.get(BASE_URL, headers=HEADERS, timeout=TIMEOUT)
    soup = BeautifulSoup(r.text, 'html.parser')

    base_data = {
        '__EVENTTARGET':     '',
        '__EVENTARGUMENT':   '',
        '__SCROLLPOSITIONX': '0',
        '__SCROLLPOSITIONY': '0',
        **get_hidden_fields(soup),
    }
    for cb in CHECKBOXES:
        base_data[cb] = 'on'
    base_data['ctl00$DefaultContent$ContractorSearch1$dfSearch$search'] = 'Search'

    r2 = session.post(BASE_URL, data=base_data, headers=HEADERS, timeout=TIMEOUT)
    soup = BeautifulSoup(r2.text, 'html.parser')

    all_rows, _ = parse_results_table(soup)
    total_pages, total_items = get_total_pages(soup)
    print(f'  Page 1/{total_pages} — {len(all_rows)} rows (total: {total_items})')

    if total_items == 0:
        print('No results. Exiting.')
        return

    # --- Remaining pages ---
    for page_num in range(2, total_pages + 1):
        time.sleep(DELAY)
        page_data = {
            '__EVENTTARGET':     GRID_PAGER_TARGET,
            '__EVENTARGUMENT':   f'1${page_num}',
            '__SCROLLPOSITIONX': '0',
            '__SCROLLPOSITIONY': '0',
            **get_hidden_fields(soup),
        }
        for cb in CHECKBOXES:
            page_data[cb] = 'on'

        retries = 3
        for attempt in range(1, retries + 1):
            try:
                rp = session.post(BASE_URL, data=page_data, headers=HEADERS, timeout=TIMEOUT)
                soup = BeautifulSoup(rp.text, 'html.parser')
                rows, _ = parse_results_table(soup)
                if not rows:
                    print(f'  Page {page_num}: no rows returned — stopping early')
                    break
                all_rows.extend(rows)
                if page_num % 10 == 0 or page_num == total_pages:
                    print(f'  Page {page_num}/{total_pages} — running total: {len(all_rows)}')
                break
            except Exception as e:
                if attempt < retries:
                    print(f'  Page {page_num} attempt {attempt} failed ({e}) — retrying in 5s...')
                    time.sleep(5)
                else:
                    print(f'  ERROR on page {page_num} after {retries} attempts: {e}')
                    print(f'  Stopping at page {page_num}. Collected {len(all_rows)} rows so far.')
                    # Don't fully abort — save what we have
                    break
        else:
            continue
        # If inner loop broke due to empty rows, break outer too
        if not rows:
            break

    print(f'\nScraped {len(all_rows)} Windows & Doors rows.')

    # Build lookup from scraped data
    new_by_seai_id = {}
    for row in all_rows:
        sid = row['seai_id']
        if not sid:
            continue
        new_by_seai_id[sid] = row

    # --- Load existing providers.json ---
    with open(OUTPUT, 'r', encoding='utf-8') as f:
        existing = json.load(f)

    # Build seai_id → existing record lookup
    # seai_id is not stored in the output JSON — need to reconstruct
    # The original scraper dropped _seai_id. We'll match by name+county as fallback,
    # but actually the simplest path: rebuild from scratch merging both datasets.
    # Since we have all other categories complete, just add W&D to existing records
    # by name+county match, and add genuinely new providers.

    print('Merging into existing providers.json...')

    # Index existing by (name, county) since seai_id was stripped from output
    existing_by_key = {}
    for p in existing:
        key = (p['name'].strip().lower(), p['county'].strip().lower())
        existing_by_key[key] = p

    added_new   = 0
    added_cat   = 0
    already_had = 0

    for sid, row in new_by_seai_id.items():
        county = normalise_county(row['raw_county'])
        key    = (row['name'].strip().lower(), county.strip().lower())

        if key in existing_by_key:
            p = existing_by_key[key]
            if CATEGORY not in p['categories']:
                p['categories'].append(CATEGORY)
                p['description'] = make_description(
                    p['name'], p['county'], p['categories'], row['serviced_areas']
                )
                added_cat += 1
            else:
                already_had += 1
        else:
            # Genuinely new provider not in any other category
            phone  = format_phone(row['phone'])
            mobile = format_phone(row['mobile'])
            best_phone = phone if phone else mobile

            new_provider = {
                'id':          0,   # reassigned below
                'name':        row['name'],
                'county':      county,
                'categories':  [CATEGORY],
                'phone':       best_phone,
                'email':       row['email'].lower().strip(),
                'website':     '',
                'description': make_description(
                    row['name'], county, [CATEGORY], row['serviced_areas']
                ),
                'featured':    False,
            }
            existing.append(new_provider)
            existing_by_key[key] = new_provider
            added_new += 1

    print(f'  {added_cat} existing providers gained Windows & Doors category')
    print(f'  {added_new} new providers added')
    print(f'  {already_had} already had the category')

    # Re-sort and reassign sequential IDs
    existing.sort(key=lambda x: (x['county'], x['name']))
    for i, p in enumerate(existing, start=1):
        p['id'] = i

    with open(OUTPUT, 'w', encoding='utf-8') as f:
        json.dump(existing, f, indent=2, ensure_ascii=False)

    print(f'\nDone. {len(existing)} total providers in providers.json.')


if __name__ == '__main__':
    main()
