import mysql.connector
import  requests
import time
import datetime

class CONST(object):
    BD_USER = "bdd_dissertacao"
    BD_PASSWORD = "Smil123!"
    BD_HOST = "50.62.209.195"
    BD_DATABASE = "uff_bdd_dissertacao"
    REPO_DIR="//home//eduardosmil//featuretoggles//git_repositories//"
    username = 'edsumil'

    token="ed5bb3cc975f60c38$948e632284654a769bcf81e"

    def __setattr__(self, *_):
        pass

CONST = CONST()

login = requests.get('https://api.github.com/search/repositories?q=github+api', auth=(CONST.username,CONST.token.replace("$","")))

cnx = mysql.connector.connect(user=CONST.BD_USER, password=CONST.BD_PASSWORD,
                              host=CONST.BD_HOST,
                              database=CONST.BD_DATABASE,connection_timeout=300,buffered=True)
cursor = cnx.cursor()

select_search= "SELECT t.id, t.name, t.language, t.full_name FROM git_table t " 
select_search= select_search + "where  t.dt_clone is not null and "
select_search= select_search + " exists (select 1 from git_issues gl where id_repo=t.id)  and ((t.cd_classe is null) or (t.cd_classe = 'ok')) limit 0,1;"
cursor.execute(select_search)
rs_git_search = cursor.fetchall()
cnx.close()

for row in cursor._rows:
    sql_insert=""
    
    sql_update_git_table = "update git_table set dt_issues=now() where id=" + str(row[0].decode("utf-8")) + ";"
    for i in range(1,100):
        headers = {'Accept': 'application/vnd.github.cloak-preview', 'Authorization': 'token ' + CONST.token.replace("$","")}
        url = "https://api.github.com/repos/"+row[3].decode("utf-8")+"/issues?state=all&per_page=100&page=" + str(i)
        data = requests.get(url,headers=headers).json()
        
        if len(data) == 0:
            break

        for _issues in data:
            if not _issues.get("message") is None:
                print("erro limite:" + str(row[0].decode("utf-8")))
            _id = _issues.get("id")

            sql_verify = "select 1 from git_issues where id=" + str(_id) + ";"
            cnx = mysql.connector.connect(user=CONST.BD_USER, password=CONST.BD_PASSWORD,
                                host=CONST.BD_HOST,
                                database=CONST.BD_DATABASE,connection_timeout=300,buffered=True)
            cursor_v = cnx.cursor()
            
            cursor_v.execute(sql_verify)
            rs_git_issues = cursor_v.fetchall()
            cnx.close()

            if cursor_v.rowcount == 0:
                _number = _issues.get("number")
                _title = _issues.get("title")
                _state = _issues.get("state")
                _body = _issues.get("body") if not _issues.get("body") is None else "null"
                _create_date = datetime.datetime.strptime(_issues.get("created_at"), '%Y-%m-%dT%H:%M:%S%fZ').isoformat() if not _issues.get("created_at") is None else "null"
                _close_date = datetime.datetime.strptime(_issues.get("closed_at"), '%Y-%m-%dT%H:%M:%S%fZ').isoformat() if not _issues.get("closed_at") is None else "null"
                _updated_at = datetime.datetime.strptime(_issues.get("updated_at") , '%Y-%m-%dT%H:%M:%S%fZ').isoformat() if not _issues.get("updated_at") is None else "null"
                _milestone_state = "null"
                _milestone_title = "null"
                _milestone_number = "null"
                _milestone_id = "null"
                if not _issues.get("milestone") is None:
                    _milestone = _issues.get("milestone")
                    _milestone_state = _milestone.get("state")
                    _milestone_title = _milestone.get("title")
                    _milestone_number = str(_milestone.get("number"))
                    _milestone_id = _milestone.get("id")

                sql_insert = sql_insert + ("(" + str(_id) + "," + str(row[0].decode("utf-8")) + "," +
                                            "'" + str(_number) + "'," +
                                            "'" + _title.replace(chr(39),"").replace("\\","").replace(chr(34),"") + "'," +
                                            "'" + _body.replace(chr(39),"").replace("\\","").replace(chr(34),"") + "'," +                                       
                                            "'" + _state + "'," +
                                            "'" + _close_date + "'," +
                                            "'" + _create_date + "'," +
                                            "'" + _updated_at + "'," +
                                            "'" + _milestone_state + "'," +
                                            "'" + _milestone_title.replace(chr(39),"").replace("\\","").replace(chr(34),"") + "'," +
                                            "'" +_milestone_number + "'," +
                                                    str(_milestone_id) + ", NOW()),")

                _labels = _issues.get("labels")

                sql_insert_label = ""

                for _label in data:
                    _id_label = _label.get("id")
                    _issues_label_name = "'" + _label.get("name").replace(chr(39)) + "'" if not _label.get("name") is None else "null"
                    _issues_label_description = "'" + _label.get("description").replace(chr(39)) + "'" if not _label.get("description") is None else "null"
                    
                    sql_insert_label = sql_insert_label + ("(" + str(_id_label) + "," + 
                                                        str(row[0].decode("utf-8")) + "," +
                                                        _issues_label_name + "," +
                                                        _issues_label_description + "),")

    if sql_insert != "":
        sql_insert = sql_insert[:len(sql_insert)-1]

        cnx = mysql.connector.connect(user=CONST.BD_USER, password=CONST.BD_PASSWORD,
                              host=CONST.BD_HOST,
                              database=CONST.BD_DATABASE,connection_timeout=300,buffered=True)
        cursor = cnx.cursor()
        sql_insert= ("insert into git_issues (id, id_repo, git_issue_number, git_issue_title, git_issue_body, git_issue_status, " +
                        "                       git_issues_close_date, git_issues_create_date,git_issues_update_date,git_issues_milestone_state, " +
                        "                       git_issues_milestone_title,git_issues_milestone_number,git_issues_milestone_id,dt_operation) values " + sql_insert + ";")
        #print(sql_insert)
        cursor.execute(sql_insert)
        cnx.close()

        if sql_insert_label != "":
            sql_insert_label = sql_insert_label[:len(sql_insert_label)-1]

            cnx = mysql.connector.connect(user=CONST.BD_USER, password=CONST.BD_PASSWORD,
                              host=CONST.BD_HOST,
                              database=CONST.BD_DATABASE,connection_timeout=300,buffered=True)
            cursor = cnx.cursor()
            
            sql_insert_label= ("insert into git_issues_label (id,id_issue,git_issues_label_name,git_issues_label_description) values  " +
                            sql_insert_label + ";")
            cursor.execute(sql_insert_label)
            cnx.close()

    cnx = mysql.connector.connect(user=CONST.BD_USER, password=CONST.BD_PASSWORD,
                              host=CONST.BD_HOST,
                              database=CONST.BD_DATABASE,connection_timeout=300,buffered=True)
    cursor = cnx.cursor()    
    cursor.execute(sql_update_git_table)
    cnx.close()

    cnx = mysql.connector.connect(user=CONST.BD_USER, password=CONST.BD_PASSWORD,
                              host=CONST.BD_HOST,
                              database=CONST.BD_DATABASE,connection_timeout=300,buffered=True)
    cursor_issues = cnx.cursor()
    select_search= ("SELECT id, id_repo, git_issue_number FROM git_issues i " +
                    "where not exists (select 1 from git_issues_events e where i.id = e.id_issue) and i.id_repo="+row[0].decode("utf-8")+"; " )
    cursor_issues.execute(select_search)
    rs_git_issues = cursor_issues.fetchall()
    cnx.close()

    sql_insert_event=""

    for row_issue in cursor_issues._rows:
        for i in range(1,100):
            headers = {'Accept': 'application/vnd.github.cloak-preview', 'Authorization': 'token ' + CONST.token.replace("$","")}
            url = "https://api.github.com/repos/"+row[3].decode("utf-8")+"/issues/"+row_issue[2].decode("utf-8")+"/events?per_page=100&page=" + str(i)
            data_events = requests.get(url,headers=headers).json()

            if len(data_events) == 0:
                break

            for _issues_events in data_events:
                _id_issue_event = _issues_events.get("id")
                _cd_event = "'" + _issues_events.get("event") + "'" if not _issues_events.get("event") is None else "null"
                _id_commit_event = "'" + _issues_events.get("commit_id") + "'" if not _issues_events.get("commit_id") is None else "null"
                _create_date_event = "'" + datetime.datetime.strptime(_issues_events.get("created_at"), '%Y-%m-%dT%H:%M:%S%fZ').isoformat() + "'" if not _issues.get("created_at")  is None else "null"

                sql_insert_event = sql_insert_event + ("(" + str(_id_issue_event) + "," + 
                                                    str(row_issue[0].decode("utf-8")) + "," + 
                                                    _cd_event + "," +
                                                    _id_commit_event + "," +
                                                    _create_date_event + "),")

    if sql_insert_event != "":
        sql_insert_event = sql_insert_event[:len(sql_insert_event)-1]

        cnx = mysql.connector.connect(user=CONST.BD_USER, password=CONST.BD_PASSWORD,
                              host=CONST.BD_HOST,
                              database=CONST.BD_DATABASE,connection_timeout=300,buffered=True)
        cursor = cnx.cursor()
            
        sql_insert_event= ("insert into git_issues_events (id,id_issue,cd_event,id_commit,git_create_date) values  " +
                        sql_insert_event + ";")
        cursor.execute(sql_insert_event)
        cnx.close()