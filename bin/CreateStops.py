#!/usr/bin/env python3

import requests
from itertools import groupby, chain
from functools import reduce

API_BASE_URL = 'http://overpass-api.de/api/interpreter?data='
REQUEST_QUERY = '''
    [out:json];
    area["name"~"室蘭市|登別市"];
    node(area)["highway"="bus_stop"];
    out body;
'''
API_URL = API_BASE_URL + REQUEST_QUERY
HEADER = 'stop_id,stop_code,stop_name,stop_desc,stop_lat,stop_lon,zone_id,' \
         'stop_url,location_type,parent_station,stop_timezone,wheelchair_boarding'


def f_chain(*args):
    return reduce(lambda x, f: f(x), args)


def fetch_json():
    return requests.get(API_URL).json()


def extract_elements(raw_json):
    return raw_json['elements']


def has_ref(node):
    return 'ref' in node['tags']


def has_desc(node):
    return 'description' in node['tags'].keys()


def extract_valid_nodes(nodes):
    return [node for node in nodes if has_ref(node)]


def sort_nodes(nodes):
    return sorted(nodes, key=lambda node: node['tags']['ref'])


def create_pole(node):
    n = node
    t = n['tags']
    refs = t['ref'].split()
    if has_desc(node):
        return [f"{ref},,{t['name']},{t['description']},{n['lat']},{n['lon']},,,0,{ref[:-2]},," for ref in refs]
    else:
        return [f"{ref},,{t['name']},,{n['lat']},{n['lon']},,,0,{ref[:-2]},," for ref in refs]


def create_poles(nodes):
    return chain.from_iterable([create_pole(node) for node in nodes])


def create_stop(nodes):
    lat = sum([float(n['lat']) for n in nodes]) / len(nodes)
    lon = sum([float(n['lon']) for n in nodes]) / len(nodes)
    name = nodes[0]['tags']['name']
    ref = nodes[0]['tags']['ref'][:4]
    return f"{ref},,{name},,{lat},{lon},,,1,,,"


def create_stops(nodes):
    grouped = groupby(nodes, lambda n: n['tags']['ref'][:4])
    return [create_stop(list(g[1])) for g in grouped]


def main():
    nodes = f_chain(fetch_json(),
                    extract_elements,
                    extract_valid_nodes,
                    sort_nodes)

    poles = create_poles(nodes)
    stops = create_stops(nodes)

    print(HEADER)

    for p in poles:
        print(p)

    for s in stops:
        print(s)


if __name__ == "__main__":
    main()
