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
        list_NewDf = []  # list_NewDf 는 df의 임시저장소, 전역변수
        if base == "now" or base == "NOW" or base == "Now":  # 시간인자 now 이면 현재시각 기준
            base = datetime.datetime(self.now.year,  # 해당 시간 0분으로 셋팅
                                     self.now.month, self.now.day,
                                     self.now.hour)
            df = pyupbit.get_ohlcv(self.ticker, interval="minute60",
                                   count=count * 24, to=base, period=1)

        else:
            start_date = datetime.datetime(self.now.year,  # 해당 시간 0분으로 셋팅
                                           self.now.month, self.now.day)
            print("in else, start_date", start_date)
            tttt = f'{start_date}'
            print("tttt", tttt)
            df = pyupbit.get_ohlcv(self.ticker, interval="minute60",
                                   count=count * 24, to=f'{start_date}', period=1)

        print("count*24: %d" % (count * 24))  # 임시
        print("df: \n", df)  # 임시
        print("base", base)  # 임시
        df.to_excel("a.xlsx")  # 임시
        df['high'] = df['high'].rolling(24).max()
        df['low'] = df['low'].rolling(24).min()
        df['volume'] = df['volume'].rolling(24).sum()

        df.to_excel("b.xlsx")  # 임시
        count_a = count * 24
        print("count_a = %d" % count_a)  # 임시
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
