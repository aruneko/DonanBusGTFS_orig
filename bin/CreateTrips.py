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


def create_trip(sheet, service_id):
    col_nums = sheet.ncols
    trip_nums = range(1, col_nums - 4)
    route_id = sheet.name
    return [f"{route_id},{service_id},{route_id}_{service_id}_{n},,,{get_dir(route_id)},,,0,0,,," for n in trip_nums]


def create_trips(sheets, service_id):
    return chain.from_iterable([create_trip(sheet, service_id) for sheet in sheets])


def main():
    week_sheets_file = xlrd.open_workbook(WEEK_FILE_NAME).sheets()
    holy_sheets_file = xlrd.open_workbook(HOLY_FILE_NAME).sheets()

    raw_week_sheets = extract_valid_sheets(week_sheets_file)
    raw_holy_sheets = extract_valid_sheets(holy_sheets_file)

    week_trips = create_trips(raw_week_sheets, 'weekday')
    holy_trips = create_trips(raw_holy_sheets, 'holiday')

    print(HEADER)

    for t in week_trips:
        print(t)

    for t in holy_trips:
        print(t)


if __name__ == '__main__':
    main()
