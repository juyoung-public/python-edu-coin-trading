# 1. 함수(Function): 반복되는 로직을 하나로 묶기

def get_target_price(open_price, last_range):
    """시가와 전일 변동폭을 넣으면 목표가를 계산해줌"""
    target = open_price + (last_range * 0.5)
    return target

# 함수 사용
btc_target = get_target_price(90000000, 2000000)
print(f"비트코인 매수 목표가: {btc_target}원")

# 2. 라이브러리와 pip: "남이 만든 도구 가져오기"

import time           # 파이썬 기본 내장 라이브러리
import pybithumb      # 방금 설치한 라이브러리

print("3초 뒤에 시세를 조회합니다...")
time.sleep(3)         # 3초 대기
print(pybithumb.get_current_price("BTC"))

# 3. 클래스(Class)와 객체(Object): 데이터와 기능을 하나로 묶기

class TradingBot:
    def __init__(self, name, balance):
        self.name = name        # 봇의 이름
        self.balance = balance  # 초기 잔고
    
    def buy(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            print(f"[{self.name}] {amount}원 매수 완료. 남은 잔고: {self.balance}원")
        else:
            print(f"[{self.name}] 잔고가 부족합니다!")

# 객체 생성 (설계도에서 실제 봇을 찍어냄)
my_bot = TradingBot("고딩트레이더1호", 1000000)
my_bot.buy(300000)

# 4. 종합: 라이브러리 속의 객체 활용하기

import pybithumb
from pprint import pprint

# 현재가(종가) 조회
price = pybithumb.get_current_price("BTC")
print("현재가(종가):", price)

# 호가(orderbook) 조회
orderbook = pybithumb.get_orderbook("BTC")
# orderbook은 dict 구조로 bids/asks 정보가 들어있습니다.
print("호가(매도/매수 샘플):")
pprint(orderbook)
