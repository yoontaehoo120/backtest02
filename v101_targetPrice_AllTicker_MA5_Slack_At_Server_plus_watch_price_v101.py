# 변동성돌파 + 5일이동평균 전략, 서버실행
# 0시 기준 + 현재가가 5일 이동평균선을 넘는 코인만 매수
#
# 최종업데이트 : 2022 01.03
title = "v101_변동성돌파 + 5일이동평균 전략, (0시기준, 감시가, 목표변동성)"

import time
import datetime
import pyupbit
import requests
import slack
import config


access = config.UPBIT_ACCESS
secret = config.UPBIT_SECRET


# 슬랙 봇 준비
token = config.SLACK_TOKEN
client = slack.WebClient(token=token)

############ 가장 좋은 k값 ##########
best_k = 0.5
watch_k = 0.2

############ N개 자산 값입력 ############
n_number = 6


# 슬랙 봇 메시지함수
def post_message(token, channel, text):
    response = requests.post("https://slack.com/api/chat.postMessage",
                             headers={"Authorization": "Bearer " + token},
                             data={"channel": channel, "text": text}
                             )


def get_target_price(ticker, k=0.5):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    print("today: %s in get_target_price" % today)
    df = pyupbit.get_ohlcv(ticker, interval="minute60",
                           count=24, to=f'{today}' + " 00:00:00")
    high = df['high'].max()
    low = df['low'].min()
    target_price = df.iloc[23]['close'] + (high - low) * k
    return target_price


def get_ma5(ticker):
    """5일 이동 평균선 조회"""
    print("today: %s in get_ma5" % today)
    df = pyupbit.get_ohlcv(ticker, interval="minute60",
                           count=117, to=f'{today}' + " 00:00:00")
    ma5 = df['close'].rolling(117).mean().iloc[-1]
    return ma5

def get_noise(ticker):
    """30일 노이즈 평균값 조회"""
    time.sleep(1)
    print("today: %s in get_noise" % today)
    df = pyupbit.get_ohlcv(ticker, interval="minute240",
                           count=180, to=f'{today}'+" 00:00:00")
    df['noise'] = 1 - abs(df['open'] - df['close']) / (df['high'] - df['low'])
    noise = df['noise'].sum() / 180
    return noise

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]


# 목표변동성 구하기
def get_volatility(ticker):
    print("today: %s in get_volatility" % today)
    df = pyupbit.get_ohlcv(ticker, count=7)
    df['volatility'] = (df['high'].shift(-1) - df['low'].shift(-1)) / df['open'] * 100

    # 5일간의 변동성값 평균
    process_volatility = df['volatility'].iloc[1:6].mean()
    # print(ticker, "5일간의 변동성 평균값 :", process_volatility)
    return process_volatility


def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0


# 로그인
upbit = pyupbit.Upbit(access, secret)

# 0시기준 날짜
now = datetime.datetime.now()
today = now.strftime("%Y%m%d")
print(today)
mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)


# 시작 메세지 슬랙 전송
client.chat_postMessage(channel='#upbit_autotrade', text="전략명: %s\n"
                                                         " - 시작합니다 - today: %s" % (title, today))

decision = ""
while True:

    try:
        ############ ticker 모두 얻어오기 ###############
        tickers = pyupbit.get_tickers(fiat="KRW")

        for ticker in tickers:

            now = datetime.datetime.now()
            today = now.strftime("%Y%m%d")
            target_price = get_target_price(ticker, best_k)
            # 감시가
            watch_price = get_target_price(ticker, watch_k)
            ma5 = get_ma5(ticker)
            noise = get_noise(ticker)
            process_volatility = get_volatility(ticker)

            if mid < now < mid + datetime.timedelta(seconds=10):
                target_price = get_target_price(ticker, best_k)
                mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)

                # 감시가
                watch_price = get_target_price(ticker, watch_k)
                ma5 = get_ma5(ticker)
                noise = get_noise(ticker)
                process_volatility = get_volatility(ticker)
                print("자정 목표가 갱신\n")

            current_price = get_current_price(ticker)

            # ticker 확인
            print("###### %s ########" % ticker)

            # 임시
            print("current_price: ", current_price)
            print("ma5          : ", ma5)
            print("watch_price  : ", watch_price)
            print("target_price : ", target_price)
            print("noise value  : ", noise)

            if current_price >= ma5:
                print("현재가 >= 5일이동평균")
            elif noise <= 0.4:
                print("%s 30일 노이즈 평균값: %0.2f" % (ticker, noise))
            elif current_price >= watch_price:
                print("현재가 >= 감시가")
            elif current_price >= target_price:
                print("현재가 >= 목표가")
            else:
                print("조건 미해당")

            bought = get_balance(ticker[4:])
            if bought > 0:
                print("매수됨\n")


            ################# 감시가격 조건 #################
            elif current_price > ma5 and watch_price <= current_price < target_price:
                print("%s: 감시조건\n"
                      "today         : %s\n"
                      "mid           : %s\n"
                      % (ticker, today, mid))

                # 목표변동성 1%
                target_volatility_1pro = (1 / process_volatility) * 100
                # 목표변동성 2%
                target_volatility_2pro = (2 / process_volatility) * 100

                client.chat_postMessage(channel='#upbit_autotrade',
                                        text="%s감시가:(k값:%0.2f)\n"
                                             " -목표가: %0.2f "
                                             " -현재가: %0.2f\n"
                                             " -감시가: %0.2f\n"
                                             " -노이즈: %0.2f(최적값:0.4이하)\n"
                                             " -5일간의 변동성 평균값: %0.2f\n"
                                             " -목표변동성 2%%: 자산의 %0.2f%% 투자\n"
                                             " -%d개종목대비 투자비율: %d%%\n"
                                             " -목표변동성 1%%: 자산의 %0.2f%% 투자\n"
                                             " -%d개종목대비 투자비율: %d%%\n"
                                             " -today: %s\n"
                                             " -mid time: %s\n"
                                             "전략명: %s\n"
                                             % (ticker, watch_k, target_price,
                                                current_price, watch_price,
                                                noise,
                                                process_volatility,
                                                target_volatility_2pro, n_number,
                                                (target_volatility_2pro / n_number),
                                                target_volatility_1pro, n_number,
                                                (target_volatility_1pro / n_number),
                                                today, mid,
                                                title))


            ################# 목표가 성립조건 #################
            elif target_price < current_price and ma5 < current_price:
                print("%s: 매수\n"
                      "today         : %s\n"
                      "mid           : %s\n"
                      % (ticker, today, mid))

                # 목표변동성 1%
                target_volatility_1pro = (1 / process_volatility) * 100
                # 목표변동성 2%
                target_volatility_2pro = (2 / process_volatility) * 100

                client.chat_postMessage(channel='#upbit_autotrade',
                                        text="%s목표가: buy!(k값:%0.2f)\n"
                                             " -목표가: %0.2f "
                                             " -현재가: %0.2f\n"
                                             " -노이즈: %0.2f(최적값:0.4이하)\n"
                                             " -5일간의 변동성 평균값: %0.2f\n"
                                             " -목표변동성 2%%: 자산의 %0.2f%% 투자\n"
                                             " -%d개종목대비 투자비율: %d%%\n"
                                             " -목표변동성 1%%: 자산의 %0.2f%% 투자\n"
                                             " -%d개종목대비 투자비율: %d%%\n"
                                             " -today: %s\n"
                                             " -mid time: %s\n"
                                             " 전략명: %s\n"
                                             % (ticker, best_k, target_price, current_price,
                                                noise,
                                                process_volatility,
                                                target_volatility_2pro, n_number,
                                                (target_volatility_2pro / n_number),
                                                target_volatility_1pro, n_number,
                                                (target_volatility_1pro / n_number),
                                                today, mid,
                                                title))
            else:
                print("%s: 아직!" % ticker)
                decision = "yet!"

                print("\n")

            time.sleep(1)
        # 한바퀴 돌아, 메세지 슬랙 전송
        client.chat_postMessage(channel='#upbit_autotrade', text="%s\n한바퀴 돌았어요. today: %s" % (title, today))


    except Exception as e:
        print(e)
        time.sleep(1)
