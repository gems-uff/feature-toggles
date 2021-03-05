'''
goes through the entries in the csv for the projects in the dataset, checking if they have any CI files. 
Combines the existing information with the new extracted information and generates a new table (csv)
'''

import pandas as pd
import time
import os
import subprocess
import pathlib
import glob

CI_files = {
'jenkins ci'	:	['jenkinsfile'],
'travis ci'	:	['.travis.yml'],
'red hat ansible'	:	['playbook.yml'],
'jitpack.io'	:	['jitpack.yml'],
'solano ci'	:	['solano.yml'],
'circle ci'	:	['circle.yml', '.circle.yml'],
'cloud foundry'	:	['manifest.yml'],
'gitlab ci'	:	['.gitlab-ci.yml'],
}

def checkout_revision(revision):
    executed = execute_command('git reset --hard')
    if(executed):
        checkout_command = f"git checkout -f {revision}"
        executed = execute_command(checkout_command)
    return executed    

def execute_command(command):
    executed = False
    try:
        my_env = os.environ.copy()
        result = subprocess.check_output([command], stderr=subprocess.STDOUT, text=True, shell=True, env=my_env)
        output = '{} ### {}'.format(time.ctime(), result)
#         print(output)
        executed = True
    except subprocess.CalledProcessError as e:
        print("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output), flush=True)
    return executed

def check_CI_files():
   detected_files = []
   print(os.getcwd())
   print(os.listdir())
   for file_name in os.listdir():
      for service, service_files in CI_files.items():
         for service_file in service_files:
            if(file_name.lower() == service_file.lower()):
               detected_files.append(service_file.lower())
   return detected_files


def load_data(dataset):
   return pd.read_csv(dataset, header=0, delimiter=';')

'''
- checkout the 'SHA clone' revision
- check if the repository has any of the CI tools files (CI_files)
- add the information to the csv
'''
def detect_CI(dataset, projects_folder):
   starting_folder = pathlib.Path(__file__).parent.absolute()
   os.chdir(projects_folder)
   has_CI_column = []
   CI_files_column = []
   for index, repo in dataset.iterrows():
      project_name = repo['full_name'].replace('/','-')
      print(project_name)
      project_path = f"{projects_folder}/{project_name}"
      clone_date = repo['dt_clone']
      try:
         os.chdir(project_path)
         checkout_revision(repo['SHA_clone'])
         files = check_CI_files()
         print(files)
         has_CI_column.append(True if len(files) > 0 else False)
         CI_files_column.append(files)
      except:
         has_CI_column.append(False)
         CI_files_column.append('')
      
   os.chdir(starting_folder)
   dataset['has_CI_files'] = has_CI_column
   dataset['CI_files'] = CI_files_column
   dataset.to_csv('repos_3.csv', index=False, sep=';')

dataset = load_data('repos_2.csv')
detect_CI(dataset, "/home/developer/Documents/workspace/ft_eduardo/projects")
# clone_projects(dataset, '/Users/helenocampos/Documents/workspace/test')
#result = subprocess.check_output(['git clone https://github.com/ibroadfo/flowerpot.git C:/Users/Heleno.DESKTOP-89HH2F6/Documents/workspace_test/test/ibroadfo/flowerpot'], stderr=subprocess.STDOUT, text=True, shell=True)
#print(result)