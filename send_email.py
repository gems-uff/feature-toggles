# coding=utf-8 
import mysql.connector
import smtplib
import time 
# Import the email modules we'll need
from email.mime.text import MIMEText

class CONST(object):
    BD_USER = "bdd_dissertacao"
    BD_PASSWORD = "Smil123!"
    BD_HOST = "50.62.209.195"
    BD_DATABASE = "uff_bdd_dissertacao"
    REPO_DIR="//home//eduardosmil//featuretoggles//git_repositories//"
    TEMPO_LIMITE = 60

    def __setattr__(self, *_):
        pass

CONST = CONST()

def Verifica_Clonagem():

    print("conectado ao banco")
    cnx = mysql.connector.connect(user=CONST.BD_USER, password=CONST.BD_PASSWORD,
                                host=CONST.BD_HOST,
                                database=CONST.BD_DATABASE,connection_timeout=300,buffered=True)
    cursor = cnx.cursor()
    print("banco de dados conectado")

    select_search= "SELECT FLOOR((UNIX_TIMESTAMP(now())-UNIX_TIMESTAMP(max(dt_clone)))/60), max(dt_clone) as dt_ult_clone FROM git_table;"
    cursor.execute(select_search)
    rs_git_search = cursor.fetchall()
    
    cnx.close()

    for row in cursor._rows:
        tempo_decorrido = row[0].decode("utf-8")
        if int(tempo_decorrido) > int(CONST.TEMPO_LIMITE):

            server = smtplib.SMTP('smtp.sistemaisbet.org.br',587)
            server.ehlo()
            server.starttls()
            #Next, log in to the server
            server.login("sistema@sistemaisbet.org.br", "isbet123")

            #Send the mail
            body = "Ùltima data de clone:" + str(row[1].decode("utf-8"))# The /n separates the message from the headers
            msg = MIMEText(body)
            msg['From'] = "sistema@sistemaisbet.org.br"
            msg['To'] = "eduardosmil@gmail.com"
            msg['Subject'] = "Monitoramento Pegasus"
            server.sendmail("sistema@sistemaisbet.org.br", "eduardosmil@gmail.com", msg.as_string())

            server.quit()

while True:
    Verifica_Clonagem()
    time.sleep(1800)   # Delay for 1 minute (60 seconds).