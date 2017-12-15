WEEKDAY_FILE_NAME = '../raw/timetable_weekday_20170401.xls'
WEEKEND_FILE_NAME = '../raw/timetable_weekend_20170401.xls'


def extract_valid_sheets(sheets_file):
    # 学生便と郊外線、何も書かれていない路線を除去
    return [s for s in sheets_file if (int(s.name) < 120700 or 127310 < int(s.name) < 140000) and s.ncols != 2]
