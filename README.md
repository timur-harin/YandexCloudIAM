# Permission Changer 3000

The Permission Changer 3000 Management System allows administrators to grant different levels of access to users within their organization. There are three main roles available: Viewer, Group, and Admin. These roles determine the level of access users have to resources within the Yandex Cloud platform.

## Requirements

 - Get Yandex OAuth Token [here](https://oauth.yandex.ru/authorize?response_type=token&client_id=1a6990aa636648e9b2ef855fa7bec2fb). 
 - Different IDs you can find on Yandex Cloud Console.
 - You also need to create three groups with corrsponding permissions (viewer, editor, admin)

 - You need Docker for launching

## Build

You can use public image (`fatm1nd/tv-image`) or build image yourself in project root folder:

```
docker build -t tv-image .
```

## Deploy

Run the built container 

`docker run -p 8080:5000 -e OAUTHTOKEN='<YandexTokenOauth>' \
-e ORGANISTIONID='<yandexCloudOrganistionID>' \
-e VIEWER_GROUP_ID='<viewerGroup>' \
-e EDITOR_GROUP_ID='<editorGroup>' \
-e ADMIN_GROUP_ID='<adminGroup>' \
-d -v /logs.tv:/app/logs --name permission-changer \
tv-image`

(replace `tv-image` with `fatm1nd/tv-image` for pulling built image)

## Access to demo

You could access the project on [this link](http://158.160.149.1). You should be added to specific Cloud Organisation. Due to problems, ask [FatM1nd](https://t.me/fatm1nd) on telegram.

## Logs

Logs could be accessible on `/logs` route. For example `http://158.160.149.1/logs`

## Video demonstration
Short PoC demo of the service
https://streamable.com/rif6ar
