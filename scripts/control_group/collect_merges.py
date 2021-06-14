import os
import subprocess
import pandas as pd
import time
from datetime import datetime

def execute_command(command, path):
    try:
        # print(command)
        my_env = os.environ.copy()
        result = subprocess.check_output([command], stderr=subprocess.STDOUT, text=True, shell=True, env=my_env, cwd=path, encoding="latin-1")
        return result.strip()
    except subprocess.CalledProcessError as e:
        print("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output), flush=True)
        return ''

def get_merges(project_path):
    command = "git rev-list --all --min-parents=2 --before='2018-05-31'"
    return execute_command(command, project_path)

def get_commit_date(commit_sha, project_path):
    command = f'git show -s --format=%ci {commit_sha}'
    return execute_command(command, project_path)

def get_parents_list(commit_sha, project_path):
    command = f"git log --pretty=%P -n 1 {commit_sha}"
    return execute_command(command, project_path)

def get_merge_base(commit1_sha, commit2_sha, project_path):
    command = f"git merge-base {commit1_sha} {commit2_sha}"
    return execute_command(command, project_path)

'''
separator is a \n between commits
'''
def get_commits_between(base_sha, parent_sha, project_path):
    command = f"git log --format=%H {base_sha}..{parent_sha}"
    return execute_command(command, project_path)

'''
separator is a \n between commits
'''
def get_authors_between(commit1, commit2, project_path):
    command = f"git shortlog -sne --no-merges {commit1}..{commit2}"
    return execute_command(command, project_path)

'''
separator is a \n between commits
'''
def get_authors_between_including(commit1, commit2, project_path):
    command = f"git show -s --format='%ae' {commit1}..{commit2}"
    authors_text = execute_command(command, project_path)
    authors = set()
    for author in authors_text.split('\n'):
        authors.add(author.strip())
    return list(authors)

def get_author(commit, project_path):
    command = f"git show -s --format='%ae' {commit}"
    return normalize_text(execute_command(command, project_path))

def normalize_text(text):
    return text.replace('\n', ' ').strip()

def get_commit_message(commit, project_path):
    command = f"git log --format=%B -n 1 {commit}"
    message = execute_command(command, project_path)
    return normalize_text(message)

def get_control_point(project):
    control_points = pd.read_csv('../../data/projects_control_points.csv')
    project_row = control_points[control_points['project'] == project]
    return project_row.iloc[0]['middle_commit_date']

'''
checks whether there is more than one commit author between base and commit
'''
def includes_multiple_authors(commit_sha, base_sha, project_path):
    # print(f'Checking authors between base: {base_sha}  commit: {commit_sha}')
    commits = get_commits_between(base_sha, commit_sha, project_path)
    
    if commit_sha == base_sha: 
        # print(get_author(commit_sha, project_path))
        return False
    if commits == '':
        return False
    # print(commits)
    commits = commits.split('\n')
    authors = get_authors_between_including(base_sha, commits[0], project_path)
    # print(authors)
    return len(authors) > 1

def is_branch_merge(commit_sha, project_path):
    
    parents = get_parents_list(commit_sha, project_path)
    parents = parents.split(" ")
    if len(parents) >= 2:
        parent1_sha = parents[0]
        parent2_sha = parents[1]
        merge_base = get_merge_base(parent1_sha, parent2_sha, project_path)
        # print(f"merge: {commit_sha} \n parent1: {parent1_sha} \n parent2: {parent2_sha} \n base: {merge_base}")
        # print('left')
        left = includes_multiple_authors(parent1_sha, merge_base, project_path)
        # print('right')
        right = includes_multiple_authors(parent2_sha, merge_base, project_path)
        multiple_authors_branches = left and right 
        branch_merge_message = False
        commit_message = get_commit_message(commit_sha, project_path)
        # print(commit_message)
        if 'merge branch' in commit_message.lower():
            branch_merge_message = True
        # print(multiple_authors_branches, branch_merge_message)
        return multiple_authors_branches, branch_merge_message
    return False, False


projects = pd.read_csv('../../data/control_projects.csv')
results = []
print(f'{time.ctime()} ### Starting the collection process...')
for index_project, row in projects.iterrows():
    project = row['project']
    project_path = f"../../repos/{project}"
    project_path = os.path.abspath(project_path)
    control_point = get_control_point(project)
    control_point_datetime = datetime.strptime(control_point, '%Y-%m-%d %H:%M:%S %z')
    merges = get_merges(project_path)
    merges_list = merges.split()
    for index_merge, merge in enumerate(merges_list):
        print(f"Merge {index_merge+1} of {len(merges_list)}. Project: {index_project} of {len(projects)} - {project}")
        merge_sha = merge
        commit_date = get_commit_date(merge_sha, project_path)
        commit_datetime = datetime.strptime(commit_date, '%Y-%m-%d %H:%M:%S %z')
        multiple_devs, branch_merge_message = is_branch_merge(merge_sha, project_path)
        results.append([project, merge_sha, commit_date, multiple_devs, branch_merge_message, commit_datetime >= control_point_datetime])
df = pd.DataFrame(results, columns=['project', 'sha', 'date', 'multiple_devs', 'branch_merge_message', 'after_control'])
df.to_csv('../../data/branch_merges.csv', index=False)

