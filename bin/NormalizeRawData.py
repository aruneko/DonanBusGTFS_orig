#!/usr/bin/env python3

import xlrd
import xlwt
from datetime import datetime
from unicodedata import normalize
from LoadStops import find_stop_id, get_pole_id
from util import WEEKDAY_FILE_NAME, WEEKEND_FILE_NAME, extract_valid_sheets

NORM_WEEKDAY_FILE = '../raw/normalized_weekday_20170401.xls'
NORM_WEEKEND_FILE = '../raw/normalized_weekend_20170401.xls'
POLE_COMPLETION = '../raw/pole_completions.csv'


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
            service_id = serv_id
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
                if sheet.name == '109210' and i == 45:
                    # 2回目の絵鞆2丁目を区別する
                    pole_id = 'C'
                else:
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
    weekday_sheets_file = xlrd.open_workbook(WEEKDAY_FILE_NAME).sheets()
    weekend_sheets_file = xlrd.open_workbook(WEEKEND_FILE_NAME).sheets()

    raw_weekday_sheets = extract_valid_sheets(weekday_sheets_file)
    raw_weekend_sheets = extract_valid_sheets(weekend_sheets_file)

    new_weekday_sheets = xlwt.Workbook()
    new_weekend_sheets = xlwt.Workbook()

    pole_file = open(POLE_COMPLETION)
    poles = [p[:-1].split(',') for p in pole_file.readlines()]

    create_sheet(raw_weekday_sheets, new_weekday_sheets, 'weekday', poles)
    create_sheet(raw_weekend_sheets, new_weekend_sheets, 'weekend', poles)

    new_weekday_sheets.save(NORM_WEEKDAY_FILE)
    new_weekend_sheets.save(NORM_WEEKEND_FILE)


if __name__ == '__main__':
    main()
