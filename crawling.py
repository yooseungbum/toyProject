import urllib
from collections import Counter
import numpy as np
import requests
from bs4 import BeautifulSoup as bs


def lotto_crawling():
    minDrwNo = 1        #취득하고 싶은 회차 시작
    maxDrwNo = 1037     #취득하고 싶은 회차 종료
    drwtNo1 = []        #1등 첫번째 번호
    drwtNo2 = []        #1등 두번째 번호
    drwtNo3 = []        #1등 세번째 번호
    drwtNo4 = []        #1등 네번째 번호
    drwtNo5 = []        #1등 다섯번째 번호
    drwtNo6 = []        #1등 여섯번째 번호
    bnusNo = []         #보너스 번호
    drwNoDate = []      #로또 추첨일
    firstAccumamnt = [] #1등 전체상금
    totSellamnt = []    #회차 전체상금
    firstWinamnt = []   #1등 수령상금
    firstPrzwnerCo = [] #1등 당첨인원
    drwtNo = []         #1등 전체번호

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
        drwtNo.append(h)

    # 결과 출력
    print(drwtNo)

def powerBall_crawling():

    page = "https://www.gglotto1.com/kr/lottery_result/powerball_result.asp"
    html = urllib.request.urlopen(page)
    soup = bs(html, "html.parser")

    # elements = soup.select('#ajaxthislist > div.tablebox1 > div > table > tbody > tr')

    elements = soup.select('div#tablebox2 > tbody > tr.txtcenter')
    print(elements)


