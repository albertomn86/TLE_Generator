#!/usr/bin/env python3

__author__ = "Alberto MN"
__version__ = "2.2"

import argparse
import urllib.request
import logging
import os
import re

_norad_url = 'http://www.amsat.celestrak.net/satcat/tle.php?CATNR='

def parseList(tracked_file):
    sat_list = []
    with open(tracked_file, 'r') as input:
        for line in input:
            if line.startswith('#'):
                continue
            match = re.match(r"([0-9]{5}).*",line)
            if match:
                logging.debug('Found number: {0}.'.format(match.group(1)))
                sat_list.append(match.group(1))
    return sat_list


def download_tle(elem):
    data = []
    url = _norad_url + elem
    try:
        body = urllib.request.urlopen(url).read()
        if body:
            raw = body.split(b'\r\n')
            data = [x for x in raw if x.strip()]
    except urllib.error.URLError as e_url:
        logging.error(e_url.reason)
    return data


if __name__== "__main__":

    logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s', level=logging.INFO)

    parser = argparse.ArgumentParser(description='Custom TLE file generator.', prog='tle_gen')
    parser.add_argument('-i','--input', help='Download TLE for the specified catalog numbers.')
    parser.add_argument('-o','--output', help='Output file path.')
    parser.add_argument('-v','--version', help='Show version.', action='version', version='%(prog)s v' + __version__)

    args = vars(parser.parse_args())

    # Tracked satellites file
    tr_file = 'satellites.txt'

    # Output default file
    out_file = 'custom_TLE.txt'

    if args['output']:
        out_file = args['output']

    if args['input']:
        input_list = args['input'].replace(" ", "").split(',')
    else:
        input_list = parseList(tr_file)

    if len(input_list) == 0:
        logging.info('Invalid satellite list.')
        exit(1)

    with open(out_file, 'wb') as output:
        for elem in input_list:
            data = download_tle(elem)
            if not len(data) == 3:
                logging.warning('Could not get TLE for: {0}'.format(elem))
                continue
            for line in data:
                output.write(line + b'\r\n')
            logging.info('Saved TLE for {0}.'.format((data[0].decode()).strip()))

    logging.info('Custom TLE file saved in \"{0}\".'.format(os.path.abspath(out_file)))

    input("Press Enter to exit...")
