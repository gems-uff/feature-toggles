import os
import subprocess
import pandas as pd
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

def get_commits_list(project_path):
    command = "git rev-list --all --before='2018-05-31'"
    return execute_command(command, project_path)

def get_commit_date(commit_sha, project_path):
    command = f'git show -s --format=%ci {commit_sha}'
    return execute_command(command, project_path)

def get_commits_parameter_after(date, project_path):
    command = f"git rev-list --all --after='2018-05-31' --before='{date}'"
    return execute_command(command, project_path)

def get_commits_parameter_before(date, project_path):
    command = f"git rev-list --all --after='{date}' --before='2018-05-31'"
    return execute_command(command, project_path)

projects = pd.read_csv('../../data/control_projects.csv')
results = []
print(f'{time.ctime()} ### Starting the collection process...')
for index, row in projects.iterrows():
    project = row['project']
    project_path = f"../../repos/{project}"
    project_path = os.path.abspath(project_path)

    commits = get_commits_list(project_path).split('\n')
    if len(commits) > 0:
        middle_index = len(commits)//2
        middle_commit = commits[middle_index]
        middle_commit_date = get_commit_date(middle_commit, project_path)
        commits_before = get_commits_parameter_before(middle_commit_date, project_path)
        commits_before_list = commits_before.split('\n')
        commits_after = get_commits_parameter_after(middle_commit_date, project_path)
        commits_after_list = commits_before.split('\n')
        results.append([project, middle_commit, middle_commit_date, middle_index, len(commits), len(commits_before_list), len(commits_after_list)])
    else:
        print('Empty commits list!')

df = pd.DataFrame(results, columns=['project', 'middle_commit', 'middle_commit_date', 'middle_index', 'total_commits', 'QT_COMMIT_BFR', 'QT_COMMIT_AFT'])
df.to_csv('../../data/projects_control_points.csv', index=False)

