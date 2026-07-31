# Chapter 09. 파이썬 입출력과 데이터 저장

프로그램은 계산한 결과를 화면에 보여주고, 사용자가 입력한 데이터를 읽고, 필요한 결과를 파일에 저장해야 합니다. Python은 문자열 포맷팅과 파일 객체를 이용해 이런 입출력 작업을 간단하게 처리할 수 있습니다.

이번 장에서는 Python 공식 튜토리얼의 [Input and Output](https://docs.python.org/3/tutorial/inputoutput.html)을 바탕으로 다음 내용을 학습합니다.

- `str()`와 `repr()`의 차이
- f-string으로 출력 형식 지정하기
- `str.format()` 사용하기
- 수동 문자열 정렬과 `zfill()`
- `print()`의 `sep`, `end` 사용하기
- 파일 열기 모드와 인코딩
- `with open()`으로 파일 읽고 쓰기
- `read()`, `readline()`, `readlines()`, 파일 반복
- `seek()`, `tell()`로 파일 위치 다루기
- JSON으로 리스트와 딕셔너리 저장하기

예제는 코인 가격과 거래 기록을 화면에 출력하고 파일로 저장하는 흐름으로 구성했습니다.

---

## 1. 화면에 값 출력하기

가장 간단한 출력 방법은 표현식과 `print()` 함수입니다.

```python
symbol = "BTC"
price = 105_000_000

print(symbol)
print(price)
print("거래 대상:", symbol, "현재 가격:", price)
```

`print()`는 여러 인자를 전달하면 기본적으로 공백으로 구분하고, 마지막에 줄바꿈을 추가합니다.

```python
print("BTC", "ETH", "XRP")
print("BTC", "ETH", "XRP", sep=" / ")
print("다음 줄로", end="")
print("이어집니다.")
```

- `sep`: 여러 인자 사이에 넣을 문자열입니다.
- `end`: 모든 인자를 출력한 뒤 마지막에 넣을 문자열입니다.

로그나 표를 출력할 때 `sep`와 `end`를 활용하면 문자열을 직접 이어 붙이는 일을 줄일 수 있습니다.

---

## 2. `str()`와 `repr()`

`str()`와 `repr()`은 값을 문자열로 표현하지만 목적이 다릅니다.

- `str()`: 사람이 읽기 쉬운 표현을 만듭니다.
- `repr()`: 개발자가 값의 자료형과 내용을 파악하기 좋은 표현을 만듭니다.

```python
message = "Hello, world.\n"

print(str(message))
print(repr(message))
```

`repr()` 결과에서는 줄바꿈 문자가 실제 줄바꿈이 아니라 `\n`으로 보이고 문자열을 나타내는 따옴표도 표시됩니다.

```python
value = ("BTC", 105_000_000)

print(str(value))
print(repr(value))
```

리스트, 튜플, 딕셔너리처럼 구조를 가진 값은 두 함수의 결과가 비슷해 보일 수 있습니다. 문자열 안의 특수문자나 공백을 정확히 확인해야 할 때 `repr()`이 특히 유용합니다.

---

## 3. f-string으로 출력 형식 지정하기

f-string은 문자열 앞에 `f`를 붙이고 중괄호 `{}` 안에 Python 표현식을 작성하는 방식입니다.

```python
symbol = "BTC"
price = 105_000_000
change_rate = 2.35

print(f"{symbol} 가격은 {price}원이고 변동률은 {change_rate}%입니다.")
```

중괄호 안에는 변수뿐 아니라 계산식과 함수 호출도 사용할 수 있습니다.

```python
buy_price = 100
sell_price = 110

print(f"수익률: {(sell_price - buy_price) / buy_price:.2%}")
```

`:.2%`는 값을 백분율로 바꾸고 소수점 둘째 자리까지 표시합니다.

### 숫자 형식 지정

콜론 뒤에 형식 지정자를 쓰면 자릿수, 소수점, 정렬 등을 제어할 수 있습니다.

```python
price = 105_000_000
volume = 1234.5678

print(f"가격: {price:,}원")
print(f"거래량: {volume:.2f}")
print(f"가격: {price:15,d}원")
```

- `,`: 천 단위 구분 기호를 표시합니다.
- `.2f`: 소수점 이하 2자리까지 표시합니다.
- `15`: 최소 필드 너비를 15칸으로 지정합니다.
- `d`: 정수를 표시합니다.

표 형태로 여러 코인을 출력할 때 최소 너비를 지정하면 열을 맞출 수 있습니다.

```python
prices = {"BTC": 105_000_000, "ETH": 3_500_000, "XRP": 800}

for symbol, price in prices.items():
    print(f"{symbol:>4} | {price:>12,d}원")
```

`>`는 오른쪽 정렬, `<`는 왼쪽 정렬, `^`는 가운데 정렬입니다.

### 표현식과 디버깅 출력

f-string의 `=` 지정자를 사용하면 표현식과 결과를 함께 출력할 수 있습니다.

```python
price = 105_000_000
fee_rate = 0.0004

print(f"{price=}, {fee_rate=}")
print(f"{price * fee_rate=}")
```

문자열 표현이나 디버깅이 필요할 때는 `!r`을 사용할 수 있습니다.

```python
symbol = "BTC"
print(f"일반 출력: {symbol}")
print(f"repr 출력: {symbol!r}")
```

---

## 4. `str.format()` 메서드

f-string 이전부터 사용된 `str.format()`은 문자열의 `{}` 위치에 전달한 값을 넣습니다.

```python
print("{} 가격은 {}원입니다.".format("BTC", 105_000_000))
```

중괄호 안에 위치 번호를 지정할 수 있습니다.

```python
print("{0}에서 {1}로 변경되었습니다.".format("BTC", "ETH"))
print("{1}에서 {0}로 변경되었습니다.".format("BTC", "ETH"))
```

키워드 인자를 사용하면 이름으로 값을 지정할 수 있어 긴 문자열에서 의미가 더 분명합니다.

```python
print(
    "{symbol}의 가격은 {price:,}원입니다.".format(
        symbol="BTC",
        price=105_000_000,
    )
)
```

딕셔너리를 `**`로 풀어 키워드 인자로 전달할 수도 있습니다.

```python
market = {"symbol": "BTC", "price": 105_000_000}
message = "{symbol}의 가격은 {price:,}원입니다."

print(message.format(**market))
```

숫자 형식 지정 방법은 f-string과 비슷합니다.

```python
for number in range(1, 4):
    print("{0:2d}의 제곱은 {1:3d}입니다.".format(number, number ** 2))
```

새 코드에서는 표현식이 가까이 있어 읽기 쉬운 f-string을 자주 사용하지만, 이미 만들어진 템플릿이나 외부에서 받은 형식 문자열에는 `format()`이 편리할 수 있습니다.

---

## 5. 수동 문자열 포맷팅

문자열 메서드를 이용해 직접 열 너비를 정할 수도 있습니다.

```python
for number in range(1, 4):
    square = str(number ** 2).rjust(3)
    cube = str(number ** 3).rjust(4)
    print(str(number).rjust(2), square, cube)
```

- `rjust(width)`: 왼쪽을 공백으로 채워 오른쪽 정렬합니다.
- `ljust(width)`: 오른쪽을 공백으로 채워 왼쪽 정렬합니다.
- `center(width)`: 양쪽에 공백을 채워 가운데 정렬합니다.

이 메서드는 원본 문자열을 수정하지 않고 새 문자열을 반환합니다.

```python
label = "BTC"
print(label.rjust(8))
print(label.ljust(8, "-"))
print(label.center(8, "-"))
```

문자열이 지정한 너비보다 길면 잘리지 않고 그대로 반환됩니다. 실제로 자르려면 슬라이스를 함께 사용합니다.

```python
long_label = "BITCOIN"
print(long_label.ljust(5)[:5])
```

### `zfill()`

`zfill(width)`은 숫자 문자열의 왼쪽을 `0`으로 채웁니다. 부호가 있으면 부호 뒤에 0을 넣습니다.

```python
print("12".zfill(5))       # 00012
print("-3.14".zfill(7))   # -003.14
print("3.141592".zfill(5)) # 길이가 이미 길면 그대로
```

---

## 6. 오래된 `%` 문자열 포맷팅

Python에는 `%` 연산자를 사용하는 예전 방식의 문자열 포맷팅도 있습니다.

```python
import math

print("pi는 약 %5.3f입니다." % math.pi)
```

`%s`, `%d`, `%f` 같은 변환 지정자를 사용합니다.

```python
symbol = "BTC"
price = 105_000_000

print("%s 가격은 %d원입니다." % (symbol, price))
```

기존 코드에서 자주 볼 수 있지만, 새 코드에서는 f-string이나 `str.format()`이 더 읽기 쉽고 기능이 풍부합니다.

---

## 7. 파일 열기: `open()`

파일을 읽거나 쓰려면 `open(filename, mode, encoding=...)`을 사용합니다.

```python
file = open("market.txt", "w", encoding="utf-8")
file.write("BTC,105000000\n")
file.close()
```

`close()`를 호출해야 파일이 정상적으로 닫히고 버퍼의 내용이 디스크에 반영됩니다. 하지만 예외가 발생하면 `close()`가 실행되지 않을 수 있으므로 일반적으로 `with` 문을 사용합니다.

### 파일 모드

- `"r"`: 읽기. 기본 모드입니다.
- `"w"`: 쓰기. 기존 파일이 있으면 내용을 지웁니다.
- `"a"`: 이어 쓰기. 기존 내용 끝에 추가합니다.
- `"r+"`: 읽기와 쓰기
- `"b"`: 바이너리 모드. 예: `"rb"`, `"wb"`

텍스트 파일은 `encoding="utf-8"`을 명시하는 것이 좋습니다. Windows와 다른 운영체제에서 기본 인코딩이 다를 수 있기 때문입니다.

바이너리 모드에서는 문자열이 아니라 `bytes`를 읽고 쓰며, `encoding`을 지정할 수 없습니다.

---

## 8. `with open()`으로 파일 안전하게 다루기

`with` 문을 사용하면 블록이 끝날 때 파일이 자동으로 닫힙니다. 중간에 오류가 발생해도 정리 작업이 수행되므로 권장되는 방식입니다.

```python
with open("market.txt", "w", encoding="utf-8") as file:
    file.write("BTC,105000000\n")
    file.write("ETH,3500000\n")
```

블록이 끝난 뒤 파일은 자동으로 닫힙니다.

```python
with open("market.txt", encoding="utf-8") as file:
    content = file.read()

print(content)
```

파일을 직접 열고 닫는 코드보다 짧고 안전합니다.

---

## 9. 파일 읽기 메서드

### `read()`

`read()`는 파일의 전체 내용을 문자열로 반환합니다. 숫자를 전달하면 최대 그만큼의 문자를 읽습니다.

```python
with open("market.txt", encoding="utf-8") as file:
    content = file.read()
    print(content)
```

파일 끝에 도달한 뒤 다시 `read()`를 호출하면 빈 문자열을 반환합니다. 큰 파일 전체를 한 번에 읽으면 메모리를 많이 사용할 수 있으므로 주의하세요.

### `readline()`

`readline()`은 한 줄을 읽습니다. 줄 끝의 `\n`은 보통 결과에 포함됩니다.

```python
with open("market.txt", encoding="utf-8") as file:
    first_line = file.readline()
    second_line = file.readline()

print(repr(first_line))
print(repr(second_line))
```

### 파일 객체 반복하기

파일 객체를 직접 반복하면 한 줄씩 읽을 수 있어 메모리 효율이 좋습니다.

```python
with open("market.txt", encoding="utf-8") as file:
    for line in file:
        print(line, end="")
```

`print()`도 기본적으로 줄바꿈을 넣기 때문에 파일의 줄바꿈이 두 번 출력되지 않도록 `end=""`을 사용했습니다.

### `readlines()`와 `list()`

모든 줄을 리스트로 받고 싶다면 `readlines()`나 `list(file)`을 사용할 수 있습니다.

```python
with open("market.txt", encoding="utf-8") as file:
    lines = file.readlines()

print(lines)
```

줄 끝의 줄바꿈을 제거하고 싶다면 `strip()`을 사용합니다.

```python
with open("market.txt", encoding="utf-8") as file:
    symbols = [line.strip() for line in file]

print(symbols)
```

---

## 10. 파일에 쓰기

`write(string)`은 문자열을 파일에 쓰고, 실제로 작성한 문자 수를 반환합니다.

```python
with open("orders.txt", "w", encoding="utf-8") as file:
    written = file.write("BTC,BUY,10000\n")
    print(f"작성한 문자 수: {written}")
```

문자열이 아닌 값은 먼저 문자열로 변환해야 합니다.

```python
order = ("BTC", "BUY", 10_000)

with open("orders.txt", "a", encoding="utf-8") as file:
    file.write(str(order) + "\n")
```

단순한 텍스트 기록에는 가능하지만, 리스트나 딕셔너리 같은 구조화 데이터를 저장할 때는 JSON을 사용하는 편이 더 좋습니다.

---

## 11. 파일 위치: `tell()`과 `seek()`

`tell()`은 현재 파일 위치를 반환하고, `seek()`은 파일 위치를 이동합니다.

```python
with open("market.txt", encoding="utf-8") as file:
    print(file.tell())
    print(file.read(3))
    print(file.tell())
    file.seek(0)
    print(file.read(3))
```

텍스트 모드의 위치는 단순한 문자 수와 항상 같다고 가정하기보다 `tell()`이 반환한 위치를 `seek()`에 다시 전달하는 방식으로 사용하세요.

바이너리 파일에서는 위치가 바이트 단위로 동작합니다.

```python
with open("data.bin", "wb") as file:
    file.write(b"0123456789")

with open("data.bin", "rb") as file:
    file.seek(5)
    print(file.read(1))  # b'5'
```

이미지나 실행 파일처럼 텍스트가 아닌 파일은 바이너리 모드로 처리해야 합니다.

---

## 12. JSON으로 구조화 데이터 저장하기

문자열은 그대로 파일에 쓸 수 있지만, 리스트와 딕셔너리 같은 복잡한 자료구조를 직접 문자열로 저장하면 다시 복원하기 어렵습니다. JSON은 이런 데이터를 저장하고 다른 언어와 교환하기 위한 대표적인 형식입니다.

Python의 표준 `json` 모듈을 사용합니다.

```python
import json

market = ["BTC", 105_000_000, 2.35]
json_text = json.dumps(market)

print(json_text)
```

Python 객체를 JSON 문자열로 바꾸는 것을 **직렬화(serializing)**라고 합니다. JSON 문자열을 다시 Python 객체로 바꾸는 것은 **역직렬화(deserializing)**입니다.

```python
import json

json_text = '["BTC", 105000000, 2.35]'
market = json.loads(json_text)

print(market)
print(type(market))
```

### `json.dump()`와 `json.load()`

문자열을 중간에 만들지 않고 파일에 바로 저장하려면 `json.dump()`를 사용합니다.

```python
import json

markets = {
    "BTC": {"price": 105_000_000, "change_rate": 2.35},
    "ETH": {"price": 3_500_000, "change_rate": -1.2},
}

with open("markets.json", "w", encoding="utf-8") as file:
    json.dump(markets, file, ensure_ascii=False, indent=2)
```

- `ensure_ascii=False`: 한국어가 유니코드 이스케이프 문자열로 바뀌지 않게 합니다.
- `indent=2`: JSON 파일을 읽기 좋게 들여씁니다.

저장한 JSON 파일은 `json.load()`로 다시 읽습니다.

```python
import json

with open("markets.json", encoding="utf-8") as file:
    markets = json.load(file)

print(markets["BTC"]["price"])
```

JSON 파일은 반드시 UTF-8 인코딩으로 열어야 합니다. JSON은 여러 프로그래밍 언어에서 사용할 수 있다는 장점이 있지만, 모든 Python 객체를 그대로 저장할 수 있는 것은 아닙니다. 날짜 객체나 사용자 정의 클래스는 문자열이나 딕셔너리 같은 JSON 지원 자료형으로 변환해야 합니다.

### JSON과 pickle의 차이

`pickle`은 Python 객체를 더 다양하게 직렬화할 수 있지만 Python에 종속적이며, 신뢰할 수 없는 pickle 데이터를 읽으면 악성 코드가 실행될 수 있습니다. 외부에서 받은 데이터에는 pickle을 사용하지 말고, 서로 다른 프로그램과 데이터를 주고받을 때는 JSON처럼 안전하고 공개된 형식을 우선 고려하세요.

---

## 13. 코인 거래 기록 저장 실습

앞에서 배운 포맷팅과 JSON을 함께 사용해 거래 기록을 저장하고 읽어 보겠습니다.

```python
import json

trade = {
    "symbol": "BTC",
    "side": "buy",
    "price": 105_000_000,
    "quantity": 0.001,
    "fee_rate": 0.0004,
}

print(
    f"{trade['symbol']} {trade['side']} "
    f"가격: {trade['price']:,}원, "
    f"수량: {trade['quantity']:.4f}"
)

with open("trade.json", "w", encoding="utf-8") as file:
    json.dump(trade, file, ensure_ascii=False, indent=2)
```

다시 읽은 뒤 수수료와 총 거래 금액을 계산할 수도 있습니다.

```python
import json

with open("trade.json", encoding="utf-8") as file:
    trade = json.load(file)

gross_amount = trade["price"] * trade["quantity"]
fee = gross_amount * trade["fee_rate"]

print(f"거래 금액: {gross_amount:,.0f}원")
print(f"수수료: {fee:,.0f}원")
```

화면 출력은 사람이 읽기 좋은 f-string으로 만들고, 파일 저장은 JSON으로 처리하면 각각의 목적에 맞는 형식을 사용할 수 있습니다.

---

## ✅ 이번 챕터 요약 과제

1. 여러 코인의 심볼, 가격, 변동률을 f-string으로 표 형태로 출력하세요.
2. 가격을 천 단위 구분 기호와 소수점 형식으로 표시해 보세요.
3. `market.txt` 파일에 코인 가격을 한 줄씩 저장하고 다시 읽어 출력하세요.
4. `with open()`을 사용해 거래 기록을 추가 모드(`"a"`)로 저장하세요.
5. 가격 목록을 JSON 파일로 저장하고 `json.load()`로 다시 불러오세요.
6. JSON 저장 시 `ensure_ascii=False`와 `indent=2`의 동작 차이를 확인하세요.
7. `read()`, `readline()`, 파일 객체 반복 방식으로 같은 파일을 각각 읽어 보세요.
8. 거래 기록 딕셔너리에서 총 거래 금액과 수수료를 계산해 화면과 JSON 파일에 각각 저장하세요.

---

## 참고 자료

- [Python 공식 문서: Input and Output](https://docs.python.org/3/tutorial/inputoutput.html)
- [Python 공식 문서: Built-in `open()`](https://docs.python.org/3/library/functions.html#open)
- [Python 공식 문서: `json` 모듈](https://docs.python.org/3/library/json.html)

다음 장에서는 프로그램 실행 중 발생하는 오류를 이해하고, 예외를 처리하는 방법을 배웁니다.
