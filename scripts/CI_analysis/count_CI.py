import pandas as pd
import ast

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

def load_data(dataset):
   return pd.read_csv(dataset, header=0, delimiter=';')


def count_CI_usage(dataset):
   usage = {
      'jenkins ci':0,
      'travis ci': 0,
      'red hat ansible':0,
      'jitpack.io'	:0,
      'solano ci'	:	0,
      'circle ci'	:	0,
      'cloud foundry':0,
      'gitlab ci'	:	0
   }
   for index, repo in dataset.iterrows():
      files = repo['CI_files']
      try:
         files = ast.literal_eval(files)
      except:
         files = []
      
      
      for f in files:
         for CI_service, service_files in CI_files.items():
            for service_file in service_files:
               if(f.lower() == service_file.lower()):
                  usage[CI_service] += 1



      
   print(usage)

dataset = load_data('repos_3.csv')
count_CI_usage(dataset)
