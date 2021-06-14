# -*- coding: UTF-8 -*-
import os
import time
import subprocess
import platform
import pandas as pd

#TODO: add a timeout. when input is requested, timeout if no input is given.
def clone_project(project_fullname):
    REPOS_PATH = os.path.abspath("../../repos")

    if(not os.path.exists(REPOS_PATH)):
        os.mkdir(REPOS_PATH)
    project_path = os.path.join(REPOS_PATH,project_fullname)
    project_path = os.path.abspath(project_path)
    project_URL = f"https://www.github.com/{project_fullname}"
    print(f'{time.ctime()} ### Cloning {project_fullname} into {project_path}...')
    if(not os.path.exists(project_path)):
        command = 'git clone {} {}'.format(project_URL, project_fullname)
        return execute_command(command, REPOS_PATH)
    else:
        print(f"Project {project_fullname} already exists.")
        return True
    return False

def execute_command(command, path):
    executed = False
    try:
        my_env = os.environ.copy()
        result = subprocess.check_output([command], stderr=subprocess.STDOUT, text=True, cwd=path, shell=True, env=my_env)
        executed = True
    except subprocess.CalledProcessError as e:
        print("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output), flush=True)
    return executed

def main():
    projects = pd.read_csv('../../data/control_projects.csv')
    
    print(f'{time.ctime()} ### Starting the clone process...')
    for index, row in projects.iterrows():
        project = row['project']
        print(f'Cloning project {index+1} of {len(projects)} - {project}')
        clone_project(project)
        
if __name__ == '__main__':
    main()