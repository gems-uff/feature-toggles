Scripts execution order:

1. select_control_projects.py
    - Purpose: randomly selects and clones projects from the input file that meet the minimum requirements. Currently the requirements are: at least 171 commits, at least 1 issue, does not use any FT framework in the current version. The number of selected projects is equal to about 10% of the amount of projects in C_Cleaned for each language.
    - Input: data/github_projects_unfiltered.xlsx, original dataset mysql database
    - Output: data/control_projects.csv, cloned project in repos folder
2. collect_control_points.py
    - Purpose: splits the commit's history of each project in the middle (considers the end of the history to be 2018-05-31, the collection date of the main dataset) and collects the following metrics: QT_COMMIT_BEFORE, QT_COMMIT_AFTER.
    - Input: data/control_projects.csv
    - Output: data/projects_control_points.csv
3. collect_merges.py
    - Purpose: collects the list of branch merges (before 2018-05-31) for each selected project. In order to be considered a branch merge, it must have at least two unique authors on each branch OR include 'merge branch' in its commit message. It also records if the branch merge has occurred after the control point of the project (middle of its commit history).
    - Input: data/control_projects.csv
    - Output: data/branch_merges.csv
4. collect_merge_effort.py
    - Purpose: collects the merge effort metric for each branch merge of each selected project. Uses the [merge effort tool](https://github.com/gems-uff/merge-effort).
    - Input: data/branch_merges.csv
    - Output: data/merge_effort.csv
5. collect_loc.py
    - Purpose: collects the number of lines of code (LOC) for each commit (before 2018-05-31) in each selected project. It also collects the date for each commit. Uses the [CLOC tool](https://github.com/AlDanial/cloc). Since the execution might take time for very large projects, it can also be executed for different slices of the selected projects. For example, if executed using `python collect_loc.py 3 1`, it will collect the loc the first split of the selected projects divided in three parts. The first argument is the number of splits to split control_projects and the second is the current split to execute.
    - Input: data/control_projects.csv
    - Output: data/control_group_commits_loc.csv or data/control_group_commits_loc-\<splitnumber>.csv
6. collect_issues.py
    - Purpose: queries the GitHub API to collect issues (created before 2018-05-31) data for each selected project. Selects only issues that are considered bug issues, according to the method described in the paper (inspects issue title, body and tags). Extracted data for each issue includes: issue number, creation date, closing date, evidence to be considered a bug issue, and whether it will be considered in the before or after the control point group. To classify in before or after control point, we follow the same procedure described in the paper for the main dataset. This script requires that an environment variable GITHUB_TOKEN be set with a GitHub developer token.
    - Input: data/projects_control_points.csv, data/control_projects.csv
    - Output: data/control_issues.csv
7. merge_data_files.py
    - Purpose: merges the data files that were splitted during the collection process. Currently only the control_group_commits_loc.csv may be splitted.
    - Input: data/control_group_commits_loc-\<splitnumber>.csv files
    - Output: control_group_commits_loc.csv
8. process_metrics.csv
    - Purpose: calculates the remaining metrics using the collected data. 
    - Input: data/projects_control_points.csv, data/branch_merges.csv, data/merge_effort.csv, data/control_group_commits_loc.csv, data/control_issues.csv
    - Output: R Scripts/Dataset/control/control_projects_extracted_metrics.csv

---

Breakdown of the raw metrics collected for each control project:
- QT_COMMIT_BEFORE: number of commits before the control point.
- QT_COMMIT_AFTER: number of commits after the control point.
- MERGES_BEFORE: number of branch merges before the control point.
- MERGES_AFTER: number of branch merges after the control point.
- MERGE_EFFORT_BEFORE: branch merge effort sum before the control point.
- MERGE_EFFORT_AFTER:  branch merge effort sum after the control point.
- ISSUES_BEFORE: number of bug issues before the control point.
- ISSUES_AFTER: number of bug issues after the control point.
- LOC_BEFORE: sum of the project's LOC for commits before the control point.
- LOC_AFTER: sum of the project's LOC for commits after the control point.
- TOTAL_TIME_BEFORE: sum of the number of days to close issues that happened before the control point.
- TOTAL_TIME_AFTER: sum of the number of days to close issues that happened after the control point.

---

Composite metrics (calculted using both raw and composite metrics):

- (RQ 2.1) NUM_MERGES_PER_100_COMMITS_BEFORE = (MERGES_BEFORE * 100) / QT_COMMIT_BEFORE
- (RQ 2.1) NUM_MERGES_PER_100_COMMITS_AFTER = (MERGES_AFTER * 100) / QT_COMMIT_AFTER
- (RQ 2.2) AVERAGE_EFFORT_PER_MERGE_BEFORE = MERGE_EFFORT_BEFORE / MERGES_BEFORE
- (RQ 2.2) AVERAGE_EFFORT_PER_MERGE_AFTER = MERGE_EFFORT_AFTER / MERGES_AFTER
- (RQ 2.3) TOTAL_AVG_MERGE_EFFORT_IN_100_COMMITS_BEFORE = AVERAGE_EFFORT_PER_MERGE_BEFORE * NUM_MERGES_PER_100_COMMITS_BEFORE
- (RQ 2.3) TOTAL_AVG_MERGE_EFFORT_IN_100_COMMITS_AFTER = AVERAGE_EFFORT_PER_MERGE_AFTER * NUM_MERGES_PER_100_COMMITS_AFTER
- AVG_K_LOC_PER_COMMIT_BEFORE = (LOC_BEFORE)/1000)/ QT_COMMIT_BEFORE 
- AVG_K_LOC_PER_COMMIT_AFTER = (LOC_AFTER)/1000)/ QT_COMMIT_AFTER
- (RQ 3.1) ISSUES_KLOC_IN_100_COMMITS_BEFORE = (ISSUES_BEFORE * 100) / QT_COMMIT_BEFORE / AVG_K_LOC_PER_COMMIT_BEFORE
- (RQ 3.1) ISSUES_KLOC_IN_100_COMMITS_AFTER = (ISSUES_AFTER * 100) / QT_COMMIT_AFTER / AVG_K_LOC_PER_COMMIT_AFTER
- (RQ 3.2) AVG_TIME_PER_ISSUES_BEFORE = TOTAL_TIME_BEFORE / ISSUES_BEFORE
- (RQ 3.2) AVG_TIME_PER_ISSUES_AFTER = TOTAL_TIME_AFTER / ISSUES_AFTER
- (RQ 3.3) TOTAL_TIME_PER_KLOC_IN_100_COMMITS_BEFORE = (TOTAL_TIME_BEFORE * 100) / QT_COMMIT_BEFORE / AVG_K_LOC_PER_COMMIT_BEFORE
- (RQ 3.3) TOTAL_TIME_PER_KLOC_IN_100_COMMITS_AFTER = (TOTAL_TIME_AFTER * 100) / QT_COMMIT_AFTER / AVG_K_LOC_PER_COMMIT_AFTER
