import mysql.connector
from github import Github


# using username and password
#g = Github("user", "password")

# or using an access token
g = Github("U-k9OBXUjX0AvtRoZIpAjg")


r = g.get_repo("edusmil/feature_toggles")
print(r)
issues = r.get_issues()
print(issues)



