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
    pole_id = chr(64 + int(pole_num)) if pole_num.isdigit() else ''
    return pole_id if pole_id.isalpha() else ''


def find_stop_id(stop_name, pole_num=None):
    if pole_num is not None:
        pole_id = get_pole_id(pole_num)
        stop_id = [s.stop_id for s in stops if s.location_type == 0 and stop_name in s.stop_name and pole_id in s.stop_id]
    else:
        stop_id = []
    tmp_stop_id = [s.stop_id for s in stops if s.location_type == 1 and s.stop_name == stop_name]
    if len(stop_id) == 0:
        stop_id = ['']
    if len(tmp_stop_id) == 0:
        tmp_stop_id = ['']
    return stop_id if stop_id[0] is not '' else tmp_stop_id
