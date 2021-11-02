import pandas as pd


def create_rider_result_properties(mens_properties_df, csv_path=None):
    result_properties_list = ['IndividualDisplayName', 'IndividualFirstName', 'IndividualLastName',
                            'RankNumber', 'Rank', 'Bib', 'Age', 'DisplayName', 'DisplayFirstName', 'DisplayLastName',
                            'ResultValue', 'PointPcR', 'MandatoryDate']

    race_list = []
    for i, an_event in mens_properties_df.iterrows():
        race_results_df = pd.DataFrame(get_results(event_id=an_event['EventId']))

        race_results_df = race_results_df[result_properties_list]
        race_results_df['EventId'] = an_event['EventId']
        race_results_df['ResultTime'] = race_results_df.ResultValue.apply(extract_time)
        race_results_df['TimeFromLeader'] = race_results_df['ResultTime'] - race_results_df['ResultTime'].iloc[0]
        race_results_df['RaceDate'] = race_results_df.MandatoryDate.apply(parse_mandatory_date)
        race_results_df['FinishingLap'] = race_results_df.ResultValue.apply(parse_laps)

        race_list.append(race_results_df)
        rider_result_df = pd.concat(race_list)
        if csv_path == None:
            return rider_result_df
        else:
            rider_result_df.to_csv("{}/rider_result_df".format(csv_path))

