# coding=utf-8 
import subprocess
import mysql.connector
import os
import re
import sys

class CONST(object):
    BD_USER = "bdd_dissertacao"
    BD_PASSWORD = "Smil123!"
    BD_HOST = "50.62.209.195"
    BD_DATABASE = "uff_bdd_dissertacao"
    REPO_DIR="//home//eduardosmil//featuretoggles//git_repositories//"

    def __setattr__(self, *_):
        pass

CONST = CONST()

def save_commit_date(id_repo, commit, date, cnx_commit):
    if not cnx_commit.is_connected():
        cnx_commit = mysql.connector.connect(user=CONST.BD_USER, password=CONST.BD_PASSWORD,
                                  host=CONST.BD_HOST,
                                database=CONST.BD_DATABASE,connection_timeout=300,buffered=True)
                            
    cursor_v = cnx_commit.cursor()

    update ="update git_stats_local set stats_value_aux2='" + str(date) + "' where id_repo='" + str(id_repo) + "'and stats_value='" + str(commit) + "' and id_stats=1;"
    cursor_v.execute(update)
        

cnx = mysql.connector.connect(user=CONST.BD_USER, password=CONST.BD_PASSWORD,
                              host=CONST.BD_HOST,
                              database=CONST.BD_DATABASE,connection_timeout=300,buffered=True)
cursor = cnx.cursor()

select_search= "SELECT t.id, t.name, t.language, s.git_word, s.git_file_extension FROM git_table t, git_search s " 
select_search= select_search + "where s.id_gitsearch=t.id_gitsearch and t.dt_clone is not null and updated_at is null;"
cursor.execute(select_search)
rs_git_search = cursor.fetchall()
cnx.close()

repo_dir="//home//eduardosmil//featuretoggles//git_repositories//"
#repo_dir="C:\\git_repositories\\"
for row in cursor._rows:
    sql_update = ""
    os.chdir(repo_dir + str(row[1].decode("utf-8")) + "_" + str(row[0].decode("utf-8")))
    print(repo_dir + str(row[1].decode("utf-8")) + "_" + str(row[0].decode("utf-8")))
    try:
        subprocess.Popen(["git checkout -f master"],shell = True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)

        lista_commit = subprocess.Popen(["git","log","--pretty=%H;%cI","--all"],stdout=subprocess.PIPE)
        stdout, _ = lista_commit.communicate()
        stdout = stdout.decode("utf-8")

        _split_commit = stdout.split("\n")
        
        for _commit in _split_commit:
            if not _commit is None and len(_commit) > 0:
                print(str(_commit))            
                _split_item_commit = _commit.strip().split(";")
                sql_update = sql_update + "update git_stats_local set stats_value_aux2='" + str(_split_item_commit[1]) + "' where id_repo='" + str(row[0].decode("utf-8")) + "'and stats_value='" + str(_split_item_commit[0]) + "' and id_stats=1;"

        cnx_commit = mysql.connector.connect(user=CONST.BD_USER, password=CONST.BD_PASSWORD,
                                  host=CONST.BD_HOST,
                                database=CONST.BD_DATABASE,connection_timeout=500,buffered=True)
        cursor_v = cnx_commit.cursor()
        
        if sql_update != "":
            cursor_v.execute(sql_update,multi=True)

        sql_update ="update git_table set updated_at=now() where id=" + str(row[0].decode("utf-8")) +";"
        cursor_v = cnx_commit.cursor()
        cursor_v.execute(sql_update)
        cnx_commit.close()

    except subprocess.CalledProcessError as e:
        print(e.output)


