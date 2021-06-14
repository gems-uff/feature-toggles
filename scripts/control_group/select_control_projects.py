import pandas as pd
import clone_projects
import check_framework_usage

MIN_COMMITS = 171
MIN_ISSUES = 1
def get_number_projects(language):
    projects_amount = {
        'C#': 9,
        'Java': 20,
        'JavaScript': 38,
        'PHP': 2,
        'Python': 16,
        'Ruby': 13,
    }
    if language in projects_amount:
        return projects_amount[language]
    return 0

def get_programming_languages():
    return ['C#', 'Java', 'JavaScript', 'PHP', 'Python', 'Ruby']

df = pd.read_excel('../../data/github_projects_unfiltered.xlsx')
df = df.astype({"owner": str, "name": str})
df['project'] = df[['owner','name']].agg('/'.join, axis=1)

selected_projects = pd.DataFrame([], columns=df.columns)
for programming_language in get_programming_languages():
    print(f'Checking {programming_language} projects:')
    selected_projects_language = pd.DataFrame([], columns=df.columns)
    checked_projects = pd.DataFrame([], columns=df.columns)
    df_language = df[df['primaryLanguage'] == programming_language]
    while len(selected_projects_language) < get_number_projects(programming_language):
        project = df_language[(~df_language.index.isin(checked_projects.index)) 
                              & (df_language['commits'] >= MIN_COMMITS)
                              & (df_language['issues'] >= MIN_ISSUES)]
        selected_project = project.sample(n=1, random_state = 99)
        project_name = selected_project.iloc[0]['project']
        project_language = selected_project.iloc[0]['primaryLanguage']
        project_cloned = clone_projects.clone_project(project_name)
        if project_cloned:
            uses_feature_toggle= check_framework_usage.uses_framework(project_name, project_language)
            if not uses_feature_toggle:
                selected_projects_language = pd.concat([selected_projects_language, selected_project])
            print(f"Project {project_name} uses feature toggle framework? {uses_feature_toggle}")
        else:
            print(f'Could not clone project {project_name}. Getting next one on the list.')
        checked_projects = pd.concat([checked_projects, selected_project])
    selected_projects = pd.concat([selected_projects, selected_projects_language])
selected_projects.to_csv('../../data/control_projects.csv', index=False)