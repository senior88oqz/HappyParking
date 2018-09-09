
from sodapy import Socrata
from datetime import datetime, time
import json

database_path = "data.melbourne.vic.gov.au"
data_year = "2016"
data_code = "dj7e-rdx9"  # year 2016
data_limit = 100000000

client = Socrata(database_path, None)


# Get all street names
def get_streets(code, limit):
    dis_street = client.get(code, select="distinct(streetname)", limit=limit)
    street_collection = []
    for item in dis_street[1:]:
        street = item['streetname_1']
        street_collection.append(street)

    return street_collection


def get_occupation(code, streets, limit):
    m_peak_duration = 9000  # 9000 seconds are from 6.30am to 9.00am, morning peak
    e_peak_duration = 12600  # 12600 seconds are from 15.00pm to 18.30pm, evening peak
    n_unpeak_duration = 21600 # 21600 seconds are from 9.00am to 15.00pm, noon unpeak
    weekday_unpeak = (24 - 6) * 3600
    weekend_unpeak = 24 * 3600
    total_peak = 6*3600
    street_collection = {}
    i = 0
    for street in streets:
        d_ids = client.get(code, select="distinct(deviceid)", streetname=street, limit=limit)
        num_bays = len(d_ids)
        date_collection = {}
        occs = client.get(code, select="arrivaltime, departuretime, durationseconds",  streetname=street, order="arrivaltime", limit=limit)
        for occ in occs:
            unpeak_duration = 0
            peak_duration = 0
            if int(occ["durationseconds"]) > 0:
                arri = datetime.strptime(occ['arrivaltime'], '%Y-%m-%dT%H:%M:%S.000')
                depa = datetime.strptime(occ['departuretime'], '%Y-%m-%dT%H:%M:%S.000')
                weekday = arri.isoweekday()
                curr_date = str(arri.date())
                m_peak_start = datetime.strptime((curr_date + "T06:30:00"),"%Y-%m-%dT%H:%M:%S")
                m_peak_end = datetime.strptime((curr_date + "T09:00:00"),"%Y-%m-%dT%H:%M:%S")
                e_peak_start = datetime.strptime((curr_date + "T15:00:00"),"%Y-%m-%dT%H:%M:%S")
                e_peak_end = datetime.strptime((curr_date + "T18:30:00"),"%Y-%m-%dT%H:%M:%S")

                if weekday < 6:
                    if arri.time() < time(6, 30):
                        if depa.time() < time(6, 30):
                            unpeak_duration += int(occ["durationseconds"])
                        if time(6, 30) < depa.time() < time(9,00):
                            unpeak_duration += (m_peak_start - arri).total_seconds()
                            peak_duration += (depa - m_peak_start).total_seconds()
                        if time(15,00) > depa.time() > time(9, 00):
                            unpeak_duration += (m_peak_start - arri).total_seconds()
                            unpeak_duration += (depa - m_peak_end).total_seconds()
                            peak_duration += m_peak_duration
                        if time(15,00) < depa.time() < time(18, 30):
                            unpeak_duration += (m_peak_start - arri).total_seconds()
                            unpeak_duration += n_unpeak_duration
                            peak_duration += m_peak_duration
                            peak_duration += (depa - e_peak_start).total_seconds()
                        if depa.time() > time(18, 30):
                            unpeak_duration += (m_peak_start - arri).total_seconds()
                            unpeak_duration += n_unpeak_duration
                            unpeak_duration += (depa - e_peak_end).total_seconds()
                            peak_duration += m_peak_duration
                            peak_duration += e_peak_duration

                    if time(9,00) > arri.time() > time(6, 30):
                        if time(9,00) > depa.time() > time(6, 30):
                            peak_duration += int(occ["durationseconds"])
                        if time(9, 00) < depa.time() < time(15, 00):
                            peak_duration += (m_peak_end - arri).total_seconds()
                            unpeak_duration += (depa - m_peak_end).total_seconds()
                        if time(18,30) > depa.time() > time(15, 00):
                            peak_duration += (m_peak_end - arri).total_seconds()
                            unpeak_duration += n_unpeak_duration
                            peak_duration += (depa - e_peak_start).total_seconds()
                        if depa.time() > time(18,30):
                            peak_duration += (m_peak_end - arri).total_seconds()
                            unpeak_duration += n_unpeak_duration
                            peak_duration += e_peak_duration
                            unpeak_duration += (depa - e_peak_end).total_seconds()

                    if time(9,00) < arri.time() < time(15,00):
                        if time(9, 00) < depa.time() < time(15, 00):
                            unpeak_duration += int(occ["durationseconds"])
                        if time(18, 30) > depa.time() > time(15, 00):
                            unpeak_duration += (e_peak_start - arri).total_seconds()
                            peak_duration += (depa - e_peak_start).total_seconds()
                        if depa.time() > time(18, 30):
                            unpeak_duration += (e_peak_start - arri).total_seconds()
                            peak_duration += e_peak_duration
                            unpeak_duration += (depa - e_peak_end).total_seconds()

                    if time(15,00) < arri.time() < time(18, 30):
                        if time(18, 30) > depa.time() > time(15, 00):
                            peak_duration += int(occ["durationseconds"])
                        if depa.time() > time(18, 30):
                            peak_duration += (e_peak_end - arri).total_seconds()
                            unpeak_duration += (depa - e_peak_end).total_seconds()

                    if arri.time() > time(18, 30):
                        unpeak_duration += int(occ["durationseconds"])

                    unpeak_ratio = unpeak_duration / (weekday_unpeak * num_bays)
                    peak_ratio = peak_duration / (total_peak * num_bays)
                    day_ratio = (unpeak_duration + peak_duration) / ((total_peak + weekday_unpeak) * num_bays)

                else:
                    unpeak_duration += int(occ["durationseconds"])
                    unpeak_ratio = unpeak_duration / (weekend_unpeak * num_bays)
                    peak_ratio = peak_duration / (total_peak * num_bays)
                    day_ratio = (unpeak_duration + peak_duration) / ((total_peak + weekend_unpeak) * num_bays)

                ratio = {}
                if curr_date not in date_collection:
                    ratio["unpeak_ratio"] = unpeak_ratio
                    ratio["peak_ratio"] = peak_ratio
                    ratio["day_ratio"] = day_ratio
                    date_collection[curr_date] = ratio
                else:
                    date_collection[curr_date]["unpeak_ratio"] += unpeak_ratio
                    date_collection[curr_date]["peak_ratio"] += peak_ratio
                    date_collection[curr_date]["day_ratio"] += day_ratio

        street_collection[street] = date_collection
        i = i + 1
        print("i = ", i)
    return street_collection


def is_peak_hour(date):
    if time(6, 30) <= date.time() <= time(9, 00):
        return 1
    elif time(15, 00) <= date.time() <= time(18, 30):
        return 2
    else:
        return 0


if __name__ == "__main__":
    streets = get_streets(data_code, data_limit)
    occupations = get_occupation(data_code, streets, data_limit)
    with open("street_occupation_"+data_year+".json", "w") as write_file:
        json.dump(occupations, write_file)
