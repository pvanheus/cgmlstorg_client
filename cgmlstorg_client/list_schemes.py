#!/usr/bin/env python3


import re

from .utils import get

def get_cgmlst_schemes(base_url: str,
                       pattern:str | None = None,
                       exclude_pattern: str | None = None,
                       names_only: bool = False) -> list[dict]:
    
    base_response = get(base_url)

    scheme_list: list[dict[str, str]] = []
    for index, scheme in enumerate(base_response):
        if exclude_pattern is not None:
            if re.search(exclude_pattern, scheme['Scheme'], re.IGNORECASE):
                continue
        if pattern is not None:
            scheme_match = re.search(pattern, scheme['Scheme'])
            include_scheme = scheme_match is not None
        else:
            include_scheme = True
        if include_scheme:
            scheme_details = {}
            scheme_name = scheme['Scheme']
            scheme_details['name'] = scheme_name
            if not names_only:
                # name    id      description     locus_count     records last_added      last_updated
                scheme_details['id'] = index
                scheme_details['locus_count'] = scheme['Target Count']
                scheme_details['records'] = 'UNKNOWN'
                scheme_def = get(scheme['Scheme Href'])
                last_updated_match = re.search(r'\([^;]+, (\d+-\w+-\d+).*\)', scheme_def['Seed Genome'])
                if last_updated_match:
                    scheme_details['last_added'] = last_updated_match.group(1)
                else:
                    scheme_details['last_added'] = 'UNKNOWN'
                scheme_details['last_updated'] = scheme_def.get('Last Change', 'UNKNOWN')
            scheme_list.append(dict(scheme_details))
    return scheme_list        


def list_schemes(names_only: bool = False, base_url: str = 'https://cgmlst.org/ncs/api',
                 pattern: str | None = None, exclude_pattern: str | None = None):    
    fields = ['name', 'id', 'locus_count', 'records', 'last_added', 'last_updated']

    if names_only:
        print('name')
    else:
        print("\t".join(fields))
    
    for entry in get_cgmlst_schemes(base_url, pattern, exclude_pattern, names_only):
        if names_only:
            print(entry['name'])
        else:
            print('\t'.join(str(entry[field]) for field in fields))
