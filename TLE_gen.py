__author__ = "Alberto MN"
__version__ = "1.0"

import argparse
import urllib.request
import logging
import os

tracked_list = {
    'METEOR-M 1',
    'METEOR-M 2',
    'METEOR-M2 2',
    'NOAA 15',
    'NOAA 18',
    'NOAA 19',
    'ISS (ZARYA)',
    'FUNCUBE-1 (AO-73)',
    'RADFXSAT (FOX-1B)',
    'FOX-1CLIFF (AO-95)',
    'FOX-1D (AO-92)',
    'NAYIF-1 (EO-88)',
    'JY1SAT (JO-97)'
}

elements_files = ['weather.txt', 'amateur.txt']

norad_url = 'https://www.celestrak.com/NORAD/elements/'


def download_elements(elem_file):
    data = []
    url = norad_url + elem_file
    try:
        data = urllib.request.urlopen(url)
    except urllib.error.URLError as e_url:
        logging.error(e_url.reason)
    return data


def parse_elements(elements_list, output_file):
    for line in elements_list:
        if not line.startswith(b'1') and not line.startswith(b'2'):
            current = line.decode('ascii').strip()
            if current in tracked_list:
                logging.info('Writting TLE for {0}.'.format(current))
                output_file.write(line)
                output_file.write(next(elements_list))
                output_file.write(next(elements_list))
                tracked_list.remove(current)


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
        print('Tracked satellites:\n{0}'.format('\n'.join(tracked_list)))
        exit(0)

    with open(out_file, 'wb') as output:
        for elem in elements_files:
            data = download_elements(elem)
            parse_elements(data, output)


    if len(tracked_list):
        logging.warning('Could not get TLE for the following satellites: {0}'.format(', '.join(tracked_list)))

    logging.info('Custom TLE file saved in \"{0}\".'.format(os.path.abspath(out_file)))
