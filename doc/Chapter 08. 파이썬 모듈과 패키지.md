# Chapter 08. 파이썬 모듈과 패키지

프로그램이 길어지면 하나의 파일에 모든 코드를 작성하기 어렵습니다. 관련된 함수와 변수를 여러 파일로 나누면 코드를 재사용하기 쉽고, 수정할 때도 필요한 부분만 확인할 수 있습니다.

Python에서는 이런 역할을 하는 파일을 **모듈(module)**이라고 합니다. 여러 모듈을 디렉터리 구조로 묶으면 **패키지(package)**가 됩니다.

이번 장에서는 Python 공식 튜토리얼의 [Modules](https://docs.python.org/3/tutorial/modules.html)를 바탕으로 다음 내용을 학습합니다.

- 모듈 파일 만들기와 `import` 사용하기
- `from ... import ...`, 별칭, 선택적 import
- 모듈을 스크립트로 실행하기
- `__name__ == "__main__"`의 의미
- 모듈 검색 경로와 `sys.path`
- 표준 모듈과 `dir()` 함수
- 패키지와 `__init__.py`
- 절대 import와 상대 import
- `__all__`과 패키지에서 `import *` 사용하기

---

## 1. 모듈이란?

모듈은 Python 정의와 실행문을 담은 `.py` 파일입니다. 예를 들어 가격 계산에 필요한 함수를 `coin_utils.py`라는 파일에 저장할 수 있습니다.

```python
# coin_utils.py

def calculate_return(buy_price, sell_price):
    """매수가와 매도가로 수익률을 계산합니다."""
    return (sell_price - buy_price) / buy_price


def calculate_fee(amount, fee_rate=0.0004):
    """거래 금액과 수수료율로 수수료를 계산합니다."""
    return amount * fee_rate
```

이 파일을 다른 Python 파일에서 불러오면 함수를 복사하지 않고 재사용할 수 있습니다.

```python
# analyze_coin.py
import coin_utils

return_rate = coin_utils.calculate_return(100, 110)
fee = coin_utils.calculate_fee(10_000)

print(return_rate)
print(fee)
```

`import coin_utils`는 현재 네임스페이스에 `coin_utils`라는 모듈 이름을 추가합니다. 함수 이름이 바로 추가되는 것은 아니므로 `coin_utils.calculate_return()`처럼 모듈 이름과 점(`.`)을 함께 사용합니다.

모듈에 정의된 전역 변수도 같은 방식으로 접근합니다.

```python
# settings.py
DEFAULT_FEE_RATE = 0.0004

# 다른 파일
import settings

print(settings.DEFAULT_FEE_RATE)
```

모듈마다 별도의 전역 네임스페이스가 있으므로, 서로 다른 모듈에서 같은 변수 이름을 사용해도 충돌 가능성이 줄어듭니다.

---

## 2. 함수와 변수 직접 가져오기

모듈 이름을 매번 쓰고 싶지 않다면 `from 모듈 import 이름` 형식을 사용할 수 있습니다.

```python
from coin_utils import calculate_fee, calculate_return

print(calculate_return(100, 110))
print(calculate_fee(10_000))
```

이 방식에서는 현재 파일에 `calculate_fee`와 `calculate_return` 이름이 직접 추가됩니다. 대신 `coin_utils`라는 이름 자체는 자동으로 추가되지 않습니다.

필요한 이름만 가져오는 것이 좋습니다. 모듈의 모든 이름을 가져오는 `from coin_utils import *`도 있지만, 어떤 이름이 현재 네임스페이스에 들어왔는지 알기 어려워지고 기존 이름을 덮어쓸 수 있으므로 일반적인 프로그램에서는 권장하지 않습니다.

### 별칭 사용하기

`as`를 사용하면 모듈이나 함수에 다른 이름을 붙일 수 있습니다.

```python
import coin_utils as utils
from coin_utils import calculate_return as get_return

print(utils.calculate_fee(10_000))
print(get_return(100, 110))
```

긴 모듈 이름을 짧게 만들거나, 같은 이름의 함수가 여러 모듈에 있을 때 구분하기 위해 사용할 수 있습니다.

---

## 3. Fibonacci 모듈 예제

Python 공식 문서에서는 Fibonacci 수열을 출력하고 리스트로 반환하는 함수를 `fibo.py` 모듈에 작성합니다.

```python
# fibo.py

def fib(n):
    """n보다 작은 Fibonacci 수를 출력합니다."""
    first, second = 0, 1
    while first < n:
        print(first, end=" ")
        first, second = second, first + second
    print()


def fib2(n):
    """n보다 작은 Fibonacci 수를 리스트로 반환합니다."""
    result = []
    first, second = 0, 1
    while first < n:
        result.append(first)
        first, second = second, first + second
    return result
```

같은 디렉터리에서 Python을 실행한 다음 모듈을 import할 수 있습니다.

```python
import fibo

fibo.fib(100)
print(fibo.fib2(100))
print(fibo.__name__)  # fibo
```

함수를 자주 사용할 때는 현재 파일의 다른 이름에 대입할 수도 있습니다.

```python
import fibo

fibonacci = fibo.fib
fibonacci(50)
```

모듈을 import해도 모듈 안의 함수 정의가 현재 파일에 복사되는 것은 아닙니다. Python은 모듈 객체를 만들고, 그 객체를 통해 정의에 접근하게 합니다.

---

## 4. 모듈을 스크립트로 실행하기

모듈은 다른 파일에서 import할 수도 있고, 직접 실행할 수도 있습니다. 이 두 경우를 구분하는 데 `__name__`을 사용합니다.

```python
# fibo.py

def fib(n):
    """n보다 작은 Fibonacci 수를 출력합니다."""
    first, second = 0, 1
    while first < n:
        print(first, end=" ")
        first, second = second, first + second
    print()


if __name__ == "__main__":
    fib(50)
```

파일을 직접 실행하면 Python은 해당 모듈의 `__name__`을 `"__main__"`으로 설정합니다.

```bash
python fibo.py
```

반대로 다른 파일에서 `import fibo`로 불러오면 `fibo.__name__`은 `"fibo"`가 됩니다. 따라서 `if __name__ == "__main__":` 아래의 코드는 import할 때 실행되지 않습니다.

```python
# test_fibo.py
import fibo

print(fibo.fib2(30))
```

이 패턴은 다음 두 목적에 유용합니다.

- 모듈을 라이브러리처럼 import할 수 있습니다.
- 같은 파일을 간단한 실행 프로그램이나 테스트 코드로도 사용할 수 있습니다.

---

## 5. 명령줄 인자 받기

직접 실행하는 스크립트에 값을 전달하려면 `sys.argv`를 사용할 수 있습니다. `sys.argv[0]`은 실행된 파일 이름이고, 그 뒤의 항목은 명령줄에서 전달한 문자열입니다.

```python
# show_coin.py
import sys

print(f"실행 파일: {sys.argv[0]}")
print(f"전달된 인자: {sys.argv[1:]}")
```

```bash
python show_coin.py BTC 100000000
```

명령줄 인자는 문자열로 전달되므로 숫자로 사용할 때는 변환해야 합니다.

```python
# calculate_square.py
import sys

number = int(sys.argv[1])
print(number ** 2)
```

```bash
python calculate_square.py 5
```

인자가 없는 경우에는 `IndexError`가 발생할 수 있으므로, 실제 프로그램에서는 `argparse` 같은 표준 모듈을 사용해 인자를 안전하게 처리하는 방법을 함께 고려합니다.

---

## 6. 모듈 검색 경로: `sys.path`

Python이 `import coin_utils`를 실행하면 모듈을 찾을 수 있는 디렉터리를 순서대로 검색합니다. 이 목록은 `sys.path`에 들어 있습니다.

```python
import sys

for path in sys.path:
    print(path)
```

검색 경로에는 일반적으로 다음 위치가 포함됩니다.

1. 실행한 스크립트가 있는 디렉터리 또는 현재 디렉터리
2. `PYTHONPATH` 환경 변수에 지정한 디렉터리
3. Python 설치 과정에서 정해진 표준 라이브러리와 `site-packages` 디렉터리

따라서 현재 프로젝트의 모듈을 import하려면 파일 위치와 실행 위치가 중요합니다.

```text
project/
    app.py
    coin_utils.py
```

`app.py`를 `project` 디렉터리에서 실행하면 같은 디렉터리의 `coin_utils.py`를 찾을 수 있습니다. 다른 위치에서 실행할 때는 패키지 구조나 `python -m` 실행 방식을 사용하는 것이 더 안정적입니다.

`sys.path`는 리스트이므로 실행 중에 경로를 추가할 수도 있습니다.

```python
import sys

sys.path.append("C:/my_python_modules")
```

다만 프로젝트의 정상적인 import 문제를 해결하기 위해 `sys.path`를 무분별하게 수정하는 것은 권장하지 않습니다. 파일 구조와 실행 위치를 먼저 확인하세요.

---

## 7. 컴파일된 Python 파일과 `__pycache__`

Python은 모듈을 빠르게 불러오기 위해 내부적으로 바이트코드 형태의 컴파일 결과를 캐시할 수 있습니다. 이 결과는 보통 모듈 디렉터리 아래의 `__pycache__` 폴더에 저장됩니다.

```text
project/
    coin_utils.py
    __pycache__/
        coin_utils.cpython-3xx.pyc
```

이 파일은 Python이 자동으로 관리하므로 직접 수정할 필요가 없습니다. `.pyc` 파일이 있다고 해서 프로그램이 더 빠르게 실행되는 것은 아니며, 주로 모듈을 다시 읽어 들이는 시간이 줄어듭니다.

실행된 메인 파일은 일반적으로 캐시를 사용하지 않고, 소스 파일의 수정 시간이 달라지면 Python이 캐시를 다시 만듭니다. `__pycache__`는 소스 코드와 함께 배포할 필요가 없는 생성물인 경우가 많습니다.

---

## 8. 표준 모듈 사용하기

Python에는 날짜, 운영체제, 파일 경로, 수학 계산 등을 처리하는 표준 모듈이 함께 제공됩니다. 별도의 설치 없이 사용할 수 있습니다.

```python
import math
import random
from datetime import datetime

print(math.sqrt(16))
print(random.choice(["BTC", "ETH", "XRP"]))
print(datetime.now())
```

운영체제와 상호작용할 때는 `sys`와 `os`를 사용할 수 있습니다.

```python
import os
import sys

print(os.getcwd())
print(sys.version)
```

표준 모듈은 Python 설치에 포함되어 있으므로 외부 패키지보다 배포가 간단합니다. 어떤 기능이 표준 라이브러리에 있는지 먼저 확인하면 불필요한 패키지 설치를 줄일 수 있습니다.

---

## 9. `dir()` 함수로 이름 확인하기

`dir()`은 모듈이나 객체가 제공하는 이름을 확인할 때 사용하는 내장 함수입니다.

```python
import math

print(dir(math))
```

인자 없이 사용하면 현재 네임스페이스에 정의된 이름을 보여줍니다.

```python
import math

coin = "BTC"

def show_coin():
    print(coin)

print(dir())
```

`dir()`의 결과에는 변수, 함수, 모듈 등 현재 접근할 수 있는 이름이 모두 포함됩니다. 이름의 정확한 사용법이나 설명까지 보여주는 함수는 아니므로, 자세한 설명은 `help()`를 함께 사용할 수 있습니다.

```python
import math

help(math.sqrt)
```

모듈의 이름 앞에 밑줄(`_`)이 붙은 내부 이름도 `dir()` 결과에 나타날 수 있습니다. 이런 이름은 일반 사용자에게 공개하지 않으려는 내부 구현일 수 있으므로 문서와 사용 목적을 확인하세요.

---

## 10. 패키지란?

패키지는 관련된 모듈을 디렉터리 계층으로 묶어 관리하는 방법입니다. 예를 들어 거래소별 기능을 다음처럼 나눌 수 있습니다.

```text
trading/
    __init__.py
    price.py
    order.py
    indicators/
        __init__.py
        moving_average.py
```

여기서 `trading`은 패키지이고, `price.py`와 `order.py`는 패키지 안의 모듈입니다. `indicators`는 `trading` 안에 있는 하위 패키지입니다.

`__init__.py`는 Python이 해당 디렉터리를 패키지로 인식하도록 하는 파일입니다. 비어 있어도 되지만, 패키지 초기화 코드나 공개 이름을 정의할 수도 있습니다.

```python
# trading/price.py

def get_current_price(symbol):
    """예제용 현재 가격을 반환합니다."""
    prices = {"BTC": 105_000_000, "ETH": 3_500_000}
    return prices.get(symbol)
```

패키지 모듈은 점으로 연결한 이름으로 import합니다.

```python
import trading.price

price = trading.price.get_current_price("BTC")
print(price)
```

---

## 11. 패키지에서 모듈 가져오기

패키지의 모듈을 더 짧게 사용하려면 다음과 같이 작성할 수 있습니다.

```python
from trading import price

print(price.get_current_price("ETH"))
```

모듈 안의 함수까지 직접 가져올 수도 있습니다.

```python
from trading.price import get_current_price

print(get_current_price("BTC"))
```

세 방식의 차이는 현재 파일에 만들어지는 이름입니다.

- `import trading.price`: `trading` 이름으로 접근합니다.
- `from trading import price`: `price` 이름으로 접근합니다.
- `from trading.price import get_current_price`: 함수 이름을 직접 사용합니다.

일반적으로 모듈의 출처를 코드에서 명확히 보이게 하려면 `import trading.price` 또는 `from trading import price` 형식을 자주 사용합니다.

---

## 12. 하위 패키지와 절대 import

하위 패키지가 있으면 전체 경로를 사용하는 절대 import로 다른 모듈을 가져올 수 있습니다.

```python
# trading/indicators/moving_average.py
from trading.price import get_current_price


def describe_price(symbol):
    price = get_current_price(symbol)
    return f"{symbol}: {price}"
```

절대 import는 프로젝트의 최상위 패키지부터 경로를 작성하므로 코드의 출처를 파악하기 쉽습니다.

```python
from trading.indicators.moving_average import describe_price

print(describe_price("BTC"))
```

실행 파일이 프로젝트의 최상위 모듈일 때는 보통 절대 import를 사용해야 합니다. 메인 모듈은 자체 패키지 이름이 없기 때문에 상대 import를 직접 사용할 수 없습니다.

---

## 13. 상대 import

패키지 내부의 모듈에서는 현재 패키지 또는 부모 패키지를 기준으로 상대 import를 사용할 수 있습니다. 점 하나는 현재 패키지, 점 두 개는 부모 패키지를 뜻합니다.

```python
# trading/indicators/moving_average.py
from .. import price
from . import volatility
```

- `from . import volatility`: 현재 `indicators` 패키지의 `volatility` 모듈
- `from .. import price`: 부모인 `trading` 패키지의 `price` 모듈
- `from ..price import get_current_price`: 부모 패키지의 함수

상대 import는 패키지 내부 구조를 간결하게 표현할 수 있지만, 파일을 단독으로 실행하면 현재 패키지 정보를 알 수 없어 실패할 수 있습니다. 패키지 모듈은 프로젝트 루트에서 `python -m 패키지.모듈` 형식으로 실행하는 것이 안전합니다.

```bash
python -m trading.indicators.moving_average
```

---

## 14. 패키지에서 `import *`와 `__all__`

패키지에서 `from trading.indicators import *`를 사용할 때 어떤 모듈을 공개할지 `indicators/__init__.py`의 `__all__`로 지정할 수 있습니다.

```python
# trading/indicators/__init__.py
__all__ = ["moving_average", "volatility"]
```

그러면 `__all__`에 포함된 이름을 패키지의 공개 목록으로 사용할 수 있습니다.

```python
from trading.indicators import *
```

하지만 `import *`는 현재 파일에 어떤 이름이 추가되는지 명확하지 않고 기존 이름을 가릴 수 있습니다. 따라서 일반적인 프로그램에서는 다음처럼 필요한 모듈이나 함수만 명시하는 편이 좋습니다.

```python
from trading.indicators import moving_average
from trading.indicators.volatility import calculate_volatility
```

`__all__`은 패키지의 공개 API를 문서화하는 용도로도 사용할 수 있습니다. 패키지 작성자가 외부에 제공할 이름을 통제하고 싶을 때 유용합니다.

---

## 15. 모듈은 한 번만 import됩니다

Python은 같은 실행 세션에서 모듈을 처음 import할 때 모듈의 코드를 실행하고, 이후에는 이미 만들어진 모듈 객체를 재사용합니다.

```python
# counter.py
print("counter 모듈을 초기화합니다.")
count = 0
```

```python
import counter
import counter

print(counter.count)
```

위 코드에서 초기화 메시지는 보통 한 번만 출력됩니다. 모듈 파일을 수정한 뒤 이미 실행 중인 인터프리터에서 변경 내용을 확인하려면 인터프리터를 다시 시작하거나 `importlib.reload()`를 사용할 수 있습니다.

```python
import importlib
import counter

importlib.reload(counter)
```

일반적인 프로그램에서는 프로그램을 다시 시작하는 편이 더 예측하기 쉽습니다.

---

## 16. 모듈을 나누는 기준

코인을 다루는 프로그램을 다음처럼 기능별로 나눌 수 있습니다.

```text
coin_trading/
    main.py
    config.py
    market_data.py
    indicators.py
    strategy.py
    backtest.py
```

예를 들어 역할을 다음과 같이 구분합니다.

- `config.py`: 수수료율, 기본 설정
- `market_data.py`: 가격 데이터 수집
- `indicators.py`: 이동평균과 지표 계산
- `strategy.py`: 매수·매도 신호 계산
- `backtest.py`: 과거 데이터로 전략 검증
- `main.py`: 프로그램 실행 흐름 조합

모듈을 나눌 때는 기능과 책임이 자연스럽게 묶이도록 합니다. 서로 강하게 의존하는 코드를 무작정 여러 파일로 나누면 import가 복잡해질 수 있으므로, 각 모듈이 하나의 명확한 역할을 가지도록 설계하는 것이 중요합니다.

```python
# strategy.py
from indicators import moving_average


def should_buy(prices):
    average = moving_average(prices)
    return prices[-1] > average
```

```python
# main.py
from strategy import should_buy

prices = [100, 102, 104, 106]

if should_buy(prices):
    print("매수 신호")
```

이처럼 계산 로직과 실행 로직을 분리하면 전략만 바꾸거나 테스트하기 쉬워집니다.

---

## ✅ 이번 챕터 요약 과제

1. `coin_utils.py`를 만들고 수익률과 거래 수수료를 계산하는 함수를 작성하세요.
2. 다른 Python 파일에서 `import coin_utils`와 `from coin_utils import 함수이름`을 각각 사용해 보세요.
3. 모듈을 직접 실행할 때만 동작하는 `if __name__ == "__main__":` 테스트 코드를 추가하세요.
4. `market_data.py`, `strategy.py`, `main.py`로 파일을 나누어 간단한 매매 신호 프로그램을 만들어 보세요.
5. `trading` 패키지와 `indicators` 하위 패키지를 만들고 절대 import와 상대 import를 비교해 보세요.
6. `sys.path`를 출력해 현재 Python이 모듈을 찾는 경로를 확인하세요.
7. `dir(math)`와 `help(math.sqrt)`를 실행해 표준 모듈을 탐색하세요.

---

## 참고 자료

- [Python 공식 문서: Modules](https://docs.python.org/3/tutorial/modules.html)
- [Python 공식 문서: The import system](https://docs.python.org/3/reference/import.html)
- [Python 공식 문서: Python Module Index](https://docs.python.org/3/py-modindex.html)

다음 장에서는 Python에서 파일을 읽고 쓰며, 문자열을 형식에 맞게 출력하는 방법을 배웁니다.
