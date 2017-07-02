#!/usr/bin/env python3

import xlrd
from datetime import time

WEEK_FILE_NAME = '../raw/normalized_weekday_20170401.xls'
HOLY_FILE_NAME = '../raw/normalized_holiday_20170401.xls'
HEADER = 'trip_id,arrival_time,departure_time,stop_id,stop_sequence,stop_headsign,pickup_type,drop_off_type,shape_dist_travel,timepoint'


def create_stop_times(sheets, service_id):
    for sheet in sheets:
        for i in range(1, sheet.nrows):
            row = sheet.row_values(i)
            trip_id = sheet.name
            raw_time = int(row[3] * 24 * 3600)
            arrival_time = time(raw_time//3600, (raw_time % 3600)//60, raw_time % 60)
            stop_id = f'{row[1]}_{row[2]}'
            stop_seq = i
            pick_type = 0 if i is not sheet.nrows - 1 else 1
            drop_type = 0 if i is not 1 else 1
            stop_time = f'{trip_id},{arrival_time},{arrival_time},{stop_id},{stop_seq},,{pick_type},{drop_type},,'
            yield stop_time


def main():
    week_sheets_file = xlrd.open_workbook(WEEK_FILE_NAME).sheets()
    holy_sheets_file = xlrd.open_workbook(HOLY_FILE_NAME).sheets()

    week_stop_times = create_stop_times(week_sheets_file, 'weekday')
    holy_stop_times = create_stop_times(holy_sheets_file, 'holiday')

    print(HEADER)

    for s in week_stop_times:
        print(s)

    for s in holy_stop_times:
        print(s)


if __name__ == '__main__':
    main()
