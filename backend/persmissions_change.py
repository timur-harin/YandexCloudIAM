import requests
import os
# export $(xargs <.env)
# Получить IAM

OAUTHTOKEN = os.environ["OAUTHTOKEN"]
ORGANISTIONID = os.environ["ORGANISTIONID"]

def getIAMToken(OAUTHTOKEN):
    body = {
        "yandexPassportOauthToken": OAUTHTOKEN
    }
    r = requests.post(f"https://iam.api.cloud.yandex.net/iam/v1/tokens", json=body)
    return r.json()['iamToken']


def getAllGroups(iamToken, ORGANISTIONID):
    headers = {
        "Authorization": f"Bearer {iamToken}",
    }
    r = requests.get(f"https://organization-manager.api.cloud.yandex.net/organization-manager/v1/groups?organization_id={ORGANISTIONID}", headers=headers)
    groups = {}
    for group in r.json()['groups']:
        groups[group['name']] = group['id']
    return groups

def getGroupUsers(iamToken, groupId):
    headers = {
        "Authorization": f"Bearer {iamToken}",
    }
    r = requests.get(f"https://organization-manager.api.cloud.yandex.net/organization-manager/v1/groups/{groupId}:listMembers", headers=headers)
    return r.json()

# print(getGroupUsers(getIAMToken(OAUTHTOKEN),"ajevfe3je1vgqeihfsfh"))

# Получить всех пользователей всех групп (viewer, editor, admin). Он достает только почту и его subjectId Преобразуя его в словарь


def getAllUsers(iamToken, ORGANISTIONID):
    headers = {"Authorization": f"Bearer {iamToken}"}
    r = requests.get(f"https://organization-manager.api.cloud.yandex.net/organization-manager/v1/organizations/{ORGANISTIONID}/users", headers=headers)
    users = {}
    for user in r.json()['users']:
        if user['subjectClaims']['subType'] == "USER_ACCOUNT":
            users[user['subjectClaims']['sub']] = user['subjectClaims']['email']
    return users

def getUserSubjectID(iamToken, userEmail):
    users = getAllUsers(iamToken, ORGANISTIONID)
    for subjectID, email in users.items():
        if email == userEmail:
           return subjectID

# print(getAllUsers(getIAMToken(OAUTHTOKEN), ORGANISTIONID))

# def getUserGroups(iamToken, userEmail):
#     userSubjectID = ""
#     users = getAllUsers(iamToken, ORGANISTIONID)
#     for subjectID, email in users.items():
#         if email == userEmail:
#            userSubjectID = subjectID
#            break
    


def changeUserGroup(iamToken, email, groupId, action):
    headers = {"Authorization": f"Bearer {iamToken}"}
    subjectId = getUserSubjectID(iamToken, email)
    r = requests.post(f"https://organization-manager.api.cloud.yandex.net/organization-manager/v1/groups/{groupId}:updateMembers", headers=headers, json={"memberDeltas" : {"action": action, "subjectId": subjectId}})
    if r.status_code == 200:
        return True

def changePermission(email, newPermission):

    VIEWER_GROUP_ID = os.environ["VIEWER_GROUP_ID"]
    EDITOR_GROUP_ID = os.environ["EDITOR_GROUP_ID"]
    ADMIN_GROUP_ID = os.environ["ADMIN_GROUP_ID"]

    viewerGroupUsers = getGroupUsers(getIAMToken(OAUTHTOKEN), VIEWER_GROUP_ID)
    editorGroupUsers = getGroupUsers(getIAMToken(OAUTHTOKEN), EDITOR_GROUP_ID)
    adminGroupUsers = getGroupUsers(getIAMToken(OAUTHTOKEN), ADMIN_GROUP_ID)

    userSubjectID = getUserSubjectID(getIAMToken(OAUTHTOKEN), email)
    userGroupID = None
    if 'members' in viewerGroupUsers:
        for user in viewerGroupUsers['members']:
            if user['subjectId'] == userSubjectID:
                userGroupID = VIEWER_GROUP_ID
                break
    if 'members' in editorGroupUsers:
        for user in editorGroupUsers['members']:
            if user['subjectId'] == userSubjectID:
                userGroupID = EDITOR_GROUP_ID
                break
    if 'members' in adminGroupUsers:
        for user in adminGroupUsers['members']:
            if user['subjectId'] == userSubjectID:
                userGroupID = ADMIN_GROUP_ID
                break
    changeUserGroup(getIAMToken(OAUTHTOKEN), email, userGroupID, "REMOVE")
    if newPermission == "viewer": 
        changeUserGroup(getIAMToken(OAUTHTOKEN), email, VIEWER_GROUP_ID, "ADD")
    elif newPermission == "editor":
        changeUserGroup(getIAMToken(OAUTHTOKEN), email, EDITOR_GROUP_ID, "ADD")
    elif newPermission == "admin":
        changeUserGroup(getIAMToken(OAUTHTOKEN), email, ADMIN_GROUP_ID, "ADD")
    else:
        print("Неверный ввод")

    return True



if __name__ == '__main__':
    changePermission('semeritskiy@yandex.ru', "editor")