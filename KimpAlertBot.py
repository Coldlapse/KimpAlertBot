# for python 2.8
#-*- coding: utf-8 -*-
import sys
import urllib, urllib2
import requests
import time
import json
import datetime
reload(sys)
sys.setdefaultencoding('utf-8')

currentkimp = 0
kimp_max = -65535
kimp_max_print = 0
kimp_min = 65535
kimp_min_print = 0
noticecount = 0
now = datetime.datetime.now() + datetime.timedelta(hours=9)
nowTuple = now.timetuple()
maxtime_hour = 0
maxtime_mmin = 0
mintime_hour = 0
mintime_mmin = 0


def send_telegram(sendData):
	BOT_ID = "" # Bot API Key
	CHAT_ID = 0 # Bot Chat-id

	urllib2.urlopen("https://api.telegram.org/bot" + BOT_ID + "/sendMessage",
        			urllib.urlencode({ "chat_id": CHAT_ID, "text": sendData}))

while True:
    kimp = 0
    print("\n루프문 시작")
    sys.stdout.flush()
    tempdate = datetime.datetime.now() + datetime.timedelta(hours=9)
    tempdateTuple = tempdate.timetuple()
    if nowTuple.tm_mday != tempdateTuple.tm_mday:
        noticecount = 0
        print("날짜 갱신 감지! noticecount 리셋됨")
        sys.stdout.flush()
    now = datetime.datetime.now() + datetime.timedelta(hours=9)
    nowTuple = now.timetuple()
    print("현재 시각 : " + str(now))
    sys.stdout.flush()


    for i in range(1, 61):
        usdkrw = requests.get("https://api.manana.kr/exchange/rate/KRW/USD.json")
        usdkrw_data = json.loads(usdkrw.text)
        usdkrwrate = usdkrw_data[0]['rate']

        upbit_trx_raw = requests.get("https://api.upbit.com/v1/ticker?markets=KRW-trx")
        upbit_trx_price = json.loads(upbit_trx_raw.text)
        upbit_trx_finalprice = upbit_trx_price[0]['trade_price']
        binance_trx_raw = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=TRXUSDT")
        binance_trx_price = json.loads(binance_trx_raw.text)
        binance_trx_finalprice = float(binance_trx_price['price']) * usdkrwrate
        kimp_trx = upbit_trx_finalprice / binance_trx_finalprice * 100

        upbit_xrp_raw = requests.get("https://api.upbit.com/v1/ticker?markets=KRW-xrp")
        upbit_xrp_price = json.loads(upbit_xrp_raw.text)
        upbit_xrp_finalprice = upbit_xrp_price[0]['trade_price']
        binance_xrp_raw = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=XRPUSDT")
        binance_xrp_price = json.loads(binance_xrp_raw.text)
        binance_xrp_finalprice = float(binance_xrp_price['price']) * usdkrwrate
        kimp_xrp = upbit_xrp_finalprice / binance_xrp_finalprice * 100

        upbit_xlm_raw = requests.get("https://api.upbit.com/v1/ticker?markets=KRW-xlm")
        upbit_xlm_price = json.loads(upbit_xlm_raw.text)
        upbit_xlm_finalprice = upbit_xlm_price[0]['trade_price']
        binance_xlm_raw = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=XLMUSDT")
        binance_xlm_price = json.loads(binance_xlm_raw.text)
        binance_xlm_finalprice = float(binance_xlm_price['price']) * usdkrwrate
        kimp_xlm = upbit_xlm_finalprice / binance_xlm_finalprice * 100


        upbit_eos_raw = requests.get("https://api.upbit.com/v1/ticker?markets=KRW-eos")
        upbit_eos_price = json.loads(upbit_eos_raw.text)
        upbit_eos_finalprice = upbit_eos_price[0]['trade_price']
        binance_eos_raw = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=EOSUSDT")
        binance_eos_price = json.loads(binance_eos_raw.text)
        binance_eos_finalprice = float(binance_eos_price['price']) * usdkrwrate
        kimp_eos = upbit_eos_finalprice / binance_eos_finalprice * 100

        kimp = kimp + (kimp_eos + kimp_xrp + kimp_trx + kimp_xlm) / 4
        time.sleep(10)

    kimp = kimp / 60 # 10분마다 김프 평균 산출

    # 역프 발생시 100 아래, 김프 발생시 100 위
    if (kimp > kimp_max):
        kimp_max = kimp
        kimp_max_print = kimp_max - 100
        kimp_max_print = round(kimp_max_print, 2)
        maxtime_hour = nowTuple.tm_hour
        maxtime_mmin = nowTuple.tm_min

    if (kimp < kimp_min):
        kimp_min = kimp
        kimp_min_print = kimp_min - 100
        kimp_min_print = round(kimp_min_print, 2)
        mintime_hour = nowTuple.tm_hour
        mintime_mmin = nowTuple.tm_min

    if (noticecount == 0):
        firsttext = "📢 "
        noticedate = datetime.datetime.now() + datetime.timedelta(days=-1, hours=9)
        noticedateTuple = noticedate.timetuple()
        datestring = str(noticedateTuple.tm_mon) + "월 " + str(noticedateTuple.tm_mday) + "일"
        noticestring = "의 김프 고점과 저점 알림!\n"
        maxstring = "고점 : " + str(kimp_max_print) + "%, " + str(maxtime_hour) + "시 " + str(maxtime_mmin) + "분 경\n"
        minstring = "저점 : " + str(kimp_min_print) + "%, " + str(mintime_hour) + "시 " + str(mintime_mmin) + "분 경"
        text = firsttext + datestring + noticestring + maxstring + minstring
        print(text)
        sys.stdout.flush()
        send_telegram(text.encode('utf-8'))
        noticecount = 1

    if 100 - kimp >= 0 :
        burgerp = True
    else:
        burgerp = False

    kimp = abs(100 - kimp)
    kimp = round(kimp, 2)

    print(str(kimp))
    sys.stdout.flush()

    if (kimp < 0.5) & (kimp >= 0) & (currentkimp != 0):
        currentkimp = 0
        if burgerp == True:
            firsttext = "🍔 역프 0%권 도달!\n현재 역프 : "
            text = firsttext + str(kimp) + "%"
            print(text)
            sys.stdout.flush()
            send_telegram(text.encode('utf-8'))
        else:
            firsttext = "🥓 김프 0%권 도달!\n현재 김프 : "
            text = firsttext + str(kimp) + "%"
            print(text)
            sys.stdout.flush()
            send_telegram(text.encode('utf-8'))

    if (kimp < 1) & (kimp >= 0.5) & (currentkimp != 0.5):
        currentkimp = 0.5
        if burgerp == True:
            firsttext = "🍔 역프 0.5%권 도달!\n현재 역프 : "
            text = firsttext + str(kimp) + "%"
            print(text)
            sys.stdout.flush()
            send_telegram(text.encode('utf-8'))
        else:
            firsttext = "🥓 김프 0.5%권 도달!\n현재 김프 : "
            text = firsttext + str(kimp) + "%"
            print(text)
            sys.stdout.flush()
            send_telegram(text.encode('utf-8'))

    if (kimp < 1.5) & (kimp >= 1) & (currentkimp != 1):
        currentkimp = 1
        if burgerp == True:
            firsttext = "🍔 역프 1%권 도달!\n현재 역프 : "
            text = firsttext + str(kimp) + "%"
            print(text)
            sys.stdout.flush()
            send_telegram(text.encode('utf-8'))
        else:
            firsttext = "🥓 김프 1%권 도달!\n현재 김프 : "
            text = firsttext + str(kimp) + "%"
            print(text)
            sys.stdout.flush()
            send_telegram(text.encode('utf-8'))

    if (kimp < 2) & (kimp >= 1.5) & (currentkimp != 1.5):
        currentkimp = 1.5
        if burgerp == True:
            firsttext = "🍔 역프 1.5%권 도달!\n현재 역프 : "
            text = firsttext + str(kimp) + "%"
            print(text)
            sys.stdout.flush()
            send_telegram(text.encode('utf-8'))
        else:
            firsttext = "🥓 김프 1.5%권 도달!\n현재 김프 : "
            text = firsttext + str(kimp) + "%"
            print(text)
            sys.stdout.flush()
            send_telegram(text.encode('utf-8'))

    if (kimp < 2.5) & (kimp >= 2) & (currentkimp != 2):
        currentkimp = 2
        if burgerp == True:
            firsttext = "🍔 역프 2%권 도달!\n현재 역프 : "
            text = firsttext + str(kimp) + "%"
            print(text)
            sys.stdout.flush()
            send_telegram(text.encode('utf-8'))
        else:
            firsttext = "🥓 김프 2%권 도달!\n현재 김프 : "
            text = firsttext + str(kimp) + "%"
            print(text)
            sys.stdout.flush()
            send_telegram(text.encode('utf-8'))

    if (kimp < 3) & (kimp >= 2.5) & (currentkimp != 2.5):
        currentkimp = 2.5
        if burgerp == True:
            firsttext = "🍔 역프 2.5%권 도달!\n현재 역프 : "
            text = firsttext + str(kimp) + "%"
            print(text)
            sys.stdout.flush()
            send_telegram(text.encode('utf-8'))
        else:
            firsttext = "🥓 김프 2.5%권 도달!\n현재 김프 : "
            text = firsttext + str(kimp) + "%"
            print(text)
            sys.stdout.flush()
            send_telegram(text.encode('utf-8'))

    if (kimp < 3.5) & (kimp >= 3) & (currentkimp != 3):
        currentkimp = 3
        if burgerp == True:
            firsttext = "🍔 역프 3%권 도달!\n현재 역프 : "
            text = firsttext + str(kimp) + "%"
            print(text)
            sys.stdout.flush()
            send_telegram(text.encode('utf-8'))
        else:
            firsttext = "🥓 김프 3%권 도달!\n현재 김프 : "
            text = firsttext + str(kimp) + "%"
            print(text)
            sys.stdout.flush()
            send_telegram(text.encode('utf-8'))

    if (kimp < 4) & (kimp >= 3.5) & (currentkimp != 3.5):
        currentkimp = 3.5
        if burgerp == True:
            firsttext = "🍔 역프 3.5%권 도달!\n현재 역프 : "
            text = firsttext + str(kimp) + "%"
            print(text)
            sys.stdout.flush()
            send_telegram(text.encode('utf-8'))
        else:
            firsttext = "🥓 김프 3.5%권 도달!\n현재 김프 : "
            text = firsttext + str(kimp) + "%"
            print(text)
            sys.stdout.flush()
            send_telegram(text.encode('utf-8'))

    if (kimp < 4.5) & (kimp >= 4) & (currentkimp != 4):
        currentkimp = 4
        if burgerp == True:
            firsttext = "🍔 역프 4%권 도달!\n현재 역프 : "
            text = firsttext + str(kimp) + "%"
            print(text)
            sys.stdout.flush()
            send_telegram(text.encode('utf-8'))
        else:
            firsttext = "🥓 김프 4%권 도달!\n현재 김프 : "
            text = firsttext + str(kimp) + "%"
            print(text)
            sys.stdout.flush()
            send_telegram(text.encode('utf-8'))

    if (kimp < 5) & (kimp >= 4.5) & (currentkimp != 4.5):
        currentkimp = 4.5
        if burgerp == True:
            firsttext = "🍔 역프 4.5%권 도달!\n현재 역프 : "
            text = firsttext + str(kimp) + "%"
            print(text)
            sys.stdout.flush()
            send_telegram(text.encode('utf-8'))
        else:
            firsttext = "🥓 김프 4.5%권 도달!\n현재 김프 : "
            text = firsttext + str(kimp) + "%"
            print(text)
            sys.stdout.flush()
            send_telegram(text.encode('utf-8'))

    if (kimp < 5.5) & (kimp >= 5) & (currentkimp != 5):
        currentkimp = 5
        if burgerp == True:
            firsttext = "🍔 역프 5%권 도달!\n현재 역프 : "
            text = firsttext + str(kimp) + "%"
            print(text)
            sys.stdout.flush()
            send_telegram(text.encode('utf-8'))
        else:
            firsttext = "🥓 김프 5%권 도달!\n현재 김프 : "
            text = firsttext + str(kimp) + "%"
            print(text)
            sys.stdout.flush()
            send_telegram(text.encode('utf-8'))

    if (kimp < 6) & (kimp >= 5.5) & (currentkimp != 5.5):
        currentkimp = 5.5
        if burgerp == True:
            firsttext = "🍔 역프 5.5%권 도달!\n현재 역프 : "
            text = firsttext + str(kimp) + "%"
            print(text)
            sys.stdout.flush()
            send_telegram(text.encode('utf-8'))
        else:
            firsttext = "🥓 김프 5.5%권 도달!\n현재 김프 : "
            text = firsttext + str(kimp) + "%"
            print(text)
            sys.stdout.flush()
            send_telegram(text.encode('utf-8'))

    if (kimp < 6.5) & (kimp >= 6) & (currentkimp != 6):
        currentkimp = 6
        if burgerp == True:
            firsttext = "🍔 역프 6%권 도달!\n현재 역프 : "
            text = firsttext + str(kimp) + "%"
            print(text)
            sys.stdout.flush()
            send_telegram(text.encode('utf-8'))
        else:
            firsttext = "🥓 김프 6%권 도달!\n현재 김프 : "
            text = firsttext + str(kimp) + "%"
            print(text)
            sys.stdout.flush()
            send_telegram(text.encode('utf-8'))

    if (kimp < 7) & (kimp >= 6.5) & (currentkimp != 6.5):
        currentkimp = 6.5
        if burgerp == True:
            firsttext = "🍔 역프 6.5%권 도달!\n현재 역프 : "
            text = firsttext + str(kimp) + "%"
            print(text)
            sys.stdout.flush()
            send_telegram(text.encode('utf-8'))
        else:
            firsttext = "🥓 김프 6.5%권 도달!\n현재 김프 : "
            text = firsttext + str(kimp) + "%"
            print(text)
            sys.stdout.flush()
            send_telegram(text.encode('utf-8'))

    if (kimp < 7.5) & (kimp >= 7) & (currentkimp != 7):
        currentkimp = 7
        if burgerp == True:
            firsttext = "🍔 역프 7%권 도달!\n현재 역프 : "
            text = firsttext + str(kimp) + "%"
            print(text)
            sys.stdout.flush()
            send_telegram(text.encode('utf-8'))
        else:
            firsttext = "🥓 김프 7%권 도달!\n현재 김프 : "
            text = firsttext + str(kimp) + "%"
            print(text)
            sys.stdout.flush()
            send_telegram(text.encode('utf-8'))

    if (kimp < 8) & (kimp >= 7.5) & (currentkimp != 7.5):
        currentkimp = 7.5
        if burgerp == True:
            firsttext = "🍔 역프 7.5%권 도달!\n현재 역프 : "
            text = firsttext + str(kimp) + "%"
            print(text)
            sys.stdout.flush()
            send_telegram(text.encode('utf-8'))
        else:
            firsttext = "🥓 김프 7.5%권 도달!\n현재 김프 : "
            text = firsttext + str(kimp) + "%"
            print(text)
            sys.stdout.flush()
            send_telegram(text.encode('utf-8'))

    if (kimp < 8.5) & (kimp >= 8) & (currentkimp != 8):
        currentkimp = 8
        if burgerp == True:
            firsttext = "🍔 역프 8%권 도달!\n현재 역프 : "
            text = firsttext + str(kimp) + "%"
            print(text)
            sys.stdout.flush()
            send_telegram(text.encode('utf-8'))
        else:
            firsttext = "🥓 김프 8%권 도달!\n현재 김프 : "
            text = firsttext + str(kimp) + "%"
            print(text)
            sys.stdout.flush()
            send_telegram(text.encode('utf-8'))

    if (kimp < 9) & (kimp >= 8.5) & (currentkimp != 8.5):
        currentkimp = 8.5
        if burgerp == True:
            firsttext = "🍔 역프 8.5%권 도달!\n현재 역프 : "
            text = firsttext + str(kimp) + "%"
            print(text)
            sys.stdout.flush()
            send_telegram(text.encode('utf-8'))
        else:
            firsttext = "🥓 김프 8.5%권 도달!\n현재 김프 : "
            text = firsttext + str(kimp) + "%"
            print(text)
            sys.stdout.flush()
            send_telegram(text.encode('utf-8'))

    if (kimp < 9.5) & (kimp >= 9) & (currentkimp != 9):
        currentkimp = 9
        if burgerp == True:
            firsttext = "🍔 역프 9%권 도달!\n현재 역프 : "
            text = firsttext + str(kimp) + "%"
            print(text)
            sys.stdout.flush()
            send_telegram(text.encode('utf-8'))
        else:
            firsttext = "🥓 김프 9%권 도달!\n현재 김프 : "
            text = firsttext + str(kimp) + "%"
            print(text)
            sys.stdout.flush()
            send_telegram(text.encode('utf-8'))

    if (kimp < 10) & (kimp >= 9.5) & (currentkimp != 9.5):
        currentkimp = 9.5
        if burgerp == True:
            firsttext = "🍔 역프 9.5%권 도달!\n현재 역프 : "
            text = firsttext + str(kimp) + "%"
            print(text)
            sys.stdout.flush()
            send_telegram(text.encode('utf-8'))
        else:
            firsttext = "🥓 김프 9.5%권 도달!\n현재 김프 : "
            text = firsttext + str(kimp) + "%"
            print(text)
            sys.stdout.flush()
            send_telegram(text.encode('utf-8'))

    if (kimp >= 10):
        currentkimp = 10
        if burgerp == True:
            firsttext = "🍔 역프 10% 초과!\n현재 역프 : "
            text = firsttext + str(kimp) + "%"
            print(text)
            sys.stdout.flush()
            send_telegram(text.encode('utf-8'))
        else:
            firsttext = "🥓 김프 10% 초과!\n현재 김프 : "
            text = firsttext + str(kimp) + "%"
            print(text)
            sys.stdout.flush()
            send_telegram(text.encode('utf-8'))