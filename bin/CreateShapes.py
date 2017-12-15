#!/usr/bin/env python3

import math
import requests


def create_req():
    entry_url = 'http://overpass-api.de/api/interpreter?data='
    query = '[out:json];area["name"~"室蘭市|登別市"];rel(area)[route=bus];out geom;'
    return requests.get(entry_url + query).json()['elements']


def extract_position(way):
    if way['role'] == 'forward':
        return way['geometry']
    else:
        return list(reversed(way['geometry']))


def concat_position(src, res):
    if len(src) == 1:
        return res + src[0]
    else:
        return concat_position(src[1:], res + src[0][:-1])


def create_shape(rel):
    rel_id = rel['id']
    ways = [w for w in rel['members'] if w['role'] != 'stop']
    geoms = [extract_position(g) for g in ways]
    return rel_id, concat_position(geoms, [])


def lat_to_km(lat):
    pole_r = 6356.752314
    return 2 * math.pi * pole_r / 360 * lat


def lon_to_km(lat, lon):
    eq_r = 6378.137
    return 2 * math.pi * eq_r * math.cos(math.radians(lat)) / 360 * lon


def calc_dist(lat_prev, lon_prev, lat, lon):
    lat_diff = lat_to_km(abs(lat - lat_prev))
    lat_ave = (lat_prev + lat) / 2
    lon_diff = lon_to_km(lat_ave, abs(lon_prev - lon))
    return math.sqrt(pow(lat_diff, 2) + pow(lon_diff, 2))


def main():
    print('shape_id,shape_pt_lat,shape_pt_lon,shape_pt_sequence,shape_dist_traveled')
    shapes = [create_shape(r) for r in create_req()]
    for (s_id, shape) in shapes:
        diff = 0
        lat_prev, lon_prev = (shape[0]['lat'], shape[0]['lon'])
        for (i, s) in enumerate(shape):
            diff += calc_dist(lat_prev, lon_prev, s['lat'], s['lon'])
            lat_prev, lon_prev = (s['lat'], s['lon'])
            print(f"{s_id},{s['lat']},{s['lon']},{i},{diff}")


if __name__ == '__main__':
    main()
