import time
import datetime

import pandas as pd
import pyupbit
import numpy as np
import inspect  # 함수안에서 자기함수 이름 알아내려고


class upbit_ticker_data:
    def __init__(self, ticker_name):
        self.ticker = ticker_name
        self.now = datetime.datetime.now()
        self.today = self.now.strftime("%Y%m%d")

    def ohlcv_base_is_now(self, count=1, base="00:00:00"):
        """60분봉으로 1일 ohlcv 구하기,
         데이터 전처리, 요청일이 8일 이상이면 8일씩 잘라서 가공 및 합치기 """
        global df
        df_list = []
        list_NewDf = []  # list_NewDf 는 df의 임시저장소, 전역변수
        print("count: %d" % count)
        if base == "now" or base == "NOW" or base == "Now":  # 시간인자 now 이면 현재시각 기준
            end_datetime = datetime.datetime(self.now.year,  # 해당 시간 0분으로 셋팅
                                             self.now.month, self.now.day,
                                             self.now.hour)
            start_datetime = end_datetime - datetime.timedelta(count)  # 시작일자 설정
            print("start_datetime", start_datetime)
            print("end_datetime", end_datetime)

            for i in range(count, 0, -1):
                print("\ni = %d" % i)
                to_datetime = end_datetime - datetime.timedelta(i)
                print("to_datime: ", to_datetime)
                df = pyupbit.get_ohlcv(self.ticker, interval="minute60",
                                       count=24, to=to_datetime)

                df_list.append(df)
                time.sleep(0.1)

        else:

            end_datetime = datetime.datetime(self.now.year,  # 해당 시간 0분으로 셋팅
                                             self.now.month, self.now.day,
                                             self.now.hour)
            start_datetime = end_datetime - datetime.timedelta(count)
            print("start_datetime", start_datetime)
            print("end_datetime", end_datetime)
            for i in range(count, 0, -1):
                print("\ni = %d" % i)
                to_datetime = end_datetime - datetime.timedelta(i)
                to_datetime = to_datetime.strftime("%Y%m%d")  # 예)날짜를 20220120 포맷으로 변환
                print("to_datime: ", to_datetime)
                df = pyupbit.get_ohlcv(self.ticker, interval="minute60",
                                       count=24, to=f'{to_datetime}' + " " + base)

                df_list.append(df)
                time.sleep(0.1)

        df_total = pd.concat(df_list)
        print(df_total)
        df_total.to_excel("a.xlsx")  # 임시
        df_total['high'] = df_total['high'].rolling(24).max()
        df_total['low'] = df_total['low'].rolling(24).min()
        df_total['volume'] = df_total['volume'].rolling(24).sum()

        df_total.to_excel("b.xlsx")  # 임시
        for i in range(0, count_a, 24):
            i_delta = i + 23
            print("i = %d" % i)  # 임시
            print("i_delta = %d" % i_delta)  # 임시

            df.iloc[i]['high'] = df.iloc[i_delta]['high']
            df.iloc[i]['low'] = df.iloc[i_delta]['low']
            df.iloc[i]['close'] = df.iloc[i_delta]['close']
            df.iloc[i]['volume'] = df.iloc[i_delta]['volume']
            df.iloc[i]['value'] = df.iloc[i_delta]['value']

            list_NewDf.append(i)  # 최종 행 위치 생성

        print(list_NewDf)  # 임시
        df = df.iloc[list_NewDf]
        print(self.ticker, "\n", df)  # 임시
        df.to_excel("c.xlsx")  # 임시
        return df


########### 클래스 생성  끝 ##########

coin = upbit_ticker_data("KRW-ETH")
df = coin.ohlcv_base_is_now(count=20)
