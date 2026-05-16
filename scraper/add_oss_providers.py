#!/usr/bin/env python3
"""
Add SEAI-approved One-Stop-Shop retrofit providers to data/providers.json.
Source: solarinfo.ie/one-stop-shops-directory (32 providers, verified May 2026)
Contact details gathered from individual company websites where accessible.
"""

import json
import os

OUTPUT = os.path.join(os.path.dirname(__file__), '..', 'data', 'providers.json')

CATEGORY = 'One-Stop-Shop Retrofit'

OSS_PROVIDERS = [
    {
        'name': 'Activ8 Solar Energies',
        'county': 'Monaghan',
        'phone': '',
        'email': '',
        'website': 'https://www.activ8solar.ie',
    },
    {
        'name': 'Ashgrove Renewables',
        'county': 'Cork',
        'phone': '',
        'email': '',
        'website': 'https://ashgrove.ie',
    },
    {
        'name': 'Aspen Eco Power',
        'county': 'Carlow',
        'phone': '',
        'email': '',
        'website': '',
    },
    {
        'name': 'Bayview Contracts',
        'county': 'Dublin',
        'phone': '',
        'email': '',
        'website': '',
    },
    {
        'name': 'Bord Gáis Energy',
        'county': 'Dublin',
        'phone': '1850 632 632',
        'email': '',
        'website': 'https://www.bordgaisenergy.ie',
    },
    {
        'name': 'Breffni Insulation',
        'county': 'Cavan',
        'phone': '',
        'email': '',
        'website': '',
    },
    {
        'name': 'Churchfield Home Services',
        'county': 'Mayo',
        'phone': '',
        'email': '',
        'website': '',
    },
    {
        'name': 'Cooper Insulation',
        'county': 'Meath',
        'phone': '046 924 6730',
        'email': 'info@cooperinsulation.ie',
        'website': 'https://cooperinsulation.ie',
    },
    {
        'name': 'Electric Ireland Superhomes',
        'county': 'Tipperary',
        'phone': '0818 600 700',
        'email': 'info@electricirelandsuperhomes.ie',
        'website': 'https://electricirelandsuperhomes.ie',
    },
    {
        'name': 'Energlaze Home Energy Upgrades',
        'county': 'Wexford',
        'phone': '01 901 1635',
        'email': 'info@energlaze.ie',
        'website': 'https://www.energlaze.ie',
    },
    {
        'name': 'Energyfix',
        'county': 'Dublin',
        'phone': '',
        'email': '',
        'website': '',
    },
    {
        'name': 'Energywise Ireland',
        'county': 'Cork',
        'phone': '',
        'email': '',
        'website': 'https://energywiseireland.ie',
    },
    {
        'name': 'Envirobead',
        'county': 'Cork',
        'phone': '',
        'email': '',
        'website': 'https://envirobead.ie',
    },
    {
        'name': 'Greenwatt',
        'county': 'Cavan',
        'phone': '046 924 5851',
        'email': 'info@greenwatt.ie',
        'website': 'https://greenwatt.ie',
    },
    {
        'name': 'Home Comfort Retrofits',
        'county': 'Kildare',
        'phone': '',
        'email': '',
        'website': '',
    },
    {
        'name': 'House2Home Retrofit',
        'county': 'Dublin',
        'phone': '',
        'email': '',
        'website': '',
    },
    {
        'name': 'Insulex',
        'county': 'Clare',
        'phone': '021 477 8562',
        'email': 'info@insulex.ie',
        'website': 'https://insulex.ie',
    },
    {
        'name': 'Integrate Home Energy Upgrades',
        'county': 'Wicklow',
        'phone': '',
        'email': '',
        'website': '',
    },
    {
        'name': 'Kingdom Installation',
        'county': 'Kerry',
        'phone': '',
        'email': '',
        'website': '',
    },
    {
        'name': 'Kingspan Insulation',
        'county': 'Carlow',
        'phone': '',
        'email': '',
        'website': 'https://www.kingspan.com/ie',
    },
    {
        'name': 'KORE Retrofit',
        'county': 'Cavan',
        'phone': '049 437 4002',
        'email': 'info@koreretrofit.com',
        'website': 'https://www.koreretrofit.com',
    },
    {
        'name': 'Larkrock',
        'county': 'Dublin',
        'phone': '',
        'email': '',
        'website': 'https://larkrock.ie',
    },
    {
        'name': 'Leetherm Project Management',
        'county': 'Tipperary',
        'phone': '',
        'email': '',
        'website': '',
    },
    {
        'name': 'Lough Projects',
        'county': 'Dublin',
        'phone': '',
        'email': '',
        'website': '',
    },
    {
        'name': 'NRG Panel',
        'county': 'Monaghan',
        'phone': '',
        'email': '',
        'website': '',
    },
    {
        'name': 'OHK Energy',
        'county': 'Monaghan',
        'phone': '',
        'email': '',
        'website': '',
    },
    {
        'name': 'Rend Master',
        'county': 'Mayo',
        'phone': '',
        'email': '',
        'website': '',
    },
    {
        'name': 'Retrofit Design',
        'county': 'Kerry',
        'phone': '066 976 2746',
        'email': 'info@retrofitdesignltd.ie',
        'website': 'https://retrofitdesign.ie',
    },
    {
        'name': 'Retrofit Energy Ireland',
        'county': 'Meath',
        'phone': '',
        'email': '',
        'website': '',
    },
    {
        'name': 'SE Systems',
        'county': 'Cork',
        'phone': '',
        'email': '',
        'website': '',
    },
    {
        'name': 'SSE Airtricity Energy Services',
        'county': 'Carlow',
        'phone': '1800 222 333',
        'email': '',
        'website': 'https://www.sseairtricity.com/ie/home',
    },
    {
        'name': 'WiEnergy',
        'county': 'Waterford',
        'phone': '',
        'email': '',
        'website': '',
    },
]


def make_description(name, county, categories, website):
    cats = ' and '.join(categories)
    area = 'nationwide' if website and any(k in name.lower() for k in ['bord gáis', 'electric ireland', 'sse', 'kore', 'ashgrove']) else county
    return (
        f'SEAI-approved {cats.lower()} provider based in {county}. '
        f'Manages the full retrofit process end-to-end — survey, design, installation, and grant paperwork. '
        f'Serving: {area}.'
    )


def main():
    with open(OUTPUT, 'r', encoding='utf-8') as f:
        existing = json.load(f)

    existing_by_key = {}
    for p in existing:
        key = p['name'].strip().lower()
        existing_by_key[key] = p

    added_new = added_cat = already_had = 0

    for oss in OSS_PROVIDERS:
        key = oss['name'].strip().lower()

        if key in existing_by_key:
            p = existing_by_key[key]
            if CATEGORY not in p['categories']:
                p['categories'].append(CATEGORY)
                # Update website if we have one and they don't
                if oss['website'] and not p.get('website'):
                    p['website'] = oss['website']
                p['description'] = make_description(p['name'], p['county'], p['categories'], p.get('website', ''))
                added_cat += 1
            else:
                already_had += 1
        else:
            new_p = {
                'id':          0,
                'name':        oss['name'],
                'county':      oss['county'],
                'categories':  [CATEGORY],
                'phone':       oss['phone'],
                'email':       oss['email'],
                'website':     oss['website'],
                'description': make_description(oss['name'], oss['county'], [CATEGORY], oss['website']),
                'featured':    False,
            }
            existing.append(new_p)
            existing_by_key[key] = new_p
            added_new += 1

    print(f'{added_new} new OSS providers added')
    print(f'{added_cat} existing providers gained One-Stop-Shop category')
    print(f'{already_had} already had the category')

    existing.sort(key=lambda x: (x['county'], x['name']))
    for i, p in enumerate(existing, start=1):
        p['id'] = i

    with open(OUTPUT, 'w', encoding='utf-8') as f:
        json.dump(existing, f, indent=2, ensure_ascii=False)

    print(f'\nDone. {len(existing)} total providers in providers.json.')


if __name__ == '__main__':
    main()
