# coding=utf-8 

import codecs
from github import Github
import  requests
import mysql.connector
from json2html import json2html
from datetime import datetime
from requests.auth import HTTPBasicAuth

class CONST(object):
    BD_USER = "bdd_dissertacao"
    BD_PASSWORD = "Smil123!"
    BD_HOST = "50.62.209.195"
    BD_DATABASE = "uff_bdd_dissertacao"

    def __setattr__(self, *_):
        pass

CONST = CONST()



cnx = mysql.connector.connect(user=CONST.BD_USER, password=CONST.BD_PASSWORD,
                              host=CONST.BD_HOST,
                              database=CONST.BD_DATABASE,connection_timeout=300,buffered=True)
cursor = cnx.cursor()

select_search= "SELECT git_language, git_word, id_gitsearch FROM git_search where git_status='P';"
cursor.execute(select_search)
rs_git_search = cursor.fetchall()

for row in cursor._rows:
    
    print("início linguagem:" + str(row[2].decode("utf-8")))
    
    select_repository = "SELECT id, git_page FROM git_control where git_entity='repository' and id_gitsearch=" + str(row[2].decode("utf-8"))
    cursor.execute(select_repository)
    rs_git_control = cursor.fetchall()    
    if cursor.rowcount == 0:
        add_control = ("INSERT INTO git_control "
                        "(git_entity, git_page, git_date,git_language, id_gitsearch) "
                        "VALUES ('repository', 1, now(), '"+str(row[0].decode("utf-8"))+"',"+str(row[2].decode("utf-8"))+");")
        cursor.execute(add_control)
        page = -1
    else:     
        for row_control in cursor._rows:
            page =  int(row_control[1].decode("utf-8"))

    cnx.close()

    g = Github("edusmil", "Smil123!")
    g.per_page=100
    page=-1
    for i in range(page, 9):
        page = page + 1
        print("pagina="+str(page))
        
        cnx = mysql.connector.connect(user=CONST.BD_USER, password=CONST.BD_PASSWORD,
                              host=CONST.BD_HOST,
                              database=CONST.BD_DATABASE)
        cursor = cnx.cursor(buffered=True)
        
        print("pesquisando:" + row[1].decode("utf-8"))
        rpo1 = g.search_code(chr(34) + row[1].decode("utf-8")+chr(34)+" language:"+row[0].decode("utf-8"),'indexed','desc').get_page(page)
        
        for r in rpo1:
            
	    print("-------------------------------------------------")
            print("gravando:" + r.repository.full_name + " " + r.name)
            select_repository = ("SELECT 1 FROM git_table where id='" + str(r.repository.id) +"';")
            cursor.execute(select_repository)
            if cursor.rowcount == 0:
                description = r.repository.description
                if r.repository.description is None:
 		   description = "NULL"
                else:
                   description = r.repository.description.encode("utf-8","ignore").decode("utf-8")
		
                add_repository = ("INSERT INTO git_table "
                    "(id, name, full_name,owner, private, html_url, description,fork, url, forks_url, keys_url,collaborators_url, teams_url, hooks_url, "
                    " language,stargazers_count,watchers_count,size,id_gitsearch) "
                    "VALUES ('" + str(r.repository.id) + "','"+str(r.repository.name.decode("utf-8"))+"','" + str(r.repository.full_name.decode("utf-8")) +"','"
                                + str(r.repository.owner) + "','" + str(r.repository.private) + "','" + str(r.repository.html_url) + "','" 
                                + description.replace(chr(39),"") +"','" + str(r.repository.fork) +"','"
                                + str(r.repository.url) + "','" + str(r.repository.forks_url) + "','" + str(r.repository.keys_url) + "','"
                                + str(r.repository.collaborators_url) + "','" + str(r.repository.teams_url) + "','" + str(r.repository.hooks_url) + "','"
                                + str(r.repository.language) + "','" + str(r.repository.stargazers_count) + "','" + str(r.repository.watchers_count) + "','" 
                                + str(r.repository.size) + "'," + str(row[2].decode("utf-8")) + ");")
                cursor.execute(add_repository)
            else:
                update_repository = "update git_table set id_gitsearch=" + str(row[2].decode("utf-8")) + " where id='" + str(r.repository.id) + "';"
                cursor.execute(update_repository)
                
            print("gravado:" + r.repository.full_name + " " + r.name)
	    print("--------------------------------")	
        add_control = ("UPDATE git_control SET  git_page=" + str(page) +", git_date=now() where git_entity='repository' and id_gitsearch="+str(row[2].decode("utf-8"))+";")
        cursor.execute(add_control)

        cnx.commit()    
        print("fim pagina:" + str(page))       

        cnx.close()

    
  
cnx.close()
print("fim linguagem:" + str(row[2].decode("utf-8")))

print("fim")

   
'''
, full_name, owner, private, html_url, description, fork, url, forks_url, keys_url, " +
               "  collaborators_url, teams_url, hooks_url, issue_events_url, events_url, assignees_url, branches_url," +
               "  tags_url, blobs_url
, git_tags_url, git_refs_url, trees_url, statuses_url, languages_url, stargazers_url," + 
               "  contributors_url, subscribers_url, subscription_url, commits_url, git_commits_url, comments_url, " +
               "  issue_comment_url, contents_url, compare_url, merges_url, archive_url, downloads_url, issues_url, " +
               " pulls_url, milestones_url, notifications_url, labels_url, releases_url, deployments_url, created_at, " +
               "  updated_at, pushed_at, git_url, ssh_url, clone_url, svn_url, homepage, size, stargazers_count, watchers_count, " +
               "  language, has_issues, has_projects, has_downloads, has_wiki, has_pages, forks_count, mirror_url, " +
               "  open_issues_count, forks, open_issues, watchers, default_branch, score
'''
