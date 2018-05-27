# coding=utf-8
import mysql.connector
import sys
sys.path.insert(0, '/inetpub/wwwroot/merge-effort/merge-effort/mergeeffort')
import merge_analysis
from pygit2 import *

class CONST(object):
    BD_USER = "bdd_dissertacao"
    BD_PASSWORD = "Smil123!"
    BD_HOST = "50.62.209.195"
    BD_DATABASE = "uff_bdd_dissertacao"
    REPO_DIR="//home//eduardosmil//featuretoggles//git_repositories//"

    def __setattr__(self, *_):
        pass

CONST = CONST()

cnx = mysql.connector.connect(user=CONST.BD_USER, password=CONST.BD_PASSWORD,
                              host=CONST.BD_HOST,
                              database=CONST.BD_DATABASE,connection_timeout=300,buffered=True)
cursor = cnx.cursor()

select_search= ("select distinct t.id, t.name, t.language "
                "from git_table t, git_stats_local gl "
                "where "
                "   t.id=gl.id_repo and "
                "   gl.id_stats=5 and "
                "   not exists (select 1 from git_stats_local s where s.id_stats=11 and s.id_repo=gl.id_repo) limit 0,1; ")
cursor.execute(select_search)
rs_git_search = cursor.fetchall()
cnx.close()

for row in cursor._rows:    
    repo_path = CONST.REPO_DIR + str(row[1].decode("utf-8")) + "_" + str(row[0].decode("utf-8"))
    print("Repositório:" + repo_path)
    repo = Repository(repo_path)

    cnx = mysql.connector.connect(user=CONST.BD_USER, password=CONST.BD_PASSWORD,
                              host=CONST.BD_HOST,
                              database=CONST.BD_DATABASE,connection_timeout=300,buffered=True)
    cursor_repo = cnx.cursor()

    select_search= ("select gl.stats_value "
                "from git_stats_local gl "
                "where gl.id_repo='" + str(row[0].decode("utf-8")) + "' and "
                "   gl.id_stats=5 and "
                "   not exists (select 1 from git_stats_local s where s.id_stats=11 and s.id_repo=gl.id_repo) ")
    cursor_repo.execute(select_search)
    rs_git_search = cursor_repo.fetchall()
    cnx.close()

    sql_insert = ""

    for row_repo in cursor_repo._rows:
        commits = []
        _commit = str(row_repo[0].decode("utf-8"))
        commits.append(repo.get(_commit))
        _merge_analisys= merge_analysis.analyse(commits,repo)

        if not _merge_analisys is None:
            sql_insert = sql_insert + "(" + str(row[0].decode("utf-8")) +  ",8,now(),'" + str(_commit) + "','" + str(_merge_analisys[commits[0].hex]["branch1"]) + "'),"
            sql_insert = sql_insert + "(" + str(row[0].decode("utf-8")) +  ",9,now(),'" + str(_commit) + "','" + str(_merge_analisys[commits[0].hex]["branch2"]) + "'),"
            sql_insert = sql_insert + "(" + str(row[0].decode("utf-8")) +  ",10,now(),'" + str(_commit) + "','" + str(_merge_analisys[commits[0].hex]["Parents rework"]) + "'),"
            sql_insert = sql_insert + "(" + str(row[0].decode("utf-8")) +  ",11,now(),'" + str(_commit) + "','" + str(_merge_analisys[commits[0].hex]["merge"]) + "'),"
            sql_insert = sql_insert + "(" + str(row[0].decode("utf-8")) +  ",12,now(),'" + str(_commit) + "','" + str(_merge_analisys[commits[0].hex]["Wasted actions"]) + "'),"
            sql_insert = sql_insert + "(" + str(row[0].decode("utf-8")) +  ",13,now(),'" + str(_commit) + "','" + str(_merge_analisys[commits[0].hex]["Additional actions"]) + "'),"

    if not sql_insert is None:
        sql_insert = sql_insert[:len(sql_insert)-1]

        cnx = mysql.connector.connect(user=CONST.BD_USER, password=CONST.BD_PASSWORD,
                              host=CONST.BD_HOST,
                              database=CONST.BD_DATABASE,connection_timeout=300,buffered=True)
        cursor_insert_repo = cnx.cursor()

        insert_search= "insert into git_stats_local (id_repo, id_stats, timestamp, stats_value, stats_value_aux) values " + sql_insert + ";"
        cursor_insert_repo.execute(insert_search)
        cnx.close()

print("fim")        



