#!/usr/bin/env python3

import xlrd
import xlwt
from datetime import datetime
from unicodedata import normalize
from CreateTrips import get_service_id
from LoadStops import find_stop_id, get_pole_id

WEEK_FILE_NAME = '../raw/timetable_weekday_20170401.xls'
HOLY_FILE_NAME = '../raw/timetable_holyday_20170401.xls'
NORM_WEEK_FILE = '../raw/normalized_weekday_20170401.xls'
NORM_HOLY_FILE = '../raw/normalized_holiday_20170401.xls'
POLE_COMPLETION = '../raw/pole_completions.csv'


def extract_valid_sheets(sheets_file):
    return [s for s in sheets_file if int(s.name) < 140000 and s.ncols != 2]


def is_noboribetsu_civic_center(route_id):
    if route_id == '101110' or \
       route_id == '104300' or \
       route_id == '104310' or \
       route_id == '107600' or \
       route_id == '107610' or \
       route_id == '127100' or \
       route_id == '131100' or \
       route_id == '131110':
        return True
    else:
        return False


def find_pole(poles, route_id, stop_id, stop_seq):
    stop_seq = f'{stop_seq:02d}'
    found_poles = [p[4] for p in poles if p[0] == route_id and p[3] == stop_id and p[1] == stop_seq]
    return found_poles[0]


def create_sheet(raw_sheet, new_sheet, serv_id, poles):
    for sheet in raw_sheet:
        for time_i in range(0, sheet.ncols - 5):
            # シートの準備
            service_id = get_service_id(serv_id, sheet.name, time_i + 1)
            trip_id = f'{sheet.name}_{service_id}_{time_i + 1}'
            curr_sheet = new_sheet.add_sheet(trip_id)
            # stop_nameの書き込み
            stop_names = sheet.col_values(1)[6:]
            # なぜか2重になっている工大の除去
            if sheet.name == '130200':
                del(stop_names[39])
            elif sheet.name == '130210':
                del(stop_names[38])
            stop_names.insert(0, 'stop_name')
            col = 0
            for i, name in enumerate(stop_names):
                curr_sheet.write(i, col, name)
            # stop_idの書き込み
            stop_ids = [find_stop_id(normalize('NFKC', name)) for name in stop_names]
            stop_ids[0] = ['stop_id']
            col += 1
            for i, stop_id in enumerate(stop_ids):
                if len(stop_id) == 2 and is_noboribetsu_civic_center(sheet.name):
                    stop_id = stop_id[1]
                else:
                    stop_id = stop_id[0]
                curr_sheet.write(i, col, stop_id)
            # pole_idの書き込み
            pole_ids = [get_pole_id(p) for p in sheet.col_values(2)[6:]]
            if sheet.name == '130200':
                del(pole_ids[39])
            elif sheet.name == '130210':
                del(pole_ids[38])
            pole_ids.insert(0, 'pole_id')
            col += 1
            for i, pole_id in enumerate(pole_ids):
                pole_id = pole_id if pole_id is not '' else find_pole(poles, sheet.name, stop_ids[i][0], i)
                curr_sheet.write(i, col, pole_id)
            # departure_timeの書き込み
            times = [s + ':00' for s in sheet.col_values(time_i + 5)[6:]]
            if sheet.name == '130200':
                del(times[39])
            elif sheet.name == '130210':
                del(times[38])
            curr_sheet.write(0, 3, f'departure_time')
            date_format = xlwt.XFStyle()
            date_format.num_format_str = 'hh:mm:ss'
            col += 1
            for j, t in enumerate(times):
                curr_sheet.write(j + 1, col, datetime.strptime(t, '%X').time(), date_format)


def main():
    week_sheets_file = xlrd.open_workbook(WEEK_FILE_NAME).sheets()
    holy_sheets_file = xlrd.open_workbook(HOLY_FILE_NAME).sheets()

    raw_week_sheets = extract_valid_sheets(week_sheets_file)
    raw_holy_sheets = extract_valid_sheets(holy_sheets_file)

    new_week_sheets = xlwt.Workbook()
    new_holy_sheets = xlwt.Workbook()

    pole_file = open(POLE_COMPLETION)
    poles = [p[:-1].split(',') for p in pole_file.readlines()]

    create_sheet(raw_week_sheets, new_week_sheets, 'weekday', poles)
    create_sheet(raw_holy_sheets, new_holy_sheets, 'holiday', poles)

    new_week_sheets.save(NORM_WEEK_FILE)
    new_holy_sheets.save(NORM_HOLY_FILE)


if __name__ == '__main__':
    main()
