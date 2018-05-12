# coding=utf-8 
import mysql.connector
import os
import subprocess
import datetime

class CONST(object):
    BD_USER = "bdd_dissertacao"
    BD_PASSWORD = "Smil123!"
    BD_HOST = "50.62.209.195"
    BD_DATABASE = "uff_bdd_dissertacao"
    REPO_DIR="//home//eduardosmil//featuretoggles//git_repositories//"

    def __setattr__(self, *_):
        pass

CONST = CONST()

def f_retorna_data_hora():
    return datetime.datetime.now().strftime("%H:%M:%S -- %d/%m/%Y")

def f_clone_pull(_url_repository, path, erro):
    try:
        if os.path.exists(path):          
            print("acessando diretório " + path)
            os.chdir(path)
            print("git checkout master " + _url_repository)
            git_clone = subprocess.Popen(["git checkout master"],
                             stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
            print("git pull " + _url_repository)
            git_clone = subprocess.Popen(["for i in $(git branch | sed 's/^.//'); do git checkout $i; git pull; done"],
                             stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)        
        else:
	        print("criando diretório " + path)
            os.makedirs(path)            
            print("inicio: git clone " + _url_repository)
            git_clone = subprocess.Popen(["git", "clone", _url_repository, path],
                               stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
            print("fim:  git clone " + _url_repository)
        output, error = git_clone.communicate()	
        return git_clone.returncode

    except:
	erro = True
        return "erro ao clonar repositório:" + _url_repository


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
ret = ""

for row in cursor._rows:
    print(f_retorna_data_hora() + "=====================================================")
    git_url = str(row[0].decode("utf-8"))+".git"
    directory = CONST.REPO_DIR + str(row[1].decode("utf-8")) + "_" + str(row[2].decode("utf-8"))

    try:
  	erro = False

    	ret = f_clone_pull(git_url, directory,erro)
        if not erro:
            cnx = mysql.connector.connect(user=CONST.BD_USER, password=CONST.BD_PASSWORD,
                                          host=CONST.BD_HOST,
                                  database=CONST.BD_DATABASE,connection_timeout=300,buffered=True)
            cursor = cnx.cursor()
            update_clone="update git_table set dt_clone=now() where id="+str(row[2].decode("utf-8"))+";"
            cursor.execute(update_clone)
            cnx.commit() 
            cnx.close()

        else:
            print(ret)
       
	print(f_retorna_data_hora() + "======================================================")
    except Exception as error:
        print("erro: " + error.strerror)


print("FIM")
