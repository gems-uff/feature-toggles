# coding=utf-8
from mergeeffort import merge_analysis
from pygit2 import *
import pandas as pd
import os
import time

results = []
merges = pd.read_csv('../../data/branch_merges.csv')
print(f'{time.ctime()} ### Starting the collection process...')
for index, row in merges.iterrows():
    merge_sha = row['sha']
    project = row['project']
    print(f"Merge {index+1} of {len(merges)}. Project: {project}")
    if row['multiple_devs'] == True or row['branch_merge_message'] == True:
        project_path = "../../repos/" + project
        project_path = os.path.abspath(project_path)
        repo = Repository(project_path)
    
        commits = []
        _commit = merge_sha
        print(_commit)
        commits.append(repo.get(_commit))
        _merge_analisys= merge_analysis.analyse(commits,repo)

        if len(_merge_analisys) > 0:
            print(_merge_analisys)
            merge_effort = _merge_analisys[commits[0].hex]["extra"]
            results.append([project, merge_sha, merge_effort])    

df = pd.DataFrame(results, columns=['project', 'sha', 'merge_effort'])
df.to_csv('../../data/merge_effort.csv', index=False)