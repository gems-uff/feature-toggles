from git import Repo
import mysql.connector
import os

print("conectado ao banco")
cnx = mysql.connector.connect(user='bdd', password='bdduff!!',
                              host='50.62.209.195',
                              database='edusmil_bdd',connection_timeout=300,buffered=True)
cursor = cnx.cursor()
print("banco de dados conectado")

select_search= "SELECT html_url, name, id FROM git_table where dt_clone is null order by id;"
cursor.execute(select_search)
rs_git_search = cursor.fetchall()
cnx.close()
print("consulta realizada")
repo_dir="//home//eduardosmil//featuretoggles//git_repositories//"

for row in cursor._rows:
    git_url = str(row[0].decode("utf-8"))+".git"
    directory = repo_dir + str(row[1].decode("utf-8")) + "_" + str(row[2].decode("utf-8"))

    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
        Repo.clone_from(git_url, directory)
        cnx = mysql.connector.connect(user='bdd', password='bdduff!!',
                              host='50.62.209.195',
                              database='edusmil_bdd',connection_timeout=300,buffered=True)
        cursor = cnx.cursor()
        update_clone="update git_table set dt_clone=now() where id="+str(row[2].decode("utf-8"))+";"
        cursor.execute(update_clone)
        cnx.commit() 
        cnx.close()

        print(git_url)
    except Exception as error:
        print("erro" + str(error))


print("FIM")
