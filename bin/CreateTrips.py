#!/usr/bin/env python3

import xlrd
from itertools import chain

WEEK_FILE_NAME = '../raw/timetable_weekday_20170401.xls'
HOLY_FILE_NAME = '../raw/timetable_holyday_20170401.xls'
HEADER = 'route_id,service_id,trip_id,trip_headsign,trip_shot_name,direction_id,block_id,shape_id,wheelchair_accesible,bikes_allowed,jp_trip_desc,jp_trip_desc_symbol,jp_office_id'


def extract_valid_sheets(sheets_file):
    return [s for s in sheets_file if int(s.name) < 140000 and s.ncols != 2]


def get_dir(route_id):
    if route_id[-2:] == '00':
        return '1'
    else:
        return '0'


def get_service_id(service_id, route_id, n):
    if service_id == 'weekday' and route_id == '108700' and n == 2:
        return 'seiryo'
    elif route_id == '120700' or \
            route_id == '120800' or \
            route_id == '120900' or \
            route_id == '123800' or \
            route_id == '123810' or \
            route_id == '124210' or \
            route_id == '124400' or \
            route_id == '126710' or \
            route_id == '127100' or \
            route_id == '127200' or \
            route_id == '127310':
        return 'shimizu'
    elif route_id == '121000':
        return 'tosho'
    elif service_id == 'weekday' and route_id == '131100' and n == 2:
        return 'seiryo_akebi'
    else:
        return service_id


def create_trip(sheet, service_id, shapes):
    col_nums = sheet.ncols
    trip_nums = range(1, col_nums - 4)
    route_id = sheet.name
    pair = [(get_service_id(service_id, route_id, n), n) for n in trip_nums]
    shape_id = [sh[1] for sh in shapes if sh[0] == sheet.name][0]
    return [f"{route_id},{s},{route_id}_{s}_{n},,,{get_dir(route_id)},,{shape_id},0,0,,," for s, n in pair]


def create_trips(sheets, service_id, shapes):
    return chain.from_iterable([create_trip(sheet, service_id, shapes) for sheet in sheets])


def main():
    week_sheets_file = xlrd.open_workbook(WEEK_FILE_NAME).sheets()
    holy_sheets_file = xlrd.open_workbook(HOLY_FILE_NAME).sheets()

    raw_week_sheets = extract_valid_sheets(week_sheets_file)
    raw_holy_sheets = extract_valid_sheets(holy_sheets_file)

    shape_file = open('../raw/trip_shape.csv', 'r').readlines()
    shapes = [s[:-1].split(',') for s in shape_file]

    week_trips = create_trips(raw_week_sheets, 'weekday', shapes)
    holy_trips = create_trips(raw_holy_sheets, 'holiday', shapes)

    print(HEADER)

    for t in week_trips:
        print(t)

    for t in holy_trips:
        print(t)


if __name__ == '__main__':
    main()
