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


def getAuthorCommit(hash_parent):
    #separador espaço
    try:
        git_author = subprocess.check_output(["git --no-pager show -s --format='%ae' " + hash_parent[0:6]],stderr=subprocess.STDOUT,shell=True)
        git_author = git_author.decode("utf-8")
        return git_author
    except:
        return ""


cnx = mysql.connector.connect(user=CONST.BD_USER, password=CONST.BD_PASSWORD,
                              host=CONST.BD_HOST,
                              database=CONST.BD_DATABASE,connection_timeout=300,buffered=True)
cursor = cnx.cursor()

select_search= "SELECT t.id, t.name, t.language, s.git_word, s.git_file_extension FROM git_table t, git_search s " 
select_search= select_search + "where s.id_gitsearch=t.id_gitsearch and t.dt_clone is not null and "
select_search= select_search + " not exists (select 1 from git_stats_local gl where id_repo=t.id and id_stats=14)  and ((cd_classe is null) or (cd_classe = 'ok'));"
cursor.execute(select_search)
rs_git_search = cursor.fetchall()
cnx.close()

repo_dir="//home//eduardosmil//featuretoggles//git_repositories//"
for row in cursor._rows:
    os.chdir(repo_dir + str(row[1].decode("utf-8")) + "_" + str(row[0].decode("utf-8")))
    print(repo_dir + str(row[1].decode("utf-8")) + "_" + str(row[0].decode("utf-8")))
    try:
        subprocess.check_output(["git checkout -f master"],stderr=subprocess.STDOUT,shell=True)

        lista_commit = subprocess.check_output(["git rev-list --all"],stderr=subprocess.STDOUT,shell=True)
        lista_commit = lista_commit.decode("utf-8")

        _split_commit = lista_commit.split("\n")
        sql_insert = ""
        ultimo_commit = ""
        for _commit in _split_commit:
            if _commit != "":
                if sql_insert == "":
                    ultimo_commit = str(_commit) 
               
                print(str(_commit))
                subprocess.check_output(["git checkout -f "+_commit],stderr=subprocess.STDOUT,shell=True)
                git_author=getAuthorCommit(_commit)
                try:
                    git_author=str(git_author[:100])
                except:
                    git_author=""

                sql_insert = sql_insert + "(" + str(row[0].decode("utf-8")) +  ",14,now(),'" + str(_commit) + "','" + git_author + "'),"
	 
        cnx = mysql.connector.connect(user=CONST.BD_USER, password=CONST.BD_PASSWORD,
                              host=CONST.BD_HOST,
                              database=CONST.BD_DATABASE,connection_timeout=900,buffered=True)
        cursor = cnx.cursor()
        if sql_insert != "":
            sql_insert = sql_insert[:len(sql_insert)-1]

            insert_search= "insert into git_stats_local (id_repo, id_stats, timestamp, stats_value, stats_value_aux) values " + sql_insert + ";"
            cursor.execute(insert_search)
            cnx.close()   

 
    except subprocess.CalledProcessError as e:
        print(e.output)
