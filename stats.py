# -*- coding: utf-8 -*-

# Sample Python code for youtube.channels.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import time

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]


def saver(vid_name: str,counter: str):
    os.chdir('../confs')
    csvfile = open('saver.csv', 'w')
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    csvfile.write(vid_name + ';' + counter + ";" + current_time + '\n')


class yt_counter:
    def __init__(self):
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
        api_service_name = "youtube"
        api_version = "v3"
        DEVELOPER_KEY =  os.environ.get('KEY')
        client_secrets_file = os.environ.get('secret_file')

        # Get credentials and create an API client
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            client_secrets_file, scopes)
        credentials = flow.run_console()
        self.youtube = googleapiclient.discovery.build(
            api_service_name, api_version, developerKey=DEVELOPER_KEY)
        #   api_service_name, api_version, credentials=credentials)


    def vid_view(self, vid_id: str) -> str:
        request = self.youtube.videos().list(
            part="statistics",
            id=vid_id
        )
        response = request.execute()
        #print(response)
        return response['items'][0]['statistics']['viewCount']

def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"

    DEVELOPER_KEY = "AIzaSyCoFZPZeFMAoFjlsBo5S2ICVKR30jWQxiQ"

    client_secrets_file = "C:\\Users\Arlas\PycharmProjects\Since\ytcounter\confs\client_secret_71806463033-vkd567f7oct0vvm0vtf67lifc6o9oe60.apps.googleusercontent.com.json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY)
    #   api_service_name, api_version, credentials=credentials)

    request = youtube.channels().list(
        part="statistics",
#        forUsername="TWICE"
        id="UCzgxx_DM2Dcb9Y1spb9mUJA"
    )
    response = request.execute()

    print(response)
    print(response['items'][0]['statistics'])

if __name__ == "__main__":

    yt = yt_counter()
    saver('Fancy', yt.vid_view("kOHB85vDuow"))


#    main()