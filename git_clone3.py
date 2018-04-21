import mysql.connector
import os

class CONST(object):
    BD_USER = "bdd_dissertacao"
    BD_PASSWORD = "Smil123!"
    BD_HOST = "50.62.209.195"
    BD_DATABASE = "uff_bdd_dissertacao"
    REPO_DIR="//home//eduardosmil//featuretoggles//git_repositories//"

    def __setattr__(self, *_):
        pass

CONST = CONST()

def f_clone_pull(_url_repository, path):
    try:
        if os.path.exists(path)                       
            os.chdir(path)
            git_grep = subprocess.Popen(["git pull origin master"],
                             shell = True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)        
        else:
            if not os.path.exists(path):
                os.makedirs(path)        
                git_grep = subprocess.Popen(["git clone -q " +  _url_repository + " " + path],
                               shell = True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = git_grep.communicate()
        return git_grep.returncode

    except:
        return ""


print("conectado ao banco")
cnx = mysql.connector.connect(user=CONST.BD_USER, password=CONST.BD_PASSWORD,
                              host=CONST.BD_HOST,
                              database=CONST.BD_DATABASE,connection_timeout=300,buffered=True)
cursor = cnx.cursor()
print("banco de dados conectado")

select_search= "SELECT html_url, name, id FROM git_table where dt_clone is null order by id;"
cursor.execute(select_search)
rs_git_search = cursor.fetchall()
cnx.close()
print("consulta realizada")


for row in cursor._rows:
    git_url = str(row[0].decode("utf-8"))+".git"
    directory = REPO_DIR + str(row[1].decode("utf-8")) + "_" + str(row[2].decode("utf-8"))

    try:
        
        cnx = mysql.connector.connect(user=CONST.BD_USER, password=CONST.BD_PASSWORD,
                              host=CONST.BD_HOST,
                              database=CONST.BD_DATABASE,connection_timeout=300,buffered=True)
        cursor = cnx.cursor()
        update_clone="update git_table set dt_clone=now() where id="+str(row[2].decode("utf-8"))+";"
        cursor.execute(update_clone)
        cnx.commit() 
        cnx.close()

        print(git_url)
    except Exception as error:
        print("erro" + str(error))


print("FIM")
