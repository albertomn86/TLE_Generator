#!/usr/bin/env python3

__author__ = 'Alberto MN'
__version__ = '3.0'

from argparse import ArgumentParser
import requests
from os import path
from re import match
import logging
from lib.tle import Tle

# Tracked satellites file
TR_FILE = 'satellites.txt'

# Output default file
OUT_FILE = 'custom_TLE.txt'

DEFAULT_GROUPS = ['weather', 'amateur']

NORAD_URL = 'https://celestrak.com/NORAD/elements/gp.php'


def read_satellites_file(file_path: str) -> list:
    satellites = []
    if not path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(file_path, 'r') as input:
        for line in input:
            if line.startswith('#'):
                continue
            matched = match(r"([0-9]{5}).*", line)
            if matched:
                catalog_number = matched.group(1)
                logging.debug(f'Found catalog number: {catalog_number}.')
                satellites.append(catalog_number)

    return satellites


def download_data(url: str) -> list:
    data = []
    response = requests.get(url)

    if response.status_code == 200:
        raw = response.content.split(b'\r\n')
        data = [x for x in raw if x.strip()]
    else:
        logging.error(response.reason)

    return data


def parse_raw_data(data: list) -> dict:
    parsed_data = {}
    i = 0

    while i < len(data):
        if len(data[i]) == 24:
            title_line = data[i]
            l1 = data[i + 1]
            l2 = data[i + 2]
            sat_id = l2.decode().split()[1]
            parsed_data[sat_id] = Tle(title_line, l1, l2)
            i += 3
        else:
            i += 1

    return parsed_data


def get_data_by_catalog_number(catalog_number: str) -> list:
    url = f'{NORAD_URL}?CATNR={catalog_number}&FORMAT=TLE'

    return download_data(url)


def get_data_by_group(group_name: str) -> list:
    url = f'{NORAD_URL}?GROUP={group_name}&FORMAT=TLE'

    return download_data(url)


def save_to_file(sat_data: dict, input_list: str, out_file: str):
    with open(out_file, 'wb') as output:
        for elem in input_list:
            tle_data = sat_data.get(elem)

            if tle_data is None:
                logging.debug('TLE for {0} not found in default groups data. Searching by catalog number...'.format(elem))
                data = parse_raw_data(get_data_by_catalog_number(elem))
                tle_data = data.get(elem)

                if tle_data is None:
                    logging.warning('Could not get TLE for: {0}'.format(elem))
                    continue

            for line in tle_data.getLines():
                output.write(line + b'\r\n')

            logging.info('Saved TLE for {0}.'.format(tle_data.object_name))

    logging.info('Custom TLE file saved in \"{0}\".'.format(path.abspath(out_file)))


if __name__ == "__main__":

    logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s', level=logging.INFO)

    parser = ArgumentParser(description='Custom TLE file generator.', prog='tle_gen')
    parser.add_argument('-i', '--input', help='Download TLE for the specified catalog numbers.')
    parser.add_argument('-o', '--output', help='Output file path.')
    parser.add_argument('-v', '--version', help='Show version.', action='version', version='%(prog)s v' + __version__)

    args = vars(parser.parse_args())

    out_file = args['output'] if args['output'] else OUT_FILE

    if args['input']:
        input_list = args['input'].replace(" ", "").split(',')
    else:
        try:
            input_list = read_satellites_file(TR_FILE)
        except FileNotFoundError as err:
            logging.error(err)
            exit(1)

    if len(input_list) == 0:
        logging.info('Invalid satellite list.')
        exit(1)

    default_sat_data = []
    for group in DEFAULT_GROUPS:
        default_sat_data += get_data_by_group(group)

    sat_data = parse_raw_data(default_sat_data)

    save_to_file(sat_data, input_list, out_file)
