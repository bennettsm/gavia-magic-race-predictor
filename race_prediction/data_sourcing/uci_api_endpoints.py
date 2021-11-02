import requests
import re
import datetime as dt


base_url = "https://dataride.uci.ch/iframe/Competitions/"


def get_season():
    query = "https://dataride.uci.ch/iframe/GetRestrictedResultsDisciplineSeasons?disciplineId=3"

    seasons = requests.get(query)
    return seasons.json()


def get_competition(season_id=147, discipline_id=3):
    comp_url = "https://dataride.uci.ch/iframe/Competitions/"
    comps_list = []
    comp_query = {
        "disciplineId": discipline_id,
        "take": 40,
        "skip": 0,
        "pageSize": 40,
        "sort[0][field]": "StartDate",
        "sort[0][dir]": "desc",
        "filter[filters][0][field]": "RaceTypeId",
        "filter[filters][0][value]": 0,
        "filter[filters][1][field]": "CategoryId",
        "filter[filters][1][value]": 0,
        "filter[filters][2][field]": "SeasonId",
        "filter[filters][2][value]": season_id,
    }

    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    total = 10
    page = 1
    while len(comps_list) < total:
        comp_query['page'] = page

        response = requests.post(comp_url, data=comp_query, headers=headers).json()
        comps_list += response['data']
        total = response['total']
        page = page + 1

    return comps_list


def filter_competitions(comp_dict):
    compt_keys = ['CompetitionName',
                  'CompetitionId',
                  'CategoryCode',
                  'StartDate',
                  'ClassCode']
    comp_dict = {k: v for k, v in comp_dict.items() if k in (compt_keys)}
    comp_dict['StartDate'] = dt.datetime.fromtimestamp(int(re.sub("[^0-9]", "", comp_dict['StartDate']))/1000)

    return comp_dict


def get_races(competition_id, season_id, discipline_id=3):
    races_url = "https://dataride.uci.ch/iframe/Races/"

    body = {"disciplineId": discipline_id,
            "competitionId": competition_id,
            "take": 40,
            "skip": 0,
            "page": 1,
            "pageSize": 40,
            "filter[filters][0][field]": "SeasonId",
            "filter[filters][0][value]": season_id}

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    races = requests.post(races_url, data=body, headers=headers).json()

    return races


def get_events(race_id, discipline_id=3):
    events_url = "https://dataride.uci.ch/iframe/Events/"

    post_query = {"disciplineId": discipline_id,
                  "raceId": race_id}

    events = requests.post(events_url, data=post_query).json()
    return events[0]


def get_results(event_id, discipline_id=3):

    results_url = "https://dataride.uci.ch/iframe/Results/"
    post_query = {"disciplineId": discipline_id,
                  "eventId": event_id,
                  "take": 40,
                  "skip": 0,
                  "pageSize": 40}
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    total = 10
    page = 1
    res_list = []
    while len(res_list) < total:
        post_query['page'] = page
        results = requests.post(results_url, post_query, headers=headers).json()
        res_list += results['data']
        total = results['total']
        page += 1

    return res_list
