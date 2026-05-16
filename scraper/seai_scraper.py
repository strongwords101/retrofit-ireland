#!/usr/bin/env python3
"""
SEAI Contractor Register Scraper — RetrofitList.ie
Scrapes hes.seai.ie/GrantProcess/ContractorSearch.aspx
Outputs data/providers.json in the RetrofitList.ie format.

Checkbox mapping (confirmed by probe):
  WallInsulation ctl02$0 = Cavity
  WallInsulation ctl02$1 = Dry-Lining (Internal)
  WallInsulation ctl02$2 = External
"""

import requests
import json
import time
import re
import sys
import os
from bs4 import BeautifulSoup
from datetime import datetime

BASE_URL   = 'https://hes.seai.ie/GrantProcess/ContractorSearch.aspx'
OUTPUT     = os.path.join(os.path.dirname(__file__), '..', 'data', 'providers.json')
LOG_FILE   = os.path.join(os.path.dirname(__file__), 'scrape_log.txt')
DELAY      = 0.8   # seconds between page requests — be polite
MAX_PAGES  = 999   # effectively unlimited

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml',
    'Accept-Language': 'en-IE,en;q=0.9',
}

# Each config: our category label + the checkboxes to tick for that search.
# Searching with no county = nationwide.
SEARCH_CONFIGS = [
    {
        'category': 'Attic & Floor Insulation',
        'checkboxes': [
            'ctl00$DefaultContent$ContractorSearch1$dfSearch$RoofInsulation$ctl02$0',
        ],
    },
    {
        'category': 'External Wall Insulation',
        'checkboxes': [
            'ctl00$DefaultContent$ContractorSearch1$dfSearch$WallInsulation$ctl02$2',
        ],
    },
    {
        'category': 'Internal Wall Insulation',
        'checkboxes': [
            'ctl00$DefaultContent$ContractorSearch1$dfSearch$WallInsulation$ctl02$0',
            'ctl00$DefaultContent$ContractorSearch1$dfSearch$WallInsulation$ctl02$1',
        ],
    },
    {
        'category': 'Heat Pumps',
        'checkboxes': [
            'ctl00$DefaultContent$ContractorSearch1$dfSearch$HeatPump$ctl02$0',
            'ctl00$DefaultContent$ContractorSearch1$dfSearch$HeatPump$ctl02$1',
            'ctl00$DefaultContent$ContractorSearch1$dfSearch$HeatPump$ctl02$2',
            'ctl00$DefaultContent$ContractorSearch1$dfSearch$HeatPump$ctl02$3',
            'ctl00$DefaultContent$ContractorSearch1$dfSearch$HeatPump$ctl02$4',
            'ctl00$DefaultContent$ContractorSearch1$dfSearch$HeatPump$ctl02$5',
        ],
    },
    {
        'category': 'Windows & Doors',
        'checkboxes': [
            'ctl00$DefaultContent$ContractorSearch1$dfSearch$ExternalWindowsAndDoors$ctl02$0',
        ],
    },
]

# Northern Ireland county IDs to skip (49-54); Republic only
NI_COUNTY_IDS = {49, 50, 51, 52, 53, 54}

# Normalise Dublin postcodes to just "Dublin"
def normalise_county(raw):
    raw = raw.strip()
    if raw.lower().startswith('dublin'):
        return 'Dublin'
    if raw.lower() == 'co dublin':
        return 'Dublin'
    return raw

def get_hidden_fields(soup):
    """Extract all ASP.NET hidden form fields from the page."""
    fields = {}
    for name in [
        '__VIEWSTATE', '__VIEWSTATEGENERATOR', '__EVENTVALIDATION',
        '__VIEWSTATEENCRYPTED', 'ctl00$forgeryToken',
    ]:
        el = soup.find('input', {'name': name})
        fields[name] = el['value'] if el and el.get('value') else ''
    return fields

GRID_PAGER_TARGET = 'ctl00$DefaultContent$ContractorSearch1$gridContractor$grid_pager'

def get_total_pages(soup):
    """Read 'Total items: N' from the page and return number of pages (10 per page)."""
    m = re.search(r'Total items:\s*(\d+)', soup.get_text())
    if m:
        total_items = int(m.group(1))
        return max(1, (total_items + 9) // 10), total_items
    return 1, 0

def parse_results_table(soup):
    """
    Find the results <table> and return list of dicts.
    Returns (rows, total_count).
    """
    rows = []
    total = 0

    # Try to find total count from page text
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
                'seai_id':       cells[col.get('Contractor ID', 0)],
                'name':          cells[col.get('Company/Trading Name', 1)],
                'phone':         cells[col.get('Phone', 2)],
                'mobile':        cells[col.get('Mobile', 3)],
                'email':         cells[col.get('Email', 4)],
                'raw_county':    cells[col.get('County', 5)],
                'serviced_areas': cells[col.get('Serviced Areas', 6)] if len(cells) > 6 else '',
            })
        break  # found the right table

    return rows, total

def scrape_category(session, config, log):
    category   = config['category']
    checkboxes = config['checkboxes']

    log(f'\n{"="*60}')
    log(f'Category: {category}')
    log(f'{"="*60}')

    # --- Page 1 ---
    r = session.get(BASE_URL, headers=HEADERS, timeout=20)
    soup = BeautifulSoup(r.text, 'html.parser')

    base_data = {
        '__EVENTTARGET':    '',
        '__EVENTARGUMENT':  '',
        '__SCROLLPOSITIONX': '0',
        '__SCROLLPOSITIONY': '0',
        **get_hidden_fields(soup),
    }
    for cb in checkboxes:
        base_data[cb] = 'on'
    base_data['ctl00$DefaultContent$ContractorSearch1$dfSearch$search'] = 'Search'

    r2 = session.post(BASE_URL, data=base_data, headers=HEADERS, timeout=20)
    soup = BeautifulSoup(r2.text, 'html.parser')

    all_rows, _ = parse_results_table(soup)
    total_pages, total_items = get_total_pages(soup)
    log(f'  Page 1/{total_pages} — {len(all_rows)} rows (total contractors: {total_items})')

    if total_items == 0:
        log('  No results — skipping.')
        return []

    # --- Remaining pages: POST directly with page number (1$N format) ---
    for page_num in range(2, total_pages + 1):
        time.sleep(DELAY)
        page_data = {
            '__EVENTTARGET':     GRID_PAGER_TARGET,
            '__EVENTARGUMENT':   f'1${page_num}',
            '__SCROLLPOSITIONX': '0',
            '__SCROLLPOSITIONY': '0',
            **get_hidden_fields(soup),
        }
        for cb in checkboxes:
            page_data[cb] = 'on'

        try:
            rp = session.post(BASE_URL, data=page_data, headers=HEADERS, timeout=20)
            soup = BeautifulSoup(rp.text, 'html.parser')
            rows, _ = parse_results_table(soup)
            if not rows:
                log(f'  Page {page_num}: no rows returned — stopping early')
                break
            all_rows.extend(rows)
            if page_num % 10 == 0 or page_num == total_pages:
                log(f'  Page {page_num}/{total_pages} — running total: {len(all_rows)}')
        except Exception as e:
            log(f'  ERROR on page {page_num}: {e}')
            break

    log(f'  Done: {len(all_rows)} rows for {category}')
    return all_rows

def make_description(name, county, categories, serviced_areas):
    cats = ' and '.join(categories)
    area = serviced_areas if serviced_areas else county
    return (
        f'SEAI registered {cats.lower()} contractor based in {county}. '
        f'Listed on the SEAI Better Energy Homes scheme register. '
        f'Serving: {area}.'
    )

def format_phone(raw):
    """Normalise Irish phone numbers to standard spacing."""
    digits = re.sub(r'\D', '', raw)
    if not digits:
        return ''
    # Irish mobile: 08x xxx xxxx
    if digits.startswith('08') and len(digits) == 10:
        return f'{digits[:3]} {digits[3:6]} {digits[6:]}'
    # Dublin landline: 01 xxx xxxx
    if digits.startswith('01') and len(digits) == 9:
        return f'{digits[:2]} {digits[2:5]} {digits[5:]}'
    # Other landlines: 0xx xxx xxxx
    if digits.startswith('0') and len(digits) == 10:
        return f'{digits[:3]} {digits[3:6]} {digits[6:]}'
    return raw.strip()

def main():
    log_lines = []

    def log(msg):
        print(msg, flush=True)
        log_lines.append(msg)

    log(f'RetrofitList.ie SEAI Scraper — {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    log(f'Output: {os.path.abspath(OUTPUT)}')

    session = requests.Session()

    # seai_id → merged contractor dict
    contractors = {}

    for config in SEARCH_CONFIGS:
        rows = scrape_category(session, config, log)
        category = config['category']

        for row in rows:
            sid = row['seai_id']
            county = normalise_county(row['raw_county'])

            # Skip Northern Ireland
            if not sid:
                continue

            if sid in contractors:
                # Add category if not already present
                if category not in contractors[sid]['categories']:
                    contractors[sid]['categories'].append(category)
            else:
                phone  = format_phone(row['phone'])
                mobile = format_phone(row['mobile'])
                best_phone = phone if phone else mobile

                contractors[sid] = {
                    '_seai_id':      sid,
                    'name':          row['name'],
                    'county':        county,
                    'categories':    [category],
                    'phone':         best_phone,
                    'email':         row['email'].lower().strip(),
                    'website':       '',
                    'serviced_areas': row['serviced_areas'],
                    'description':   '',  # filled in below after categories known
                    'featured':      False,
                }

        time.sleep(DELAY)

    # Generate descriptions now that all categories are known
    for sid, c in contractors.items():
        c['description'] = make_description(
            c['name'], c['county'], c['categories'], c['serviced_areas']
        )

    # Build final list sorted by county then name
    provider_list = sorted(
        contractors.values(),
        key=lambda x: (x['county'], x['name'])
    )

    # Assign sequential IDs, drop internal fields
    output = []
    for i, p in enumerate(provider_list, start=1):
        output.append({
            'id':          i,
            'name':        p['name'],
            'county':      p['county'],
            'categories':  p['categories'],
            'phone':       p['phone'],
            'email':       p['email'],
            'website':     p['website'],
            'description': p['description'],
            'featured':    p['featured'],
        })

    os.makedirs(os.path.dirname(os.path.abspath(OUTPUT)), exist_ok=True)
    with open(OUTPUT, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    log(f'\n{"="*60}')
    log(f'COMPLETE: {len(output)} unique providers written to providers.json')
    log(f'{"="*60}')

    # Write log file
    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(log_lines))

    # Print summary by category
    from collections import Counter
    cat_counts = Counter()
    for p in output:
        for c in p['categories']:
            cat_counts[c] += 1
    log('\nBreakdown by category:')
    for cat, count in sorted(cat_counts.items()):
        log(f'  {cat}: {count}')

if __name__ == '__main__':
    main()
