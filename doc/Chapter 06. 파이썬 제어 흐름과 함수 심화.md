# Chapter 06. 파이썬 제어 흐름과 함수 심화

앞에서 변수, 자료형, 자료구조를 배웠다면 이제 프로그램이 **어떤 조건에서 무엇을 실행할지**와 **반복 작업을 어떻게 줄일지**를 제어할 차례입니다.

이번 장에서는 Python 공식 튜토리얼의 [More Control Flow Tools](https://docs.python.org/3/tutorial/controlflow.html)를 바탕으로 다음 내용을 학습합니다.

- `if`, `elif`, `else`를 이용한 조건 분기
- `for`, `while`, `range()`를 이용한 반복
- `break`, `continue`, 반복문의 `else`, `pass`
- `match` 패턴 매칭
- 함수 정의, 반환값, 인자 전달 방식
- 기본값 인자, 키워드 인자, `*args`, `**kwargs`
- 람다 표현식, 독스트링, 함수 어노테이션
- 읽기 좋은 Python 코드를 작성하는 방법

예제는 암호화폐 가격 데이터나 매매 전략을 다룰 때 사용할 수 있도록 구성했습니다.

---

## 1. 조건에 따라 실행하기: `if` 문

`if` 문은 조건식의 결과가 `True`일 때 들여쓰기된 코드를 실행합니다. 조건식이 `False`이면 해당 블록은 건너뜁니다.

```python
price = 105_000_000
target_price = 100_000_000

if price > target_price:
    print("목표 가격을 돌파했습니다.")
```

`if` 다음에는 반드시 콜론(`:`)을 쓰고, 실행할 코드는 같은 수준으로 들여쓰기합니다. Python에서는 들여쓰기가 코드 블록의 범위를 결정하므로 보통 공백 4개를 사용합니다.

### `elif`와 `else`

여러 조건을 순서대로 검사할 때는 `elif`를 사용합니다. `else`는 앞의 모든 조건이 거짓일 때 실행되며 생략할 수 있습니다.

```python
change_rate = -2.5

if change_rate > 3:
    signal = "강한 매수 관심"
elif change_rate > 0:
    signal = "상승"
elif change_rate == 0:
    signal = "보합"
else:
    signal = "하락"

print(signal)
```

위 코드는 `change_rate`를 위에서부터 비교합니다. `-2.5`는 어느 조건도 만족하지 않으므로 `else`가 실행되어 `하락`이 출력됩니다. 조건이 여러 개 참이어도 처음 만나는 조건 하나만 실행됩니다.

### 비교와 논리 연산

조건식에는 비교 연산자와 논리 연산자를 조합할 수 있습니다.

```python
volume = 1_500
change_rate = 4.2

if volume >= 1_000 and change_rate > 3:
    print("거래량과 상승률 조건을 모두 만족합니다.")

if change_rate < 0 or volume == 0:
    print("매매를 잠시 멈춥니다.")
```

- `and`: 양쪽 조건이 모두 참이어야 합니다.
- `or`: 둘 중 하나라도 참이면 됩니다.
- `not`: 조건의 참과 거짓을 뒤집습니다.
- `in`: 값이 시퀀스나 집합에 포함되어 있는지 확인합니다.

```python
market = "BTC"
supported_markets = {"BTC", "ETH", "XRP"}

if market in supported_markets:
    print(f"{market} 거래를 지원합니다.")
```

---

## 2. 순서대로 반복하기: `for` 문

Python의 `for` 문은 숫자만 증가시키는 방식이 아니라 리스트, 문자열, 딕셔너리처럼 **반복 가능한(iterable) 객체의 항목을 하나씩 꺼내며** 실행합니다.

```python
coins = ["BTC", "ETH", "XRP"]

for coin in coins:
    print(f"{coin} 데이터를 확인합니다.")
```

문자열도 문자의 시퀀스이므로 반복할 수 있습니다.

```python
for letter in "BTC":
    print(letter)
```

반복 중인 리스트를 직접 수정하면 항목을 건너뛰는 등 예상하기 어려운 결과가 생길 수 있습니다. 원본의 복사본을 순회하거나 새 리스트를 만드는 방식이 안전합니다.

```python
users = {"alice": "active", "bob": "inactive", "carol": "active"}

# 복사본을 순회하면서 원본을 수정합니다.
for user, status in users.copy().items():
    if status == "inactive":
        del users[user]

print(users)
```

---

## 3. 숫자 범위 만들기: `range()`

숫자를 일정한 간격으로 반복해야 할 때는 `range()`를 사용합니다.

```python
for day in range(5):
    print(day)
```

출력은 `0`부터 `4`까지입니다. `range(stop)`에서 `stop` 값은 포함되지 않습니다.

`range()`는 다음 세 가지 형식을 지원합니다.

```python
print(list(range(5, 10)))       # [5, 6, 7, 8, 9]
print(list(range(0, 10, 3)))    # [0, 3, 6, 9]
print(list(range(10, 0, -2)))   # [10, 8, 6, 4, 2]
```

- `range(stop)`: `0`부터 `stop` 직전까지
- `range(start, stop)`: `start`부터 `stop` 직전까지
- `range(start, stop, step)`: `step`만큼 이동

`range()`의 결과는 실제 숫자를 모두 담은 리스트가 아니라 필요할 때 숫자를 제공하는 객체입니다. 따라서 큰 범위를 다룰 때도 불필요한 리스트를 미리 만들지 않습니다. 화면에서 내용을 확인하려면 `list(range(...))`처럼 변환합니다.

리스트의 인덱스를 이용할 수도 있지만, 항목만 필요하다면 직접 순회하는 방식이 더 읽기 쉽습니다.

```python
prices = [100, 105, 103]

for index in range(len(prices)):
    print(index, prices[index])

for price in prices:
    print(price)
```

---

## 4. 반복을 중단하거나 건너뛰기

### `break`: 가장 가까운 반복문 끝내기

`break`는 현재 실행 중인 가장 안쪽의 `for` 또는 `while` 반복문을 즉시 종료합니다.

```python
prices = [98, 101, 103, 99]

for price in prices:
    if price >= 102:
        print("목표 가격을 찾았습니다.")
        break
    print(f"현재 가격: {price}")
```

### `continue`: 이번 반복만 건너뛰기

`continue`는 아래쪽 코드를 실행하지 않고 다음 반복으로 이동합니다.

```python
prices = [98, None, 103, 99]

for price in prices:
    if price is None:
        continue
    print(f"유효한 가격: {price}")
```

데이터에 결측값이 있을 때 해당 항목만 건너뛰는 용도로 사용할 수 있습니다.

---

## 5. 반복문의 `else`

Python의 `for`와 `while`에는 `else`를 붙일 수 있습니다. 반복문이 `break` 없이 정상적으로 끝났을 때 `else` 블록이 실행됩니다. `if`의 `else`와 달리, 핵심 기준은 **조건이 거짓인지가 아니라 `break`가 실행되었는지**입니다.

```python
numbers = [2, 4, 6, 8]

for number in numbers:
    if number % 2 == 1:
        print("홀수를 찾았습니다.")
        break
else:
    print("홀수가 없습니다.")
```

위 예제에서는 `break`가 실행되지 않았으므로 `홀수가 없습니다.`가 출력됩니다. 검색 결과를 확인하는 코드에서 유용합니다.

```python
for coin in ["BTC", "ETH", "XRP"]:
    if coin == "DOGE":
        print("거래 대상을 찾았습니다.")
        break
else:
    print("거래 대상이 없습니다.")
```

---

## 6. 아무 동작도 하지 않기: `pass`

`pass`는 실행할 동작이 없다는 뜻의 문장입니다. 문법상 코드가 필요하지만 아직 구현하지 않은 부분에 임시로 사용할 수 있습니다.

```python
def calculate_fee(amount):
    pass
```

위 함수는 호출해도 아무 동작을 하지 않고 `None`을 반환합니다. `pass`는 구현을 완료했다는 뜻이 아니므로, 실제 기능을 넣기 전까지의 자리 표시자로 사용합니다.

---

## 7. 패턴으로 분기하기: `match`

Python 3.10부터 `match` 문을 사용할 수 있습니다. 하나의 값이 여러 패턴 중 무엇과 일치하는지 비교하며, 다른 언어의 `switch`와 비슷하지만 리스트, 튜플, 객체의 구조까지 확인할 수 있습니다.

```python
def explain_status(status):
    match status:
        case 200:
            return "정상 처리"
        case 400 | 401 | 403:
            return "요청 또는 인증 오류"
        case 404:
            return "대상을 찾을 수 없음"
        case _:
            return "알 수 없는 상태"

print(explain_status(200))
print(explain_status(500))
```

`case _`의 밑줄은 어떤 값과도 일치하는 와일드카드입니다. 위 예제에서는 앞의 어떤 패턴에도 맞지 않을 때 실행됩니다. `case 400 | 401`처럼 `|`를 사용하면 여러 리터럴을 하나의 패턴으로 묶을 수 있습니다.

### 구조 분해와 조건(guard)

패턴 안의 이름은 값이 일치했을 때 해당 위치의 값을 변수에 저장합니다. `if`를 추가하면 패턴이 맞더라도 추가 조건을 검사할 수 있습니다.

```python
def describe_point(point):
    match point:
        case (0, 0):
            return "원점"
        case (x, y) if x == y:
            return "대각선 위의 점"
        case (x, y):
            return f"x={x}, y={y}"
        case _:
            return "점이 아닙니다"

print(describe_point((3, 3)))
print(describe_point((2, 5)))
```

`case (x, y)`는 두 요소를 가진 시퀀스의 값을 `x`, `y`에 각각 저장합니다. 패턴 매칭은 입력 자료의 구조가 명확할 때 특히 유용합니다.

---

## 8. 함수 정의하기

함수는 여러 번 사용할 작업을 하나의 이름으로 묶은 코드 블록입니다. `def` 키워드, 함수 이름, 괄호 안의 매개변수, 콜론 순서로 정의합니다.

```python
def print_fibonacci(limit):
    """limit보다 작은 피보나치 수를 출력합니다."""
    first, second = 0, 1
    while first < limit:
        print(first, end=" ")
        first, second = second, first + second
    print()


print_fibonacci(100)
```

함수 본문은 들여쓰기해야 합니다. 첫 번째 문자열은 함수의 설명인 **독스트링(docstring)**으로 사용됩니다.

### 반환값: `return`

`return`은 함수 실행을 끝내고 호출한 곳으로 값을 돌려줍니다. `return`이 없거나 값 없이 `return`하면 `None`이 반환됩니다.

```python
def fibonacci_list(limit):
    """limit보다 작은 피보나치 수를 리스트로 반환합니다."""
    result = []
    first, second = 0, 1

    while first < limit:
        result.append(first)
        first, second = second, first + second

    return result


prices = fibonacci_list(100)
print(prices)
```

`result.append(first)`는 리스트 끝에 항목을 추가하는 메서드 호출입니다. 출력만 하는 함수와 달리 값을 반환하는 함수는 다른 계산에 재사용하기 쉽습니다.

---

## 9. 함수 인자 다루기

### 기본값 인자

매개변수에 기본값을 지정하면 호출할 때 해당 인자를 생략할 수 있습니다.

```python
def buy_coin(symbol, amount=10_000, fee_rate=0.0004):
    fee = amount * fee_rate
    return {
        "symbol": symbol,
        "amount": amount,
        "fee": fee,
    }


print(buy_coin("BTC"))
print(buy_coin("ETH", 20_000))
```

기본값은 함수가 정의되는 시점에 한 번만 계산됩니다. 리스트나 딕셔너리처럼 변경 가능한 객체를 기본값으로 사용하면 호출 사이에 값이 공유될 수 있으므로 `None`을 기본값으로 두고 함수 안에서 새 객체를 만드는 방식을 사용합니다.

```python
def add_coin(symbol, coins=None):
    if coins is None:
        coins = []
    coins.append(symbol)
    return coins
```

### 키워드 인자

인자의 이름을 함께 적으면 순서 대신 의미를 명확히 전달할 수 있습니다.

```python
print(buy_coin(symbol="BTC", amount=50_000, fee_rate=0.0003))
print(buy_coin(amount=30_000, symbol="ETH"))
```

위치 인자는 키워드 인자보다 먼저 써야 하며, 같은 매개변수에 값을 두 번 전달할 수 없습니다.

```python
def show_order(symbol, amount):
    print(symbol, amount)


show_order("BTC", amount=10_000)  # 정상
# show_order(symbol="BTC", "10_000")  # SyntaxError
# show_order("BTC", symbol="ETH")     # TypeError
```

### 위치 전용과 키워드 전용 매개변수

함수 정의의 `/` 앞에 있는 매개변수는 위치로만 전달할 수 있습니다. `*` 뒤의 매개변수는 키워드로만 전달할 수 있습니다.

```python
def create_order(symbol, /, amount, *, order_type="market"):
    return {
        "symbol": symbol,
        "amount": amount,
        "order_type": order_type,
    }


create_order("BTC", 10_000, order_type="limit")
# create_order(symbol="BTC", amount=10_000)  # symbol은 위치 전용
```

이 문법은 함수 사용 방법을 명확하게 만들고, 나중에 매개변수 이름을 바꾸더라도 호출 코드가 깨질 가능성을 줄입니다.

### 가변 위치 인자와 가변 키워드 인자

`*args`는 여러 위치 인자를 튜플로 모읍니다. `**kwargs`는 여러 키워드 인자를 딕셔너리로 모읍니다.

```python
def summarize_prices(*prices, **metadata):
    print(f"가격 개수: {len(prices)}")
    print(f"평균 가격: {sum(prices) / len(prices):.2f}")
    print(f"추가 정보: {metadata}")


summarize_prices(100, 105, 103, symbol="BTC", timeframe="1d")
```

`*args`와 `**kwargs`라는 이름 자체가 문법은 아니지만 널리 쓰이는 관례입니다. 일반 매개변수, `*args`, 키워드 전용 매개변수, `**kwargs` 순서로 배치할 수 있습니다.

---

## 10. 인자 목록 풀어 전달하기

리스트나 튜플 앞에 `*`를 붙이면 각 항목을 위치 인자로 풀어서 전달합니다. 딕셔너리 앞에 `**`를 붙이면 키와 값이 키워드 인자로 전달됩니다.

```python
def show_range(start, stop, step):
    print(list(range(start, stop, step)))


range_args = [0, 10, 2]
show_range(*range_args)
```

```python
def print_order(symbol, amount, order_type):
    print(symbol, amount, order_type)


order = {
    "symbol": "BTC",
    "amount": 10_000,
    "order_type": "market",
}
print_order(**order)
```

함수의 매개변수 이름과 딕셔너리의 키가 일치해야 정상적으로 전달됩니다.

---

## 11. 짧은 함수를 만드는 람다 표현식

`lambda`는 이름이 없는 작은 함수를 한 줄로 만드는 표현식입니다. 형식은 `lambda 매개변수: 반환할_표현식`입니다.

```python
add_fee = lambda amount: amount * 1.0004
print(add_fee(10_000))
```

일반 함수로 작성하면 다음과 같습니다.

```python
def add_fee_function(amount):
    return amount * 1.0004
```

람다는 보통 정렬 기준처럼 함수를 한 번만 전달할 때 사용합니다.

```python
pairs = [(3, "three"), (1, "one"), (2, "two")]
pairs.sort(key=lambda pair: pair[1])
print(pairs)
```

람다 내부에는 하나의 표현식만 작성할 수 있으므로, 복잡한 로직에는 이름 있는 `def` 함수를 사용하는 편이 좋습니다.

---

## 12. 독스트링과 함수 어노테이션

### 독스트링

함수 정의 바로 아래의 문자열은 독스트링입니다. `help()`나 `__doc__`으로 확인할 수 있으며, 함수의 목적과 인자, 반환값을 설명하는 데 사용합니다.

```python
def calculate_return(buy_price, sell_price):
    """매수가와 매도가를 이용해 단순 수익률을 계산합니다."""
    return (sell_price - buy_price) / buy_price


print(calculate_return.__doc__)
```

첫 줄에는 함수의 목적을 짧게 쓰고, 더 자세한 설명이 필요하면 빈 줄 뒤에 추가 내용을 작성합니다.

### 함수 어노테이션

어노테이션은 매개변수나 반환값에 예상 타입 등의 정보를 표시하는 선택 기능입니다. Python이 자동으로 타입을 검사하거나 실행 방식을 바꾸지는 않지만, IDE와 타입 검사 도구가 코드를 이해하는 데 도움을 줍니다.

```python
def calculate_return(buy_price: float, sell_price: float) -> float:
    """매수가와 매도가를 이용해 단순 수익률을 계산합니다."""
    return (sell_price - buy_price) / buy_price


print(calculate_return(100.0, 110.0))
print(calculate_return.__annotations__)
```

---

## 13. 읽기 좋은 Python 코드

Python 공식 스타일 가이드인 PEP 8은 다음과 같은 기본 원칙을 권장합니다.

1. 들여쓰기는 공백 4개를 사용합니다.
2. 한 줄은 가능하면 79자 이내로 작성합니다.
3. 함수와 클래스 사이에는 빈 줄을 둡니다.
4. 연산자 주변과 쉼표 뒤에 공백을 둡니다.
5. 함수와 변수는 `lowercase_with_underscores` 형식으로 이름을 짓습니다.
6. 클래스는 `UpperCamelCase` 형식으로 이름을 짓습니다.
7. 함수의 목적을 설명하는 독스트링을 작성합니다.
8. 다른 사람이 이해하기 어려운 부분에만 간결한 주석을 작성합니다.

```python
def calculate_target_price(open_price: float, previous_range: float,
                           k: float = 0.5) -> float:
    """전일 변동폭을 이용해 당일 매수 목표가를 계산합니다."""
    return open_price + previous_range * k
```

문법적으로 실행되는 코드와 유지보수하기 좋은 코드는 다릅니다. 이름을 명확히 짓고, 함수 하나가 하나의 작업에 집중하도록 만들면 이후 백테스팅 코드도 훨씬 쉽게 수정할 수 있습니다.

---

## ✅ 이번 챕터 요약 과제

1. 가격 목록을 입력받아 목표 가격 이상인 첫 번째 가격을 찾는 함수를 작성하세요. 찾으면 `break`로 반복을 끝내고, 찾지 못하면 반복문의 `else`에서 안내 문구를 출력하세요.
2. `match`를 사용해 `"buy"`, `"sell"`, `"hold"` 매매 신호에 따른 한국어 메시지를 반환하세요.
3. `calculate_target_price(open_price, previous_range, k=0.5)` 함수를 만들고 `k` 값을 `0.1`, `0.5`, `0.9`로 바꾸어 결과를 비교하세요.
4. 여러 가격을 `*prices`로 받아 최댓값, 최솟값, 평균을 딕셔너리로 반환하는 함수를 작성하세요.
5. 작성한 함수에 독스트링과 타입 어노테이션을 추가하세요.

---

## 참고 자료

- [Python 공식 문서: More Control Flow Tools](https://docs.python.org/3/tutorial/controlflow.html)
- [Python 공식 문서: PEP 8 스타일 가이드](https://peps.python.org/pep-0008/)

다음 장에서는 Python의 리스트, 튜플, 집합, 딕셔너리 같은 자료구조를 더 깊이 다룹니다.