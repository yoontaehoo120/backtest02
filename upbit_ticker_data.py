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

        # this_function_name = inspect.stack()[0][3]  # 함수이름 값 얻기
        # df.to_excel(this_function_name + ".xlsx", sheet_name=this_function_name)

        high = df['high'].max()
        low = df['low'].min()
        target_price = df.iloc[23]['close'] + (high - low) * k
        return target_price

    def get_target_price_min60_now(self, k=0.5):
        """변동성 돌파 전략으로 매수 목표가 조회"""
        to_datetime = datetime.datetime(self.now.year,  # 해당 시간 0분으로 셋팅
                                        self.now.month, self.now.day,
                                        self.now.hour)
        df = pyupbit.get_ohlcv(self.ticker, interval="minute60",
                               count=24, to=to_datetime)

        # this_function_name = inspect.stack()[0][3]  # 함수이름 값 얻기
        # df.to_excel(this_function_name + ".xlsx", sheet_name=this_function_name)

        high = df['high'].max()
        low = df['low'].min()
        target_price = df.iloc[23]['close'] + (high - low) * k
        return target_price

    ######## 이동평균 시작 ################
    def get_ytday_ma3_60m_00h(self):
        """전일 3일 자정기준 이동 평균선 조회"""
        df = pyupbit.get_ohlcv(self.ticker, interval="minute60",
                               count=72, to=f'{self.today}' + " 00:00:00")

        if len(df) >= 72:
            # 데이터 전처리 시작
            df = df.iloc[[23, 47, 71]]  # 일별 종가 추출
            get_ytday_ma3_60m_00h = df['close'].mean()
            # 데이터 전처리 끝
        else:
            this_function_name = inspect.stack()[0][3]  # 함수이름 값 얻기
            # df.to_excel(this_function_name + ".xlsx", sheet_name=this_function_name)
            get_ytday_ma3_60m_00h = 0
            this_function_name = inspect.stack()[0][3]  # 함수이름 값 얻기
            print("%s, %s 신규코인 데이터 부족" % (this_function_name, self.ticker))
        return get_ytday_ma3_60m_00h

    def get_ytday_ma5_60m_00h(self):
        """전일 5일 자정기준 이동 평균선 조회"""
        df = pyupbit.get_ohlcv(self.ticker, interval="minute60",
                               count=120, to=f'{self.today}' + " 00:00:00")

        """ 신규 코인 조건, 데이타 불충분으로 에러"""
        if len(df) >= 120:
            # 데이터 전처리 시작
            df = df.iloc[[23, (23 + 24), (23 + 24 + 24),
                          (23 + 24 + 24 + 24), (23 + 24 + 24 + 24 + 24)]]  # 일별 종가 추출
            get_ytday_ma5_60m_00h = df['close'].mean()
            # 데이터 전처리 끝

            this_function_name = inspect.stack()[0][3]  # 함수이름 값 얻기
            df.to_excel(this_function_name + ".xlsx", sheet_name=this_function_name)
        else:
            get_ytday_ma5_60m_00h = 0
            this_function_name = inspect.stack()[0][3]  # 함수이름 값 얻기
            print("%s, %s 신규코인 데이터 부족" % (this_function_name, self.ticker))
        return get_ytday_ma5_60m_00h

    def get_ytday_ma5_60m_now(self):
        """전일 5일 자정기준 이동 평균선 조회"""
        to_datetime = datetime.datetime(self.now.year,  # 해당 시간 0분으로 셋팅
                                        self.now.month, self.now.day,
                                        self.now.hour)
        df = pyupbit.get_ohlcv(self.ticker, interval="minute60",
                               count=120, to=to_datetime)

        if len(df) >= 120:
            # 데이터 전처리 시작
            df = df.iloc[[23, (23 + 24), (23 + 24 + 24),
                          (23 + 24 + 24 + 24), (23 + 24 + 24 + 24 + 24)]]  # 일별 종가 추출
            get_ytday_ma5_60m_00h = df['close'].mean()
            # 데이터 전처리 끝


        else:
            get_ytday_ma5_60m_00h = 0
            this_function_name = inspect.stack()[0][3]  # 함수이름 값 얻기
            # df.to_excel(this_function_name + ".xlsx", sheet_name=this_function_name)
            print("%s, %s 신규코인 데이터 부족" % (this_function_name, self.ticker))

        return get_ytday_ma5_60m_00h

    def get_ytday_ma10_240m_00h(self):
        """전일 10일 자정기준 이동 평균선 조회"""
        df = pyupbit.get_ohlcv(self.ticker, interval="minute240",
                               count=60, to=f'{self.today}' + " 00:00:00")
        if len(df) >= 60:
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
        else:
            this_function_name = inspect.stack()[0][3]  # 함수이름 값 얻기
            # df.to_excel(this_function_name + ".xlsx", sheet_name=this_function_name)
            get_ytday_ma10_60m_00h = 0
            print("%s, %s 신규코인 데이터 부족" % (this_function_name, self.ticker))
        return get_ytday_ma10_60m_00h

    def get_ytday_ma20_240m_00h(self):
        """전일 20일 자정기준 이동 평균선 조회"""
        df = pyupbit.get_ohlcv(self.ticker, interval="minute240",
                               count=120, to=f'{self.today}' + " 00:00:00")

        if len(df) >= 120:
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
        else:
            this_function_name = inspect.stack()[0][3]  # 함수이름 값 얻기
            # df.to_excel(this_function_name + ".xlsx", sheet_name=this_function_name)
            get_ytday_ma20_60m_00h = 0
            print("%s, %s 신규코인 데이터 부족" % (this_function_name, self.ticker))
        return get_ytday_ma20_60m_00h

    ############ 이동평균 끝 #################

    ############ 노이즈 시작 #####################
    def get_noise_20day(self):
        """20일 노이즈 평균값 조회"""
        df = pyupbit.get_ohlcv(self.ticker, interval="minute240",
                               count=120, to=f'{self.today}' + " 00:00:00")
        if len(df) >= 120:
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
            noise_20day = df['noise'].rolling(20).mean().iloc[-1]
        else:
            this_function_name = inspect.stack()[0][3]  # 함수이름 값 얻기
            # df.to_excel(this_function_name + ".xlsx", sheet_name=this_function_name)
            noise_20day = 0
            print("%s, %s 신규코인 데이터 부족" % (this_function_name, self.ticker))

        return noise_20day

    def get_noise_30day(self):
        """30일 노이즈 평균값 조회"""
        df = pyupbit.get_ohlcv(self.ticker, interval="minute240",
                               count=180, to=f'{self.today}' + " 00:00:00")

        if len(df) >= 180:
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
            noise_30day = df['noise'].rolling(30).mean().iloc[-1]
        else:
            this_function_name = inspect.stack()[0][3]  # 함수이름 값 얻기
            # df.to_excel(this_function_name + ".xlsx", sheet_name=this_function_name)
            noise_30day = 0
            print("%s: %s 신규코인 데이터 부족!!!" % (this_function_name, self.ticker))
        return noise_30day

    def get_noise_30day_now(self):
        """30일 노이즈 평균값 조회"""
        to_datetime = datetime.datetime(self.now.year,  # 해당 시간 0분으로 셋팅
                                        self.now.month, self.now.day,
                                        self.now.hour)
        df = pyupbit.get_ohlcv(self.ticker, interval="minute240",
                               count=180, to=to_datetime)

        if len(df) >= 180:
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
            noise_30day = df['noise'].rolling(30).mean().iloc[-1]
        else:
            this_function_name = inspect.stack()[0][3]  # 함수이름 값 얻기
            # df.to_excel(this_function_name + ".xlsx", sheet_name=this_function_name)
            noise_30day = 0
            print("%s, %s 신규코인 데이터 부족" % (this_function_name, self.ticker))

        return noise_30day

    ############ 노이즈 끝 #####################

    def get_volatility_5days(self):
        """ 전일 5일 목표변동성 구하기 """
        df = pyupbit.get_ohlcv(self.ticker, interval="minute60",
                               count=120, to=f'{self.today}' + " 00:00:00")

        if len(df) >= 120:
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



            # 5일간의 변동성값 평균
            volatility_5days = df['volatility'].mean()
        else:
            this_function_name = inspect.stack()[0][3]  # 함수이름 얻기
            # df.to_excel(this_function_name + ".xlsx", sheet_name=this_function_name)
            volatility_5days = 0
            print("%s, %s 신규코인 데이터 부족" % (this_function_name, self.ticker))
        return volatility_5days

    def get_volatility_5days_now(self):
        """ 전일 5일 목표변동성 구하기 """
        to_datetime = datetime.datetime(self.now.year,  # 해당 시간 0분으로 셋팅
                                        self.now.month, self.now.day,
                                        self.now.hour)
        df = pyupbit.get_ohlcv(self.ticker, interval="minute60",
                               count=120, to=to_datetime)

        if len(df) >= 120:
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

            # 5일간의 변동성값 평균
            volatility_5days = df['volatility'].mean()

        else:
            this_function_name = inspect.stack()[0][3]  # 함수이름 얻기
            # df.to_excel(this_function_name + ".xlsx", sheet_name=this_function_name)
            volatility_5days = 0
            print("%s, %s 신규코인 데이터 부족" % (this_function_name, self.ticker))

        return volatility_5days

    def ohlcv_base_is_now(self, count=1, base="00:00:00"):
        """60분봉으로 1일 ohlcv 구하기,
         데이터 전처리, 요청일이 8일 이상이면 8일씩 잘라서 가공 및 합치기 """
        global df
        df_list = []
        list_NewDf = []  # list_NewDf 는 df의 임시저장소, 전역변수
        time_shift_flag = False
        print("count       : %d" % count)
        print("count * 24  : %d" % (count * 24))
        # print("self.now.hour: ", self.now.hour)

        if base[3:] == "00:00":  # base 값을 시간지정 할 경우 현재 시간 오버되면 하루 전으로 count 값 변경
            input_hour = int(base[0:2])
            if input_hour > self.now.hour:
                time_shift_flag = True
                # print("time_shift_flag: True")

        if base == "now" or base == "NOW" or base == "Now":  # 시간인자 now 이면 현재시각 기준
            end_datetime = datetime.datetime(self.now.year,  # 해당 시간 0분으로 셋팅
                                             self.now.month, self.now.day,
                                             self.now.hour)
            if time_shift_flag:
                end_datetime = end_datetime - datetime.timedelta(1)
                # print("time_flag = True, end_datetime: ", end_datetime)
            start_datetime = end_datetime - datetime.timedelta(count)  # 시작일자 설정
            print("start_datetime in now", start_datetime)
            print("end_datetime in now", end_datetime)

            for i in range(count - 1, -1, -1):
                # print("\ni = %d" % i)
                to_datetime = end_datetime - datetime.timedelta(i)
                # print("to_datime: ", to_datetime)
                df = pyupbit.get_ohlcv(self.ticker, interval="minute60",
                                       count=24, to=to_datetime)

                df_list.append(df)
                # df_list[count_a] =
                if i % 28 == 0:
                    now = datetime.datetime.today().strftime("%H시%M분%S초")
                    print("28회 요청시 마다 0.2초 sleep: ", now)
                time.sleep(0.2)
        else:

            end_datetime = datetime.datetime(self.now.year,  # 해당 시간 0분으로 셋팅
                                             self.now.month, self.now.day,
                                             self.now.hour)

            if time_shift_flag:
                end_datetime = end_datetime - datetime.timedelta(1)
                # print("time_flag = True, end_datetime: ", end_datetime)

            start_datetime = end_datetime - datetime.timedelta(count)
            print("start_datetime in Not now", start_datetime.strftime("%Y%m%d"))
            print("end_datetime in Not now", end_datetime)
            for i in range(count - 1, -1, -1):
                # print("\ni = %d" % i)
                to_datetime = end_datetime - datetime.timedelta(i)
                to_datetime = to_datetime.strftime("%Y%m%d")  # 예)날짜를 20220120 포맷으로 변환
                # print("to_datetime: ", to_datetime)
                df = pyupbit.get_ohlcv(self.ticker, interval="minute60",
                                       count=24, to=f'{to_datetime}' + " " + base)

                df_list.append(df)
                if i % 28 == 0:
                    now = datetime.datetime.today().strftime("%H시%M분%S초")
                    print("28회 요청시 마다 0.2초 sleep: ", now)
                time.sleep(0.2)

        df_total = pd.concat(df_list)
        print(df_total)
        df_total.to_excel("a.xlsx")  # 임시
        df_total['high'] = df_total['high'].rolling(24).max()
        df_total['low'] = df_total['low'].rolling(24).min()
        df_total['volume'] = df_total['volume'].rolling(24).sum()
        # df_total.to_excel("b.xlsx")  # 임시

        count_a = count * 24

        for i in range(0, count_a, 24):
            i_delta = i + 23
            # print("i = %d" % i)  # 임시
            # print("i_delta = %d" % i_delta)  # 임시

            df_total.iloc[i]['high'] = df_total.iloc[i_delta]['high']
            df_total.iloc[i]['low'] = df_total.iloc[i_delta]['low']
            df_total.iloc[i]['close'] = df_total.iloc[i_delta]['close']
            df_total.iloc[i]['volume'] = df_total.iloc[i_delta]['volume']
            df_total.iloc[i]['value'] = df_total.iloc[i_delta]['value']

            list_NewDf.append(i)  # 최종 행 위치 생성

        # print("list_NewDf: ", list_NewDf)  # 임시
        df_total = df_total.iloc[list_NewDf]
        # print(self.ticker, "\n", df_total)  # 임시
        # df_total.to_excel("c.xlsx")  # 임시
        return df_total

    def get_ror_days_00h(self, count, k=0.5):
        """ 00시 일봉기준 기간 200일"""
        df = self.ohlcv_base_is_now(count=count)

        # 레인지 계산하기
        df['range'] = (df['high'] - df['low']) * k

        # 목표가 계산하기
        df['target'] = df['open'] + df['range'].shift(1)

        fee = 0.0032
        # 매수, 매도 그리고 수익률
        df['ror'] = np.where(df['high'] > df['target'],
                             df['close'] / df['target'] - fee,
                             1)

        # # 엑셀저장
        now = datetime.datetime.today().strftime("%Y년%m월%d일_%H시")  # 현재시간 얻기
        this_function_name = inspect.stack()[0][3]  # 함수이름 값 얻기
        df.to_excel(this_function_name + f'{now}' + ".xlsx",
                    sheet_name=this_function_name)

        # 누적 수익률 계산
        ror = df['ror'].cumprod()[-2]
        return ror

    def get_ror_200days_00h(self, k=0.5):
        """ 00시 일봉기준 기간 200일"""
        df = self.ohlcv_base_is_now(count=200)

        # 레인지 계산하기
        df['range'] = (df['high'] - df['low']) * k

        # 목표가 계산하기
        df['target'] = df['open'] + df['range'].shift(1)

        fee = 0.0032
        # 매수, 매도 그리고 수익률
        df['ror'] = np.where(df['high'] > df['target'],
                             df['close'] / df['target'] - fee,
                             1)

        # # 엑셀저장
        # now = datetime.datetime.today().strftime("%Y년%m월%d일_%H시")  # 현재시간 얻기
        # this_function_name = inspect.stack()[0][3]  # 함수이름 값 얻기
        # df.to_excel(this_function_name + f'{now}' + ".xlsx",
        #             sheet_name=this_function_name)

        # 누적 수익률 계산
        ror = df['ror'].cumprod()[-2]
        return ror

########### 클래스 생성  끝 ##########,
