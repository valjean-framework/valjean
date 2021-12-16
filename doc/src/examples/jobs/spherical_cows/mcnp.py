# coding: utf-8

import enum
import re
import logging
from collections import OrderedDict

import numpy as np

from valjean.eponine.dataset import Dataset

# set up logging
LOGGER = logging.getLogger('mcnp')

class MCTALResult:
    STATE = enum.Enum('STATE',
                      'SEARCH_TALLY '
                      'SEARCH_F '
                      'READ_F '
                      'SEARCH_X '
                      'READ_X '
                      'SEARCH_ZONE '
                      'SEARCH_VALS '
                      'READ_VALS')

    def __init__(self, file_name):
        self.file_name = file_name
        self.start_dict = {}
        self.result_dict = {}
        self._parse()

    def _parse(self):
        with open(self.file_name) as f:
            line = f.readline()
            while line:
                match = re.match('tally +([0-9]+)', line, re.I)
                if match:
                    tally_number = int(match.group(1))
                    LOGGER.debug('Found tally %d', tally_number)
                    self.start_dict[tally_number] = f.tell()
                line = f.readline()

    def result(self, tally_number, zone_number):
        res = self.result_dict.get((tally_number, zone_number), None)
        if res is None:
            res = self.extract_result(tally_number, zone_number)
            self.result_dict[(tally_number, zone_number)] = res
        return res

    def extract_result(self, tally_number, zone_number):
        xs = []
        ys = []
        eys = []
        exs = []
        state = self.STATE.SEARCH_F

        last_pos = self.start_dict.get(tally_number, None)
        if last_pos is None:
            raise Exception('Could not find tally ' + str(tally_number))

        with open(self.file_name) as f:
            f.seek(last_pos)
            line = f.readline()
            while line:
                if state == self.STATE.SEARCH_F:
                    match = re.match('f +([0-9]+)', line, re.I)
                    if match:
                        n_zones = int(match.group(1))
                        if n_zones > 0:
                            LOGGER.debug('Found %d zones', n_zones)
                            state = self.STATE.READ_F
                            zones = []
                elif state == self.STATE.READ_F:
                    # split the string
                    splitted = re.split(' +', line.strip())
                    ints = list(map(int, splitted))
                    LOGGER.debug('Parsed %d ints: %s', len(ints), str(ints))
                    zones += ints
                    if len(zones) >= n_zones:
                        zone_index = zones.index(zone_number)
                        state = self.STATE.SEARCH_X
                elif state == self.STATE.SEARCH_X:
                    match = re.match('([usmcet][tc]?) +([0-9]+)', line, re.I)
                    if match:
                        n_vals = int(match.group(2)) - 1
                        if n_vals > 0:
                            LOGGER.debug('Found independent variable: %s, %d '
                                         'values', match.group(1), n_vals)
                            state = self.STATE.READ_X
                elif state == self.STATE.READ_X:
                    # split the string
                    splitted = re.split(' +', line.strip())
                    floats = list(map(float, splitted))
                    LOGGER.debug('Parsed %d floats: %s', len(floats),
                                 str(floats))
                    xs += floats
                    if len(xs) >= n_vals:
                        state = self.STATE.SEARCH_VALS
                        xs = xs[:n_vals]
                elif state == self.STATE.SEARCH_VALS:
                    if re.match('vals', line, re.I):
                        LOGGER.debug('Found values')
                        must_skip = 2*zone_index*(n_vals+1)
                        LOGGER.debug('Will skip %d items', must_skip)
                        state = self.STATE.SEARCH_ZONE
                elif state == self.STATE.SEARCH_ZONE:
                    # split the string
                    splitted = re.split(' +', line.strip())
                    must_skip -= len(splitted)
                    LOGGER.debug('Read %d values, %d to go: starts with %s',
                                 len(splitted), must_skip, splitted[0])
                    if must_skip < 0:
                        LOGGER.debug('Moving to READ_VALS state')
                        line = ' '.join(splitted[must_skip:])
                        LOGGER.debug('Handing over %s to parser', line)
                        state = self.STATE.READ_VALS

                if state == self.STATE.READ_VALS:
                    stripped = line.strip()
                    if stripped:
                        # split the string
                        splitted = re.split(' +', stripped)
                        floats = list(map(float, splitted))
                        LOGGER.debug('Parsed %d floats: %s', len(floats),
                                     str(floats))
                        ys += floats[::2]
                        eys += floats[1::2]
                        if len(ys) >= n_vals + 1:
                            ys = ys[1:n_vals]
                            eys = eys[1:n_vals]
                            break

                line = f.readline()

        if len(xs) != len(ys)+1 or \
                (eys and len(ys) != len(eys)) or \
                (exs and len(exs) != len(xs)):
            raise Exception(f'Inconsistent lengths of x ({len(xs)})/y '
                            f'({len(ys)})/ey ({len(eys)})/ex ({len(exs)}) '
                            'arrays')

        LOGGER.debug('Parsing succeeded')
        LOGGER.debug('xs=%s', xs)
        LOGGER.debug('ys=%s', ys)
        LOGGER.debug('exs=%s', exs)
        LOGGER.debug('eys=%s', eys)

        xarr = np.array(xs)
        yarr = np.array(ys)
        eyarr = np.array(eys)

        # MCNP yields relative errors: normalize
        eyarr *= yarr

        dataset = Dataset(yarr, eyarr, bins=OrderedDict([('e', xarr)]),
                          what='flux', name='mcnp')

        return dataset
