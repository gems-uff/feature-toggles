# coding=utf-8
import mysql.connector
import sys
sys.path.insert(0, '//home//eduardosmil//merge-effort//mergeeffort')
import merge_analysis
from pygit2 import *
import configs as cf

cnx = mysql.connector.connect(user=cf.db_user, password=cf.db_pass,
                              host=cf.db_host,
                              database=cf.db_name,connection_timeout=300,buffered=True)
cursor = cnx.cursor()

select_search= ("select distinct t.id, t.name, t.language "
                "from git_table t, git_stats_local gl "
                "where "
                "   t.id=gl.id_repo and "
                "   gl.id_stats in (5) and "
                "   not exists (select 1 from git_stats_local s where s.stats_value=gl.stats_value and s.id_stats in (8,9,10,11,12,13) and s.id_repo=gl.id_repo);")
cursor.execute(select_search)
rs_git_search = cursor.fetchall()
cnx.close()

for row in cursor._rows:    
    repo_path = cf.repo_dir + str(row[1].decode("utf-8")) + "_" + str(row[0].decode("utf-8"))
    print("Repositório:" + repo_path)
    repo = Repository(repo_path)

    cnx = mysql.connector.connect(user=cf.db_user, password=cf.db_pass,
                              host=cf.db_host,
                              database=cf.db_name,connection_timeout=300,buffered=True)
    cursor_repo = cnx.cursor()

    select_search= ("select distinct gl.stats_value "
                "from git_stats_local gl "
                "where gl.id_repo='" + str(row[0].decode("utf-8")) + "' and "
                "   gl.id_stats in (5) and "
                "   not exists (select 1 from git_stats_local s where s.stats_value=gl.stats_value and s.id_stats in (8,9,10,11,12,13) and s.id_repo=gl.id_repo) ")
    cursor_repo.execute(select_search)
    rs_git_search = cursor_repo.fetchall()
    cnx.close()

    sql_insert = ""

    for row_repo in cursor_repo._rows:
        commits = []
        _commit = str(row_repo[0].decode("utf-8"))
        print(_commit)
        commits.append(repo.get(_commit))
        _merge_analisys= merge_analysis.analyse(commits,repo)

        if len(_merge_analisys) > 0:
            print(_merge_analisys)
            sql_insert = sql_insert + "(" + str(row[0].decode("utf-8")) +  ",8,now(),'" + str(_commit) + "','" + str(_merge_analisys[commits[0].hex]["branch1"]) + "',null),"
            sql_insert = sql_insert + "(" + str(row[0].decode("utf-8")) +  ",9,now(),'" + str(_commit) + "','" + str(_merge_analisys[commits[0].hex]["branch2"]) + "',null),"
            sql_insert = sql_insert + "(" + str(row[0].decode("utf-8")) +  ",10,now(),'" + str(_commit) + "','" + str(_merge_analisys[commits[0].hex]["rework"]) + "',null),"
            sql_insert = sql_insert + "(" + str(row[0].decode("utf-8")) +  ",11,now(),'" + str(_commit) + "','" + str(_merge_analisys[commits[0].hex]["merge"]) + "',null),"
            sql_insert = sql_insert + "(" + str(row[0].decode("utf-8")) +  ",12,now(),'" + str(_commit) + "','" + str(_merge_analisys[commits[0].hex]["wasted"]) + "',null),"
            sql_insert = sql_insert + "(" + str(row[0].decode("utf-8")) +  ",13,now(),'" + str(_commit) + "','" + str(_merge_analisys[commits[0].hex]["merge_effort"]) + "',null),"

    if sql_insert != "":
        sql_insert = sql_insert[:len(sql_insert)-1]                

        cnx = mysql.connector.connect(user=cf.db_user, password=cf.db_pass,
                              host=cf.db_host,
                              database=cf.db_name,connection_timeout=300,buffered=True)
        cursor_insert_repo = cnx.cursor()

        insert_search= "insert into git_stats_local(id_repo, id_stats, timestamp, stats_value, stats_value_aux,stats_value_aux2) values " + sql_insert + ";"
        cursor_insert_repo.execute(insert_search)
        cnx.close()

print("fim")        

