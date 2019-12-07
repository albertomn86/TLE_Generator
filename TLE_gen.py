__author__ = "Alberto MN"
__version__ = "2.1"

import argparse
import urllib.request
import logging
import os
import re

tracked_list = [
    ['40069', 'METEOR-M 2'],
    ['44387', 'METEOR-M2 2'],
    ['25338', 'NOAA 15'],
    ['28654', 'NOAA 18'],
    ['33591', 'NOAA 19'],
    ['25544', 'ISS (ZARYA)'],
    ['39444', 'FUNCUBE-1 (AO-73)'],
    ['43017', 'RADFXSAT (FOX-1B)'],
    ['43770', 'FOX-1CLIFF (AO-95)'],
    ['43137', 'FOX-1D (AO-92)'],
    ['42017', 'NAYIF-1 (EO-88)'],
    ['43803', 'JY1SAT (JO-97)'],
    ['43780', 'MOVE-II'],
    ['42778', 'MAX VALIER SAT'],
    ['43937', 'NEXUS (FO-99)']
]

_norad_url = 'http://www.amsat.celestrak.net/satcat/tle.php?CATNR='


def download_tle(elem):
    data = []
    url = _norad_url + elem[0]
    try:
        body = urllib.request.urlopen(url).read()
        if body:
            raw = body.split(b'\r\n')
            filtered = [x for x in raw if x.strip()]
            if elem[1] in filtered[0].decode():
                data = filtered
    except urllib.error.URLError as e_url:
        logging.error(e_url.reason)
    return data


if __name__== "__main__":

    logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s', level=logging.INFO)

    parser = argparse.ArgumentParser(description='Custom TLE file generator.', prog='TLE_gen')
    parser.add_argument('-o','--output', help='Output file path.')
    parser.add_argument('-v','--version', help='Show version.', action='version', version='%(prog)s v' + __version__)
    parser.add_argument('-l','--list', help='List tracked satellites.', action='store_true')
    args = vars(parser.parse_args())

    out_file = 'custom_TLE.txt'
    if args['output']:
        out_file = args['output']
    if args['list']:
        print('Tracked satellites:\n{0}'.format('\n'.join(x[1] for x in tracked_list)))
        exit(0)

    with open(out_file, 'wb') as output:
        for elem in tracked_list:
            data = download_tle(elem)
            if not len(data) == 3:
                logging.warning('Could not get TLE for: {0}'.format(elem[1]))
                continue
            for line in data:
                output.write(line + b'\r\n')
            logging.info('Saved TLE for {0}.'.format(elem[1]))

    logging.info('Custom TLE file saved in \"{0}\".'.format(os.path.abspath(out_file)))
    
    input("Press Enter to exit...")
