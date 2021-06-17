#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from datetime import datetime, timezone

def try_strptime(s):
    fmts=["%Y-%m-%dT%H:%M:%S.%f","%Y-%m-%d %H:%M:%S %z", "%Y-%m-%d %H:%M:%S.%f%z", "%Y-%m-%d %H:%M:%S%z"]
#     print(s)
    for fmt in fmts:
        try:
            return datetime.strptime(s, fmt)
        except:
            continue
    return None

def is_after_control_date(project, date):
    project = control_points[control_points['project'] == project]
    control_date = project.iloc[0]['middle_commit_date']
    control_date = try_strptime(control_date)
    local_timezone = datetime.now(timezone.utc).astimezone().tzinfo
    control_date = control_date.astimezone(local_timezone)
    bkp_date = date
    date = try_strptime(date)
    if date == None:
        print(date)
        print(bkp_date)
    date = date.astimezone(local_timezone)
    if date >= control_date:
        return True
    return False

merges = pd.read_csv("../../data/branch_merges.csv")
# print(merges.shape)
merges = merges[(merges['multiple_devs'] | merges['branch_merge_message'])]
# print(merges.shape)
# display(merges.head())


merge_effort = pd.read_csv("../../data/merge_effort.csv")
# print(merge_effort.shape)
# display(merge_effort.head())


merges_effort = pd.merge(merges, merge_effort, on=['sha', 'project'])
# print(merges_effort.shape)
# display(merges_effort.head())


issues = pd.read_csv('../../data/control_issues.csv')
# print(issues.shape)
# display(issues.head())


commits_loc = pd.read_csv('../../data/control_group_commits_loc.csv')
# print(commits_loc.shape)
# display(commits_loc.head())


control_points = pd.read_csv('../../data/projects_control_points.csv')
# print(control_points.shape)
# display(control_points.head())

# calculate MERGES_before and MERGES_after
projects = merges['project'].unique()
results = []
for project in projects:
    merges_project = merges[merges['project'] == project]
    merges_before = merges_project[merges_project['after_control'] == False]
    merges_after = merges_project[merges_project['after_control'] == True]
    results.append([project, len(merges_before), len(merges_after), len(merges_project)])
number_merges = pd.DataFrame(results, columns=['project', 'MERGES_BEFORE', 'MERGES_AFTER', 'total_merges'])
# number_merges

# calculate MERGE_EFFORT_BEFORE and MERGE_EFFORT_AFTER
results = []
for project in projects:
    merges_project = merges_effort[merges_effort['project'] == project]
    merges_before = merges_project[merges_project['after_control'] == False]
    merges_after = merges_project[merges_project['after_control'] == True]
    merge_effort_before = merges_before['merge_effort'].sum()
    merge_effort_after = merges_after['merge_effort'].sum()
    results.append([project, merge_effort_before, merge_effort_after])
merge_effort = pd.DataFrame(results, columns=['project', 'MERGE_EFFORT_BEFORE', 'MERGE_EFFORT_AFTER'])
# merge_effort

results = []
for project in projects:
    issues_project = issues[issues['project'] == project]
    issues_before = issues_project[issues_project['category'] == 'before']
    issues_after = issues_project[issues_project['category'] == 'after']
    results.append([project, len(issues_before), len(issues_after), len(issues_project)])
number_issues = pd.DataFrame(results, columns=['project', 'ISSUES_BEFORE', 'ISSUES_AFTER', 'total_issues'])
# number_issues


results = []
for project in projects:
    issues_project = issues[issues['project'] == project]
    sum_days_before = 0
    sum_days_after = 0
    for index, issue in issues_project.iterrows():
        create_date = try_strptime(issue['create_date'])
        close_date = try_strptime(issue['close_date'])
        if close_date != None:
            difference = close_date - create_date
            if issue['category'] == 'before':
                sum_days_before += difference.days
            else:
                sum_days_after += difference.days
    results.append([project, sum_days_before, sum_days_after])
total_time_issues = pd.DataFrame(results, columns=['project', 'TOTAL_TIME_BEFORE', 'TOTAL_TIME_AFTER'])
# total_time_issues


is_after = []
for index, commit in commits_loc.iterrows():
    commit_date = commit['commit_date']
    project = commit['project']
    is_after.append(is_after_control_date(project, commit_date))
commits_loc['after_control'] = is_after
# commits_loc.head()


# calculate LOC_BEFORE and LOC_AFTER
results = []
for project in projects:
    commits_project = commits_loc[commits_loc['project'] == project]
    commits_before = commits_project[commits_project['after_control'] == False]
    commits_after = commits_project[commits_project['after_control'] == True]
    loc_before = commits_before['loc'].sum()
    loc_after = commits_after['loc'].sum()
    results.append([project, loc_before, loc_after])
loc = pd.DataFrame(results, columns=['project', 'LOC_BEFORE', 'LOC_AFTER'])
# loc


# calculate QT_COMMIT_BEFORE and QT_COMMIT_AFTER
results = []
for project_name in projects:
    project = control_points[control_points['project'] == project_name]
    QT_COMMIT_BEFORE = project.iloc[0]['QT_COMMIT_BFR']
    QT_COMMIT_AFTER = project.iloc[0]['QT_COMMIT_AFT']
    results.append([project_name, QT_COMMIT_BEFORE, QT_COMMIT_AFTER])
qt_commit = pd.DataFrame(results, columns=['project', 'QT_COMMIT_BEFORE', 'QT_COMMIT_AFTER'])
# qt_commit


result = pd.merge(number_merges, merge_effort, on=['project'])
result = pd.merge(result, number_issues, on=['project'])
result = pd.merge(result, total_time_issues, on=['project'])
result = pd.merge(result, loc, on=['project'])
result = pd.merge(result, qt_commit, on=['project'])
# result

# Composite metrics

result['NUM_MERGES_PER_100_COMMITS_BEFORE'] = (result['MERGES_BEFORE'] * 100) / result['QT_COMMIT_BEFORE']
result['NUM_MERGES_PER_100_COMMITS_AFTER'] = (result['MERGES_AFTER'] * 100) / result['QT_COMMIT_AFTER']
result['AVERAGE_EFFORT_PER_MERGE_BEFORE'] = result['MERGE_EFFORT_BEFORE'] / result['MERGES_BEFORE']
result['AVERAGE_EFFORT_PER_MERGE_AFTER'] = result['MERGE_EFFORT_AFTER'] / result['MERGES_AFTER']
result['TOTAL_AVG_MERGE_EFFORT_IN_100_COMMITS_BEFORE'] = result['AVERAGE_EFFORT_PER_MERGE_BEFORE'] / result['NUM_MERGES_PER_100_COMMITS_BEFORE']
result['TOTAL_AVG_MERGE_EFFORT_IN_100_COMMITS_AFTER'] = result['AVERAGE_EFFORT_PER_MERGE_AFTER'] / result['NUM_MERGES_PER_100_COMMITS_AFTER']
result['AVG_K_LOC_PER_COMMIT_BEFORE'] = (result['LOC_BEFORE'] / 1000) / result['QT_COMMIT_BEFORE']
result['AVG_K_LOC_PER_COMMIT_AFTER'] = (result['LOC_AFTER'] / 1000) / result['QT_COMMIT_AFTER']
result['ISSUES_KLOC_IN_100_COMMITS_BEFORE'] = (result['ISSUES_BEFORE'] * 100) / result['QT_COMMIT_BEFORE'] / result['AVG_K_LOC_PER_COMMIT_BEFORE']
result['ISSUES_KLOC_IN_100_COMMITS_AFTER'] = (result['ISSUES_AFTER'] * 100) / result['QT_COMMIT_AFTER'] / result['AVG_K_LOC_PER_COMMIT_AFTER']
result['AVG_TIME_PER_ISSUES_BEFORE'] = result['TOTAL_TIME_BEFORE'] / result['ISSUES_BEFORE']
result['AVG_TIME_PER_ISSUES_AFTER'] = result['TOTAL_TIME_AFTER'] / result['ISSUES_AFTER']
result['TOTAL_TIME_PER_KLOC_IN_100_COMMITS_BEFORE'] = (result['TOTAL_TIME_BEFORE'] * 100) / result['QT_COMMIT_BEFORE'] / result['AVG_K_LOC_PER_COMMIT_BEFORE']
result['TOTAL_TIME_PER_KLOC_IN_100_COMMITS_AFTER'] = (result['TOTAL_TIME_AFTER'] * 100) / result['QT_COMMIT_AFTER'] / result['AVG_K_LOC_PER_COMMIT_AFTER']
# result.head()

result.to_csv('../../R Scripts/Dataset/control/control_projects_extracted_metrics.csv', index=False)