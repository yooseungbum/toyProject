import urllib
from collections import Counter
import numpy as np
import pandas as pd
import requests
import db_utils as db
import sys
from bs4 import BeautifulSoup as bs

def lotto_crawling():
    minDrwNo = 1            #취득하고 싶은 회차 시작
    maxDrwNo = 1039            #취득하고 싶은 회차 종료  (최종 : 1039 회 (2022-10-29))
    drwtNo1 = []            #1등 첫번째 번호
    drwtNo2 = []            #1등 두번째 번호
    drwtNo3 = []            #1등 세번째 번호
    drwtNo4 = []            #1등 네번째 번호
    drwtNo5 = []            #1등 다섯번째 번호
    drwtNo6 = []            #1등 여섯번째 번호
    bnusNo = []             #보너스 번호
    drwNoDate = []          #로또 추첨일
    firstAccumamnt = []     #1등 전체상금
    totSellamnt = []        #회차 전체상금
    firstWinamnt = []       #1등 수령상금
    firstPrzwnerCo = []     #1등 당첨인원
    drwtNo = []             #1등 전체번호

    # 지정한 시작 회차 부터 종료 회차 까지 취득
    for i in range(minDrwNo, maxDrwNo + 1):
        # 1등 번호를 취득
        req_url = "https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo=" + str(i)

        req_lotto = requests.get(req_url)

        lottoNo = req_lotto.json()

        drwNoDate.append(lottoNo['drwNoDate'])  # 로또 추첨일
        drwtNo1.append(lottoNo['drwtNo1'])      #1등 첫번째 번호 저장
        drwtNo2.append(lottoNo['drwtNo2'])      #1등 두번째 번호 저장
        drwtNo3.append(lottoNo['drwtNo3'])      #1등 세번째 번호 저장
        drwtNo4.append(lottoNo['drwtNo4'])      #1등 네번째 번호 저장
        drwtNo5.append(lottoNo['drwtNo5'])      #1등 다섯번째 번호 저장
        drwtNo6.append(lottoNo['drwtNo6'])      #1등 여섯번째 번호 저장
        bnusNo.append(lottoNo['bnusNo'])        #보너스 번호 저장
        firstAccumamnt.append(lottoNo['firstAccumamnt'])    #1등 전체상금 저장
        totSellamnt.append(lottoNo['totSellamnt'])  # 회차 전체상금 저장
        firstWinamnt.append(lottoNo['firstWinamnt'])    #1등 수령상금 저장
        firstPrzwnerCo.append((lottoNo['firstPrzwnerCo']))  #1등 당첨인원
        # 로또 1등 번호를 하나의 리스트로 머지
        h = np.hstack((drwtNo1[i-1], drwtNo2[i-1], drwtNo3[i-1], drwtNo4[i-1], drwtNo5[i-1], drwtNo6[i-1]))

    df_lotto = pd.DataFrame([drwNoDate, totSellamnt, firstAccumamnt, firstWinamnt, firstPrzwnerCo, drwtNo1, drwtNo2, drwtNo3, drwtNo4, drwtNo5, drwtNo6]).T
    df_lotto.columns = ['time', 'totSellamnt', 'firstAccumamnt', 'firstWinamnt', 'firstPrzwnerCo', 'no1', 'no2', 'no3', 'no4', 'no5', 'no6']

    try:
        df_lotto.to_sql(name="lotto_info", con=db.connection, if_exists="replace", index=False)
        print("lotto_info insert complete")
    except Exception as err:
        print("lotto_info insert fail")
        print(err)

def powerBall_crawling():

    minPage = 1         # crawling 할 시작 페이지
    maxPage = 101         # crawling 할 마지막 페이지 (2004.2.19 101페이지까지 존재)
    drwDate = []        # 추첨일자
    drwpNo1 = []        # 당첨 1번째 번호
    drwpNo2 = []        # 당첨 2번째 번호
    drwpNo3 = []        # 당첨 3번째 번호
    drwpNo4 = []        # 당첨 4번째 번호
    drwpNo5 = []        # 당첨 5번째 번호
    drwpNo6 = []        # 당첨 6번째 번호
    drwpNo = []         # 당첨 전체 번호
    drwResult = []      # 당첨 결과
    firstWinamnt = []   # 1등 당첨금

    for i in range(minPage, maxPage + 1):

        page = "https://www.lottousa.co.kr/result/power_result.php?page="+ str(i)
        html = urllib.request.urlopen(page)
        soup = bs(html, "html.parser")

        # elements = soup.select('#ajaxthislist > div.tablebox1 > div > table > tbody > tr')

        tr_list = soup.select('#power > div.content > table > tbody > tr')
        for tr in tr_list:
            td_list = tr.find_all('td')
            for td, item in enumerate(td_list):
                if td == 1:
                    drwDate.append(item.text.split(' ')[0].replace('.', '-'))
                if td == 2:
                    drwpNo1.append(item.text.split('\n')[2])
                    drwpNo2.append(item.text.split('\n')[3])
                    drwpNo3.append(item.text.split('\n')[4])
                    drwpNo4.append(item.text.split('\n')[5])
                    drwpNo5.append(item.text.split('\n')[6])
                    drwpNo6.append(item.text.split('\n')[7])
                    drwpNo.append(item.text.replace('\n', ' ').strip())
                if td == 3:
                    drwResult.append(item.text)
                if td == 4:
                    firstWinamnt.append(item.find('span', 'dollor').text.split(' ')[1])

    df_powerBall = pd.DataFrame([drwDate, drwResult, firstWinamnt, drwpNo1, drwpNo2, drwpNo3, drwpNo4, drwpNo5, drwpNo6]).T
    df_powerBall.columns = ['time', 'result', 'winAmnt', 'no1', 'no2', 'no3', 'no4', 'no5', 'powerball']

    try:
        df_powerBall.to_sql(name="powreball_info", con=db.connection, if_exists="replace", index=False)
        print("powerBall_info insert complete")
    except Exception as err:
        print("powerBall_info insert fail")
        print(err)

def run():
    # DB 연결
    try:
        db.mysql_connect()
        print("mariaDB connected")
    except Exception as err:
        print("connecting mariaDB error!!")
        print(err)
        sys.exit()

    lotto_crawling()
    powerBall_crawling()

    # db 연결 종료
    db.db_disconnect()
    print("mariaDB disconnected")


