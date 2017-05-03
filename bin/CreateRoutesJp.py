#!/usr/bin/env python3

import xlrd

WEEK_FILE_NAME = '../raw/timetable_weekday_20170401.xls'
HOLY_FILE_NAME = '../raw/timetable_holyday_20170401.xls'
HEADER = 'route_id,route_update_date,origin_stop,via_stop,destination_stop'
UPDATE_DATE = '20170401'


def extract_valid_sheets(sheets_file):
    return [s for s in sheets_file if int(s.name) < 140000 and s.ncols != 2]


def trans_original_name(name):
    if name == '中入':
        return '中島入口'
    elif name == 'タミ・高砂':
        return '東町ターミナル・高砂2丁目'
    elif name == '高砂・タミ':
        return '高砂2丁目・東町ターミナル'
    elif name == '幌別':
        return '幌別本町'
    elif name == '市民':
        return '室蘭市民会館前'
    elif name == '寿・千代':
        return '寿町1丁目・千代の台団地'
    elif name == '千代・寿':
        return '千代の台団地・寿町1丁目'
    elif name == '汐平・幌別':
        return '汐平団地・幌別駅西口'
    elif name == '幌別・汐平':
        return '幌別駅西口・汐平団地'
    elif name == '西口':
        return '東室蘭駅西口'
    elif name == '病院':
        return '製鉄記念室蘭病院'
    elif name == '西口・春雨':
        return '東室蘭駅西口・春雨橋'
    elif name == '春雨・西口':
        return '春雨橋・東室蘭駅西口'
    elif name == '西口・本輪':
        return '東室蘭駅西口・本輪西'
    elif name == '本輪・西口':
        return '本輪西・東室蘭駅西口'
    elif name == '西口・千代':
        return '東室蘭駅西口・千代の台団地'
    elif name == '千代・西口':
        return '千代の台団地・東室蘭駅西口'
    elif name == '弥生':
        return '弥生ショッピングセンター'
    elif name == '水族・鷲別':
        return 'みたら・水族館前・鷲別'
    elif name == '大橋':
        return '白鳥大橋'
    elif name == '中入・新道':
        return '中島入口・室蘭新道'
    elif name == '若草小':
        return '若草小学校前'
    elif name == '千代の台':
        return '千代の台団地'
    elif name == '中・鷲・東':
        return '中島入口・鷲別・東町ターミナル'
    elif name == '東・鷲・中':
        return '東町ターミナル・鷲別・中島入口'
    elif name == '室・中・鷲':
        return '室蘭港・中島入口・鷲別'
    elif name == '鷲別・工大・中入':
        return '鷲別・工大・中島入口'
    elif name == '鷲・東':
        return '鷲別・東町ターミナル'
    elif name == '西口・工大・高砂':
        return '東室蘭駅西口・工大・高砂2丁目'
    elif name == '西口・若草':
        return '幌別駅西口・若草小学校前'
    elif name == '若草・西口':
        return '若草小学校前・幌別駅西口'
    elif name == '工大・高砂・西口':
        return '工大・高砂2丁目・東室蘭駅西口'
    elif name == '西口・八丁':
        return '東室蘭駅西口・八丁平'
    elif name == '八丁・西口':
        return '八丁平・東室蘭駅西口'
    else:
        return name


def split_stops(stops):
    return [trans_original_name(n) for n in stops.split('-')]


def extract_names_and_stops(sheets):
    return [(sheet.name, split_stops(sheet.cell(0, 5).value)) for sheet in sheets]


def create_route_jp(name, stops):
    return f'{name},{UPDATE_DATE},{stops[0]},{stops[1]},{stops[2]}'


def create_route_jps(names):
    return [create_route_jp(n, s) for n, s in names]


def main():
    week_sheets_file = xlrd.open_workbook(WEEK_FILE_NAME).sheets()
    holy_sheets_file = xlrd.open_workbook(HOLY_FILE_NAME).sheets()

    raw_week_sheets = extract_valid_sheets(week_sheets_file)
    raw_holy_sheets = extract_valid_sheets(holy_sheets_file)

    week_sheet = extract_names_and_stops(raw_week_sheets)
    holy_sheet = extract_names_and_stops(raw_holy_sheets)

    names = week_sheet + holy_sheet
    routes = sorted(set(create_route_jps(names)))

    print(HEADER)

    for r in routes:
        print(r)


if __name__ == '__main__':
    main()
