#!/usr/bin/env python3

import xlrd
from unicodedata import normalize
from LoadStops import find_stop_id, get_pole_id
from NormalizeRawData import is_noboribetsu_civic_center

WEEK_FILE_NAME = '../raw/timetable_weekday_20170401.xls'
HOLY_FILE_NAME = '../raw/timetable_holyday_20170401.xls'


def extract_valid_sheets(sheets_file):
    return [s for s in sheets_file if int(s.name) < 140000 and s.ncols != 2]


def find_unknown_poles(sheets):
    for sheet in sheets:
        for i in range(6, sheet.nrows):
            # 1行ごとにポールIDとバス停名とバス停IDを抽出
            row = sheet.row_values(i)
            pole_id = get_pole_id(row[2])
            name = normalize('NFKC', row[1])
            stop_id = find_stop_id(name)
            # 工大がダブっているところは排除
            if (sheet.name == '130200' or sheet.name == '130210') and name == '工大':
                continue
            # 市民会館が室蘭か登別かを判定
            if len(stop_id) == 2 and is_noboribetsu_civic_center(sheet.name):
                stop_id = stop_id[1]
            else:
                stop_id = stop_id[0]
            # ポールIDが存在しないものだけ抽出
            if pole_id == '':
                # 工大がダブっているところは1つずらす
                if sheet.name == '130200' or sheet.name == '130210':
                    i -= 1
                yield f'{int(sheet.name)},{i - 5:02d},{name},{stop_id},'


def main():
    week_sheets_file = xlrd.open_workbook(WEEK_FILE_NAME).sheets()
    holy_sheets_file = xlrd.open_workbook(HOLY_FILE_NAME).sheets()

    raw_week_sheets = extract_valid_sheets(week_sheets_file)
    raw_holy_sheets = extract_valid_sheets(holy_sheets_file)

    week_unknown_poles = list(find_unknown_poles(raw_week_sheets))
    holy_unknown_poles = list(find_unknown_poles(raw_holy_sheets))

    for p in sorted(set(week_unknown_poles + holy_unknown_poles)):
        print(p)


if __name__ == '__main__':
    main()
