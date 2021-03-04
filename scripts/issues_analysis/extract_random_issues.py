import mysql.connector
from mysql.connector import errorcode
import pandas as pd


def get_connection():
   try:
      connection = mysql.connector.connect(user='root',
                                 database='uff_bdd_dissertacao')
      
      return connection
   except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
         print("Something is wrong with your user name or password")
      elif err.errno == errorcode.ER_BAD_DB_ERROR:
         print("Database does not exist")
      else:
         print(err)

def get_random_repos(n):
   query = f""" SELECT 
                  t.full_name as repo_name, t.id as repo_id, count(i.id) as total_issues
               FROM uff_bdd_dissertacao.git_issues i inner join git_table t on i.id_repo = t.id 
               GROUP BY id_repo 
               HAVING total_issues >= {n} 
               ORDER BY RAND(19012021) 
               LIMIT {n};"""
   
   cursor.execute(query)
   return cursor.fetchall()
   # for (repo_name, repo_id, total_issues) in cursor:
   #    print(f"{repo_name} \t {repo_id} \t {total_issues}")

def get_repos_ids_list(repos):
   id_list = ""
   for repo in repos:
      if id_list == "":
         id_list = repo['repo_id']
      else:
         id_list+=", " + repo['repo_id']
   return id_list

def get_random_issues(n, repos):
   issues = []
   for repo in repos:
      query = f"""
         SELECT          
            i.id as id_issue, i.git_issue_number as issue_number, i.id_repo as id_repo, t.full_name as full_name, 
            i.git_issue_title as issue_title, i.git_issue_body as issue_body
         FROM
            git_issues i inner join git_table t on i.id_repo = t.id
         WHERE t.id = {repo['repo_id']}
         ORDER BY RAND(19012021)
         LIMIT {n};
      """
      cursor.execute(query)
      repo_issues = cursor.fetchall()
      for repo_issue in repo_issues:
         repo_issue = add_label_column(repo_issue)
      issues.extend(repo_issues)
   return issues
  
  

def add_label_column(issue):
   issue_id = issue['id_issue']
   labels = ""
   query = f"SELECT git_issues_label_name as label from git_issues_label where id_issue = {issue_id}"
   cursor.execute(query)
   for item in cursor.fetchall():
      if labels == "":
         labels = "'" + item['label'] + "'"
      else:
         labels+= "; '" + item['label'] + "'"
   issue["labels"] = labels
   issue["URL"] = f"=HYPERLINK(\"https://github.com/{issue['full_name']}/issues/{issue['issue_number']}\")"
   return issue


connection = get_connection()
cursor = connection.cursor(dictionary=True)
repos = get_random_repos(10)
# repos_ids = get_repos_ids_list(repos)
# print(repos_ids)
issues = get_random_issues(11, repos)
# add_label_column(issues)
# print(len(issues))
try:
   df = pd.DataFrame(issues)
   # print(df)
   writer = pd.ExcelWriter(r'random_issues3.xlsx', engine='xlsxwriter',options={'strings_to_urls': False})
   df.to_excel(writer, index=False, encoding="UTF-8")
   writer.save()
except Exception as e:
   print(e)



