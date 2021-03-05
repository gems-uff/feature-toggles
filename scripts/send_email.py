# coding=utf-8 
import mysql.connector
import smtplib
import time 
# Import the email modules we'll need
from email.mime.text import MIMEText
import configs as cf

def Verifica_Clonagem():

    print("conectado ao banco")
    cnx = mysql.connector.connect(user=cf.db_user, password=cf.db_pass,
                                host=cf.db_host,
                                database=cf.db_name,connection_timeout=300,buffered=True)
    cursor = cnx.cursor()
    print("banco de dados conectado")

    select_search= "SELECT FLOOR((UNIX_TIMESTAMP(now())-UNIX_TIMESTAMP(max(dt_clone)))/60), max(dt_clone) as dt_ult_clone FROM git_table;"
    cursor.execute(select_search)
    rs_git_search = cursor.fetchall()
    
    cnx.close()

    for row in cursor._rows:
        tempo_decorrido = row[0].decode("utf-8")
        if int(tempo_decorrido) > int(cf.time_limit):

            server = smtplib.SMTP(cf.smtp_host,cf.smtp_port)
            server.ehlo()
            server.starttls()
            #Next, log in to the server
            server.login(cf.smtp_user, cf.smtp_pass)

            #Send the mail
            body = "Ùltima data de clone:" + str(row[1].decode("utf-8"))# The /n separates the message from the headers
            msg = MIMEText(body)
            msg['From'] = cf.email_from
            msg['To'] = cf.email_to
            msg['Subject'] = "Monitoramento Pegasus"
            server.sendmail(cf.email_from, cf.email_copy, msg.as_string())

            server.quit()

while True:
    Verifica_Clonagem()
    time.sleep(1800)   # Delay for 1 minute (60 seconds).
