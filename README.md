# YandexCloudIAM


## Requirements

 - Get Yandex Oauth Token [here](https://oauth.yandex.ru/authorize?response_type=token&client_id=1a6990aa636648e9b2ef855fa7bec2fb). 
 - Different IDs you can find on Yandex Cloud Console.
 - You also need to create three groups with corrsponding permissions (viewer, editor, admin)

## Deploy

Run the built container 

`docker run -p 8080:5000 -e OAUTHTOKEN='<YandexTokenOauth>' \
-e ORGANISTIONID='<yandexCloudOrganistionID>' \
-e VIEWER_GROUP_ID='<viewerGroup>' \
-e EDITOR_GROUP_ID='<editorGroup>' \
-e ADMIN_GROUP_ID='<adminGroup>' \
fatm1nd/tv-image `