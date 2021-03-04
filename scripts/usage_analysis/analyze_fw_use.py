'''
goes through the entries in the csv for the projects in the dataset, checking if they use the FWs extensively.

'''

import pandas as pd
import os
import subprocess
import pathlib

# dataset_file = "data_test.csv"
dataset_file = "data.csv"
# projects_folder = "/home/developer/Documents/workspace/ft_eduardo/projects"
projects_folder = "/home/heleno/ft_eduardo/projects"

patterns = {
   "Togglz":["Import org.togglz.core.feature"],
   "Gutter":["gutter.client"],
   "FF4J":["import org.ff4j.FF4j"],
   "Switcheroo":["IFeatureToggle"],
   "FeatureSwitcher":["using FeatureSwitcher"],
   "Rollout":["Rollout.new($redis)"],
   "featureflags":["Featureflags.defaults","class Admin::FeaturesController"],
   "Qandidate Toggle":["(.*?)Qandidate(.*?)Toggle(.*?)"],
   "Ericelliot/feature-toggle":["require\\(. feature-toggles.\\)"],
   "Gargoyle":["from gargoyle import gargoyle"],
   "angular-toggle-switch":["module.provider\\('toggleSwitchConfig'"],
   "django-waffle":["waffle.decorators", "(from|import) waffle"],
   "feature_flipper":["FeatureFlipper.features do"],
   "FeatureToggle":["using FeatureToggle","using FeatureToggle.Toggles;"],
   "Flask-FeatureFlags":["from flask_featureflags"],
   "fflip":["require\\(. flip.\\)"],
   "ember-feature-flags":["config.featureFlags"]
}


def checkout_revision(revision):
    executed = execute_command('git reset --hard')
    if(executed):
        checkout_command = f"git checkout -f {revision}"
        executed = execute_command(checkout_command)
    return executed    

def execute_command(command):
    executed = False
    output = ''
    try:
        my_env = os.environ.copy()
      #   print(command)
        output = subprocess.check_output([command], stderr=subprocess.STDOUT, text=True, shell=True, env=my_env)
      #   print(output)
        executed = True
    except subprocess.CalledProcessError as e:
        print("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output), flush=True)
    return executed, output

def check_references(framework_name, commit_SHA):
   pattern_list = patterns[framework_name]
   references_number = 0
   for pattern in pattern_list:
      _grep_string = pattern.replace(" ","(.*?)")
      _grep_string = chr(34) + _grep_string + chr(34)

      command = f"git grep -i -E {_grep_string} {commit_SHA} | wc -l"
      executed, output = execute_command(command)
      try:
         references_number+=int(output)
      except:
         pass
   return references_number

def load_data(dataset):
   return pd.read_csv(dataset, header=0, delimiter=';')


def analyze_projects(dataset, projects_folder):
   starting_folder = pathlib.Path(__file__).parent.absolute()
   os.chdir(projects_folder)
   references_adoption = []
   references_current = []
   for index, repo in dataset.iterrows():
      project_path = f"{projects_folder}/{repo['full_name']}"
      try:
         if(os.path.isdir(project_path)):
            os.chdir(project_path)
            print(os.getcwd(), flush=True)
            # checkout_revision(repo['FT_commit'])
            adoption = check_references(repo['framework'], repo['FT_commit'])

            # checkout_revision(repo['SHA_clone'])
            current = check_references(repo['framework'], repo['SHA_clone'])

            references_adoption.append(adoption)
            references_current.append(current)
         else:
            references_adoption.append("")
            references_current.append("")
      except Exception as e:
         references_adoption.append("")
         references_current.append("")
         print(e)
      
   os.chdir(starting_folder)
   dataset['references_adoption'] = references_adoption
   dataset['references_current'] = references_current
   dataset.to_csv('data_2.csv', index=False, sep=';')

dataset = load_data(dataset_file)
analyze_projects(dataset, projects_folder)
