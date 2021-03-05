'''
goes through the entries in the csv for the projects in the dataset, using the clone date to estimate the most recent commit at the time. 
Combines the existing information with the commit hash and generates a new table (csv)
'''

import pandas as pd
import time
import os
import subprocess

def load_data(dataset):
   return pd.read_csv(dataset, header=0, delimiter=';')


def clone_projects(dataset, projects_path):
    if(not os.path.exists(projects_path)):
        os.mkdir(projects_path)
    current_index = 0
    for index, repo in dataset.iterrows():
        current_index +=1
        status = (current_index / len(dataset)) * 100
        project_name = repo['full_name'].replace('/','-')
        print(project_name)
        print('{} ### {:.1f}% completed. Processing project: {}'.format(time.ctime(), status, repo[2]))
        folder = projects_path + '/' + project_name
        clone_url = 'https://github.com/{}.git'.format(repo['full_name'])
        if(not os.path.exists(folder)):
            command = 'git clone {} {}'.format(clone_url, folder)

            try:
                result = subprocess.check_output([command], stderr=subprocess.STDOUT, text=True, shell=True)
                print(result)
            except subprocess.CalledProcessError as e:
                print ("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))


dataset = load_data('repos_test.csv')
clone_projects(dataset, '/home/developer/Documents/workspace/ft_eduardo/projects')