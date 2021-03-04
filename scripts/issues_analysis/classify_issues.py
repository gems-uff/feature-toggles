#Given the manually classified csv, apply the automatic classification and add it as a column
INPUT_CSV = "classified_issues_manual.csv"

import pandas as pd

label_keywords = ["Bug", "kind/bug", "Priority: Critical", "Priority: Medium", "Type – Bug", "install-bug", "404", "403", "type: bug",
"bug (open source)", "error", "contrib: good first bug", "contrib: maybe good first bug", "hotfix", "incorrect", "mistake"]

title_description_keywords = ["fix", "error", "problem", "invalid", "defect", "500", "404", "403", "exception", "bug", "resolve", "does not", "exception thrown", "not able", "hotfix", "incorrect", "mistake", "broken", "not work", "not respond", "unable to", "failing", "failure", "502", "cannot", "troubleshooting", "wrong"]



def is_bug_issue(issue_body, issue_label, issue_title):
   for label_keyword in label_keywords:
      if label_keyword in str(issue_label):
         return True, 'label:' + label_keyword
   for title_description_keyword in title_description_keywords:
      if title_description_keyword in str(issue_body) or title_description_keyword in str(issue_title):
         return True, 'title/desc: ' + title_description_keyword
   return False, ''


def classify_issues():
   data = pd.read_csv(INPUT_CSV, header=0, delimiter=';',  encoding = "ISO-8859-1")
   classifications = []
   keywords = []

   for index, row in data.iterrows():
      title = row['issue_title']
      body = row['issue_body']
      labels = row['labels']
      is_bug, keyword = is_bug_issue(body, labels, title)
      classifications.append(is_bug)
      keywords.append(keyword)

   data['auto_classification'] = classifications
   data['keyword_classif'] = keywords
   data.to_csv('classified_issues.csv', index=None, sep=';',  encoding = "utf-8")

if __name__ == "__main__":
   classify_issues()
