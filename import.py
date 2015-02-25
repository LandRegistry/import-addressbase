#!/usr/bin/env python

import csv
from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from itertools import groupby
from operator import itemgetter
import os

from record_types import Header, BLPU, DPA


CSV_PATH = '/vagrant/apps/import-addressbase/abp-sample/SX9090_small.csv'
HEADER_ID = 10  # Header record                (contains entry date)
BLPU_ID = 21    # Basic Land and Property Unit (contains coordinates)
DPA_ID = 28     # Delivery Point Address       (contains addresses)


# the record identifier column index is common to all records
RECORD_IDENTIFIER = 0
# the following column indexes are common to all non-header records
CHANGE_TYPE = 1
CHANGE_TYPE_CODE = 2
UPRN = 3

ADDRESS_KEY_FIELDS = ['organisation_name', 'sub_building_name', 'building_name',
                      'building_number', 'dependent_thoroughfare_name',
                      'thoroughfare_name', 'double_dependent_locality',
                      'dependent_locality', 'post_town', 'postcode']


def make_es_action(dpa, position, entry_datetime):
    dpa_dict = dpa._asdict()
    address_key = '_'.join([dpa_dict[f].replace(' ', '_')
                            for f in ADDRESS_KEY_FIELDS if dpa_dict[f]])
    doc = {
            'uprn': dpa.uprn,
            'organisationName': dpa.organisation_name,
            'departmentName': dpa.department_name,
            'subBuildingName': dpa.sub_building_name,
            'buildingName': dpa.building_name,
            'buildingNumber': dpa.building_number,
            'dependentThoroughfareName': dpa.dependent_thoroughfare_name,
            'thoroughfareName': dpa.thoroughfare_name,
            'doubleDependentLocality': dpa.double_dependent_locality,
            'dependentLocality': dpa.dependent_locality,
            'postTown': dpa.post_town,
            'postcode': dpa.postcode,
            'position': position,
            'entryDatetime': entry_datetime,
        }
    if dpa.change_type == 'I':
        action_dict = {
            '_index': 'landregistry',
            '_type': 'property',
            '_id': address_key,
            '_ttl': '1d',
            '_source': doc,
        }
    elif dpa.change_type == 'U':
        action_dict = {
            '_op_type': 'update',
            '_index': 'landregistry',
            '_type': 'property',
            '_id': address_key,
            'doc': doc,
        }
    elif dpa.change_type == 'D':
        action_dict = {
            '_op_type': 'delete',
            '_index': 'landregistry',
            '_type': 'property',
            '_id': address_key,
        }
    return action_dict


def get_action_dicts():
    """A generator which yields address dicts for groups of records with one DPA
    and zero or one BPLU
    """
    with open(CSV_PATH, 'r') as csv_file:
        data_reader = csv.reader(csv_file)

        rec_types = {BLPU_ID: BLPU, DPA_ID: DPA}

        entry_datetime = None

        for i, (_, group) in enumerate(groupby(data_reader, itemgetter(UPRN))):
            rows = list(group)
            if (i == 0 and len(rows) == 1 and
                    int(rows[0][RECORD_IDENTIFIER]) == HEADER_ID):
                header = Header(*rows[0])
                entry_datetime_str = '{} {}'.format(header.entry_date,
                                                    header.time_stamp)
                entry_datetime = datetime.strptime(entry_datetime_str,
                                                   '%Y-%m-%d %H:%M:%S')
                continue

            filtered = {k: [] for k in rec_types.keys()}
            # create namedtuples from each line
            for row in rows:
                rec_type = int(row[RECORD_IDENTIFIER])
                if rec_type in rec_types.keys():
                    # create a record using the values in the row
                    new_rec = rec_types[rec_type](*row)
                    filtered[rec_type] += [new_rec]

            # we must have one DPA and zero or one BPLU
            if len(filtered[DPA_ID]) == 1 and len(filtered[BLPU_ID]) in [0, 1]:
                dpa = filtered[DPA_ID][0]
                position = None
                if len(filtered[BLPU_ID]) == 1:
                    blpu = filtered[BLPU_ID][0]
                    position = {'x': blpu.x_coordinate, 'y': blpu.y_coordinate}
                action_dict = make_es_action(dpa, position, entry_datetime)

                # TODO: remove debug print statement
                from pprint import pprint
                pprint(action_dict, width=1)

                yield action_dict


if __name__ == '__main__':
    action_dicts = get_action_dicts()
    client = Elasticsearch(['localhost:4900'])
    bulk(client, action_dicts)
