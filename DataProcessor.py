import numpy as np
import pandas


# 데이터 전처리 모듈
# 데이터 상태변수
#     1. 시간    2. 1시간-가격상승률   3. 3시간-가격상승률   4. 5시간-가격상승률 5, 10시간-가격상승률

class DataProcessor:

    # Data -> State 변수 처리
    def preProcessor(self, data):
        #price = self.load_data()

        # 시 , 1시간 / 3시간 / 5시간 / 10시간 대비 상승률
        hours = []
        pv1 = []
        pv3 = []
        pv5 = []
        pv10 = []

        for i in range(len(data)):
            hour = i % 24 + 1
            hours.append(hour)

            if i < 10:
                pv10.append(1)
                if i < 5:
                    pv5.append(1)
                    if i < 3:
                        pv3.append(1)
                        if i < 1:
                            pv1.append(1)
                        else:
                            pv1.append(data[i] / data[i - 1])

                    else:
                        pv1.append(data[i] / data[i - 1])
                        pv3.append(data[i] / data[i - 3])

                else:
                    pv1.append(data[i] / data[i - 1])
                    pv3.append(data[i] / data[i - 3])
                    pv5.append(data[i] / data[i - 5])

            else:
                pv1.append(data[i] / data[i - 1])
                pv3.append(data[i] / data[i - 3])
                pv5.append(data[i] / data[i - 5])
                pv10.append(data[i] / data[i - 10])

        MetaData = [hours, pv1, pv3, pv5, pv10]
        return MetaData

    # Data load
    def load_data(self):
        data = pandas.read_csv('SMP.csv', encoding = 'CP949')
        return data


if __name__ == "__main__":
    dp = DataProcessor()
    data = dp.load_data()
    data