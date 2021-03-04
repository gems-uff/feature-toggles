'''
goes through the entries in the csv for the projects in the dataset, using the clone date to estimate the most recent commit at the time. 
Combines the existing information with the commit hash and generates a new table (csv)
'''

import pandas as pd
import time
import os
import subprocess
import pathlib

def load_data(dataset):
   return pd.read_csv(dataset, header=0, delimiter=';')


def collect_data(dataset, projects_folder):
   starting_folder = pathlib.Path(__file__).parent.absolute()
   os.chdir(projects_folder)
   hashes = []
   for index, repo in dataset.iterrows():
      project_name = repo['full_name'].replace('/','-')
      project_path = f"{projects_folder}/{project_name}"
      clone_date = repo['dt_clone']
      try:
         os.chdir(project_path)
         command = "git rev-list -1 --before='{}' master ".format(clone_date)
         try:
            result = subprocess.check_output([command], stderr=subprocess.STDOUT, text=True, shell=True)
            hashes.append(result.strip())
         except subprocess.CalledProcessError as e:
            print ("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))
      except:
            hashes.append('')
            print(f'project {project_name} not found')
   os.chdir(starting_folder)
   dataset['SHA_clone'] = hashes
   dataset.to_csv('repos_2.csv', index=False, sep=';')

dataset = load_data('repos_test.csv')
collect_data(dataset, "/home/developer/Documents/workspace/ft_eduardo/projects")
