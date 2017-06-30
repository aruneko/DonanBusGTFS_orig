#!/usr/bin/env python3


class Stop:
    def __init__(self, stop_id, stop_name, location_type):
        self.stop_id = stop_id
        self.stop_name = stop_name
        self.location_type = int(location_type)


stops_file = open('../gtfs/stops.txt')
raw_stops = stops_file.readlines()
stops_file.close()

splitted = [s.split(',') for s in raw_stops[1:]]
stops: [Stop] = [Stop(s[0], s[2], s[8]) for s in splitted]


def get_pole_id(pole_num):
    return chr(64 + int(pole_num)) if pole_num.isdigit() else '0'


def find_stop_id(pole_num, stop_name):
    pole_id = get_pole_id(pole_num)
    stop_id = [s.stop_id for s in stops if s.location_type == 0 and stop_name in s.stop_name and pole_id in s.stop_id]
    tmp_stop_id = [s.stop_id for s in stops if s.location_type == 1 and s.stop_name == stop_name]
    return stop_id if stop_id is not [] else tmp_stop_id
