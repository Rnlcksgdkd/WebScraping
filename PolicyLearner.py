import numpy as np
import os
import locale
import logging

from keras.models import Sequential
from keras.layers import Activation, LSTM, Dense, BatchNormalization
from keras.optimizers import sgd
from Environment import Environment
from Agent import Agent
from PolicyNetwork import PolicyNetwork
from Visualizer import Visualizer


logger = logging.getLogger(__name__)
locale.setlocale(locale.LC_ALL, 'ko_KR.UTF-8')


# 데이터 를 받아 실제 네트워크를 학습시키는 모듈

class PolicyLearner:

    def __init__(self, training_data=None , lr=0.01):

       # Env , Agent , Vis
        self.environment = Environment()
        self.agent = Agent(self.environment)
        self.visualizer = Visualizer()

       # 학습 데이터 세팅
        self.training_data = self.environment.price_data  # 학습 데이터
        self.sample = None
        self.training_data_idx = -1


        # 탐험 파라미터
        self.start_epsilon = 1
        self.epsilon = 1
        self.rate_progress = 0

        # 정책 신경망; 입력 크기 = 학습 데이터의 크기 + 에이전트 상태 크기
        self.num_features = self.environment.State_data.__len__() + self.agent.STATE_DIM
        self.policy_network = PolicyNetwork(
            input_dim=self.num_features, output_dim=self.agent.NUM_ACTIONS, lr=lr)

        # 학습/시각화 메모리
        self.PRICE = []
        self.SAMPLE = []
        self.ACTION = []
        self.IM_REWARD = []
        self.DE_REWARD = []
        self.SOC = []
        self.PV = []
        self.MEMORY = []

    def reset(self):
        self.sample = None
        self.training_data_idx = -1

    # 실제 학습에 이용되는 함수
    def fit(
            self, num_epoches=1000, max_memory=60, balance=10000000,
            discount_factor=0 , learning=True):

        # 에이전트 초기 자본금 설정
        #self.agent.set_balance(balance)

        # 학습에 대한 정보 초기화
        # max_portfolio_value = 0
        # epoch_win_cnt = 0



        # 학습 부분
        for epoch in range(3):

            ## 1. 매 epoch 마다 초기화

            print("epoch ", epoch)

            # 현재 진행률
            self.rate_progress = epoch / num_epoches

            # epoch 마다 탐험 비율 감소
            if learning:
                self.epsilon = self.start_epsilon * (1. - float(epoch) / (num_epoches - 1))
            else:
                self.epsilon = 0

            # epoch 마다 학습 정보 출력

            # 에포크 관련 정보 초기화
            idx = 0
            loss = 0.
            itr_cnt = 0
            win_cnt = 0
            exploration_cnt = 0
            batch_size = 0
            pos_learning_cnt = 0
            neg_learning_cnt = 0

           # self.visualizer.plot(self.PRICE , self.ACTION ,self.SOC, self.PV , self.DE_REWARD)
           # self.visualizer.plot(self.PRICE , self.ACTION ,self.SOC, self.PV , self.DE_REWARD)

            # 1-epoch 진행에 따라 저장 메모리
            self.PRICE = []
            self.SAMPLE = []
            self.ACTION = []
            self.IM_REWARD = []
            self.DE_REWARD = []
            self.SOC = []
            self.PV = []

            # 학습에 이용될 batch 저장 메모리
            self.MEMORY = []

            # 환경 초기화 - 데이터 다시 시작
            self.environment.reset()


            ## 2. epoch 내 에서 학습 진행
            while True:

                ## 2-1. act , 결과를 기억
                # 정책신경망에 따라 Agent 가 act 하고 보상 획득
                [next_sample , price, soc, action, pv, immediate_reward, delayed_reward] = self.agent.act(self.policy_network , self.epsilon)

                # 데이터를 다 읽을 경우 -> epoch 반복
                if next_sample == -1:
                    break

                # 행동 및 행동에 대한 결과를 기억
                self.PRICE.append(price)                      # 실제 전기 가격 저장
                self.SAMPLE.append(next_sample)               # 실제 Input 에 해당하는 상태셈플 저장
                self.ACTION.append(action)                    # 실제 행동 저장
                self.DE_REWARD.append(delayed_reward)
                self.IM_REWARD.append(immediate_reward)          # 실제 보상 저장
                self.SOC.append(soc)
                self.PV.append(pv)    # PV 가치 저장

                # 이건 무슨 표현 ?
                memory = [(
                    self.SAMPLE[i],
                    self.ACTION[i],
                    self.IM_REWARD[i])
                    for i in list(range(len(self.ACTION)))[-max_memory:]
                ]

                # if exploration:
                #     memory_exp_idx.append(itr_cnt)
                #     memory_prob.append([np.nan] * Agent.NUM_ACTIONS)
                # else:
                #     memory_prob.append(self.policy_network.prob)

                # # 반복에 대한 정보 갱신
                # batch_size += 1
                # itr_cnt += 1
                # exploration_cnt += 1 if exploration else 0
                # win_cnt += 1 if delayed_reward > 0 else 0

                ## 2-2 정책 신경망 업데이트

                # 보상 = 0 인데 batch size 가 최대 메모리 넘어선 경우 : 초기화
                # if delayed_reward == 0 and batch_size >= max_memory:
                #     delayed_reward = immediate_reward
                #     self.agent.basePV = self.agent.PV
                #
                # if learning and delayed_reward != 0:
                #     # 배치 학습 데이터 크기
                #     batch_size = min(batch_size, max_memory)
                #     # 배치 학습 데이터 생성
                #     x, y = self._get_batch(
                #         memory, batch_size, discount_factor, delayed_reward)
                #     if len(x) > 0:
                #         if delayed_reward > 0:
                #             pos_learning_cnt += 1
                #         else:
                #             neg_learning_cnt += 1
                #         # 정책 신경망 갱신
                #         loss += self.policy_network.train_on_batch(x, y)
                #         memory_learning_idx.append([itr_cnt, delayed_reward])
                #     batch_size = 0

            # ================================#
            # 에포크 관련 정보 가시화
            # num_epoches_digit = len(str(num_epoches))
            # epoch_str = str(epoch + 1).rjust(num_epoches_digit, '0')



        #     # 학습 관련 정보 갱신
        #     max_portfolio_value = max(
        #         max_portfolio_value, self.agent.portfolio_value)
        #     if self.agent.portfolio_value > self.agent.initial_balance:
        #         epoch_win_cnt += 1
        #
        # # 학습 관련 정보 로그 기록
        # logger.info("Max PV: %s, \t # Win: %d" % (
        #     locale.currency(max_portfolio_value, grouping=True), epoch_win_cnt))

    def _get_batch(self, memory, batch_size, discount_factor, delayed_reward):
        x = np.zeros((batch_size, 1, self.num_features))
        y = np.full((batch_size, self.agent.NUM_ACTIONS), 0.5)

        for i, (sample, action, reward) in enumerate(
                reversed(memory[-batch_size:])):
            x[i] = np.array(sample).reshape((-1, 1, self.num_features))
            y[i, action] = (delayed_reward + 1) / 2
            if discount_factor > 0:
                y[i, action] *= discount_factor ** i
        return x, y

    def _build_sample(self):
        self.environment.observe()
        if len(self.training_data) > self.training_data_idx + 1:
            self.training_data_idx += 1
            self.sample = self.training_data.iloc[self.training_data_idx].tolist()
            self.sample.extend(self.agent.get_states())
            return self.sample
        return None

    def trade(self, model_path=None, balance=2000000):
        if model_path is None:
            return
        self.policy_network.load_model(model_path=model_path)
        self.fit(balance=balance, num_epoches=1, learning=False)


if __name__ == "__main__":

    model = PolicyLearner()
    model.fit()
