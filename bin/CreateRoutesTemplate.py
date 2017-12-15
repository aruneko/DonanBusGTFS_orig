#!/usr/bin/env python3

import xlrd
from util import WEEKDAY_FILE_NAME, WEEKEND_FILE_NAME, extract_valid_sheets

HEADER = 'route_id,agency_id,route_short_name,route_long_name,route_desc,route_type,route_url,route_color,route_text_color,jp_parent_route_id'


def extract_sheet_names(sheets):
    return [sheet.name for sheet in sheets]


def create_route(name):
    return f'{name},1430001056880,,,,3,,,,'


def create_routes(names):
    return [create_route(name) for name in names]


def main():
    weekday_sheets_file = xlrd.open_workbook(WEEKDAY_FILE_NAME).sheets()
    weekend_sheets_file = xlrd.open_workbook(WEEKEND_FILE_NAME).sheets()

    raw_weekday_sheets = extract_valid_sheets(weekday_sheets_file)
    raw_weekend_sheets = extract_valid_sheets(weekend_sheets_file)

    weekday_sheet_names = extract_sheet_names(raw_weekday_sheets)
    weekend_sheet_names = extract_sheet_names(raw_weekend_sheets)

    names = weekday_sheet_names + weekend_sheet_names
    without_duplicates = sorted(set(names))
    routes = create_routes(without_duplicates)

    print(HEADER)

    for r in routes:
        print(r)


if __name__ == '__main__':
    main()
