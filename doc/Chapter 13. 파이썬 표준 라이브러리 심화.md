# Chapter 13. 파이썬 표준 라이브러리 심화

Chapter 12에서는 파일, 날짜, 정규 표현식, 압축과 테스트에 사용하는 표준 라이브러리를 살펴보았습니다. 이번 장에서는 조금 더 전문적인 작업에 사용하는 모듈을 배웁니다.

이번 장에서는 Python 공식 튜토리얼의 [Brief tour of the standard library — part II](https://docs.python.org/3/tutorial/stdlib2.html)를 바탕으로 다음 내용을 학습합니다.

- `reprlib`, `pprint`, `textwrap`을 이용한 출력 형식 개선
- `string.Template`을 이용한 사용자 수정 가능 템플릿
- `struct`를 이용한 바이너리 레코드 처리
- `threading`과 `queue`를 이용한 작업 분리
- `logging`으로 프로그램 기록 남기기
- `weakref`로 약한 참조와 캐시 다루기
- `array`, `deque`, `bisect`, `heapq`로 리스트 작업 개선
- `Decimal`로 정확한 금융 계산하기

이 장의 예제는 가격 데이터 수집, 주문 처리, 거래 보고서와 연결해 설명합니다.

---

## 1. 출력 형식 개선

큰 리스트나 깊게 중첩된 딕셔너리를 그대로 출력하면 화면을 읽기 어려울 수 있습니다. 표준 라이브러리에는 목적에 맞는 출력 도구가 있습니다.

### `reprlib`: 긴 객체 줄여 표시하기

`reprlib.repr()`은 큰 컨테이너의 내용을 일부만 보여줍니다.

```python
import reprlib

large_prices = {f"COIN{index}": index * 100 for index in range(100)}
print(reprlib.repr(large_prices))
```

디버깅 중 전체 데이터를 출력하고 싶지 않을 때 유용합니다. 원본 객체를 줄이는 것이 아니라 화면에 표시되는 문자열만 축약합니다.

### `pprint`: 자료구조 예쁘게 출력하기

`pprint`은 중첩된 리스트와 딕셔너리를 줄바꿈과 들여쓰기로 정리합니다.

```python
from pprint import pprint

portfolio = {
    "BTC": {"quantity": 0.012, "average_price": 105_000_000},
    "ETH": {"quantity": 0.35, "average_price": 3_500_000},
}

pprint(portfolio, width=50)
```

`pprint` 결과는 사람이 읽기 쉬울 뿐 아니라 Python 표현식에 가까운 형태를 유지합니다.

### `textwrap`: 문단 줄바꿈

긴 설명이나 로그 메시지를 화면 너비에 맞춰 줄바꿈하려면 `textwrap`을 사용합니다.

```python
import textwrap

message = """가격 데이터 수집이 완료되었습니다. 최근 24시간 동안 거래량과 변동률을 계산하고 매매 신호를 확인했습니다."""
print(textwrap.fill(message, width=35))
```

`wrap()`은 문자열 목록을 반환하고, `fill()`은 줄바꿈 문자가 포함된 하나의 문자열을 반환합니다.

```python
lines = textwrap.wrap(message, width=20)
print(lines)
```

---

## 2. 사용자 수정 가능한 템플릿

f-string과 `str.format()`은 Python 코드 안에서 값을 정합니다. 사용자가 보고서 형식을 직접 수정하도록 하려면 `string.Template`이 편리합니다.

```python
from string import Template

report_template = Template(
    "$symbol 가격은 $price 원이며, 변동률은 $change_rate%입니다."
)

report = report_template.substitute(
    symbol="BTC",
    price="105,000,000",
    change_rate="2.35",
)
print(report)
```

템플릿 변수는 `$` 뒤의 식별자로 표시합니다. `$$`는 실제 달러 기호를 표현합니다.

```python
from string import Template

template = Template("$symbol 거래 수수료는 $$${fee}입니다.")
print(template.substitute(symbol="BTC", fee="4,200"))
```

값이 빠지면 `substitute()`는 `KeyError`를 발생시킵니다. 사용자 입력처럼 일부 값이 없을 수 있는 상황에는 `safe_substitute()`를 사용할 수 있습니다.

```python
from string import Template

template = Template("$symbol의 가격은 $price원입니다.")
print(template.safe_substitute(symbol="ETH"))
```

### 구분자 바꾸기

`Template`을 상속하면 `$` 대신 다른 구분자를 사용할 수 있습니다.

```python
from string import Template


class ReportTemplate(Template):
    delimiter = "%"


template = ReportTemplate("%symbol: %price원")
print(template.substitute(symbol="XRP", price="800"))
```

템플릿을 사용하면 프로그램 로직과 화면 문구를 분리할 수 있습니다. 텍스트 보고서, CSV 행, HTML의 일부 내용을 서로 다른 템플릿으로 관리할 수 있습니다.

---

## 3. 바이너리 레코드 처리: `struct`

`struct`는 Python 값과 고정된 바이너리 데이터 사이를 변환합니다. 네트워크 프로토콜, 파일 헤더, 장치 데이터처럼 바이트 구조가 정해진 데이터를 다룰 때 사용합니다.

```python
import struct

symbol_code = 1
price = 105_000_000
quantity = 12

packed = struct.pack("<IQH", symbol_code, price, quantity)
print(packed)
print(len(packed))

unpacked = struct.unpack("<IQH", packed)
print(unpacked)
```

형식 문자열의 의미는 다음과 같습니다.

- `<`: 리틀 엔디언, 표준 크기
- `I`: 4바이트 부호 없는 정수
- `Q`: 8바이트 부호 없는 정수
- `H`: 2바이트 부호 없는 정수

실제 포맷의 규격을 모른 채 바이너리 데이터를 해석하면 잘못된 값이 나올 수 있습니다. `struct`는 바이트 단위 프로토콜이나 파일 형식을 정확히 알고 있을 때 사용하세요.

문자열을 바이너리 고정 길이 필드로 저장할 때는 `s`를 사용할 수 있습니다.

```python
import struct

record = struct.pack("<8sQ", b"BTC", 105_000_000)
symbol_bytes, price = struct.unpack("<8sQ", record)

print(symbol_bytes.rstrip(b"\\x00").decode("ascii"))
print(price)
```

---

## 4. 멀티스레딩

스레드는 서로 순차적으로 실행할 필요가 없는 작업을 분리할 때 사용합니다. 네트워크 요청이나 파일 입출력처럼 대기 시간이 있는 작업에서 프로그램 응답성을 높일 수 있습니다.

```python
import threading


def collect_price(symbol):
    print(f"{symbol} 가격 수집 시작")
    print(f"{symbol} 가격 수집 완료")


threads = [
    threading.Thread(target=collect_price, args=(symbol,))
    for symbol in ["BTC", "ETH", "XRP"]
]

for thread in threads:
    thread.start()
for thread in threads:
    thread.join()

print("모든 수집 작업 완료")
```

- `start()`: 스레드 실행을 시작합니다.
- `join()`: 해당 스레드가 끝날 때까지 기다립니다.

CPU 계산을 여러 스레드로 나눈다고 항상 빨라지는 것은 아닙니다. Python의 일반적인 CPython 실행 환경에는 GIL이 있어 CPU 중심 작업에는 프로세스나 전문 도구를 검토해야 합니다.

### `queue`로 스레드 간 통신하기

여러 스레드가 같은 리스트나 딕셔너리를 직접 수정하면 경쟁 조건이 발생할 수 있습니다. `queue.Queue`는 스레드 안전한 작업 전달 통로를 제공합니다.

```python
import threading
from queue import Queue


def worker(tasks):
    while True:
        symbol = tasks.get()
        if symbol is None:
            tasks.task_done()
            break
        print(f"{symbol} 작업 처리")
        tasks.task_done()


tasks = Queue()
worker_thread = threading.Thread(target=worker, args=(tasks,))
worker_thread.start()

for symbol in ["BTC", "ETH", "XRP"]:
    tasks.put(symbol)
tasks.put(None)

tasks.join()
worker_thread.join()
print("작업 큐 종료")
```

공유 자원에 직접 접근하는 대신 한 스레드가 자원을 관리하고 다른 스레드는 큐에 요청을 넣는 구조가 설계와 테스트에 유리합니다.

---

## 5. 로깅: `logging`

`print()`는 간단한 확인에 좋지만, 운영 프로그램에서는 시간, 로그 수준, 모듈 이름, 파일 위치 등을 함께 기록하는 `logging`을 사용하는 것이 좋습니다.

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s:%(name)s:%(message)s",
)

logger = logging.getLogger("trading")
logger.debug("디버깅 정보")
logger.info("가격 데이터 수집 완료")
logger.warning("거래량 데이터가 부족합니다.")
logger.error("주문 처리에 실패했습니다.")
```

기본 로그 수준이 `INFO`이면 `DEBUG` 메시지는 표시되지 않습니다. 주요 로그 수준은 다음과 같습니다.

- `DEBUG`: 상세한 디버깅 정보
- `INFO`: 정상적인 진행 정보
- `WARNING`: 문제가 될 수 있는 상황
- `ERROR`: 작업이 실패한 상황
- `CRITICAL`: 프로그램을 계속하기 어려운 심각한 상황

문자열을 미리 조합하기보다 로깅 인자를 사용하는 것이 좋습니다.

```python
price = 105_000_000
logger.info("현재 가격: %s", price)
```

로그를 파일에 저장하려면 `filename`을 설정할 수 있습니다. 여러 모듈이 있는 프로젝트에서는 모듈별로 `logging.getLogger(__name__)`을 사용하는 방식이 일반적입니다.

---

## 6. 약한 참조: `weakref`

Python은 객체를 가리키는 참조가 더 이상 없을 때 메모리를 정리합니다. 캐시가 객체를 저장하기 위해 강한 참조를 만들면, 원래 사용자가 객체를 더 이상 사용하지 않아도 객체가 계속 남을 수 있습니다.

`weakref.WeakValueDictionary`는 객체를 약하게 참조합니다. 다른 강한 참조가 사라지면 캐시 항목도 자동으로 없어집니다.

```python
import gc
import weakref


class PriceSnapshot:
    def __init__(self, symbol, price):
        self.symbol = symbol
        self.price = price

    def __repr__(self):
        return f"{self.symbol}({self.price})"


snapshot = PriceSnapshot("BTC", 105_000_000)
cache = weakref.WeakValueDictionary()
cache["latest"] = snapshot

print(cache["latest"])
del snapshot
gc.collect()
print("latest" in cache)
```

약한 참조는 객체를 소유하지 않고 관찰하거나 캐시할 때 적합합니다. 모든 클래스 인스턴스가 약한 참조를 지원하는 것은 아니므로 사용하려는 객체의 문서를 확인해야 합니다.

---

## 7. 리스트 작업을 위한 도구

Python의 리스트만으로도 많은 작업을 할 수 있지만, 데이터의 특성에 따라 더 적합한 자료구조가 있습니다.

### `array`: 같은 자료형의 값 저장

`array`는 같은 자료형의 기본값을 더 효율적으로 저장합니다.

```python
from array import array

volumes = array("I", [4000, 10, 700, 22222])
print(sum(volumes))
print(volumes[1:3])
```

일반 리스트보다 기능이 제한될 수 있지만, 큰 수치 배열을 단순하게 저장할 때 메모리를 절약할 수 있습니다. 수치 분석에서는 보통 NumPy 같은 전문 도구를 사용하지만, 작은 배열에는 표준 `array`도 사용할 수 있습니다.

### `deque`: 양쪽 끝이 빠른 큐

```python
from collections import deque

orders = deque(["order-1", "order-2", "order-3"])
orders.append("order-4")
print("처리:", orders.popleft())
print(orders)
```

리스트의 앞에서 반복적으로 추가·삭제할 때보다 `deque`가 적합합니다.

### `bisect`: 정렬된 리스트에 삽입

`bisect.insort()`는 리스트를 정렬 상태로 유지하면서 항목을 삽입합니다.

```python
import bisect

scores = [(100, "alpha"), (200, "beta"), (400, "gamma")]
bisect.insort(scores, (300, "delta"))
print(scores)
```

이미 정렬된 리스트에 항목을 추가할 때 매번 전체 `sort()`를 호출하는 것보다 편리합니다. 리스트가 처음부터 정렬되어 있다는 조건이 필요합니다.

### `heapq`: 가장 작은 값 우선 처리

힙은 가장 작은 항목을 빠르게 꺼내는 자료구조입니다.

```python
from heapq import heapify, heappop, heappush

prices = [105, 98, 110, 102]
heapify(prices)
heappush(prices, 95)

smallest = [heappop(prices) for _ in range(3)]
print(smallest)
```

전체를 정렬할 필요 없이 가장 낮은 가격이나 우선순위가 높은 작업을 반복해서 처리할 때 유용합니다.

---

## 8. 정확한 금융 계산: `Decimal`

Python의 `float`는 이진 부동소수점으로 저장되므로 사람이 기대하는 십진수 계산과 아주 작은 차이가 날 수 있습니다.

```python
print(0.1 + 0.2)
print((0.1 + 0.2) == 0.3)
```

수수료, 세금, 금액처럼 소수점 자릿수와 반올림 규칙이 중요한 계산에는 `decimal.Decimal`을 사용할 수 있습니다.

```python
from decimal import Decimal

amount = Decimal("0.70")
rate = Decimal("1.05")

print(round(amount * rate, 2))
print(Decimal("0.1") * 10 == Decimal("1.0"))
```

`Decimal`을 만들 때는 float를 전달하지 말고 문자열을 전달하는 것이 좋습니다.

```python
from decimal import Decimal

safe_value = Decimal("0.1")
risky_value = Decimal(0.1)

print(safe_value)
print(risky_value)
```

`Decimal`은 정밀도와 반올림을 조절할 수 있습니다.

```python
from decimal import Decimal, ROUND_DOWN, getcontext

getcontext().prec = 28
price = Decimal("105000000.1234")
quantity = Decimal("0.0012")
fee_rate = Decimal("0.0004")

gross = price * quantity
fee = (gross * fee_rate).quantize(Decimal("0.01"), rounding=ROUND_DOWN)

print(f"거래 금액: {gross}")
print(f"수수료: {fee}")
```

어떤 정밀도와 반올림 방식이 필요한지는 거래소 규칙과 애플리케이션 요구사항에 따라 정해야 합니다. 금융 계산에서 `Decimal`을 사용한다고 모든 거래소의 금액 규칙이 자동으로 해결되는 것은 아닙니다.

---

## 9. 코인 거래 프로그램에 적용하기

표준 라이브러리의 로깅, 큐, `Decimal`, `Template`을 조합해 간단한 주문 처리 구조를 만들어 보겠습니다.

```python
import logging
from decimal import Decimal
from queue import Queue
from string import Template


logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(message)s")
logger = logging.getLogger("order_processor")

order_template = Template("$symbol $side 주문: $amount원")
order_queue = Queue()


def process_order(order):
    amount = Decimal(order["price"]) * Decimal(order["quantity"])
    message = order_template.substitute(
        symbol=order["symbol"],
        side=order["side"],
        amount=f"{amount:,.0f}",
    )
    logger.info(message)
    return amount


orders = [
    {"symbol": "BTC", "side": "buy", "price": "105000000", "quantity": "0.001"},
    {"symbol": "ETH", "side": "sell", "price": "3500000", "quantity": "0.1"},
]

for order in orders:
    order_queue.put(order)

while not order_queue.empty():
    process_order(order_queue.get())
```

이 예제에서는 다음 역할을 분리했습니다.

- `Queue`: 처리할 주문을 전달합니다.
- `Decimal`: 금액을 십진수로 계산합니다.
- `Template`: 출력 문구를 데이터와 분리합니다.
- `logging`: 처리 기록을 남깁니다.

실제 거래 시스템에서는 주문 전송 전에 잔액, 수량 단위, 가격 단위, 네트워크 오류, 중복 주문을 추가로 검증해야 합니다.

---

## ✅ 이번 챕터 요약 과제

1. `pprint`와 `reprlib`으로 중첩된 포트폴리오 데이터를 각각 출력해 차이를 비교하세요.
2. `Template`으로 코인 거래 보고서의 출력 형식을 분리하세요.
3. `struct.pack()`과 `struct.unpack()`으로 가격과 수량을 바이너리 레코드로 변환하세요.
4. `Queue`와 `threading`을 이용해 여러 가격 수집 작업을 처리하세요.
5. `logging`을 파일에 기록하고 로그 수준을 바꿔 결과를 비교하세요.
6. `deque`, `bisect`, `heapq`를 각각 사용해 주문 처리 순서를 구현하세요.
7. float와 `Decimal`로 수수료를 계산하고 결과 차이를 확인하세요.
8. 약한 참조를 사용하는 가격 객체 캐시를 만들고 객체가 삭제될 때 캐시가 어떻게 변하는지 관찰하세요.

---

## 참고 자료

- [Python 공식 문서: Brief tour of the standard library — part II](https://docs.python.org/3/tutorial/stdlib2.html)
- [Python 공식 문서: Python Standard Library](https://docs.python.org/3/library/)
- [Python 공식 문서: `decimal`](https://docs.python.org/3/library/decimal.html)

다음 장에서는 가상 환경을 만들고 외부 패키지를 설치·관리하는 방법을 배웁니다.
