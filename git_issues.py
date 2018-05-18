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
    token="???????????"

    def __setattr__(self, *_):
        pass

CONST = CONST()

login = requests.get('https://api.github.com/search/repositories?q=github+api', auth=(CONST.username,CONST.token))

_full_name = "edusmil/feature_toggles"


cnx = mysql.connector.connect(user=CONST.BD_USER, password=CONST.BD_PASSWORD,
                              host=CONST.BD_HOST,
                              database=CONST.BD_DATABASE,connection_timeout=300,buffered=True)
cursor = cnx.cursor()

select_search= "SELECT t.id, t.name, t.language, t.full_name FROM git_table t " 
select_search= select_search + "where  t.dt_clone is not null and "
select_search= select_search + " not exists (select 1 from git_issues gl where id_repo=t.id)  and ((cd_classe is null) or (cd_classe = 'ok')) limit 0,10;"
cursor.execute(select_search)
rs_git_search = cursor.fetchall()
cnx.close()

for row in cursor._rows:
    headers = {'Accept': 'application/vnd.github.cloak-preview', 'Authorization': 'token ' + CONST.token}
    url = "https://api.github.com/repos/"+row[3].decode("utf-8")+"/issues?state=all"
    data = requests.get(url,headers=headers).json()
    
    sql_insert=""

    for _issues in data:
        _id = _issues.get("id")
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
            _milestone_number = _milestone.get("number")
            _milestone_id = _milestone.get("id")

        print(_create_date)

        sql_insert = sql_insert + ("(" + str(_id) + "," + str(row[0].decode("utf-8")) + "," +
                                      "'" + _title + "'," +
                                      "'" + _body.replace(chr(39),"") + "'," + 
                                      "'" + _state + "'," +
                                      "'" + _close_date + "'," +
                                      "'" + _create_date + "'," +
                                      "'" + _updated_at + "'," +
                                      "'" + _milestone_state + "'," +
                                      "'" + _milestone_title + "'," +
                                      "'" + _milestone_number + "'," +
                                            _milestone_id + "),")
    if sql_insert != "":
        sql_insert = sql_insert[:len(sql_insert)-1]

        cnx = mysql.connector.connect(user=CONST.BD_USER, password=CONST.BD_PASSWORD,
                              host=CONST.BD_HOST,
                              database=CONST.BD_DATABASE,connection_timeout=300,buffered=True)
        cursor = cnx.cursor()
        sql_insert= ("insert into git_issues (id, id_repo, git_issue_number, git_issue_title, git_issue_body, git_issue_status, " +
                        "                       git_issues_close_date, git_issues_create_date,git_issues_update_date,git_issues_milestone_state, " +
                        "                       git_issues_milestone_title,git_issues_milestone_number,git_issues_milestone_id) values " + sql_insert + ";")
        cursor.execute(sql_insert)
        cnx.close()




