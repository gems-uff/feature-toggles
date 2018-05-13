# coding=utf-8 
import subprocess
import mysql.connector
import os
import re

class CONST(object):
    BD_USER = "bdd_dissertacao"
    BD_PASSWORD = "Smil123!"
    BD_HOST = "50.62.209.195"
    BD_DATABASE = "uff_bdd_dissertacao"
    REPO_DIR="//home//eduardosmil//featuretoggles//git_repositories//"

    def __setattr__(self, *_):
        pass

CONST = CONST()

def grep(grep_string, files):
    try:
        print(grep_string)
        if files != "":
            git_grep = subprocess.Popen(["git grep -E -i -q " + chr(34) + grep_string + chr(34) + " -- '" + files+"'"],
                               shell = True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            git_grep = subprocess.Popen(["git grep -E -i -q " + chr(34) + grep_string + chr(34)],
                               shell = True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = git_grep.communicate()
        return git_grep.returncode

    except:
        return ""

def getParentCommitMerge(hash_parent):
    #separador espaço
    try:
        git_parents = subprocess.Popen(["git log --pretty=%P -n 1",hash_parent],
                                shell = True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        return git_parents
    except:
        return ""

def getCommitsBetween(hash_parent1, hash_parent2):
    #separador \n
    try:
        git_hashs = subprocess.Popen(["git log --format=%H --no-merges ",hash_parent1 + ".. " + hash_parent2],                    
                                shell = True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        return git_hashs
    except:
        return ""

def getMergeBase(hash_parent1, hash_parent2):
    #separador \n
    try:
        git_hashBase = subprocess.Popen(["git merge-base " + hash_parent1 + " " + hash_parent2],
                                shell = True,stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = git_grep.communicate()
        return git_hashBase
    except:
        return ""

def getAuthorsBetween(hash_parent1, hash_parent2):
    #separador \n
    try:
        git_Authors = subprocess.Popen(["git shortlog -sne --no-merges ",hash_parent1 + ".. " + hash_parent2],
                                shell = True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = git_grep.communicate()
        return git_Authors
    except:
        return ""


cnx = mysql.connector.connect(user=CONST.BD_USER, password=CONST.BD_PASSWORD,
                              host=CONST.BD_HOST,
                              database=CONST.BD_DATABASE,connection_timeout=300,buffered=True)
cursor = cnx.cursor()

select_search= "SELECT t.id, t.name, t.language, s.git_word, s.git_file_extension FROM git_table t, git_search s " 
select_search= select_search + "where s.id_gitsearch=t.id_gitsearch and t.dt_clone is not null and "
select_search= select_search + " not exists (select 1 from git_stats_local gl where id_repo=t.id)  and ((cd_classe is null) or (cd_classe = 'ok')) limit 0,1;"
cursor.execute(select_search)
rs_git_search = cursor.fetchall()
cnx.close()

repo_dir="//home//eduardosmil//featuretoggles//git_repositories//"
for row in cursor._rows:
    os.chdir(repo_dir + str(row[1].decode("utf-8")) + "_" + str(row[0].decode("utf-8")))
    print(repo_dir + str(row[1].decode("utf-8")) + "_" + str(row[0].decode("utf-8")))
    try:
        subprocess.check_output(["git checkout -f master"],stderr=subprocess.STDOUT,shell=True)

        #
        #lista_commit = subprocess.check_output(["git rev-list --all"],stderr=subprocess.STDOUT,shell=True)
        #lista_commit = lista_commit.decode("utf-8")

        #_split_commit = lista_commit.split("\n")
        #sql_insert = ""
        #ultimo_commit = ""
        for _commit in _split_commit:
            if _commit != "":
                if sql_insert == "":
                    ultimo_commit = str(_commit) 
               
        #       print(str(_commit))
        #        subprocess.check_output(["git checkout -f "+_commit],stderr=subprocess.STDOUT,shell=True)
        #        git_grep =grep(str(row[3].decode("utf-8")),str(row[4].decode("utf-8")))
        #
        #        flag_fw = ""
        #   
        #        if git_grep == 0: # found
        #          #print("achou")                
        #          flag_fw = "'fw'"
        #                    
        #        elif git_grep == 1: # not found
        #          #print("nao achou")                
        #          flag_fw = "NULL"

        #        elif git_grep > 1: # error
        #          print("erro:" + str(row[0].decode("utf-8")))        
        #          break
            
        #        sql_insert = sql_insert + "(" + str(row[0].decode("utf-8")) +  ",1,now(),'" + str(_commit) + "'," + str(flag_fw) + "),"
	 
        #cnx = mysql.connector.connect(user=CONST.BD_USER, password=CONST.BD_PASSWORD,
        #                      host=CONST.BD_HOST,
        #                      database=CONST.BD_DATABASE,connection_timeout=300,buffered=True)
        #cursor = cnx.cursor()
        #if sql_insert != "":
        #    sql_insert = sql_insert[:len(sql_insert)-1]

        #    insert_search= "insert into git_stats_local (id_repo, id_stats, timestamp, stats_value, stats_value_aux) values " + sql_insert + ";"
        #    cursor.execute(insert_search)
        #    cnx.close()   
	
        lista_commit = subprocess.check_output([" git rev-list --min-parents=2 " +  ultimo_commit],stderr=subprocess.STDOUT,shell=True)
        lista_commit = lista_commit.decode("utf-8")

        _split_commit = lista_commit.split("\n")
        sql_insert = ""
        sql_insert_merge_branch = ""
        
        for _commit in _split_commit:
            if _commit != "":
                sql_insert = sql_insert + "(" + str(row[0].decode("utf-8")) +  ",5,now(),'" + str(_commit) + "',NULL),"

                print("Verificando Merge Parents...")
                lista_commit_parents = getParentCommitMerge(_commit)
                if lista_commit_parents != "":
                    _split_commit_parents = lista_commit_parents.split(" ")
                    git_parent = getMergeBase(_split_commit_parents(0),_split_commit_parents(1))

                    _mais_dev_1 = False
                    _mais_dev_2 = False

                    if git_parent != "":
                        _lista_commit_b1 = getCommitsBetween(git_parent,_split_commit_parents(0))
                        _lista_commit_b2 = getCommitsBetween(git_parent,_split_commit_parents(2))

                        print("Merge: " + _commit + " Pai 1:" + _split_commit_parents(0))

                        _split_commit_b1 = _lista_commit_b1.split("\n")
                        _lista_commit_p1 = getAuthorsBetween(git_parent,_split_commit_b1(0))
                        
                        _split_commit_p1 = _lista_commit_p1.split("\n")
                        if len(_split_commit_p1) >= 2: # mais de 2 desenvolvedores
                            _mais_dev_1 = True
                        
                        _lista_commit_p2 = getAuthorsBetween(git_parent,_lista_commit_b2(0))
                        
                        _split_commit_p2 = _lista_commit_p2.split("\n")
                        if len(_lista_commit_p2) >= 2: # mais de 2 desenvolvedores
                            _mais_dev_2 = True

                        if ((_mais_dev_1 == True) and (_mais_dev_2 == True)):
                            print("Merge Branch: " + str(_commit))
                            sql_insert_merge_branch = sql_insert_merge_branch + + "(" + str(row[0].decode("utf-8")) +  ",6,now(),'" + str(_commit) + "',NULL),"
            
        cnx = mysql.connector.connect(user=CONST.BD_USER, password=CONST.BD_PASSWORD,
                            host=CONST.BD_HOST,
                            database=CONST.BD_DATABASE,connection_timeout=300,buffered=True)
        cursor = cnx.cursor()
        if sql_insert != "":
            sql_insert = sql_insert[:len(sql_insert)-1]
       	    insert_search= "insert into git_stats_local (id_repo, id_stats, timestamp, stats_value, stats_value_aux) values " + sql_insert + ";"
            cursor.execute(insert_search)
            cnx.close()

        if sql_insert_merge_branch != "":
            sql_insert_merge_branch = sql_insert_merge_branch[:len(sql_insert_merge_branch)-1]
       	    insert_search= "insert into git_stats_local (id_repo, id_stats, timestamp, stats_value, stats_value_aux) values " + sql_insert_merge_branch + ";"
            cursor.execute(insert_search)
            cnx.close()

        lista_commit = subprocess.check_output(["git log --regexp-ignore-case --grep 'merge branch' --format=format:%H "],stderr=subprocess.STDOUT,shell=True)
        lista_commit = lista_commit.decode("utf-8")

        _split_commit = lista_commit.split("\n")
        sql_insert = ""
        
        for _commit in _split_commit:
            if _commit != "":
               sql_insert = sql_insert + "(" + str(row[0].decode("utf-8")) +  ",7,now(),'" + str(_commit) + "',NULL),"
            
        cnx = mysql.connector.connect(user=CONST.BD_USER, password=CONST.BD_PASSWORD,
                            host=CONST.BD_HOST,
                            database=CONST.BD_DATABASE,connection_timeout=300,buffered=True)
        cursor = cnx.cursor()
        if sql_insert != "":
            sql_insert = sql_insert[:len(sql_insert)-1]
       	    insert_search= "insert into git_stats_local (id_repo, id_stats, timestamp, stats_value, stats_value_aux) values " + sql_insert + ";"
            cursor.execute(insert_search)
            cnx.close()

 
    except subprocess.CalledProcessError as e:
        print(e.output)
