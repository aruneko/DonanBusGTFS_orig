#!/usr/bin/env python3

import xlrd

WEEKDAY_FILE_NAME = '../raw/normalized_weekday_20170401.xls'
WEEKEND_FILE_NAME = '../raw/normalized_weekend_20170401.xls'
HEADER = 'trip_id,arrival_time,departure_time,stop_id,stop_sequence,' \
         'stop_headsign,pickup_type,drop_off_type,shape_dist_traveled,timepoint'


def create_stop_times(sheets, book):
    for sheet in sheets:
        for i in range(1, sheet.nrows):
            row = sheet.row_values(i)
            trip_id = sheet.name
            arrival_time = xlrd.xldate.xldate_as_datetime(row[3], book.datemode).strftime('%H:%M:%S')
            stop_id = f'{row[1]}_{row[2]}'
            stop_seq = i
            pick_type = 3 if i is not sheet.nrows - 1 else 1
            drop_type = 3 if i is not 1 else 1
            stop_time = f'{trip_id},{arrival_time},{arrival_time},{stop_id},{stop_seq},,{pick_type},{drop_type},,'
            yield stop_time


def main():
    weekday_workbook = xlrd.open_workbook(WEEKDAY_FILE_NAME)
    weekend_workbook = xlrd.open_workbook(WEEKEND_FILE_NAME)

    weekday_sheets_file = weekday_workbook.sheets()
    weekend_sheets_file = weekend_workbook.sheets()

    weekday_stop_times = create_stop_times(weekday_sheets_file, weekday_workbook)
    weekend_stop_times = create_stop_times(weekend_sheets_file, weekend_workbook)

    print(HEADER)

    for s in weekday_stop_times:
        print(s)

    for s in weekend_stop_times:
        print(s)


if __name__ == '__main__':
    main()
