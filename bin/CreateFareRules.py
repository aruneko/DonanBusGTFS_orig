#!/usr/bin/env python3

import xlrd
from itertools import chain

HEADER = 'fare_id,route_id,origin_id,destination_id,contains_id'


def create_fare_rule_by_route(route, route_id):
    start_stop_id, _ = route[0]
    tail = route[1:]
    return [f'k_{int(fare)},{route_id},{start_stop_id},{stop_id},' for stop_id, fare in tail]


def create_fare_rule(sheet):
    stop_ids = sheet.col_values(1)
    route_id = sheet.name
    fare_data_by_routes = [list(zip(stop_ids, sheet.col_values(i)))[i-2:] for i in range(2, sheet.ncols)]
    result = [create_fare_rule_by_route(route, route_id) for route in fare_data_by_routes]
    return list(chain.from_iterable(result))


def create_fare_rules(triangle_table_sheets):
    return list(chain.from_iterable([create_fare_rule(sheet) for sheet in triangle_table_sheets]))


def main() -> None:
    triangle_table_sheets = xlrd.open_workbook('../raw/triangle_table.xlsx').sheets()
    fare_rules = create_fare_rules(triangle_table_sheets)

    print(HEADER)
    for fare_rule in fare_rules:
        print(fare_rule)


if __name__ == '__main__':
    main()
