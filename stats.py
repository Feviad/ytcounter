# -*- coding: utf-8 -*-

# Sample Python code for youtube.channels.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import os
import time

#import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

import win32com.client
Excel = win32com.client.Dispatch("Excel.Application")


scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
twice_MV_dict = {'Fancy': 'kOHB85vDuow',
                 'BDZ': 'CMNahhgR_ss',
                 'Likey kor': 'V2hlQkVJZhE',
                 'BRAND NEW GIRL': 'r1CMjQ0QJ1E',
                 'Dance The Night Away': 'Fm5iP0S1z9w',
                 'TT jap': 't35H2BVq490',
                 'Yes or Yes': 'mAKsZ26SabQ',
                 'TT kor': 'ePpPVE-GGJw',
                 'I want you back': 'X3H-4crGD6k',
                 'What is Love kor': 'i0p1bmr0EmE',
                 'TBTIED': 'CfUGjK6gGgs',
                 'What is Love jap': '3zQXMPbK5jU',
                 'Heart Shaker': 'rRzxEiBLQCA',
                 'Likey jap': 'N7MKlhS2ysU',
                 'Knock Knock': '8A2t_tAjMz8',
                 'Cheer Up': 'c7rCyll5AeY',
                 'One more time': 'HuoOEry-Yc4',
                 'Wake me up': 'DdLYSziSXII',
                 'Stay by my side': '96K5RxgTfW4',
                 'Signal': 'VQtonf1fv_s',
                 'Merry & Happy': 'zi_6oaQyckM',
                 'Like OOH-AHH': '0rtV5esQT6I'
                 }

blackpink_MV_dict = {'Kill this love': '2S24-y0Ij3Y',
                     'DDU-DU DDU-DU': 'IHNzOHi8sJs',
                     'BOOMBAYAH': 'bwmSjveL3Lc',
                     'SOLO': 'b73BI9eUkjM',
                     'AIIYL': 'Amq-qlqbjYA',
                     'WHISTLE': 'dISNgvVpWlo',
                     'PLAYING WITH FIRE': '9pdj4iJD08s'
                     }


class yt_counter:
    def __init__(self):
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
        api_service_name = "youtube"
        api_version = "v3"
        DEVELOPER_KEY = os.environ.get('KEY')

        # client_secrets_file = os.environ.get('secret_file')
        # Get credentials and create an API client
        # flow = google_auth_oauthlib.flow.InstalledAppFlow.
        #               from_client_secrets_file(client_secrets_file, scopes)
        # credentials = flow.run_console()

        self.youtube = googleapiclient.discovery.build(
            api_service_name, api_version, developerKey=DEVELOPER_KEY)
        #   api_service_name, api_version, credentials=credentials)

    def vid_view(self, vid_id: str) -> str:
        request = self.youtube.videos().list(
            part="statistics",
            id=vid_id
        )
        response = request.execute()
        return response['items'][0]['statistics']['viewCount']

    def vid_duration(self, vid_id: str) -> str:
        request = self.youtube.videos().list(
            part="contentDetails",
            id=vid_id
        )
        response = request.execute()
        timestamp = response['items'][0]['contentDetails']['duration']
        try:
            t = time.strptime(timestamp, 'PT%MM%SS')
        except:
            try:
                t = time.strptime(timestamp, 'PT%MM')
            except:
                t = ''
                print('WTF ' + timestamp)

        return time.strftime("%H:%M:%S", t)


def saver(yt: yt_counter):
    os.chdir('../confs')
    wb = Excel.Workbooks.Open(os.getcwd() + '\\test.xlsx')
    sheet = wb.ActiveSheet

    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    i = 3
    while sheet.Cells(2, i).value:
        i = i+1
    sheet.Cells(2, i).value = current_time
    for mv_name in twice_MV_dict:
        c = sheet.Range('A3:A24').Find(mv_name, LookIn='xlValues')
        views = yt.vid_view(twice_MV_dict[mv_name])
        sheet.Cells(c.row, i).value = views
        print(mv_name + ' ' + str(c.row) + ' : ' + views)

    for mv_name in blackpink_MV_dict:
        c = sheet.Range('A27:A33').Find(mv_name, LookIn='xlValues')
        views = yt.vid_view(blackpink_MV_dict[mv_name])
        sheet.Cells(c.row, i).value = views
        print(mv_name + ' ' + str(c.row) + ' : ' + views)

    wb.Save()
    # закрываем ее
    wb.Close()
    # закрываем COM объект
    Excel.Quit()


def settler(yt: yt_counter):
    os.chdir('../confs')

    wb = Excel.Workbooks.Open(os.getcwd() + '\\test.xlsx')
    sheet = wb.ActiveSheet
    mv = sheet.Cells(3, 1).value
    print(mv)
    if not mv:
        i = 3
        for mv_name in twice_MV_dict:
            sheet.Cells(i, 1).value = mv_name
            mv_dur = yt.vid_duration(twice_MV_dict[mv_name])
            # sheet.cell(row=i, column=2).value = mv_dur
            sheet.Cells(i, 2).value = mv_dur
            i = i + 1
        i = 27
        for mv_name in blackpink_MV_dict:
            sheet.Cells(i, 1).value = mv_name
            mv_dur = yt.vid_duration(blackpink_MV_dict[mv_name])
            sheet.Cells(i, 2).value = mv_dur
            i = i + 1

    wb.Save()
    # закрываем ее
    wb.Close()
    # закрываем COM объект
    Excel.Quit()


def main():
    yt = yt_counter()
    settler(yt)
    for i in range(3):
        saver(yt)
        time.sleep(3600)


if __name__ == "__main__":
    main()
