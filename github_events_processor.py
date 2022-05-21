'''
Github events processor
Author: Krzysztof Kruszczynski
version:0.1
This script provides functionality to calculate daily aggregates for repositories and users for a given period of time
'''

import json
import os
import pandas as pd
import copy


def read_json_data(path):
    with open(path) as json_file:
        data = json.load(json_file)
    json_file.close()
    return data


if __name__ == "__main__":
    # Define names for DataFrame columns. Optimize this layout later.
    # In general code below should be reorganized into classes and methods
    hours_start = 0
    hours_end = 2 #max=23
    config_file = read_json_data("config_file.json")
    raw_df_columns = ['id', 'type', 'actor', 'repo', 'payload', 'public', 'created_at',
                      'org', 'project_id', 'project_name', 'user_id', 'user_name']
    event_columns_map = {"StarEvent": 'stars', "ForkEvent": 'forks', "IssueEvent": 'issues', "PullRequestEvent": 'PRs'}
    events_list = ["StarEvent", "ForkEvent", "IssueEvent", "PullRequestEvent"]
    repo_aggreated_columns = ['Date', 'project_id', 'project_name', 'stars', 'forks', 'issues', 'PRs']
    user_aggreated_columns = ['Date', 'user_id', 'user_name', 'stars', 'issues', 'PRs']
    repo_aggregated_df = pd.DataFrame(columns=repo_aggreated_columns)
    user_aggregated_df = pd.DataFrame(columns=user_aggreated_columns)

    # iterate over particular rawData files
    for i in range(config_file["start_day"], config_file["end_day"] + 1):
        aggregated_df = pd.DataFrame(columns=raw_df_columns)
        for hour in range(hours_start, hours_end):
            # Condition statement for day name should be implemented also for months
            if i <= 9:
                path_to_data = f"{os.getcwd()}\\.RawData\\{config_file['year']}-0{config_file['month']}-0{i}-{hour}.json.gz"
            else:
                path_to_data = f"{os.getcwd()}\\.RawData\\{config_file['year']}-0{config_file['month']}-{i}-{hour}.json.gz"
            try:
                temp_df = pd.read_json(path_to_data, lines=True, compression='gzip')
                repo_specific_df = temp_df['repo'].apply(pd.Series)
                user_specific_df = temp_df['actor'].apply(pd.Series)
                temp_df['project_id'] = repo_specific_df['id']
                temp_df['project_name'] = repo_specific_df['name']
                temp_df['user_id'] = user_specific_df['id']
                temp_df['user_name'] = user_specific_df['login']
                aggregated_df = aggregated_df.append(temp_df, ignore_index=True)
            except Exception as e:
                print(f"Not able to process file {path_to_data}")

        repo_grouped_df_raw = aggregated_df.groupby(["project_name", "type"])
        repo_grouped_df = aggregated_df.groupby(["project_name", "type"]).count()

        user_grouped_df_raw = aggregated_df.groupby(["user_name", "type"])
        user_grouped_df = aggregated_df.groupby(["user_name", "type"]).count()

        aggregated_df["Date"] = f"{config_file['year']}-0{config_file['month']}-{i}"
        aggregated_df["forks"] = 0
        aggregated_df["stars"] = 0
        aggregated_df["issues"] = 0
        aggregated_df["PRs"] = 0
        repo_index_left = [repo_grouped_df.index[i] for i in range(0, len(repo_grouped_df.index)) if
                           repo_grouped_df.index[i][1] in events_list]
        user_index_left = [user_grouped_df.index[i] for i in range(0, len(user_grouped_df.index)) if
                           user_grouped_df.index[i][1] in events_list]
        # Need to find solution without copying data
        aggregated_user_df = copy.deepcopy(aggregated_df)
        for item in repo_index_left:
            try:
                occurences = repo_grouped_df_raw.get_group(item).shape[0]
                aggregated_df.loc[aggregated_df["project_name"] == item[0], event_columns_map[item[1]]] = occurences
            except Exception as e:
                print(f"{item} not added to the report")
                continue
        # Copy/Paste of solution above. Here is place for improvement
        for item_user in user_index_left:
            try:
                occurences = user_grouped_df_raw.get_group(item_user).shape[0]
                aggregated_user_df.loc[
                    aggregated_user_df["user_name"] == item[0], event_columns_map[item[1]]] = occurences
            except Exception as e:
                print(f"{item} not added to the report")
                continue
        aggregated_df.drop_duplicates(subset='project_name', keep='first', inplace=True)
        aggregated_df.reset_index(drop=True, inplace=True)
        repo_aggregated_df = pd.concat([repo_aggregated_df, aggregated_df], join='inner')

        aggregated_user_df.drop_duplicates(subset='user_name', keep='first', inplace=True)
        aggregated_user_df.reset_index(drop=True, inplace=True)
        user_aggregated_df = pd.concat([user_aggregated_df, aggregated_user_df], join='inner')

    repo_aggregated_df.to_csv(config_file["repository_data_file_name"], columns=repo_aggreated_columns, index=False)
    user_aggregated_df.to_csv(config_file["user_data_file_name"], columns=user_aggreated_columns, index=False)
