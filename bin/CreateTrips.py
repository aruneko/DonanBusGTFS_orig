#!/usr/bin/env python3

import xlrd
from itertools import chain
from util import WEEKDAY_FILE_NAME, WEEKEND_FILE_NAME, extract_valid_sheets

HEADER = 'route_id,service_id,trip_id,trip_headsign,trip_short_name,direction_id,block_id,' \
         'shape_id,wheelchair_accessible,bikes_allowed,jp_trip_desc,jp_trip_desc_symbol,jp_office_id'


def get_dir(route_id):
    if route_id[-2:] == '00':
        return '1'
    else:
        return '0'


def create_trip(sheet, service_id, shapes):
    col_nums = sheet.ncols
    trip_nums = range(1, col_nums - 4)
    route_id = sheet.name
    pair = [(service_id, n) for n in trip_nums]
    shape_id = [sh[1] for sh in shapes if sh[0] == sheet.name][0]
    return [f"{route_id},{s},{route_id}_{s}_{n},,,{get_dir(route_id)},,{shape_id},0,0,,," for s, n in pair]


def create_trips(sheets, service_id, shapes):
    return chain.from_iterable([create_trip(sheet, service_id, shapes) for sheet in sheets])


def main():
    weekday_sheets_file = xlrd.open_workbook(WEEKDAY_FILE_NAME).sheets()
    weekend_sheets_file = xlrd.open_workbook(WEEKEND_FILE_NAME).sheets()

    raw_weekday_sheets = extract_valid_sheets(weekday_sheets_file)
    raw_weekend_sheets = extract_valid_sheets(weekend_sheets_file)

    shape_file = open('../raw/trip_shape.csv', 'r').readlines()
    shapes = [s[:-1].split(',') for s in shape_file]

    weekday_trips = create_trips(raw_weekday_sheets, 'weekday', shapes)
    weekend_trips = create_trips(raw_weekend_sheets, 'weekend', shapes)

    print(HEADER)

    for t in weekday_trips:
        print(t)

    for t in weekend_trips:
        print(t)


if __name__ == '__main__':
    main()
