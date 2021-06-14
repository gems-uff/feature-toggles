import subprocess
import configs as cf
import mysql.connector
import os

'''
    outputs 0 when there is a match and 1 otherwise.
'''
def grep(grep_string, files, path):
    try:
        # print(grep_string)
        # print(files)
        # print(path)
        grep_string = grep_string.replace(" ","(.*?)")
        grep_string = chr(34) + grep_string + chr(34)

        grep = "git grep -E -i -q " +  grep_string
        if files != "":
            grep = grep + " -- '" + files+"'"
            git_grep = subprocess.Popen([grep], shell = True, stdout=subprocess.PIPE, cwd=path, 
                stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            git_grep = subprocess.Popen([grep], shell = True, stdout=subprocess.PIPE, cwd=path,
                 stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = git_grep.communicate()
        # print(grep)
        # print(error)
        return git_grep.returncode
    except:
        return ""


def uses_framework(project_fullname, programming_language):
    REPOS_PATH = os.path.abspath("../../repos")
    project_path = os.path.join(REPOS_PATH,project_fullname)
    cnx = mysql.connector.connect(user=cf.db_user, password=cf.db_pass,
            host=cf.db_host,
            database=cf.db_name,connection_timeout=300,buffered=True)
    cursor = cnx.cursor()
    select_search= f"SELECT s.git_word, s.git_file_extension FROM git_search s where s.git_language = '{programming_language}'" 
    # print(select_search)
    cursor.execute(select_search)
    rs_git_search = cursor.fetchall()
    cnx.close()

    for row in cursor._rows:
        # print(row)
        git_grep_return_code =grep(str(row[0]),str(row[1]), project_path)
        if git_grep_return_code == 0:
            return True
        
        # print(f"return code: {git_grep}")
        # print("Repositorio: " + str(row[1].decode("utf-8")) + "_" + str(row[0].decode("utf-8")))
    return False
# print(uses_framework("java", "razerdp/AnimatedPieView"))
# uses_framework("java", "guigarage/DataFX")