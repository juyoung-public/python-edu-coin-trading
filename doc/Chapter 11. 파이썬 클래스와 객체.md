# Chapter 11. 파이썬 클래스와 객체

지금까지는 함수와 자료구조를 이용해 데이터를 처리했습니다. 프로그램의 규모가 커지면 데이터와 그 데이터를 조작하는 함수를 하나의 단위로 묶는 편이 편리합니다. Python에서는 **클래스(class)**를 사용해 새로운 객체 형식을 정의할 수 있습니다.

이번 장에서는 Python 공식 튜토리얼의 [Classes](https://docs.python.org/3/tutorial/classes.html)를 바탕으로 다음 내용을 학습합니다.

- 이름, 객체, 별칭과 변경 가능한 객체
- 스코프와 네임스페이스
- 클래스 정의와 인스턴스 생성
- `__init__()`, `self`, 메서드
- 클래스 변수와 인스턴스 변수
- 상속과 메서드 재정의
- 다중 상속과 `super()`
- 비공개 이름과 이름 장식(name mangling)
- `dataclass`로 데이터 객체 만들기
- 반복자와 `__iter__()`, `__next__()`
- 제너레이터와 제너레이터 표현식

예제는 코인 가격, 주문, 포트폴리오 객체로 구성했습니다.

---

## 1. 이름과 객체

Python에서 변수는 값을 담는 상자가 아니라 **객체에 붙은 이름**입니다. 대입은 데이터를 복사하기보다 이름과 객체를 연결합니다.

```python
prices = [100, 105, 110]
alias = prices

alias.append(115)

print(prices)  # [100, 105, 110, 115]
print(alias)   # [100, 105, 110, 115]
print(prices is alias)  # True
```

`prices`와 `alias`는 같은 리스트 객체를 가리킵니다. 리스트처럼 변경 가능한 객체를 다른 이름에 대입하면 한쪽에서 수정한 내용이 다른 이름에서도 보입니다.

복사본이 필요하다면 `copy()`나 슬라이스를 사용합니다.

```python
prices = [100, 105, 110]
copied_prices = prices.copy()

copied_prices.append(115)

print(prices)         # [100, 105, 110]
print(copied_prices)  # [100, 105, 110, 115]
```

정수, 문자열, 튜플처럼 불변 객체는 값을 직접 바꿀 수 없으므로 별칭으로 인한 변경 문제가 상대적으로 적습니다. 클래스 인스턴스도 기본적으로 변경 가능한 객체이므로, 객체를 전달할 때 이 차이를 이해해야 합니다.

---

## 2. 스코프와 네임스페이스

**네임스페이스(namespace)**는 이름과 객체의 연결을 저장하는 공간입니다. 모듈 전역 변수, 함수의 지역 변수, 객체의 속성 등이 각각 네임스페이스를 가집니다.

Python은 이름을 대략 다음 순서로 찾습니다.

1. 현재 함수의 지역 스코프
2. 바깥쪽 함수의 스코프
3. 현재 모듈의 전역 스코프
4. 내장 이름 스코프

```python
message = "전역 메시지"


def show_message():
    message = "지역 메시지"
    print(message)


show_message()
print(message)
```

함수 안에서 대입한 `message`는 지역 변수이고, 함수 밖의 `message`에는 영향을 주지 않습니다.

### `global`과 `nonlocal`

전역 변수나 바깥 함수의 변수를 함수 안에서 다시 대입하려면 `global` 또는 `nonlocal`을 사용합니다. 다만 전역 상태를 많이 변경하면 코드 추적이 어려워지므로, 가능한 한 반환값과 객체를 사용하는 편이 좋습니다.

```python
signal = "대기"


def set_global_signal():
    global signal
    signal = "매수"


set_global_signal()
print(signal)
```

```python
def make_counter():
    count = 0

    def increase():
        nonlocal count
        count += 1
        return count

    return increase


counter = make_counter()
print(counter())
print(counter())
```

`nonlocal`은 중첩 함수가 바깥 함수의 지역 변수를 수정하게 합니다.

---

## 3. 클래스 정의하기

클래스는 데이터와 기능을 묶어 새로운 객체 형식을 정의합니다. 클래스 이름은 보통 `UpperCamelCase`로 작성합니다.

```python
class Coin:
    """코인 정보를 표현하는 클래스입니다."""

    pass


bitcoin = Coin()
print(type(bitcoin))
print(bitcoin.__class__)
```

`Coin()`처럼 클래스를 호출하면 새로운 인스턴스가 생성됩니다. `pass`는 클래스 본문에 문법상 필요한 블록을 임시로 채우는 역할을 합니다.

클래스 안에는 일반적으로 메서드와 클래스 속성을 작성합니다.

```python
class Market:
    name = "가상 거래소"

    def describe(self):
        return f"거래소: {self.name}"


market = Market()
print(market.describe())
```

클래스 객체에는 클래스 본문에서 정의한 속성과 메서드가 있습니다.

```python
print(Market.name)
print(Market.describe)
print(Market.__doc__)
```

---

## 4. `__init__()`와 인스턴스 속성

인스턴스마다 다른 초기 데이터를 넣으려면 특별한 메서드인 `__init__()`을 정의합니다. 인스턴스를 만들 때 `__init__()`이 자동으로 호출됩니다.

```python
class Coin:
    def __init__(self, symbol, price):
        self.symbol = symbol
        self.price = price


bitcoin = Coin("BTC", 105_000_000)
ethereum = Coin("ETH", 3_500_000)

print(bitcoin.symbol, bitcoin.price)
print(ethereum.symbol, ethereum.price)
```

`self`는 현재 메서드를 호출한 인스턴스를 가리킵니다. `self.symbol`과 `self.price`는 인스턴스마다 따로 저장되는 속성입니다.

`self`는 Python에서 특별히 예약된 이름은 아니지만, 첫 번째 인자에 `self`를 사용하는 것이 모든 Python 코드의 관례입니다.

```python
class Coin:
    def __init__(self, symbol, price):
        self.symbol = symbol
        self.price = price

    def display(self):
        return f"{self.symbol}: {self.price:,}원"


coin = Coin("BTC", 105_000_000)
print(coin.display())
```

`coin.display()`는 내부적으로 `Coin.display(coin)`과 비슷하게 동작합니다. 인스턴스가 메서드의 첫 번째 인자로 자동 전달되기 때문에 호출할 때 `self`를 직접 쓰지 않습니다.

---

## 5. 인스턴스 메서드와 상태 변경

메서드는 객체의 상태를 읽거나 변경하는 함수입니다.

```python
class Wallet:
    def __init__(self, balance=0):
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("잔액이 부족합니다.")
        self.balance -= amount

    def summary(self):
        return f"잔액: {self.balance:,}원"


wallet = Wallet(100_000)
wallet.deposit(50_000)
wallet.withdraw(30_000)
print(wallet.summary())
```

객체의 데이터를 메서드로 관리하면 잔액 검증과 같은 규칙을 한곳에 모을 수 있습니다. 외부 코드가 `wallet.balance = -1`처럼 직접 상태를 바꾸는 것도 가능하므로, Python의 클래스는 접근을 완전히 차단하기보다 사용 규칙과 관례를 통해 설계합니다.

---

## 6. 클래스 변수와 인스턴스 변수

- 인스턴스 변수: 각 인스턴스가 독립적으로 가지는 데이터
- 클래스 변수: 클래스와 모든 인스턴스가 공유하는 데이터

```python
class Order:
    market_type = "spot"

    def __init__(self, symbol, amount):
        self.symbol = symbol
        self.amount = amount


first_order = Order("BTC", 10_000)
second_order = Order("ETH", 20_000)

print(first_order.market_type)
print(second_order.market_type)
print(first_order.symbol)
print(second_order.symbol)
```

`symbol`과 `amount`는 주문마다 다르므로 인스턴스 변수입니다. `market_type`은 모든 주문이 공유하는 값이므로 클래스 변수로 만들었습니다.

### 변경 가능한 클래스 변수의 주의점

리스트나 딕셔너리 같은 변경 가능한 객체를 클래스 변수로 만들면 모든 인스턴스가 하나의 객체를 공유합니다.

```python
class WrongPortfolio:
    symbols = []

    def add(self, symbol):
        self.symbols.append(symbol)


first = WrongPortfolio()
second = WrongPortfolio()
first.add("BTC")

print(second.symbols)  # ['BTC']
```

대부분 이런 결과는 의도하지 않은 것입니다. 각 인스턴스마다 새 리스트를 만들어야 합니다.

```python
class Portfolio:
    def __init__(self):
        self.symbols = []

    def add(self, symbol):
        self.symbols.append(symbol)


first = Portfolio()
second = Portfolio()
first.add("BTC")

print(first.symbols)   # ['BTC']
print(second.symbols)  # []
```

---

## 7. 속성 검색과 메서드 객체

인스턴스에서 `object.name`을 조회하면 먼저 인스턴스의 속성을 찾고, 없으면 클래스의 속성을 찾습니다. 인스턴스에 같은 이름의 속성을 만들면 클래스 속성을 가립니다.

```python
class Warehouse:
    purpose = "storage"
    region = "west"


first = Warehouse()
second = Warehouse()
second.region = "east"

print(first.purpose, first.region)
print(second.purpose, second.region)
```

`first.region`은 클래스 변수에서 가져오지만, `second.region`은 인스턴스에 새로 저장한 값을 사용합니다.

메서드는 변수에 저장해 나중에 호출할 수도 있습니다.

```python
class Greeter:
    def greet(self, name):
        return f"안녕하세요, {name}님"


greeter = Greeter()
method = greeter.greet
print(method("학습자"))
```

`method`는 이미 `greeter` 인스턴스와 연결된 메서드이므로 호출할 때 `self`를 전달하지 않습니다.

---

## 8. 상속

상속은 기존 클래스의 기능을 물려받아 새로운 클래스를 만드는 기능입니다.

```python
class Asset:
    def __init__(self, symbol, price):
        self.symbol = symbol
        self.price = price

    def describe(self):
        return f"{self.symbol}: {self.price:,}원"


class CoinAsset(Asset):
    def change_price(self, rate):
        self.price *= 1 + rate


bitcoin = CoinAsset("BTC", 100_000_000)
bitcoin.change_price(0.05)
print(bitcoin.describe())
print(isinstance(bitcoin, CoinAsset))
print(isinstance(bitcoin, Asset))
print(issubclass(CoinAsset, Asset))
```

`CoinAsset`는 `Asset`의 `__init__()`과 `describe()`를 물려받고, `change_price()`를 추가했습니다.

- `isinstance(object, class)`: 객체가 해당 클래스 또는 하위 클래스의 인스턴스인지 확인합니다.
- `issubclass(class, parent)`: 클래스가 부모 클래스를 상속했는지 확인합니다.

### 메서드 재정의

하위 클래스는 부모 클래스의 메서드를 같은 이름으로 다시 정의할 수 있습니다.

```python
class Order:
    def summary(self):
        return "일반 주문"


class LimitOrder(Order):
    def __init__(self, limit_price):
        self.limit_price = limit_price

    def summary(self):
        return f"지정가 주문: {self.limit_price:,}원"


order = LimitOrder(100_000_000)
print(order.summary())
```

하위 클래스의 메서드가 부모 메서드를 대체하므로, `LimitOrder`의 `summary()`가 실행됩니다.

### `super()`로 부모 기능 확장하기

부모 메서드의 기능을 유지하면서 내용을 추가하려면 `super()`를 사용합니다.

```python
class Order:
    def __init__(self, symbol, amount):
        self.symbol = symbol
        self.amount = amount


class MarketOrder(Order):
    def __init__(self, symbol, amount, slippage=0.001):
        super().__init__(symbol, amount)
        self.slippage = slippage


order = MarketOrder("BTC", 10_000)
print(order.symbol, order.amount, order.slippage)
```

`super().__init__()`은 부모 클래스의 초기화 코드를 재사용합니다.

---

## 9. 다중 상속

Python은 둘 이상의 부모 클래스를 상속하는 다중 상속을 지원합니다.

```python
class PriceFeed:
    def fetch_price(self):
        return 105_000_000


class RiskChecker:
    def check_risk(self, amount):
        return amount <= 1_000_000


class TradingBot(PriceFeed, RiskChecker):
    def can_trade(self, amount):
        return self.check_risk(amount) and self.fetch_price() > 0


bot = TradingBot()
print(bot.fetch_price())
print(bot.can_trade(500_000))
print(TradingBot.__mro__)
```

부모 클래스 목록에 적은 순서를 기준으로 메서드를 찾으며, Python은 `__mro__`(Method Resolution Order)로 실제 탐색 순서를 관리합니다. 다중 상속은 강력하지만 부모 사이의 책임과 메서드 이름이 충돌하지 않도록 신중하게 사용해야 합니다.

---

## 10. 비공개 변수와 이름 장식

Python에는 다른 언어와 같은 강제된 private 속성이 없습니다. 이름 앞에 `_` 하나를 붙인 속성은 외부에서 사용하지 않는 내부 구현이라는 관례를 나타냅니다.

```python
class Account:
    def __init__(self, balance):
        self._balance = balance

    def get_balance(self):
        return self._balance


account = Account(100_000)
print(account.get_balance())
print(account._balance)  # 접근은 가능하지만 내부 속성이라는 관례를 존중해야 함
```

이름 앞에 밑줄 두 개를 붙이면 이름 장식(name mangling)이 적용됩니다. 클래스 내부의 `__balance`는 대략 `_Account__balance`라는 이름으로 바뀌어 하위 클래스와의 이름 충돌을 줄입니다.

```python
class SecureAccount:
    def __init__(self, balance):
        self.__balance = balance

    def get_balance(self):
        return self.__balance


account = SecureAccount(100_000)
print(account.get_balance())
print(account.__dict__)
```

이름 장식은 완전한 보안 기능이 아닙니다. `account._SecureAccount__balance`처럼 접근할 수 있으므로, 주된 목적은 실수로 이름이 충돌하는 일을 줄이는 것입니다.

---

## 11. 데이터클래스

데이터를 저장하는 클래스는 `dataclasses.dataclass`를 사용하면 초기화 메서드와 표현 메서드 등을 자동으로 만들 수 있습니다.

```python
from dataclasses import dataclass


@dataclass
class MarketPrice:
    symbol: str
    price: float
    change_rate: float = 0.0


market_price = MarketPrice("BTC", 105_000_000, 2.35)
print(market_price)
print(market_price.symbol)
```

`@dataclass`를 사용하면 다음과 같은 반복 코드를 줄일 수 있습니다.

- `__init__()` 자동 생성
- 객체 내용을 보여주는 `__repr__()` 자동 생성
- 필드 비교를 위한 `__eq__()` 자동 생성

```python
first = MarketPrice("ETH", 3_500_000)
second = MarketPrice("ETH", 3_500_000)

print(first == second)
```

데이터를 묶어 전달하는 객체를 만들 때는 데이터클래스가 간결하고 읽기 쉽습니다.

---

## 12. 반복자 프로토콜

`for` 문은 리스트나 문자열 같은 반복 가능한 객체에서 항목을 하나씩 꺼냅니다. 내부적으로는 `iter()`로 반복자를 얻고, `next()`로 다음 항목을 요청합니다.

```python
symbols = ["BTC", "ETH", "XRP"]
iterator = iter(symbols)

print(next(iterator))
print(next(iterator))
print(next(iterator))
```

더 이상 항목이 없을 때 `next()`는 `StopIteration`을 발생시킵니다. `for` 문은 이 예외를 내부적으로 처리합니다.

```python
iterator = iter(["BTC"])
print(next(iterator))

try:
    print(next(iterator))
except StopIteration:
    print("반복이 끝났습니다.")
```

직접 만든 클래스가 반복 가능하게 하려면 `__iter__()`와 `__next__()`를 구현합니다.

```python
class Reverse:
    """시퀀스를 뒤에서부터 순회하는 반복자입니다."""

    def __init__(self, data):
        self.data = data
        self.index = len(data)

    def __iter__(self):
        return self

    def __next__(self):
        if self.index == 0:
            raise StopIteration
        self.index -= 1
        return self.data[self.index]


for symbol in Reverse(["BTC", "ETH", "XRP"]):
    print(symbol)
```

반복자는 데이터를 한 번에 모두 만들지 않고 필요할 때 하나씩 제공합니다.

---

## 13. 제너레이터

제너레이터는 `yield`를 사용해 반복자 기능을 간단하게 작성하는 함수입니다.

```python
def reverse(data):
    for index in range(len(data) - 1, -1, -1):
        yield data[index]


for symbol in reverse(["BTC", "ETH", "XRP"]):
    print(symbol)
```

제너레이터 함수는 호출 즉시 모든 결과를 계산하지 않고 제너레이터 객체를 반환합니다. `next()`가 호출될 때마다 `yield` 다음 위치에서 실행을 이어 갑니다.

```python
def price_stream(prices):
    for price in prices:
        print("가격을 준비합니다.")
        yield price


stream = price_stream([100, 105])
print(next(stream))
print(next(stream))
```

제너레이터는 반복자의 `__iter__()`와 `__next__()`를 자동으로 만들어 줍니다. 큰 파일이나 대량의 가격 데이터처럼 모든 결과를 메모리에 저장하고 싶지 않은 경우 유용합니다.

```python
def prices_until(prices, limit):
    for price in prices:
        if price > limit:
            return
        yield price


print(list(prices_until([98, 101, 105, 99], 102)))
```

---

## 14. 제너레이터 표현식

리스트 컴프리헨션과 비슷하게 괄호를 사용하면 제너레이터 표현식을 만들 수 있습니다.

```python
prices = [100, 105, 110, 98]

price_squares = (price ** 2 for price in prices)
print(price_squares)
print(sum(price_squares))
```

리스트 컴프리헨션은 결과 리스트를 즉시 만들지만, 제너레이터 표현식은 필요한 순간에 값을 계산합니다.

```python
x_prices = [100, 105, 110]
y_prices = [2, 3, 4]

total = sum(x * y for x, y in zip(x_prices, y_prices))
print(total)
```

제너레이터 표현식은 `sum()`, `max()`, `min()`처럼 반복 가능한 객체를 받는 함수와 함께 사용할 때 특히 간결합니다.

---

## 15. 클래스 설계 실습: 주문 객체

앞에서 배운 내용을 하나의 주문 클래스로 묶어 보겠습니다.

```python
from dataclasses import dataclass


@dataclass
class Order:
    symbol: str
    price: float
    quantity: float
    side: str = "buy"

    @property
    def total_amount(self):
        return self.price * self.quantity

    def summary(self):
        return (
            f"{self.side.upper()} {self.symbol}: "
            f"{self.total_amount:,.0f}원"
        )


order = Order("BTC", 105_000_000, 0.001)
print(order.summary())
print(order.total_amount)
```

`@property`를 사용하면 메서드를 속성처럼 읽을 수 있습니다. `total_amount`처럼 다른 속성으로부터 계산되는 값을 표현할 때 편리합니다.

---

## ✅ 이번 챕터 요약 과제

1. `Coin` 클래스를 만들고 심볼, 가격, 변동률을 인스턴스 변수로 저장하세요.
2. `Coin` 클래스에 가격을 변동률만큼 변경하는 `apply_change()` 메서드를 추가하세요.
3. 모든 코인 객체가 공유하는 거래소 이름을 클래스 변수로 만들어 보세요.
4. `Asset` 부모 클래스와 `CoinAsset` 하위 클래스를 만들고 메서드를 재정의하세요.
5. `dataclass`로 거래 기록을 표현하고 총 거래 금액을 계산하는 속성을 추가하세요.
6. 가격 목록을 역순으로 순회하는 반복자 클래스를 작성하세요.
7. `yield`를 이용해 목표 가격 이하의 가격만 생성하는 제너레이터를 작성하세요.
8. 제너레이터 표현식으로 가격 목록의 평균을 계산하세요.

---

## 참고 자료

- [Python 공식 문서: Classes](https://docs.python.org/3/tutorial/classes.html)
- [Python 공식 문서: `dataclasses`](https://docs.python.org/3/library/dataclasses.html)
- [Python 공식 문서: Iterator Types](https://docs.python.org/3/library/stdtypes.html#iterator-types)

다음 장에서는 Python 표준 라이브러리에서 자주 사용하는 모듈을 살펴봅니다.
