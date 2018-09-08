# GovHack - HappyParking
# This file is to get restrictions of each parking spot.
# Author: Kenny
# Created on 08/09/2018, 17:40
# Last modified by:

from sodapy import Socrata

MyAppToken = "IwhZIr4MqqOeyb5BVZFL9fQbB"
database_path = "data.melbourne.vic.gov.au"
data_code = "rzb8-bz3y"
data_limit = 10000


def get_restriction():
    data = get_data(database_path, data_code, data_limit)

    all_features = {}
    single_features = {}

    for spot in data:
        bayid = spot['bayid']

        if 'description1' in spot:
            single_features['p_tag1'] = spot['description1']
        if 'description2' in spot:
            single_features['p_tag2'] = spot['description2']
        if 'description3' in spot:
            single_features['p_tag3'] = spot['description3']
        if 'description4' in spot:
            single_features['p_tag4'] = spot['description4']
        if 'description5' in spot:
            single_features['p_tag5'] = spot['description5']
        if 'description6' in spot:
            single_features['p_tag6'] = spot['description6']

        all_features[bayid] = single_features

    return all_features


def get_data(url, code, limit):
    client = Socrata(url, None)
    results = client.get(code, limit=limit)
    return results

