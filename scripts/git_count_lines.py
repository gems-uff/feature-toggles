# coding=utf-8 
import subprocess
import mysql.connector
import os
import re
import sys
import configs as cf

def grep(grep_string, files):
    try:
        print(grep_string)
        
        _grep_string = grep_string.replace(" ","(.*?)")
        _grep_string = chr(34) + _grep_string + chr(34)

        print(_grep_string)
        if files != "":            
            git_grep = subprocess.check_output(["git grep -i -E " + _grep_string  + " -- '" + files+"'"],stderr=subprocess.STDOUT,shell=True)
        else:
            git_grep = subprocess.check_output(["git grep -i " + chr(34) + _grep_string + chr(34)],stderr=subprocess.STDOUT,shell=True)
		
		if git_grep != "":
		    git_grep = git_grep.decode("utf-8")
        return git_grep

    except:
        return ""



cnx = mysql.connector.connect(user=cf.db_user, password=cf.db_pass,
                              host=cf.db_host,
                              database=cf.db_name,connection_timeout=300,buffered=True)
cursor = cnx.cursor()

select_search= "select distinct l.id_repo, t.name,s.git_word,s.git_file_extension "
select_search= select_search + "from git_stats_local l, git_table t, git_search s "
select_search= select_search + "where "
select_search= select_search + "s.id_gitsearch=t.id_gitsearch and "
select_search= select_search + "t.id=l.id_repo and "
select_search= select_search + "l.id_stats =1 and "
select_search= select_search + "l.id_repo in ( "
select_search= select_search + "347655,489645,552695,769182,806511,1059929,1217077,1338040,1352520,1722606,1799884,1848736,2263742, "
select_search= select_search + "2386842,2392358,2416064,2577146,2723436,2987495,2995765,4494078,4693087,5021616,5144181,5197539, "
select_search= select_search + "5203368,5287954,5421677,5541660,5614312,6127047,6388572,7031510,7358191,8484604,8884773,10199599, "
select_search= select_search + "10391073,10934610,11246402,11671912,12736575,13633443,15008139,15344614,16416867,16619668,16827151, "
select_search= select_search + "17164513,18355156,18625008,18810181,19272646,19695722,20538228,20767408,21674470,22128680,23700996, "
select_search= select_search + "23722245,23996209,24676571,24728203,24850244,24998407,25745061,26113177,26767408,27058591,27288669,28054380, "
select_search= select_search + "29340261,29364795,29641957,30175039,30702818,31377627,32340528,34396268,35300278,35489525,39788762, "
select_search= select_search + "41607639,42480983,42585709,42682761,45260412,45866355,45931203,47632133,49892996,50365703, "
select_search= select_search + "50667950,51774067,53135203,53534987,54648215,62129589,68407220,68464903,69359362,71187431,71376869, "
select_search= select_search + "71501855,72233269,72479761,73205358,73714491,74074978,74275100,75758799,76819000,78471377,79148749,79465598, "
select_search= select_search + "84507987,86124349,86282367,89386914,92938357,93316749,93964532,94167681,95210715,95443579,96212237,96530667, "
select_search= select_search + "97128753,98375316,98575487,101262862,101472507,103996987,105359284,106851769,107119628,107367707,107553659, "
select_search= select_search + "108414390,111302009,111772276,112953456,113795698,116361990,116522779,117831469,117928513,118666777,119819922, "
select_search= select_search + "122414437,122976077,124034426,124245472,124260744,124907477,126279499,126371844,127966163) and "
select_search= select_search + "l.stats_value_aux is not null and "
select_search= select_search + "not exists (select 1 from git_stats_local gl where gl.id_repo=l.id_repo) " 
select_search= select_search + " limit 0,1;"
cursor.execute(select_search)
rs_git_search = cursor.fetchall()
cnx.close()

repo_dir="//home//eduardosmil//featuretoggles//git_repositories//"
for row in cursor._rows:
    os.chdir(repo_dir + str(row[1].decode("utf-8")) + "_" + str(row[0].decode("utf-8")))
    print(repo_dir + str(row[1].decode("utf-8")) + "_" + str(row[0].decode("utf-8")))
    try:
        subprocess.check_output(["git checkout -f master"],stderr=subprocess.STDOUT,shell=True)
		
		cnx = mysql.connector.connect(user=cf.db_user, password=cf.db_pass,
                              host=cf.db_host,
                              database=cf.db_name,connection_timeout=300,buffered=True)
		cursor_commit = cnx.cursor()
		
		select_search= "select l.status_value "
		select_search= select_search + "from git_stats_local l, git_table t, git_search s "
		select_search= select_search + "where "
		select_search= select_search + "s.id_gitsearch=t.id_gitsearch and "
		select_search= select_search + "t.id=l.id_repo and "
		select_search= select_search + "l.id_stats =1 and "
		select_search= select_search + "l.id_repo = '" + str(row[1].decode("utf-8")) + ' and "
		select_search= select_search + "l.stats_value_aux is not null and "
		select_search= select_search + "not exists (select 1 from git_stats_local gl where gl.id_repo=l.id_repo and gl.status_value=l.status_value); " 		
		cursor_commit.execute(select_search)
		rs_git_search_commits = cursor_commit.fetchall()
		
		cnx.close()
		
        sql_insert = ""
        ultimo_commit = ""
        for row_commit in cursor_commit._rows:
			_commit = str(row_commit[0].decode("utf-8"))
            if _commit != "":
                
                print(str(_commit))
                subprocess.check_output(["git checkout -f "+_commit],stderr=subprocess.STDOUT,shell=True)
                git_grep =grep(str(row[2].decode("utf-8")),str(row[3].decode("utf-8")))
				
				lista_linhas = 0
		   
                if git_grep != "":                  
					lista_linhas = git_grep.split("\n")										
                
                sql_insert = sql_insert + "(" + str(row[0].decode("utf-8")) +  ",15,now(),'" + str(_commit) + "'," + str(lista_linhas) + "),"
	 
        cnx = mysql.connector.connect(user=cf.db_user, password=cf.db_pass,
                              host=cf.db_host,
                              database=cf.db_name,connection_timeout=300,buffered=True)
        cursor = cnx.cursor()
        if sql_insert != "":
            sql_insert = sql_insert[:len(sql_insert)-1]

            insert_search= "insert into git_stats_local (id_repo, id_stats, timestamp, stats_value, stats_value_aux) values " + sql_insert + ";"
            cursor.execute(insert_search)
            cnx.close()   
       
 
    except subprocess.CalledProcessError as e:
        print(e.output)