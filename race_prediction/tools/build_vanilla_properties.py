import pandas as pd


def build_vanilla_properties(csv_path=None):
    comps = get_competition()
    mens_race_list = []
    womens_race_list = []
    mens_res_list = []
    womens_res_list = []
    race_ids = []
    results_list = []

    season_list = [25, 126, 141, 147, 158]

    for a_season in season_list:

        comps = get_competition(a_season)
        for acomp in comps:

            # top level competetion data
            race_dict = filter_competitions(acomp)
            mens_race, womens_race = extract_races_from_competitions(competition_id=acomp['CompetitionId'],
                                                                     season_id=a_season)
            mens_race = {**mens_race, **race_dict}
            womens_race = {**womens_race, **race_dict}

            try:
                mens_event = get_events(race_id=mens_race['Id'])
                womens_event = get_events(race_id=womens_race['Id'])
            except KeyError:
                print(mens_event)
                print(womens_event)

            mens_race_dict = {**mens_race, **{'EventId': mens_event['EventId']}}
            womens_race_dict = {**womens_race, **{'EventId': womens_event['EventId']}}
            mens_race_list.append(mens_race_dict)
            womens_race_list.append(womens_race_dict)

            mens_race_results = get_results(event_id=mens_race_dict['EventId'])
            womens_race_ressults = get_results(event_id=womens_race_dict['EventId'])

            # TODO merge my more knowledge based fields
            mens_res_list.append(flatten_results_to_race_properties(mens_race_results, mens_race_dict))
            womens_res_list.append(flatten_results_to_race_properties(womens_race_ressults, womens_race_dict))

    mens_res_df = pd.concat(mens_res_list)
    womens_res_df = pd.concat(womens_res_list)
    if csv_path is None:
        return mens_res_df, womens_res_df
    else:
        mens_res_df.to_csv("{}".format(csv_path))
        womens_res_df.to_csv("{}".format(csv_path))