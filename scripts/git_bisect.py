import subprocess
import mysql.connector
import os
import re
import configs as cf

def grep(grep_string, files):
    try:
        print(grep_string);
        print(files);
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

cnx = mysql.connector.connect(user=cf.bd_user, user=cf.db_pass,
                              host=cf.db_host,
                              database=cf.db_name,connection_timeout=300,buffered=True)
cursor = cnx.cursor()

select_search= "SELECT t.id, t.name, t.language, s.git_word, s.git_file_extension FROM git_table t, git_search s " 
select_search= select_search + "where s.id_gitsearch=t.id_gitsearch and t.dt_clone is not null and t.git_commit1 is null and  t.id=6733206"
select_search= select_search + " order by t.id ;"
cursor.execute(select_search)
rs_git_search = cursor.fetchall()
cnx.close()

repo_dir="//home//eduardosmil//featuretoggles//git_repositories//"

for row in cursor._rows:
    os.chdir(repo_dir + str(row[1].decode("utf-8")) + "_" + str(row[0].decode("utf-8")))
    print("Repositorio: " + str(row[1].decode("utf-8")) + "_" + str(row[0].decode("utf-8")))
    try:
         subprocess.check_output(["git bisect reset"],stderr=subprocess.STDOUT,shell=True)
   	 commit_head = subprocess.check_output(["git rev-parse HEAD"], stderr=subprocess.STDOUT, shell=True)
   	 commit_head =  commit_head.decode("utf-8").replace("\n","")
   	 print("commit HEAD:" + commit_head)
    except subprocess.CalledProcessError as e:
         print(e.output)
         continue

    try:
    	commit_first = subprocess.check_output(["git rev-list --max-parents=0 HEAD"],stderr=subprocess.STDOUT,shell=True)
    	commit_first = commit_first.decode("utf-8").split("\n")
    except subprocess.CalledProcessError as e:
        print(e.output)
	continue 

    indice=1
    for _c in commit_first:
        print("commit FIRST:" + _c)
        if _c == None or _c == "":
           break;
    	marca_inicial = True

    	subprocess.check_output(["git bisect start"],stderr=subprocess.STDOUT,shell=True)
	
	for_commit_first = _c
        
	commit_old_head = ""
        commit_old_first = ""
    	while for_commit_first != commit_head:
        	if for_commit_first == "" or commit_head == "":
           	   cnx = mysql.connector.connect(user=cf.bd_user, user=cf.db_pass,
                	              host=cf.db_host,
                        	      database=cf.db_name,connection_timeout=300,buffered=True)
            	   cursor = cnx.cursor() 
           	   update_search= "update git_table set git_commit"+str(indice)+"='"
            	   if for_commit_first != "":
                	commit = commit_old_head
           	   else:
                	commit =  commit_old_first

           	   update_search = update_search + commit + "' where id=" + str(row[0].decode("utf-8")) + ";"
                   cursor.execute(update_search)

            	   total_commit = subprocess.check_output(["git rev-list --all --count"], stderr=subprocess.STDOUT,shell=True)
            	   total_commit = total_commit.decode("utf-8")
            
            	   total_commit_fw = subprocess.check_output(["git rev-list " +  commit + " --count"], stderr=subprocess.STDOUT,shell=True)
            	   total_commit_fw = total_commit_fw.decode("utf-8")

		   select_stats = "select 1 from git_stats_local where id=" + str(row[0].decode("utf-8")) + " and git_commit='" + commit + "';"
		   cursor.execute(select_stats)
		   rs_git_search = cursor.fetchall()	   
		   print("aaaa=" + str(cursor.rowcount));
                   if cursor.rowcount == 0:

            	   	insert_stats = "insert into git_stats_local (id, git_commit,  git_total_commit, git_fw_commit, git_total_merges_ant_fw, git_total_merges_pos_fw) "                           
            	   	insert_stats = insert_stats +" values (" + str(row[0].decode("utf-8")) + ",'" + commit + "'," + total_commit + ","
            	   	insert_stats = insert_stats + total_commit_fw + ",null,null); "
                   	cursor.execute(insert_stats)
                   cnx.close()           	  
                   indice = indice + 1
		   break

                if marca_inicial:
                   try:
            	   	subprocess.check_output(["git bisect bad " + commit_head],stderr=subprocess.STDOUT,shell=True)
        
                   	bisect_commit_init = subprocess.check_output(["git bisect good " + for_commit_first],stderr=subprocess.STDOUT,shell=True)
                   	bisect_commit_init = bisect_commit_init.decode("utf-8")

                   	marca_inicial = False
        	   except:
                        print("erro bisect inicial")
			break;			
            
        
                git_grep =grep(str(row[3].decode("utf-8")),str(row[4].decode("utf-8")))
	        if git_grep == "":
                   break;
                '''git_grep = subprocess.Popen(["git","grep","-E","-i","Import org.togglz.core.feature", "--", "*.java"],
                                            shell = True, stdout=subprocess.PIPE)
                ''' 
        	if git_grep == 0: # found
            	   '''print("achou")'''
            	   try:
                        commit_old_head = commit_head

                	commit_head = re.findall('\W*\[(.*?)\]', bisect_commit_init)[0]

                	bisect_commit_init = subprocess.check_output(["git bisect bad"], stderr=subprocess.STDOUT,shell=True)
                	bisect_commit_init = bisect_commit_init.decode("utf-8")
                   except Exception:
                	commit_head = ""
                        
        	elif git_grep == 1: # not found
            	   try:
                        commit_old_first = for_commit_first

                	for_commit_first = re.findall('\W*\[(.*?)\]', bisect_commit_init)[0]

                	bisect_commit_init = subprocess.check_output(["git bisect good"], stderr=subprocess.STDOUT,shell=True)
                	bisect_commit_init = bisect_commit_init.decode("utf-8")
            	   except Exception:
                	for_commit_first = ""

        	elif git_grep > 1: # error
            	   print("erro:" + str(row[0].decode("utf-8")))        
            	   break
        
        	print("first=" + for_commit_first)
        	print("last=" + commit_head)
                if for_commit_first != "" and commit_head != "":
                   if len(for_commit_first) != 40 or len(commit_head) != 40:
                      print("commit diferente de 44 posicoes: first:" + for_commit_first + " last=" + commit_head)
                      break
    	subprocess.check_output(["git bisect reset"],stderr=subprocess.STDOUT,shell=True)
print("fim")
