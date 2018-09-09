#!/usr/bin/env python

import pandas as pd
from sodapy import Socrata
import json

def getData(code, limit):
    client = Socrata("data.melbourne.vic.gov.au", None)
    results = client.get(code, limit=limit)
    results_df = pd.DataFrame.from_records(results)
    return results_df

# Convert to pandas DataFrame


def getRes(restritionDataFrame):
    res_map = dict()
    for i in range(len(restritionDataFrame)):
        ## TODO Add time filed
        # res_map[results_df['bayid'][i]] = {'description1':results_df['description1'][i], 'fromday1': results_df['fromday1'][i],'today1': results_df['today1'][i],
        #                                    'starttime1':results_df['starttime1'][i],'endtime1': results_df['endtime1'][i]}
        if isinstance(restritionDataFrame['description2'][i], float):
            res_map[restritionDataFrame['bayid'][i]] = {'description1':restritionDataFrame['description1'][i]}

        elif isinstance(restritionDataFrame['description3'][i], float):
            res_map[restritionDataFrame['bayid'][i]] = {'description1':restritionDataFrame['description1'][i],
                                               'description2':restritionDataFrame['description2'][i]}
        else:
            res_map[restritionDataFrame['bayid'][i]] = {'description1':restritionDataFrame['description1'][i],
                                               'description2':restritionDataFrame['description2'][i],
                                               'description3':restritionDataFrame['description3'][i]}
    return res_map


if __name__ == '__main__':
    resData = getData(code="rzb8-bz3y", limit=5000)
    with open("restriction.json", "w") as write_file:
        json.dump(getRes(resData), write_file)