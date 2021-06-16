import requests
import time
from datetime import datetime, timezone
import os
import sys
import pandas as pd

def get_issues(project_org, project_name):
    token = os.getenv('GITHUB_TOKEN')
    if token != None:
        local_timezone = datetime.now(timezone.utc).astimezone().tzinfo
        issues = []
        project = f"{project_org}/{project_name}"
        control_date = get_control_date(project, local_timezone)
        for i in range(1,200):
            headers = {'Accept': 'application/vnd.github.cloak-preview', 'Authorization': 'token ' + token}
            url = f"https://api.github.com/repos/{project}/issues?state=all&per_page=100&page=" + str(i)
            print(f'{time.ctime()} ### Requesting issues from {project} (page {i})...')
            data = requests.get(url,headers=headers).json()
            
            if len(data) == 0:
                break
    
            for _issues in data:
                if not _issues.get("message") is None:
                    print("error:" + str(project))
                    print(_issues)
                    sys.exit()

                _number = _issues.get("number")
                _title = _issues.get("title")
                _body = _issues.get("body") if not _issues.get("body") is None else ""
                create_date = datetime.strptime(_issues.get("created_at"), '%Y-%m-%dT%H:%M:%S%fZ') if not _issues.get("created_at") is None else ""
                close_date = datetime.strptime(_issues.get("closed_at"), '%Y-%m-%dT%H:%M:%S%fZ') if not _issues.get("closed_at") is None else ""
                
                _labels = _issues.get("labels")
                labels_concat = ''
                for _label in _labels:
                    _issues_label_name = _label.get("name")
                    labels_concat += _issues_label_name + ','

                
                if create_date != "":
                    create_date = create_date.astimezone(local_timezone)
                if close_date != "":
                    close_date = close_date.astimezone(local_timezone)
                
                # print('create date local tz: ',create_date)
                # print('close date local tz: ',close_date)
                
                # print('control_date: ', control_date)
                
                if close_date != "" and close_date < control_date:
                    category = 'before'
                elif create_date != "" and create_date >= control_date:
                    category = 'after'
                else:
                    category = 'discarded'

                bug_issue, evidence = is_bug_issue(_body, labels_concat, _title)
                collect_date = datetime(2018, 5, 31)
                collect_date = collect_date.astimezone(local_timezone)
                if create_date != "" and create_date <= collect_date:
                    if bug_issue:
                        issues.append([project, _number, create_date, close_date, evidence, category])
            print('Sleeping for 1 second.')
            time.sleep(1)
    else:
        print("Please setup the github token as an environment variable")
        print("export GITHUB_TOKEN='<token>'")
        sys.exit()

    return issues

def get_remaining_calls():
    token = os.getenv('GITHUB_TOKEN')

    headers = {
        'Authorization': f'bearer {token}'
    }

    request = {
        'query': open('limit.graphql', 'r').read()
    }

    response = requests.post(url="https://api.github.com/graphql", json=request,
     headers=headers)
    result = response.json()
    try:
        remaining = result['data']['rateLimit']['remaining']
        resetAt = result['data']['rateLimit']['resetAt']
        return remaining, resetAt
    except:
        return (None, None)


def get_control_date(project, timezone):
    projects = pd.read_csv('../../data/projects_control_points.csv')
    projects = projects[projects['project'] == project]
    control_date = projects.iloc[0]['middle_commit_date']
    control_date = datetime.strptime(control_date, '%Y-%m-%d %H:%M:%S %z')
    control_date = control_date.astimezone(timezone)
    return control_date

def is_bug_issue(issue_body, issue_labels, issue_title):
    label_keywords = ["Bug", "kind/bug", "Priority: Critical", "Priority: Medium", "Type – Bug", "install-bug", "404", "403", "type: bug",
"bug (open source)", "error", "contrib: good first bug", "contrib: maybe good first bug", "hotfix", "incorrect", "mistake"]
    title_description_keywords = ["fix", "error", "problem", "invalid", "defect", "500", "404", "403", "exception", "bug", "resolve", "does not", "exception thrown", "not able", "hotfix", "incorrect", "mistake", "broken", "not work", "not respond", "unable to", "failing", "failure", "502", "cannot", "troubleshooting", "wrong"]
    for label_keyword in label_keywords:
        for issue_label in str(issue_labels).split(','):
            if label_keyword in str(issue_label):
                return True, 'label:' + label_keyword
    for title_description_keyword in title_description_keywords:
        if title_description_keyword in str(issue_body) or title_description_keyword in str(issue_title):
            return True, 'title/desc: ' + title_description_keyword
    return False, ''

# credit to https://stackoverflow.com/a/47876446
def try_strptime(s, fmts=["%Y-%m-%dT%H:%M:%S.%f","%Y-%m-%d %H:%M:%S %z"]):
    for fmt in fmts:
        try:
            return datetime.strptime(s, fmt)
        except:
            continue
    return None

projects = pd.read_csv('../../data/control_projects_test.csv')
issues = []
for index, row in projects.iterrows():
    print(f"Project {index+1} of {len(projects)} - {row['project']}")
    project_owner = row['owner']
    project_name = row['name']
    print(get_remaining_calls())
    issues.extend(get_issues(project_owner, project_name))
    print(get_remaining_calls())

columns = ["project", "number", "create_date", "close_date" ,"bug_issue_evidence", "category"]

df = pd.DataFrame(issues, columns = columns)
df.to_csv('../../data/control_issues.csv', index=False)