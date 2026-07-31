# Chapter 07. 파이썬 자료구조 심화

프로그램은 여러 개의 값을 저장하고, 찾고, 정렬하고, 변환하는 작업을 반복합니다. Python은 이런 작업을 편리하게 처리할 수 있도록 리스트, 튜플, 집합, 딕셔너리 같은 자료구조를 기본으로 제공합니다.

이번 장에서는 Python 공식 튜토리얼의 [Data Structures](https://docs.python.org/3/tutorial/datastructures.html)를 바탕으로 다음 내용을 학습합니다.

- 리스트의 주요 메서드와 스택, 큐
- 리스트 컴프리헨션과 중첩 컴프리헨션
- `del`로 항목과 슬라이스 삭제하기
- 튜플과 시퀀스 언패킹
- 집합의 중복 제거와 집합 연산
- 딕셔너리의 키와 값 다루기
- `enumerate`, `zip`, `sorted`, `reversed`를 이용한 반복
- 조건식의 단락 평가와 비교 연산
- 시퀀스의 사전식 비교

앞 장에서 배운 반복문과 함께 사용하면 가격 목록이나 거래 기록을 훨씬 간결하게 처리할 수 있습니다.

---

## 1. 리스트 복습과 주요 메서드

리스트는 여러 값을 순서대로 저장하며, 생성한 뒤 항목을 추가하거나 삭제할 수 있는 **변경 가능한(mutable)** 자료구조입니다.

```python
prices = [100, 105, 103]

prices.append(110)
print(prices)  # [100, 105, 103, 110]

prices[1] = 106
print(prices)  # [100, 106, 103, 110]
```

리스트의 인덱스는 `0`부터 시작하고, 음수 인덱스는 뒤에서부터 셉니다. 슬라이스는 `start` 이상 `stop` 미만의 항목을 새로운 리스트로 반환합니다.

```python
print(prices[0])    # 첫 번째 항목
print(prices[-1])   # 마지막 항목
print(prices[1:3])  # 인덱스 1부터 2까지
```

### 주요 리스트 메서드

```python
orders = ["BTC", "ETH"]

orders.append("XRP")
orders.extend(["SOL", "ADA"])
orders.insert(1, "DOGE")
orders.remove("DOGE")
last_order = orders.pop()
count = orders.count("BTC")
position = orders.index("ETH")

orders.sort()
orders.reverse()
copied_orders = orders.copy()

print(last_order, count, position)
print(copied_orders)
```

- `append(value)`: 리스트 끝에 한 항목을 추가합니다.
- `extend(iterable)`: 반복 가능한 객체의 항목을 모두 추가합니다.
- `insert(index, value)`: 지정한 위치 앞에 항목을 추가합니다.
- `remove(value)`: 값이 같은 첫 항목을 삭제합니다. 없으면 `ValueError`가 발생합니다.
- `pop(index)`: 지정한 위치의 항목을 삭제하고 반환합니다. 생략하면 마지막 항목을 삭제합니다.
- `clear()`: 모든 항목을 삭제합니다.
- `count(value)`: 값이 나타난 횟수를 반환합니다.
- `index(value)`: 값이 처음 나타난 인덱스를 반환합니다.
- `sort()`: 리스트 자체를 정렬합니다.
- `reverse()`: 리스트 자체의 순서를 뒤집습니다.
- `copy()`: 리스트의 얕은 복사본을 반환합니다.

리스트를 직접 변경하는 메서드 대부분은 변경된 리스트를 반환하지 않고 `None`을 반환합니다. 따라서 `orders = orders.sort()`처럼 작성하지 말고 `orders.sort()`를 별도로 호출해야 합니다.

원본을 유지하면서 정렬된 새 리스트가 필요하면 내장 함수 `sorted()`를 사용합니다.

```python
prices = [105, 98, 110]
sorted_prices = sorted(prices)

print(prices)         # [105, 98, 110]
print(sorted_prices)  # [98, 105, 110]
```

---

## 2. 리스트를 스택으로 사용하기

스택은 **후입선출(LIFO, Last In First Out)** 구조입니다. 가장 나중에 들어온 항목을 먼저 꺼냅니다. 리스트의 `append()`와 인덱스 없는 `pop()`을 사용하면 간단한 스택을 만들 수 있습니다.

```python
stack = ["매수 신호", "가격 확인"]

stack.append("주문 제출")
print(stack)

print(stack.pop())  # 주문 제출
print(stack.pop())  # 가격 확인
print(stack)        # ['매수 신호']
```

실행 취소 기록이나 최근 작업 목록처럼 마지막에 추가한 것을 먼저 처리해야 할 때 적합합니다.

---

## 3. 리스트를 큐로 사용하기

큐는 **선입선출(FIFO, First In First Out)** 구조입니다. 먼저 들어온 항목이 먼저 나갑니다.

리스트의 맨 앞에서 `insert(0, value)`나 `pop(0)`을 반복하면 비효율적입니다. 큐에는 양쪽 끝에서 빠르게 추가하고 삭제할 수 있는 `collections.deque`를 사용합니다.

```python
from collections import deque

queue = deque(["BTC 주문", "ETH 주문"])
queue.append("XRP 주문")

print(queue.popleft())  # BTC 주문
print(queue.popleft())  # ETH 주문
print(queue)            # deque(['XRP 주문'])
```

`append()`는 오른쪽 끝에 항목을 추가하고, `popleft()`는 왼쪽 끝의 항목을 삭제해 반환합니다. 주문 처리 대기열처럼 도착한 순서대로 처리하는 작업에 적합합니다.

---

## 4. 리스트 컴프리헨션

리스트 컴프리헨션은 기존 반복문으로 새 리스트를 만드는 작업을 짧고 읽기 쉽게 표현하는 문법입니다.

```python
prices = [100, 105, 110, 98]

doubled = [price * 2 for price in prices]
print(doubled)  # [200, 210, 220, 196]
```

위 코드는 다음 반복문과 같은 의미입니다.

```python
doubled = []
for price in prices:
    doubled.append(price * 2)
```

기본 형태는 `[표현식 for 변수 in 반복가능한_객체]`입니다. 조건을 추가하면 원하는 항목만 선택할 수 있습니다.

```python
prices = [100, 105, 110, 98]

rise_prices = [price for price in prices if price >= 100]
print(rise_prices)  # [100, 105, 110]
```

`if` 조건이 참인 항목만 결과에 포함됩니다. `if`와 `for`를 여러 개 사용할 수도 있습니다.

```python
coins = ["BTC", "ETH", "XRP"]
timeframes = ["1d", "1h"]

requests = [
    (coin, timeframe)
    for coin in coins
    for timeframe in timeframes
    if coin != "XRP"
]
print(requests)
```

결과가 튜플이라면 괄호를 써야 합니다. `[coin, timeframe for coin in coins]`처럼 작성하면 문법 오류가 발생합니다.

### 중첩 리스트 컴프리헨션

리스트 안에 리스트가 있는 행렬도 컴프리헨션으로 처리할 수 있습니다.

```python
matrix = [
    [1, 2, 3],
    [4, 5, 6],
]

transposed = [[row[index] for row in matrix] for index in range(3)]
print(transposed)  # [[1, 4], [2, 5], [3, 6]]
```

바깥쪽 `for`가 열을 선택하고 안쪽 `for`가 각 행에서 값을 가져옵니다. 중첩이 복잡해지면 일반 반복문이나 `zip()`을 사용하는 편이 이해하기 쉽습니다.

```python
transposed = list(zip(*matrix))
print(transposed)  # [(1, 4), (2, 5), (3, 6)]
```

---

## 5. `del`로 항목 삭제하기

`del` 문은 인덱스나 슬라이스를 이용해 리스트 항목을 삭제합니다. `pop()`과 달리 삭제한 값을 반환하지 않습니다.

```python
prices = [100, 105, 110, 98, 102]

del prices[0]
print(prices)  # [105, 110, 98, 102]

del prices[1:3]
print(prices)  # [105, 102]

del prices[:]
print(prices)  # []
```

변수 자체도 삭제할 수 있습니다.

```python
temporary_value = 123
del temporary_value
# print(temporary_value)  # NameError
```

삭제한 이름을 다시 사용하려면 먼저 새로운 값을 할당해야 합니다.

---

## 6. 튜플과 시퀀스

튜플은 쉼표로 구분한 값들의 묶음이며, 리스트와 달리 생성 후 개별 항목을 바꿀 수 없는 **불변(immutable)** 자료구조입니다.

```python
market_data = ("BTC", 105_000_000, 2.5)

print(market_data[0])
print(market_data[1:])
# market_data[1] = 106_000_000  # TypeError
```

튜플은 여러 종류의 값을 하나의 기록으로 묶을 때 유용합니다. 리스트는 보통 같은 종류의 데이터 목록에, 튜플은 서로 관련된 고정된 값의 묶음에 사용합니다.

### 튜플 생성 규칙

괄호는 생략할 수 있지만, 항목을 구분하는 쉼표가 튜플을 만드는 핵심입니다.

```python
empty = ()
single = ("BTC",)  # 항목이 하나일 때는 뒤에 쉼표 필요
pair = "BTC", 105

print(len(empty))   # 0
print(len(single))  # 1
print(pair)         # ('BTC', 105)
```

괄호 안에 값 하나만 쓰면 튜플이 아니라 해당 값 자체입니다. `("BTC")`의 자료형은 문자열이고, `("BTC",)`의 자료형은 튜플입니다.

### 언패킹

튜플이나 리스트의 항목을 여러 변수에 나누어 저장하는 것을 시퀀스 언패킹이라고 합니다.

```python
market_data = ("BTC", 105_000_000, 2.5)
symbol, price, change_rate = market_data

print(symbol)
print(price)
print(change_rate)
```

왼쪽 변수의 개수와 오른쪽 시퀀스의 항목 수가 맞아야 합니다.

```python
first, *middle, last = [1, 2, 3, 4, 5]
print(first)   # 1
print(middle)  # [2, 3, 4]
print(last)    # 5
```

`*`를 붙인 변수는 남은 항목을 리스트로 받습니다. 함수에서 `*args`를 사용하는 원리도 이와 관련이 있습니다.

---

## 7. 집합(Set)

집합은 중복되지 않은 값들의 모음입니다. 순서가 없으므로 인덱스로 항목을 가져올 수 없으며, 멤버십 검사와 중복 제거에 적합합니다.

```python
symbols = {"BTC", "ETH", "BTC", "XRP"}
print(symbols)  # BTC는 한 번만 저장됨

print("ETH" in symbols)       # True
print("DOGE" not in symbols)  # True
```

빈 집합은 `{}`가 아니라 `set()`으로 만들어야 합니다. `{}`는 빈 딕셔너리입니다.

```python
empty_set = set()
empty_dictionary = {}
```

### 집합 연산

```python
btc_markets = {"KRW", "USDT", "USD"}
eth_markets = {"KRW", "USDT", "EUR"}

print(btc_markets | eth_markets)  # 합집합
print(btc_markets & eth_markets)  # 교집합
print(btc_markets - eth_markets)  # 차집합
print(btc_markets ^ eth_markets)  # 대칭 차집합
```

- `|`: 양쪽 집합에 있는 모든 값입니다.
- `&`: 양쪽 집합에 공통으로 있는 값입니다.
- `-`: 왼쪽 집합에만 있는 값입니다.
- `^`: 한쪽 집합에만 있는 값입니다.

연산자 대신 `union()`, `intersection()`, `difference()` 같은 메서드를 사용할 수도 있습니다.

```python
print(btc_markets.union(eth_markets))
print(btc_markets.intersection(eth_markets))
print(btc_markets.difference(eth_markets))
```

집합은 순서가 없으므로 출력 순서는 실행할 때 달라질 수 있습니다. 순서가 필요하면 `sorted()`로 정렬된 리스트를 만드세요.

### 집합 컴프리헨션

리스트 컴프리헨션과 비슷하게 집합 컴프리헨션을 사용할 수 있습니다.

```python
letters = {letter for letter in "abracadabra" if letter not in "abc"}
print(letters)  # {'r', 'd'}와 같이 중복 없는 결과
```

---

## 8. 딕셔너리

딕셔너리는 `키(key): 값(value)` 쌍을 저장하는 자료구조입니다. 리스트처럼 숫자 인덱스를 사용하는 대신 키를 이용해 값을 찾습니다. 하나의 딕셔너리 안에서 키는 중복될 수 없습니다.

```python
market = {
    "symbol": "BTC",
    "price": 105_000_000,
    "change_rate": 2.5,
}

print(market["symbol"])
print(market["price"])
```

값을 추가하거나 기존 값을 수정할 때도 같은 문법을 사용합니다. 키가 이미 있으면 기존 값이 새 값으로 바뀝니다.

```python
market["volume"] = 1_500
market["price"] = 106_000_000

del market["volume"]
print(market)
```

존재하지 않는 키를 대괄호로 조회하면 `KeyError`가 발생합니다. 키가 없을 수도 있다면 `get()`을 사용하세요.

```python
print(market.get("volume"))     # None
print(market.get("volume", 0))  # 0
```

키와 값, 항목을 각각 확인할 때는 `keys()`, `values()`, `items()`를 사용합니다.

```python
print(list(market.keys()))
print(list(market.values()))
print(list(market.items()))
```

Python 3.7 이상에서는 딕셔너리에 항목을 추가한 순서가 유지됩니다. 다만 딕셔너리의 본래 목적은 키를 이용한 조회이므로, 순서가 중요한 데이터에는 리스트를 함께 고려하세요.

### 딕셔너리 만들기

`dict()` 생성자에 키와 값의 쌍을 전달하거나 키워드 인자로 딕셔너리를 만들 수 있습니다.

```python
markets = dict([
    ("BTC", "KRW"),
    ("ETH", "KRW"),
])

fees = dict(BTC=0.0004, ETH=0.0004)
print(markets)
print(fees)
```

키가 문자열이고 식별자 규칙을 만족할 때만 `dict(key=value)` 형식을 사용할 수 있습니다.

### 딕셔너리 컴프리헨션

딕셔너리도 컴프리헨션으로 만들 수 있습니다.

```python
prices = {symbol: price for symbol, price in [("BTC", 105), ("ETH", 3)]}
print(prices)  # {'BTC': 105, 'ETH': 3}
```

조건을 추가해 특정 값만 선택할 수도 있습니다.

```python
all_prices = {"BTC": 105, "ETH": 3, "XRP": 0.5}
expensive = {
    symbol: price
    for symbol, price in all_prices.items()
    if price >= 10
}
print(expensive)
```

---

## 9. 딕셔너리와 자료구조 순회하기

딕셔너리를 순회할 때 `items()`를 사용하면 키와 값을 동시에 받을 수 있습니다.

```python
prices = {"BTC": 105, "ETH": 3, "XRP": 0.5}

for symbol, price in prices.items():
    print(f"{symbol}: {price}")
```

시퀀스의 인덱스와 값을 동시에 받으려면 `enumerate()`를 사용합니다.

```python
coins = ["BTC", "ETH", "XRP"]

for index, coin in enumerate(coins):
    print(index, coin)

for rank, coin in enumerate(coins, start=1):
    print(f"{rank}위: {coin}")
```

두 개 이상의 시퀀스를 같은 위치끼리 묶으려면 `zip()`을 사용합니다. 가장 짧은 시퀀스가 끝나면 반복도 끝납니다.

```python
symbols = ["BTC", "ETH", "XRP"]
prices = [105, 3, 0.5]

for symbol, price in zip(symbols, prices):
    print(f"{symbol}: {price}")
```

반복 중인 값을 역순으로 보려면 `reversed()`, 정렬된 순서로 보려면 `sorted()`를 사용합니다.

```python
coins = ["BTC", "ETH", "XRP"]

for coin in reversed(coins):
    print(coin)

for coin in sorted(coins):
    print(coin)
```

`sorted()`와 `set()`을 함께 사용하면 중복을 제거한 뒤 정렬된 순서로 반복할 수 있습니다.

```python
coins = ["BTC", "ETH", "BTC", "XRP", "ETH"]

for coin in sorted(set(coins)):
    print(coin)
```

---

## 10. 반복 중 리스트를 변경할 때

반복 중인 리스트에서 항목을 삭제하면 다음 항목을 건너뛸 수 있습니다. 원본을 직접 수정하기보다 새 리스트를 만드는 방식이 더 안전합니다.

```python
prices = [100, None, 105, None, 110]

valid_prices = []
for price in prices:
    if price is not None:
        valid_prices.append(price)

print(valid_prices)  # [100, 105, 110]
```

이 작업은 리스트 컴프리헨션으로도 표현할 수 있습니다.

```python
valid_prices = [price for price in prices if price is not None]
```

실제 데이터에는 `float("NaN")`처럼 숫자이지만 값이 없는 특수한 값도 들어올 수 있습니다. `math.isnan()`으로 확인할 수 있습니다.

```python
import math

raw_prices = [100.0, float("nan"), 105.0]
valid_prices = [price for price in raw_prices if not math.isnan(price)]
print(valid_prices)
```

---

## 11. 조건식과 단락 평가

`in`과 `not in`은 값이 컨테이너에 포함되는지 확인합니다. `is`와 `is not`은 두 이름이 같은 객체를 가리키는지 확인합니다.

```python
coins = ["BTC", "ETH"]
price = None

if "BTC" in coins:
    print("BTC를 지원합니다.")

if price is None:
    print("가격 데이터가 없습니다.")
```

`and`와 `or`는 왼쪽부터 평가하며 결과가 이미 결정되면 오른쪽을 평가하지 않습니다. 이를 **단락 평가(short-circuit evaluation)**라고 합니다.

```python
price = None

if price is not None and price > 100:
    print("가격 조건을 만족합니다.")
```

위 코드에서 `price is not None`이 거짓이면 오른쪽의 `price > 100`을 실행하지 않습니다. 따라서 `None`과 숫자를 비교하는 오류를 피할 수 있습니다.

`or`는 왼쪽 값이 참이면 왼쪽 값을, 그렇지 않으면 오른쪽 값을 반환합니다.

```python
name = ""
display_name = name or "이름 없음"
print(display_name)  # 이름 없음
```

여러 후보 중 첫 번째로 사용할 수 있는 값을 선택할 때 유용합니다. 단, `0`, `""`, `None`, 빈 컨테이너는 거짓으로 평가된다는 점에 주의하세요.

### 비교 연산 연결하기

비교 연산은 연결해서 작성할 수 있습니다.

```python
change_rate = 2.5

if 0 < change_rate <= 5:
    print("완만한 상승 구간입니다.")
```

위 코드는 `0 < change_rate and change_rate <= 5`와 같은 의미입니다.

---

## 12. 시퀀스 비교하기

리스트, 튜플, 문자열 같은 시퀀스는 같은 종류의 시퀀스끼리 사전식(lexicographical) 순서로 비교할 수 있습니다. 앞에서부터 항목을 비교하다가 서로 다른 항목이 나오면 그 결과로 전체 비교가 결정됩니다.

```python
print((1, 2, 3) < (1, 2, 4))  # True
print([1, 2, 3] == [1, 2, 3])  # True
print("ABC" < "C")            # True
```

첫 번째와 두 번째 항목이 같으면 세 번째 항목을 비교합니다. 한 시퀀스가 다른 시퀀스의 앞부분과 같고 더 짧다면 짧은 쪽이 더 작은 것으로 판단합니다.

```python
print((1, 2) < (1, 2, -1))  # True
print((1, 2, 3) < (1, 3, 0))  # True
```

서로 비교할 수 없는 자료형이 섞여 있으면 `TypeError`가 발생합니다.

```python
# [None, "hello", 10] < [None, "hello", 20]
# 서로 다른 자료형을 정렬하는 상황에서는 TypeError가 발생할 수 있습니다.
```

숫자처럼 자연스러운 비교 규칙이 있는 자료형은 서로 다른 숫자 타입이어도 비교할 수 있습니다.

```python
print((1, 2, 3) == (1.0, 2.0, 3.0))  # True
```

---

## ✅ 이번 챕터 요약 과제

1. 여러 코인의 가격을 리스트에 저장하고, `append()`, `sort()`, `pop()`을 이용해 가격을 추가하고 정렬하고 삭제해 보세요.
2. 가격 목록에서 100 이상인 가격만 골라내는 리스트 컴프리헨션을 작성하세요.
3. `deque`를 이용해 매매 주문 대기열을 만들고, 입력된 순서대로 주문을 처리하세요.
4. 여러 코인의 심볼과 가격 리스트를 `zip()`으로 묶어 딕셔너리로 만드세요.
5. 중복된 거래 심볼 목록에서 `set()`과 `sorted()`를 이용해 중복 없는 정렬 목록을 만드세요.
6. 코인별 가격 딕셔너리에서 가격이 1 이상인 항목만 딕셔너리 컴프리헨션으로 추출하세요.
7. `enumerate()`를 이용해 코인 목록에 1위부터 순위를 붙여 출력하세요.

---

## 참고 자료

- [Python 공식 문서: Data Structures](https://docs.python.org/3/tutorial/datastructures.html)
- [Python 공식 문서: Built-in Types](https://docs.python.org/3/library/stdtypes.html)

다음 장에서는 여러 Python 파일을 나누어 작성하고, 모듈과 패키지로 불러오는 방법을 배웁니다.
