#!/usr/bin/env python3

import xlrd

WEEK_FILE_NAME = '../raw/timetable_weekday_20170401.xls'
HOLY_FILE_NAME = '../raw/timetable_holyday_20170401.xls'
HEADER = 'route_id,agency_id,route_short_name,route_long_name,route_desc,route_type,route_url,route_color,route_text_color,jp_parent_route_id'


def extract_valid_sheets(sheets_file):
    return [s for s in sheets_file if int(s.name) < 140000 and s.ncols != 2]


def extract_sheet_names(sheets):
    return [sheet.name for sheet in sheets]


def create_route(name):
    return f'{name},1430001056880,,,,3,,,,'


def create_routes(names):
    return [create_route(name) for name in names]


def main():
    week_sheets_file = xlrd.open_workbook(WEEK_FILE_NAME).sheets()
    holy_sheets_file = xlrd.open_workbook(HOLY_FILE_NAME).sheets()

    raw_week_sheets = extract_valid_sheets(week_sheets_file)
    raw_holy_sheets = extract_valid_sheets(holy_sheets_file)

    week_sheet_names = extract_sheet_names(raw_week_sheets)
    holy_sheet_names = extract_sheet_names(raw_holy_sheets)

    names = week_sheet_names + holy_sheet_names
    without_duplicates = sorted(set(names))
    routes = create_routes(without_duplicates)

    print(HEADER)

    for r in routes:
        print(r)


if __name__ == '__main__':
    main()
