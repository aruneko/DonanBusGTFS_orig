#!/usr/bin/env python3

HEADER = 'fare_id,price,currency_type,payment_method,transfers,transfer_duration'


def create_fare_attributes(fare_ids):
    return [f'{fare_id},{fare_id[2:]},JPY,0,0,' for fare_id in sorted(fare_ids)]


def main() -> None:
    fare_rules_file = open('../gtfs/fare_rules.txt', 'r').readlines()[1:]
    fare_ids = set([fare_rule.split(',')[0] for fare_rule in fare_rules_file])
    fare_attributes = create_fare_attributes(fare_ids)

    print(HEADER)
    for fare_attribute in fare_attributes:
        print(fare_attribute)


if __name__ == '__main__':
    main()
