import pandas as pd
import os
import subprocess
import json
import sys
import time

def execute_command(command, path):
    try:
        # print(command)
        my_env = os.environ.copy()
        result = subprocess.check_output([command], stderr=subprocess.STDOUT, text=True, shell=True, env=my_env, cwd=path, encoding="latin-1")
        return result.strip()
    except subprocess.CalledProcessError as e:
        print("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output), flush=True)
        return ''

def get_commits(project_path):
    command = "git rev-list --all --before='2018-05-31'"
    return execute_command(command, project_path)

def get_commit_date(commit_sha, project_path):
    command = f'git show -s --format=%ci {commit_sha}'
    return execute_command(command, project_path)

'''
separator: space
'''
def getLoc(hash_parent, project_path):
    try:
        command = f"cloc --json --sum-one {hash_parent[0:10]}"
        return execute_command(command, project_path)
    except:
        return ""

def getJSONLOC(_json):
    _json_SOMA = ""
    try:
        if _json.find("SUM") >=0:
           _json_SOMA = "{" + chr(34) +  _json[_json.find("SUM"):]
        return _json_SOMA
    except:
        return ""


def getTotalLines(_json):
    LOC = 0
    try:
        _json_SOMA = getJSONLOC(_json)
        if _json_SOMA != "":
           x=json.loads(_json_SOMA)
           LOC = x["SUM"]["code"]
        else:
           LOC = -1

        return LOC
    except:
        return sys.exc_info()[0]


projects = pd.read_csv('../../data/control_projects.csv')

'''
python collect_loc.py 3 1
Arg 1 = number of slices to split the projects
Arg 2 = current slice of the split
'''
if len(sys.argv) > 2:
    number_slices = int(sys.argv[1])
    current_slice = int(sys.argv[2])
    projects_in_slice = len(projects)//number_slices

    if current_slice == 1:
        start = 0
    else:
        start = (projects_in_slice * (current_slice - 1))
    
    if current_slice == number_slices:
        end = len(projects)
    else:
        end = (projects_in_slice * (current_slice))
    print(f"{start}:{end}")
    projects = projects[start:end]

print(f'{time.ctime()} ### Starting the collection process...')
results = []
index_project = 1
for index,row in projects.iterrows():
    project = row['project']
    project_path = f"../../repos/{project}"
    project_path = os.path.abspath(project_path)

    commits = get_commits(project_path)
    commits = commits.split('\n')
    for index_commit, commit in enumerate(commits):
        print(f"{time.ctime()} ### Commit {index_commit+1} of {len(commits)}. Project: {index_project} of {len(projects)} - {project}")
        if commit != "":
            try:                    
                git_loc=getLoc(commit, project_path)                    
            except:
                git_loc=""
            
            _nLOC = 0
            _jsonLOC = getJSONLOC(git_loc)
            if git_loc != "":
                _nLOC = getTotalLines(git_loc)
            commit_date = get_commit_date(commit, project_path)
            results.append([project, commit, commit_date, _nLOC])
    index_project+=1
df = pd.DataFrame(results, columns=['project', 'sha', 'commit_date', 'loc'])
if len(sys.argv) > 2:
    df.to_csv(f"../../data/control_group_commits_loc-{current_slice}.csv", index=False)    
else:
    df.to_csv('../../data/control_group_commits_loc.csv', index=False)