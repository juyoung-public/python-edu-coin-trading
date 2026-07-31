# Chapter 10. 파이썬 오류와 예외 처리

프로그램을 작성하다 보면 문법을 잘못 입력하거나, 실행 중 예상하지 못한 데이터와 상황을 만나게 됩니다. Python은 이런 문제를 오류 메시지와 예외(exception)로 알려주며, 프로그램이 적절히 대응할 수 있도록 예외 처리 문법을 제공합니다.

이번 장에서는 Python 공식 튜토리얼의 [Errors and Exceptions](https://docs.python.org/3/tutorial/errors.html)를 바탕으로 다음 내용을 학습합니다.

- 문법 오류와 실행 중 예외의 차이
- traceback에서 오류 위치와 종류 찾기
- `try`, `except`로 예외 처리하기
- 여러 예외를 구분하고 예외 정보 확인하기
- `else`와 `finally` 사용하기
- `raise`로 예외 발생시키기
- 예외 다시 발생시키기와 예외 연결하기
- 사용자 정의 예외 만들기
- `with`를 이용한 정리 작업
- `ExceptionGroup`, `except*`, 예외 메모

예제는 잘못된 가격 데이터나 주문 입력을 안전하게 처리하는 상황으로 구성했습니다.

---

## 1. 문법 오류와 예외

Python에서 발생하는 문제는 크게 **문법 오류(syntax error)**와 **예외(exception)**로 나눌 수 있습니다.

### 문법 오류

문법 오류는 Python이 코드를 해석할 수 없을 때 발생합니다. 괄호나 콜론을 빠뜨리거나, 잘못된 들여쓰기를 사용하면 생깁니다.

```python
# if price > 100  # 콜론이 없으므로 SyntaxError
#     print(price)
```

문법 오류가 발생하면 Python은 파일 이름과 줄 번호, 오류가 발견된 위치를 보여줍니다. 표시된 위치가 항상 실제 원인은 아닐 수 있습니다. 예를 들어 앞 줄에서 괄호나 따옴표를 닫지 않아 다음 줄에서 오류가 발견될 수도 있습니다.

### 예외

문법적으로 올바른 코드도 실행하는 순간 오류가 발생할 수 있습니다.

```python
# print(10 / 0)          # ZeroDivisionError
# print(unknown_price)   # NameError
# print("100" + 100)     # TypeError
```

예외의 종류는 문제가 발생한 원인을 알려줍니다.

- `ZeroDivisionError`: 0으로 나누려고 했습니다.
- `NameError`: 정의되지 않은 이름을 사용했습니다.
- `TypeError`: 자료형에 맞지 않는 연산을 시도했습니다.
- `ValueError`: 자료형은 맞지만 값이 허용 범위가 아닙니다.
- `IndexError`: 시퀀스에 없는 인덱스를 사용했습니다.
- `KeyError`: 딕셔너리에 없는 키를 사용했습니다.
- `FileNotFoundError`: 파일을 찾지 못했습니다.

---

## 2. traceback 읽기

처리되지 않은 예외가 발생하면 Python은 `Traceback`을 출력합니다.

```python
prices = [100, 105]
print(prices[5])
```

실행하면 대략 다음과 같은 정보가 표시됩니다.

```text
Traceback (most recent call last):
  File "example.py", line 2, in <module>
    print(prices[5])
IndexError: list index out of range
```

traceback은 보통 다음 순서로 읽습니다.

1. 오류가 발생한 파일 이름과 줄 번호를 확인합니다.
2. 해당 줄의 코드를 확인합니다.
3. 마지막 줄의 예외 종류를 확인합니다.
4. 예외 메시지에서 구체적인 원인을 확인합니다.

함수 호출이 여러 단계로 이어진 경우 traceback에는 호출 경로가 위에서 아래로 표시됩니다. 가장 아래쪽의 오류부터 읽고, 그 오류가 어떤 함수 호출을 통해 발생했는지 위쪽으로 따라가면 됩니다.

---

## 3. `try`와 `except`로 예외 처리하기

`try` 블록에는 예외가 발생할 수 있는 코드를 넣고, `except` 블록에는 그 예외를 처리할 코드를 넣습니다.

```python
text = "105000000"

try:
    price = int(text)
except ValueError:
    print("가격은 정수로 입력해야 합니다.")
else:
    print(f"가격: {price:,}원")
```

`try` 문은 다음 순서로 동작합니다.

1. 먼저 `try` 블록을 실행합니다.
2. 예외가 발생하지 않으면 `except`를 건너뜁니다.
3. 지정한 종류의 예외가 발생하면 남은 `try` 코드를 건너뛰고 해당 `except`를 실행합니다.
4. 지정하지 않은 예외는 처리하지 않고 바깥쪽 코드로 전달됩니다.

예외가 발생할 수 있는 부분만 `try` 안에 넣는 것이 좋습니다. 너무 많은 코드를 `try`에 넣으면 어느 작업에서 오류가 발생했는지 파악하기 어려워집니다.

### 사용자 입력 검증

```python
while True:
    text = input("가격을 입력하세요: ")
    try:
        price = int(text)
        break
    except ValueError:
        print("숫자를 입력해 주세요.")

print(f"입력한 가격: {price:,}원")
```

잘못된 입력이 들어오면 프로그램을 종료하지 않고 다시 입력받습니다.

---

## 4. 여러 예외 처리하기

하나의 `try`에는 여러 `except`를 작성해 예외 종류별로 다른 메시지를 출력할 수 있습니다.

```python
def get_price(prices, symbol):
    try:
        return prices[symbol]
    except KeyError:
        print(f"지원하지 않는 코인입니다: {symbol}")
    except TypeError:
        print("가격 데이터는 딕셔너리여야 합니다.")
    return None


prices = {"BTC": 105_000_000, "ETH": 3_500_000}
print(get_price(prices, "BTC"))
print(get_price(prices, "DOGE"))
```

예외가 발생하면 일치하는 `except` 하나만 실행됩니다. 더 구체적인 예외를 먼저 작성하고, 더 일반적인 예외를 뒤에 작성해야 합니다.

```python
class TradingError(Exception):
    pass

class InvalidPriceError(TradingError):
    pass


try:
    raise InvalidPriceError("가격이 올바르지 않습니다.")
except InvalidPriceError:
    print("잘못된 가격을 처리합니다.")
except TradingError:
    print("거래 관련 오류를 처리합니다.")
```

`InvalidPriceError`는 `TradingError`의 하위 클래스이므로, 부모 예외를 먼저 쓰면 자식 예외를 처리할 기회를 잃습니다.

여러 예외를 같은 방식으로 처리할 때는 튜플로 묶습니다.

```python
try:
    number = int("not a number")
except (TypeError, ValueError):
    print("숫자로 변환할 수 없습니다.")
```

---

## 5. 예외 객체와 오류 메시지 확인하기

`except 예외종류 as 변수` 형식을 사용하면 발생한 예외 객체를 변수에 저장할 수 있습니다.

```python
try:
    price = int("one hundred")
except ValueError as error:
    print(f"오류 종류: {type(error).__name__}")
    print(f"오류 내용: {error}")
    print(f"인자 정보: {error.args}")
```

예외 객체의 `args`에는 예외를 만들 때 전달한 인자가 들어 있습니다. 대부분의 경우 예외 객체 자체를 출력하면 사람이 읽을 수 있는 메시지가 표시됩니다.

예외 처리 범위를 넓히고 싶을 때 `Exception`을 사용할 수 있지만, 예상하지 못한 오류까지 숨길 수 있으므로 구체적인 예외를 먼저 처리하는 것이 좋습니다.

```python
try:
    result = 10 / 2
except ZeroDivisionError:
    print("0으로 나눌 수 없습니다.")
except Exception as error:
    print(f"예상하지 못한 오류: {error}")
    raise
```

마지막 `raise`는 오류를 기록한 뒤 같은 예외를 다시 상위 호출자에게 전달합니다. 오류를 조용히 삼키지 않고 문제를 발견하게 해 주는 방식입니다.

`KeyboardInterrupt`와 `SystemExit`는 일반적인 `Exception` 하위 예외가 아니므로 무조건 `BaseException`을 잡는 코드는 피해야 합니다.

---

## 6. `else` 절

`try`에 `else`를 붙이면 예외가 발생하지 않았을 때만 실행됩니다. `else`는 모든 `except` 뒤에 작성해야 합니다.

```python
def read_price(text):
    try:
        price = float(text)
    except ValueError:
        print("가격 형식이 올바르지 않습니다.")
        return None
    else:
        print("가격 변환에 성공했습니다.")
        return price


print(read_price("105.5"))
print(read_price("unknown"))
```

성공했을 때 실행할 코드를 `try` 안에 모두 넣는 것보다 `else`에 분리하면, 성공 후 코드에서 발생한 예외가 잘못된 입력 예외로 처리되는 일을 막을 수 있습니다.

```python
def calculate_fee(text):
    try:
        amount = float(text)
    except ValueError:
        print("거래 금액이 아닙니다.")
        return None
    else:
        # 이 부분에서 발생한 다른 오류는 위 ValueError 처리 대상이 아닙니다.
        return amount * 0.0004
```

---

## 7. `finally`로 항상 정리하기

`finally` 블록은 예외 발생 여부와 관계없이 실행됩니다. 파일, 네트워크 연결, 잠금처럼 사용 후 반드시 정리해야 하는 자원을 처리할 때 사용합니다.

```python
def process_order():
    print("주문 처리를 시작합니다.")
    try:
        raise RuntimeError("거래소 응답 오류")
    except RuntimeError as error:
        print(f"주문 실패: {error}")
    finally:
        print("주문 처리 자원을 정리합니다.")


process_order()
```

`finally`의 실행 순서는 다음과 같습니다.

- 예외가 없으면 `try` 실행 후 `finally`를 실행합니다.
- 처리할 수 있는 예외가 있으면 `except` 실행 후 `finally`를 실행합니다.
- 처리하지 않은 예외가 있어도 `finally`를 실행한 뒤 예외를 다시 전달합니다.

정리 작업에는 `finally`가 유용하지만, 파일처럼 `with`를 지원하는 객체에는 `with` 문을 우선 사용하는 것이 더 간결합니다.

`finally` 안에서 `return`을 사용하면 `try`나 `except`의 반환값과 예외를 덮어쓸 수 있어 혼란을 만들 수 있으므로 피하는 것이 좋습니다.

---

## 8. 파일과 `with` 문

파일 객체는 사용이 끝나면 닫아야 합니다. `with` 문은 블록이 끝날 때 파일을 자동으로 닫아 줍니다.

```python
with open("prices.txt", encoding="utf-8") as file:
    for line in file:
        print(line, end="")
```

파일을 처리하는 중 오류가 발생해도 `with`가 파일을 닫습니다. 이처럼 객체가 제공하는 표준 정리 동작을 **컨텍스트 관리자(context manager)**라고 합니다.

```python
try:
    with open("prices.txt", encoding="utf-8") as file:
        content = file.read()
except FileNotFoundError:
    print("가격 파일을 찾을 수 없습니다.")
else:
    print(content)
```

오류를 처리하는 `try`와 자원을 관리하는 `with`를 함께 사용할 수 있습니다.

---

## 9. `raise`로 예외 발생시키기

`raise` 문은 프로그램의 조건에 맞지 않는 상황에서 예외를 직접 발생시킵니다.

```python
def calculate_return(buy_price, sell_price):
    if buy_price <= 0:
        raise ValueError("매수 가격은 0보다 커야 합니다.")
    return (sell_price - buy_price) / buy_price


try:
    print(calculate_return(0, 110))
except ValueError as error:
    print(f"계산할 수 없습니다: {error}")
```

예외 클래스만 전달하면 기본 생성자를 호출하고, 메시지를 전달하면 예외 객체에 설명을 저장합니다.

```python
# raise ValueError
# raise ValueError("가격이 잘못되었습니다.")
```

입력값을 검사하는 함수는 잘못된 값을 조용히 처리하기보다, 호출자에게 어떤 문제가 있는지 알려주기 위해 적절한 예외를 발생시키는 것이 좋습니다.

### 예외 다시 발생시키기

예외를 잠시 기록하거나 일부 처리한 뒤 원래 예외를 다시 발생시키려면 인자 없는 `raise`를 사용합니다.

```python
def load_price(path):
    try:
        with open(path, encoding="utf-8") as file:
            return float(file.read())
    except (OSError, ValueError) as error:
        print(f"가격 파일 처리 실패: {error}")
        raise
```

이 함수의 호출자는 원래 예외를 계속 전달받으므로 필요에 따라 최종 처리나 로깅을 할 수 있습니다.

---

## 10. 예외 연결하기

하나의 예외를 다른 의미의 예외로 바꾸면서 원래 원인도 보존하고 싶을 때 `raise ... from ...`을 사용합니다.

```python
def load_market_price(path):
    try:
        with open(path, encoding="utf-8") as file:
            return float(file.read())
    except (OSError, ValueError) as error:
        raise RuntimeError("시장 가격을 불러오지 못했습니다.") from error


try:
    load_market_price("missing-price.txt")
except RuntimeError as error:
    print(error)
```

traceback에는 새로운 `RuntimeError`와 그 원인이 된 `FileNotFoundError` 또는 `ValueError`가 함께 표시됩니다. 하위 계층의 기술적인 오류를 상위 계층의 의미 있는 오류로 변환할 때 유용합니다.

자동 예외 연결을 표시하지 않으려면 `from None`을 사용할 수 있습니다.

```python
try:
    int("not a number")
except ValueError:
    raise RuntimeError("가격 입력을 처리할 수 없습니다.") from None
```

다만 원인 정보가 사라질 수 있으므로 꼭 필요한 경우에만 사용하세요.

---

## 11. 사용자 정의 예외

프로그램의 도메인에 맞는 오류를 표현하려면 `Exception`을 상속한 클래스를 만들 수 있습니다. 일반적으로 예외 클래스 이름은 `Error`로 끝냅니다.

```python
class TradingError(Exception):
    """거래 처리 중 발생하는 기본 예외입니다."""


class InsufficientBalanceError(TradingError):
    """잔액이 부족할 때 발생합니다."""


class InvalidOrderError(TradingError):
    """주문 정보가 잘못되었을 때 발생합니다."""
```

사용자 정의 예외를 사용하면 호출자가 일반 오류와 거래 오류를 구분할 수 있습니다.

```python
def place_order(balance, amount):
    if amount <= 0:
        raise InvalidOrderError("주문 금액은 0보다 커야 합니다.")
    if amount > balance:
        raise InsufficientBalanceError("잔액이 부족합니다.")
    return "주문이 접수되었습니다."


try:
    print(place_order(10_000, 20_000))
except InsufficientBalanceError as error:
    print(f"잔액 오류: {error}")
except InvalidOrderError as error:
    print(f"주문 오류: {error}")
```

예외 클래스에 추가 속성을 넣으면 오류에 필요한 정보를 함께 전달할 수 있습니다.

```python
class InsufficientBalanceError(TradingError):
    def __init__(self, balance, required):
        self.balance = balance
        self.required = required
        super().__init__(
            f"잔액 {balance:,}원이 필요 금액 {required:,}원보다 부족합니다."
        )


try:
    raise InsufficientBalanceError(10_000, 20_000)
except InsufficientBalanceError as error:
    print(error)
    print(error.balance, error.required)
```

---

## 12. 여러 개의 관련 없는 예외 처리하기

여러 작업을 동시에 수행하거나 여러 검사를 한꺼번에 모을 때는 오류가 하나만 발생하지 않을 수 있습니다. Python 3.11부터 `ExceptionGroup`으로 여러 예외를 하나의 예외 그룹에 담을 수 있습니다.

```python
def validate_markets():
    errors = [
        ValueError("BTC 가격이 없습니다."),
        TypeError("ETH 가격 형식이 잘못되었습니다."),
    ]
    raise ExceptionGroup("시장 데이터 검증 실패", errors)


try:
    validate_markets()
except ExceptionGroup as error:
    print(f"검증 오류 개수: {len(error.exceptions)}")
```

`except*`를 사용하면 그룹 안의 예외 종류별로 선택해서 처리할 수 있습니다.

```python
try:
    raise ExceptionGroup(
        "주문 검증 실패",
        [ValueError("가격 오류"), TypeError("수량 형식 오류")],
    )
except* ValueError as error_group:
    print("가격 관련 오류를 처리했습니다.")
except* TypeError as error_group:
    print("수량 형식 오류를 처리했습니다.")
```

`ExceptionGroup`과 `except*`는 여러 작업의 결과를 모아서 보고해야 하는 고급 기능입니다. 일반적인 단일 작업에서는 먼저 `try`/`except`로 충분한지 판단하세요.

---

## 13. 예외에 추가 정보 기록하기

Python 3.11부터 예외 객체에 `add_note()`로 추가 설명을 기록할 수 있습니다. 예외를 다시 발생시키면서 처리 과정의 문맥을 덧붙일 때 사용합니다.

```python
try:
    raise ValueError("가격을 숫자로 변환할 수 없습니다.")
except ValueError as error:
    error.add_note("파일: markets.json")
    error.add_note("항목: BTC.price")
    raise
```

최종 traceback에는 원래 예외 메시지와 추가한 메모가 함께 표시됩니다. 예외의 종류나 기본 메시지를 바꾸지 않고, 어느 파일과 항목에서 문제가 발생했는지 보충할 수 있습니다.

---

## 14. 예외 처리 설계 원칙

예외 처리를 작성할 때는 다음 원칙을 지키는 것이 좋습니다.

1. 예상할 수 있는 예외만 구체적으로 처리합니다.
2. `except Exception:`을 무조건 사용해 오류를 숨기지 않습니다.
3. 예외 메시지를 출력한 뒤 아무 일도 없었던 것처럼 계속 진행하지 않습니다.
4. 오류를 복구할 수 없다면 `raise`로 상위 코드에 전달합니다.
5. 파일이나 연결처럼 정리가 필요한 자원에는 `with`를 사용합니다.
6. 오류의 의미가 달라지는 계층에서는 `raise ... from ...`으로 원인을 보존합니다.
7. 입력값 검증 함수는 잘못된 값에 대해 명확한 예외를 발생시킵니다.
8. 예외 메시지에는 문제를 해결하는 데 필요한 값이나 위치를 포함합니다.

```python
def calculate_fee(amount, fee_rate):
    if amount < 0:
        raise ValueError(f"거래 금액은 음수일 수 없습니다: {amount}")
    if not 0 <= fee_rate <= 1:
        raise ValueError(f"수수료율 범위가 잘못되었습니다: {fee_rate}")
    return amount * fee_rate
```

예외 처리는 오류를 없애는 기능이 아니라, 오류를 예상 가능한 방식으로 전달하고 복구하는 기능입니다.

---

## ✅ 이번 챕터 요약 과제

1. 사용자가 입력한 가격을 `float`로 변환하고, 잘못된 입력에는 `ValueError` 메시지를 출력하세요.
2. 존재하지 않는 JSON 파일을 열 때 `FileNotFoundError`를 처리하세요.
3. 가격 계산 함수에서 0 이하의 매수가가 들어오면 `ValueError`를 발생시키세요.
4. `try`, `except`, `else`, `finally`를 모두 사용해 거래 처리 흐름을 작성하세요.
5. `TradingError`를 상속한 `InsufficientBalanceError`를 만들고 잔액 부족 상황을 처리하세요.
6. 파일 읽기 오류를 `RuntimeError`로 변환하고 `raise ... from ...`으로 원인을 연결하세요.
7. `ExceptionGroup`에 여러 데이터 검증 오류를 담고 `except*`로 종류별 처리 결과를 출력하세요.
8. 처리한 예외에 파일 이름과 코인 심볼 정보를 `add_note()`로 추가하세요.

---

## 참고 자료

- [Python 공식 문서: Errors and Exceptions](https://docs.python.org/3/tutorial/errors.html)
- [Python 공식 문서: Built-in Exceptions](https://docs.python.org/3/library/exceptions.html)
- [Python 공식 문서: Exception Groups](https://docs.python.org/3/library/exceptions.html#exception-groups)

다음 장에서는 Python 클래스를 정의하고 객체 지향 프로그래밍의 기본 개념을 배웁니다.
