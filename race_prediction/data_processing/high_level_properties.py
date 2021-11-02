import pandas as pd
import numpy as np

from race_prediction.data_sourcing.uci_api_endpoints import get_races


def extract_races_from_competitions(competition_id, season_id=147):
    """
    competition_id : int
        competition id
    season_id : int
        season_id
    Pull the mens and womens races from the competitions object
    """
    race_keys = [
        'Id',
        'CategoryCode',
        'StartDate',
        'Venue',
        'Date']
    mens_race = {}
    womens_race = {}

    races = get_races(competition_id=competition_id, season_id=season_id)['data']
    for a_race in races:
        if "Men Elite" in a_race['CategoryCode']:
            mens_race = {k: v for k, v in a_race.items() if k in (race_keys)}
        if "Women Elite" in a_race['CategoryCode']:
            womens_race = {k: v for k, v in a_race.items() if k in (race_keys)}
    return mens_race, womens_race


def flatten_results_to_race_properties(results_list, race_properties):
    """
    Flatten the results so that the properties of each race is attatech to a result

    results_list : list
    race_properties : dict
    """

    results_filter = [
        'RankNumber',
        'Rank',
        'ResultValue',
        'IndividualDisplayName',
        'TeamName'
        'Bib',
        'Age']

    entried_list = []
    for a_result in results_list:
        results = {k: v for k, v in a_result.items() if k in (results_filter)}
        entried_list.append({**race_properties, **results})
    return pd.DataFrame(entried_list)
