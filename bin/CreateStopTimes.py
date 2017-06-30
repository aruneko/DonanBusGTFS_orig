#!/usr/bin/env python3

import xlrd
from pandas import read_csv
from itertools import chain
from unicodedata import normalize
from CreateTrips import get_service_id
from LoadStops import find_stop_id

WEEK_FILE_NAME = '../raw/timetable_weekday_20170401.xls'
HOLY_FILE_NAME = '../raw/timetable_holyday_20170401.xls'
HEADER = 'trip_id,arrival_time,departure_time,stop_id,stop_sequence,stop_headsign,pickup_type,drop_off_type,shape_dist_travel,timepoint'
STOPS_CSV = read_csv('../gtfs/stops.txt')


def extract_valid_sheets(sheets_file):
    return [s for s in sheets_file if int(s.name) < 140000 and s.ncols != 2]


def extract_time(trip_id, sheet):
    stop_ids = [(trip_id, find_stop_id(sheet.row_values(n)[2], normalize('NFKC', sheet.row_values(n)[1])), sheet.row_values(n)[1]) for n in range(6, sheet.nrows - 5)]
    return stop_ids


def create_stop_time(sheet, service_id):
    col_nums = sheet.ncols
    trip_nums = range(1, col_nums - 4)
    route_id = sheet.name
    trip_ids = [f'{route_id}_{get_service_id(service_id, route_id, n)}_{n}' for n in trip_nums]
    stop_times = [extract_time(t, sheet) for t in trip_ids]
    return stop_times


def create_stop_times(sheets, service_id):
    return chain.from_iterable([create_stop_time(sheet, service_id) for sheet in sheets])


def main():
    week_sheets_file = xlrd.open_workbook(WEEK_FILE_NAME).sheets()
    holy_sheets_file = xlrd.open_workbook(HOLY_FILE_NAME).sheets()

    raw_week_sheets = extract_valid_sheets(week_sheets_file)
    raw_holy_sheets = extract_valid_sheets(holy_sheets_file)

    week_stop_times = create_stop_times(raw_week_sheets, 'weekday')
    holy_stop_times = create_stop_times(raw_holy_sheets, 'holiday')

    print(HEADER)

    for s in week_stop_times:
        print(s)

    for s in holy_stop_times:
        print(s)


if __name__ == '__main__':
    main()
