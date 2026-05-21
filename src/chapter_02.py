# 1. 변수와 자료형: 데이터를 담는 상자
## 1. 문자열 (String): 글자 데이터
coin_name = "Bitcoin"

## 2. 정수 (Integer): 소수점이 없는 숫자
current_price = 95000000

## 3. 실수 (Float): 소수점이 있는 숫자
change_rate = 2.45

## 4. 불리언 (Boolean): 참(True) 또는 거짓(False)
is_rising = True

# 2. f-string: 깔끔하게 출력하기
name = "비트코인"
price = 95000000

# 문자열 앞에 f를 붙이고 변수를 { }로 감쌉니다.
# {price:,} 처럼 쓰면 천 단위마다 콤마(,)를 자동으로 찍어줍니다.
print(f"{name}의 현재 가격은 {price:,}원입니다.")

# 3. 리스트와 딕셔너리: 데이터 묶어서 관리하기
## (1) 리스트 (List)
tickers = ["BTC", "ETH", "XRP", "DOGE"]

print(tickers[0])  # 첫 번째 항목: BTC (0부터 시작함에 주의!)
print(tickers[-1]) # 마지막 항목: DOGE

## (2) 딕셔너리 (Dictionary)
coin_info = {
    "name": "Ethereum",
    "ticker": "ETH",
    "opening_price": 4500000
}

print(f"코인 이름: {coin_info['name']}")

# 4. 조건문 (If): 판단하기
target_price = 100000000
current_price = 105000000

if current_price >= target_price:
    print("🚀 목표가 돌파! 매수 주문을 전송합니다.")
elif current_price > 90000000:
    print("👀 가격이 오르고 있습니다. 감시를 계속합니다.")
else:
    print("💤 아직 때가 아닙니다.")

# 5. 반복문 (For): 노가다 탈출하기
tickers = ["BTC", "ETH", "XRP"]

# tickers 리스트 안의 종목을 하나씩 t라는 변수에 넣으며 반복
for t in tickers:
    print(f"현재 {t} 종목의 시세를 빗썸 API에서 가져오는 중...")

print("조회 완료!")