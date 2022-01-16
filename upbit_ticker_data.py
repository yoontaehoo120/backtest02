import time
import datetime

import pandas as pd
import pyupbit
import numpy as np
import inspect  # 함수안에서 자기함수 이름 알아내려고


########## 클래스 생성 시작 ##########

class upbit_ticker_data:
    def __init__(self, ticker_name):
        self.ticker = ticker_name
        self.now = datetime.datetime.now()
        self.today = self.now.strftime("%Y%m%d")

    def get_current_price(self):
        """현재가 조회"""
        return pyupbit.get_orderbook(ticker=self.ticker)["orderbook_units"][0]["ask_price"]

    ########## 매수목표 금액 ###############
    def get_target_price_min60(self, k=0.5):
        """변동성 돌파 전략으로 매수 목표가 조회"""
        df = pyupbit.get_ohlcv(self.ticker, interval="minute60",
                               count=24, to=f'{self.today}' + " 00:00:00")

        this_function_name = inspect.stack()[0][3]  # 함수이름 값 얻기
        df.to_excel(this_function_name + ".xlsx", sheet_name=this_function_name)

        high = df['high'].max()
        low = df['low'].min()
        target_price = df.iloc[23]['close'] + (high - low) * k
        return target_price

    ######## 이동평균 시작 ################
    def get_ytday_ma3_60m_00h(self):
        """전일 3일 자정기준 이동 평균선 조회"""
        df = pyupbit.get_ohlcv(self.ticker, interval="minute60",
                               count=72, to=f'{self.today}' + " 00:00:00")

        # 데이터 전처리 시작
        df = df.iloc[[23, 47, 71]]  # 일별 종가 추출
        get_ytday_ma3_60m_00h = df['close'].mean()
        # 데이터 전처리 끝

        this_function_name = inspect.stack()[0][3]  # 함수이름 값 얻기
        df.to_excel(this_function_name + ".xlsx", sheet_name=this_function_name)

        return get_ytday_ma3_60m_00h

    def get_ytday_ma5_60m_00h(self):
        """전일 5일 자정기준 이동 평균선 조회"""
        df = pyupbit.get_ohlcv(self.ticker, interval="minute60",
                               count=120, to=f'{self.today}' + " 00:00:00")

        # 데이터 전처리 시작
        df = df.iloc[[23, (23 + 24), (23 + 24 + 24),
                      (23 + 24 + 24 + 24), (23 + 24 + 24 + 24 + 24)]]  # 일별 종가 추출
        get_ytday_ma5_60m_00h = df['close'].mean()
        # 데이터 전처리 끝

        this_function_name = inspect.stack()[0][3]  # 함수이름 값 얻기
        df.to_excel(this_function_name + ".xlsx", sheet_name=this_function_name)
        return get_ytday_ma5_60m_00h

    def get_ytday_ma10_240m_00h(self):
        """전일 10일 자정기준 이동 평균선 조회"""
        df = pyupbit.get_ohlcv(self.ticker, interval="minute240",
                               count=60, to=f'{self.today}' + " 00:00:00")

        # 데이터 전처리 시작
        df = df.iloc[[4,
                      (4 + 6),
                      (4 + 6 + 6),
                      (4 + 6 + 6 + 6),
                      (4 + 6 + 6 + 6 + 6),
                      (4 + 6 + 6 + 6 + 6 + 6),
                      (4 + 6 + 6 + 6 + 6 + 6 + 6),
                      (4 + 6 + 6 + 6 + 6 + 6 + 6 + 6),
                      (4 + 6 + 6 + 6 + 6 + 6 + 6 + 6 + 6),
                      (4 + 6 + 6 + 6 + 6 + 6 + 6 + 6 + 6 + 6)
                      ]]  # 일별 종가 추출
        get_ytday_ma10_60m_00h = df['close'].mean()
        # 데이터 전처리 끝

        this_function_name = inspect.stack()[0][3]  # 함수이름 값 얻기
        df.to_excel(this_function_name + ".xlsx", sheet_name=this_function_name)
        return get_ytday_ma10_60m_00h

    def get_ytday_ma20_240m_00h(self):
        """전일 20일 자정기준 이동 평균선 조회"""
        df = pyupbit.get_ohlcv(self.ticker, interval="minute240",
                               count=120, to=f'{self.today}' + " 00:00:00")

        # 데이터 전처리 시작
        df = df.iloc[[5,
                      (5 + 6),
                      (5 + 6 + 6),
                      (5 + 6 + 6 + 6),
                      (5 + 6 + 6 + 6 + 6),
                      (5 + 6 + 6 + 6 + 6 + 6),
                      (5 + 6 + 6 + 6 + 6 + 6 + 6),  # 7일
                      (5 + 6 + 6 + 6 + 6 + 6 + 6 + 6),  # 8일
                      (5 + 6 + 6 + 6 + 6 + 6 + 6 + 6 + 6),  # 9일
                      (5 + 6 + 6 + 6 + 6 + 6 + 6 + 6 + 6 + 6),  # 10일
                      (5 + (6 * 10)),  # 11일
                      (5 + (6 * 11)),  # 12일
                      (5 + (6 * 12)),  # 13일
                      (5 + (6 * 13)),  # 14일
                      (5 + (6 * 14)),  # 15일
                      (5 + (6 * 15)),  # 16일
                      (5 + (6 * 16)),  # 17일
                      (5 + (6 * 17)),  # 18일
                      (5 + (6 * 18)),  # 19일
                      (5 + (6 * 19))  # 20일
                      ]]  # 일별 종가 추출
        get_ytday_ma20_60m_00h = df['close'].mean()
        # 데이터 전처리 끝

        this_function_name = inspect.stack()[0][3]  # 함수이름 값 얻기
        df.to_excel(this_function_name + ".xlsx", sheet_name=this_function_name)
        return get_ytday_ma20_60m_00h

    # def get_ytday_ma5_standard(self):
    #     """전일 5일 09시기준 이동 평균선 조회"""
    #     df = pyupbit.get_ohlcv(self.ticker, interval="day", count=15)
    #     get_ytday_ma5_standard = df['close'].rolling(4).mean().iloc[-1]
    #
    #     this_function_name = inspect.stack()[0][3]  # 함수이름 값 얻기
    #     df.to_excel(this_function_name + ".xlsx", sheet_name=this_function_name)
    #     return get_ytday_ma5_standard

    ############ 이동평균 끝 #################

    ############ 노이즈 시작 #####################
    def get_noise_20day(self):
        """20일 노이즈 평균값 조회"""
        df = pyupbit.get_ohlcv(self.ticker, interval="minute240",
                               count=120, to=f'{self.today}' + " 00:00:00")

        # 데이터 전처리 시작
        """ 일별로 고가, 저가 추출"""
        df['high_1d'] = df['high'].rolling(6).max()
        df['low_1d'] = df['low'].rolling(6).min()
        df = df.iloc[[5,
                      (5 + 6),
                      (5 + 6 + 6),
                      (5 + 6 + 6 + 6),
                      (5 + 6 + 6 + 6 + 6),
                      (5 + 6 + 6 + 6 + 6 + 6),
                      (5 + 6 + 6 + 6 + 6 + 6 + 6),  # 7일
                      (5 + 6 + 6 + 6 + 6 + 6 + 6 + 6),  # 8일
                      (5 + 6 + 6 + 6 + 6 + 6 + 6 + 6 + 6),  # 9일
                      (5 + 6 + 6 + 6 + 6 + 6 + 6 + 6 + 6 + 6),  # 10일
                      (5 + (6 * 10)),  # 11일
                      (5 + (6 * 11)),  # 12일
                      (5 + (6 * 12)),  # 13일
                      (5 + (6 * 13)),  # 14일
                      (5 + (6 * 14)),  # 15일
                      (5 + (6 * 15)),  # 16일
                      (5 + (6 * 16)),  # 17일
                      (5 + (6 * 17)),  # 18일
                      (5 + (6 * 18)),  # 19일
                      (5 + (6 * 19))  # 20일
                      ]]  # 일별
        # 데이터 전처리 끝

        df['noise'] = 1 - abs(df['open'] - df['close']) / (df['high_1d'] - df['low_1d'])

        this_function_name = inspect.stack()[0][3]  # 함수이름 값 얻기
        df.to_excel(this_function_name + ".xlsx", sheet_name=this_function_name)

        noise_20day = df['noise'].rolling(20).mean().iloc[-1]
        return noise_20day

    def get_noise_30day(self):
        """30일 노이즈 평균값 조회"""
        df = pyupbit.get_ohlcv(self.ticker, interval="minute240",
                               count=180, to=f'{self.today}' + " 00:00:00")

        # 데이터 전처리 시작
        """ 일별로 고가, 저가 추출"""
        df['high_1d'] = df['high'].rolling(6).max()
        df['low_1d'] = df['low'].rolling(6).min()
        df = df.iloc[[5,
                      (5 + 6),
                      (5 + 6 + 6),
                      (5 + 6 + 6 + 6),
                      (5 + 6 + 6 + 6 + 6),
                      (5 + 6 + 6 + 6 + 6 + 6),
                      (5 + 6 + 6 + 6 + 6 + 6 + 6),  # 7일
                      (5 + 6 + 6 + 6 + 6 + 6 + 6 + 6),  # 8일
                      (5 + 6 + 6 + 6 + 6 + 6 + 6 + 6 + 6),  # 9일
                      (5 + 6 + 6 + 6 + 6 + 6 + 6 + 6 + 6 + 6),  # 10일
                      (5 + (6 * 10)),  # 11일
                      (5 + (6 * 11)),  # 12일
                      (5 + (6 * 12)),  # 13일
                      (5 + (6 * 13)),  # 14일
                      (5 + (6 * 14)),  # 15일
                      (5 + (6 * 15)),  # 16일
                      (5 + (6 * 16)),  # 17일
                      (5 + (6 * 17)),  # 18일
                      (5 + (6 * 18)),  # 19일
                      (5 + (6 * 19)),  # 20일
                      (5 + (6 * 20)),
                      (5 + (6 * 21)),
                      (5 + (6 * 22)),
                      (5 + (6 * 23)),
                      (5 + (6 * 24)),
                      (5 + (6 * 25)),
                      (5 + (6 * 26)),
                      (5 + (6 * 27)),
                      (5 + (6 * 28)),
                      (5 + (6 * 29))  # 30일
                      ]]  # 일별
        # 데이터 전처리 끝

        df['noise'] = 1 - abs(df['open'] - df['close']) / (df['high_1d'] - df['low_1d'])

        this_function_name = inspect.stack()[0][3]  # 함수이름 값 얻기
        df.to_excel(this_function_name + ".xlsx", sheet_name=this_function_name)

        noise_30day = df['noise'].rolling(30).mean().iloc[-1]
        return noise_30day

    ############ 노이즈 끝 #####################

    def get_volatility_5days(self):
        """ 전일 5일 목표변동성 구하기 """
        df = pyupbit.get_ohlcv(self.ticker, interval="minute60",
                               count=120, to=f'{self.today}' + " 00:00:00")
        # 데이터 전처리 시작
        """ 일별로 고가, 저가 추출"""
        df['high_1d'] = df['high'].rolling(24).max()
        df['low_1d'] = df['low'].rolling(24).min()

        df = df.iloc[[23,
                      (23 + 24),
                      (23 + 24 + 24),
                      (23 + 24 + 24 + 24),
                      (23 + 24 + 24 + 24 + 24),  # 일별 종가 추출
                      ]]
        # 데이터 전처리 끝

        df['volatility'] = (df['high_1d'] - df['low_1d']) / df['open'] * 100

        this_function_name = inspect.stack()[0][3]  # 함수이름 얻기
        df.to_excel(this_function_name + ".xlsx", sheet_name=this_function_name)

        # 5일간의 변동성값 평균
        volatility_5days = df['volatility'].mean()
        return volatility_5days

    def ohlcv_base_is_now(self, count=1, base="00:00:00"):
        """60분봉으로 1일 ohlcv 구하기,
         데이터 전처리, 요청일이 8일 이상이면 8일씩 잘라서 가공 및 합치기 """
        list_NewDf = []  # list_NewDf 는 df의 임시저장소, 전역변수
        if count <= 8:
            if base == "now" or base == "NOW" or base == "Now":  # 시간인자 now 이면 현재시각 기준
                base = datetime.datetime(self.now.year,  # 해당 시간 0분으로 셋팅
                                         self.now.month, self.now.day,
                                         self.now.hour)
                df = pyupbit.get_ohlcv(self.ticker, interval="minute60",
                                       count=count * 24, to=base)


            else:
                start_date = datetime.datetime(self.now.year,  # 해당 시간 0분으로 셋팅
                                               self.now.month, self.now.day)
                df = pyupbit.get_ohlcv(self.ticker, interval="minute60",
                                       count=count * 24, to=f'{start_date}' + " " + base)

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

        else:  # 기간이 9일 이상일때
            print("기간      : %d 일" % count)
            print("60분 몇개  : %d" % (count * 24))

            if base == "now" or base == "NOW" or base == "Now":  # 시간인자 now 이면 현재시각 기준
                base = datetime.datetime(self.now.year, self.now.month, self.now.day, self.now.hour)
                base = base.strftime('%H:%M:%S')  # ex) 16:00:00
                print("9일이상 now: ", base)  # 임시
            else:
                base = datetime.datetime(self.now.year, self.now.month, self.now.day)
                base = base.strftime('%H:%M:%S')
                print("9일이상 Not now: ", base)  # 임시

            count_divide_8 = count // 8  # 8을 나눈 몫, 8일씩 잘라서, 200개 갯수제한, 8일이면 60분본 기준으로 192개 나옴
            print("count_divide_8 = ", count_divide_8)
            count_percent_8 = count % 8  # 나눈 나머지 값,   10일기준 1번 서버요청
            print("count_percent_8 = ", count_percent_8)
            start_date = self.now - datetime.timedelta(count)  # 시작날짜
            start_date = datetime.datetime(start_date.year,
                                           start_date.month, start_date.day)
            print("start_date at out of base:", start_date)

            df_list = []  # df들을 저장할 리스트 변수
            for i in range(1, count_divide_8 + 1, 1):  # 첫번째 수행, 몫 값에 따라
                print("i = %d" % i)
                print("count_divide_8: ", count_divide_8)
                to_date_before = start_date + datetime.timedelta(i * 8)  # 시작날에서 i값이 증가할때 마다 8일씩 더하기
                to_date = to_date_before.strftime("%Y%m%d")  # 예)날짜를 20220120 포맷으로 변환
                print("to_date 값: ", to_date)
                print("base", base)
                df = pyupbit.get_ohlcv(self.ticker, interval="minute60",
                                       count=190, to=f'{to_date}' + " " + base)
                df_list.append(df)  # df 들 리스트에 담기
                time.sleep(0.2)
            print(df_list)
            df_1st_total = pd.concat(df_list)
            print("df 합친후 \n")
            print(df_1st_total)
            df_1st_total.to_excel("c.xlsx")

            # 8일 이하 ohlcv 서버요청
            to_date_before = self.now
            to_date = to_date_before.strftime("%Y%m%d")  # 예)날짜를 20220120 포맷으로 변환
            print("df_2nd base = ", base)
            print("df_2nd to_date = ", to_date)
            df_2nd = pyupbit.get_ohlcv(self.ticker,
                                       interval="minute60",
                                       count=count_percent_8 * 24,
                                       to=f'{to_date}' + " " + base)  # count 값에서 +1은 두개의 df 사이에 한시간이 빠져서, 넣었다.
            print("8일 이후 내에서 count_percent_8: ", df_2nd)
            df_2nd.to_excel("d.xlsx")

            df_all = pd.concat([df_1st_total, df_2nd])
            print(df_all)  # 임시
            df_all.to_excel("result.xlsx")
            return df_all

    def get_ror_200days_00h(self, k=0.5):
        """ 09시 일봉기준 기간 200일"""
        df = pyupbit.get_ohlcv(self.ticker)

        # 레인지 계산하기
        df['range'] = (df['high'] - df['low']) * k

        # 목표가 계산하기
        df['target'] = df['open'] + df['range'].shift(1)

        fee = 0.0032
        # 매수, 매도 그리고 수익률
        df['ror'] = np.where(df['high'] > df['target'],
                             df['close'] / df['target'] - fee,
                             1)

        # 누적 수익률 계산
        ror = df['ror'].cumprod()[-2]
        return ror


########### 클래스 생성  끝 ##########

coin = upbit_ticker_data("KRW-OMG")
df = coin.ohlcv_base_is_now(count=8)
