import requests
# Получить IAM

oAuthToken = ""
organizationId = ""

def getIAMToken(oAuthToken):
    body = {
        "yandexPassportOauthToken": oAuthToken
    }
    r = requests.post(f"https://iam.api.cloud.yandex.net/iam/v1/tokens", json=body)
    return r.json()['iamToken']


def getAllGroups(iamToken, organizationId):
    headers = {
        "Authorization": f"Bearer {iamToken}",
    }
    r = requests.get(f"https://organization-manager.api.cloud.yandex.net/organization-manager/v1/groups?organization_id={organizationId}", headers=headers)
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

# print(getGroupUsers(getIAMToken(""),"ajehnfe2r3pr8046tem8"))

# Получить всех пользователей всех групп (viewer, editor, admin). Он достает только почту и его subjectId Преобразуя его в словарь


def getAllUsers(iamToken, organizationId):
    headers = {"Authorization": f"Bearer {iamToken}"}
    r = requests.get(f"https://organization-manager.api.cloud.yandex.net/organization-manager/v1/organizations/{organizationId}/users", headers=headers)
    users = {}
    for user in r.json()['users']:
        if user['subjectClaims']['subType'] == "USER_ACCOUNT":
            users[user['subjectClaims']['sub']] = user['subjectClaims']['email']
    return users


def getUserGroups(iamToken, email):
   pass


def changeUserGroup(iamToken, subjectId, groupId, action):
    pass


def change_permission(email, new_permission):
    pass



if __name__ == '__main__':
    pass