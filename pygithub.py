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
                              database=BD_DATABASE,connection_timeout=300,buffered=True)
cursor = cnx.cursor()

select_search= "SELECT git_language, git_word, id_gitsearch FROM git_search where git_status='P';"
cursor.execute(select_search)
rs_git_search = cursor.fetchall()

for row in cursor._rows:
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
        
        cnx = mysql.connector.connect(user='bdd_dissertacao', password='Smil123!',
                                host='50.62.209.195',
                                database='uff_bdd_dissertacao')
        cursor = cnx.cursor(buffered=True)
        
        rpo1 = g.search_code(chr(34) + row[1].decode("utf-8")+chr(34)+" language:"+row[0].decode("utf-8"),'indexed','desc').get_page(page)
        for r in rpo1:
            print(r.repository.full_name + " " + r.name)
            
            select_repository = ("SELECT 1 FROM git_table where id='" + str(r.repository.id) +"';")
            cursor.execute(select_repository)
            if cursor.rowcount == 0:
                add_repository = ("INSERT INTO git_table "
                    "(id, name, full_name,owner, private, html_url, description,fork, url, forks_url, keys_url,collaborators_url, teams_url, hooks_url, "
                    " language,stargazers_count,watchers_count,size,id_gitsearch) "
                    "VALUES ('" + str(r.repository.id) + "','"+str(r.repository.name)+"','" + str(r.repository.full_name) +"','"
                                + str(r.repository.owner) + "','" + str(r.repository.private) + "','" + str(r.repository.html_url) + "','" 
                                + str(r.repository.description).replace(chr(39),"") +"','" + str(r.repository.fork) +"','"
                                + str(r.repository.url) + "','" + str(r.repository.forks_url) + "','" + str(r.repository.keys_url) + "','"
                                + str(r.repository.collaborators_url) + "','" + str(r.repository.teams_url) + "','" + str(r.repository.hooks_url) + "','"
                                + str(r.repository.language) + "','" + str(r.repository.stargazers_count) + "','" + str(r.repository.watchers_count) + "','" 
                                + str(r.repository.size) + "'," + str(row[2].decode("utf-8")) + ");")
                cursor.execute(add_repository)
            else:
                update_repository = "update git_table set id_gitsearch=" + str(row[2].decode("utf-8")) + " where id='" + str(r.repository.id) + "';"
                cursor.execute(update_repository)

        add_control = ("UPDATE git_control SET  git_page=" + str(page) +", git_date=now() where git_entity='repository' and id_gitsearch="+str(row[2].decode("utf-8"))+";")
        cursor.execute(add_control)

        cnx.commit()    

        cnx.close()

    '''
    headers = {'Accept': 'application/vnd.github.cloak-preview'}
    url = "https://api.github.com/search/commits?q=repo:"+rep1+"+merge:true" 
    data = requests.get(url,headers=headers).json()
    print(json2html.convert(json=data,table_attributes='border="1"'))
    '''
    cnx = mysql.connector.connect(user='bdd_dissertacao', password='Smil123!',
                                host='50.62.209.195',
                                database='uff_bdd_dissertacao',connection_timeout=300)
    cursor = cnx.cursor(buffered=True)
    select_repository = ("SELECT id, full_name FROM git_table t where not exists (select 1 from git_stats s where s.id_repo=t.id and git_last_commit is not null) order by id;")
    cursor.execute(select_repository)
    rs_git_control = cursor.fetchall()
    i=0
    for _id, _full_name in rs_git_control:
        rpo_det = g.get_repo(_full_name)

        commit =rpo_det.get_commits()
        '''cont = rpo_det.get_contributors()
        branches = rpo_det.get_branches()
            
        n_contributors = 0
        n_commits = 0
        n_branches = 0
        
        if cont is not None:
            n_contributors = len(list(cont))'''

        if commit is not None:
            n_commits = len(list(commit))
            sha = commit[0].sha
            _senha = "Basic ZWR1c21pbDpTbWkxMjMh"
            headers = {'Accept': 'application/vnd.github.cloak-preview'}
            url = "https://api.github.com/repos/"+_full_name+"/commits/"+sha
            data = requests.get(url,headers=headers).json()
            try:
                dt_last_commit = datetime.strptime(data["commit"]["committer"]["date"] ,'%Y-%m-%dT%H:%M:%SZ')
            except KeyError:
                dt_last_commit = None
        '''    
        if branches is not None:
            n_branches = len(list(branches))'''

        ''' 
        headers = {'Accept': 'application/vnd.github.cloak-preview'}
        url = "https://api.github.com/search/commits?q=repo:"+_full_name+"+merge:true&rel=last"
        data = requests.get(url,headers=headers).json()
        n_merges = data.get("total_count","{date}")'''

        
        cnx = mysql.connector.connect(user='bdd', password='bdduff!!',
                                host='50.62.209.195',
                                database='edusmil_bdd',connection_timeout=300)
        cursor = cnx.cursor(buffered=True) 

        select_repository = ("SELECT 1 FROM git_stats where id_repo=" + str(_id) +";")
        cursor.execute(select_repository)
        if cursor.rowcount == 0:
            add_statistics = ("INSERT INTO git_stats (id_repo, git_commits, git_branches, git_merges, git_contributors, git_last_commit) "
                                " values (" + str(_id) + "," + str(n_commits) +"," + str(n_branches) + ","+str(n_merges)+"," + str(n_contributors)+",")
            if dt_last_commit is not None:
                add_statistics = add_statistics + ("(STR_TO_DATE('"+dt_last_commit.strftime("%d-%m-%Y")+"', '%d-%m-%Y'))); ")
            else:
                add_statistics = add_statistics + ("null); ")
            cursor.execute(add_statistics) 
        else:
            if dt_last_commit is not None:
                add_statistics = ("update git_stats set git_last_commit=(STR_TO_DATE('"+dt_last_commit.strftime("%d-%m-%Y")+"', '%d-%m-%Y')) where id_repo=" + str(_id) + ";")
                cursor.execute(add_statistics) 
        cnx.commit()    

        cnx.close()  
        '''
        else:
            update_statistics = ("UPDATE git_stats " +
                                " set  git_commits=" + str(n_commits) +"," +
                                "      git_branches=" + str(n_branches) +"," + 
                                "      git_merges="+str(n_merges)+"," + 
                                "      git_contributors=" + str(n_contributors) +  
                                " where id_repo=" + str(_id) + ";")
        cursor.execute(update_statistics) 
        '''
  
cnx.close()
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
