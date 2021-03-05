import git
import mysql.connector
import os
import configs as cf

class Progress(git.remote.RemoteProgress):
    def update(self, op_code, cur_count, max_count=None, message=''):
        print(self._cur_line + chr(13)+chr(10))

print("conectado ao banco")
cnx = mysql.connector.connect(user=cf.bd_user, user=cf.db_pass,
                              host=cf.db_host,
                              database=cf.db_name,connection_timeout=300,buffered=True)
cursor = cnx.cursor()
print("banco de dados conectado")

select_search= "SELECT html_url, name, id FROM edusmil_bdd.git_table t where not exists (Select 1 from git_stats_local l where l.id_repo=t.id) and ((cd_classe is null) or (cd_classe = 'ok')) ;"
cursor.execute(select_search)
rs_git_search = cursor.fetchall()
cnx.close()
print("consulta realizada")
repo_dir="//home//eduardosmil//featuretoggles//git_repositories//"

for row in cursor._rows:
    git_url = str(row[0].decode("utf-8"))+".git"
    directory = repo_dir + str(row[1].decode("utf-8")) + "_" + str(row[2].decode("utf-8"))
    print(str(row[2].decode("utf-8")))
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
        git.Repo.clone_from(git_url, directory,progress=Progress())
        cnx = mysql.connector.connect(user=cf.bd_user, user=cf.db_pass,
                              host=cf.db_host,
                              database=cf.db_name,connection_timeout=300,buffered=True)
        cursor = cnx.cursor()
        update_clone="update git_table set dt_clone=now() where id="+str(row[2].decode("utf-8"))+";"
        cursor.execute(update_clone)
        cnx.commit() 
        cnx.close()

        print(git_url)
    except Exception as error:
        print("erro" + str(error))


print("FIM")
