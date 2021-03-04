from github import Github
import  requests
import mysql.connector
from json2html import json2html
from datetime import datetime
from requests.auth import HTTPBasicAuth
import configs as cf

'''
    headers = {'Accept': 'application/vnd.github.cloak-preview'}
    url = "https://api.github.com/search/commits?q=repo:"+rep1+"+merge:true" 
    data = requests.get(url,headers=headers).json()
    print(json2html.convert(json=data,table_attributes='border="1"'))
    '''
    cnx = mysql.connector.connect(user=cf.db_user, password=cf.db_pass,
                              host=cf.db_host,
                              database=cf.db_name,connection_timeout=300)
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

        
        cnx = mysql.connector.connect(user=cf.db_user, password=cf.db_pass,
                              host=cf.db_host,
                              database=cf.db_name,connection_timeout=300)
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
