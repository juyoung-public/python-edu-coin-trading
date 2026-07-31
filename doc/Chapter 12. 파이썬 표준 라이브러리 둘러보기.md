# Chapter 12. 파이썬 표준 라이브러리 둘러보기

Python은 설치할 때 다양한 기능을 기본 라이브러리로 함께 제공합니다. 운영체제와 파일을 다루고, 날짜를 계산하고, 정규 표현식으로 문자열을 찾고, 압축과 테스트까지 수행할 수 있습니다.

이번 장에서는 Python 공식 튜토리얼의 [Brief tour of the standard library](https://docs.python.org/3/tutorial/stdlib.html)를 바탕으로 다음 내용을 학습합니다.

- 운영체제 인터페이스: `os`, `shutil`, `pathlib`
- 파일 목록 검색: `glob`
- 명령줄 인자: `sys.argv`, `argparse`
- 오류 출력과 프로그램 종료: `sys.stderr`, `sys.exit()`
- 문자열 패턴 검색: `re`
- 수학과 통계: `math`, `random`, `statistics`
- 인터넷 접근: `urllib.request`
- 날짜와 시간: `datetime`
- 데이터 압축: `zlib`, `zipfile`
- 성능 측정: `timeit`
- 품질 관리: `doctest`, `unittest`
- Python의 “배터리 포함” 철학

표준 라이브러리는 별도의 `pip install` 없이 Python 설치만으로 사용할 수 있습니다.

---

## 1. 운영체제 인터페이스: `os`

`os` 모듈은 현재 작업 디렉터리, 환경 변수, 운영체제 기능에 접근할 때 사용합니다.

```python
import os

print("현재 작업 디렉터리:", os.getcwd())
print("운영체제 이름:", os.name)
print("Python 경로:", os.environ.get("PATH", "")[:80])
```

현재 디렉터리를 변경할 때는 `os.chdir()`를 사용합니다. 다만 프로그램의 전체 경로가 바뀌어 이후 파일 작업에 혼동이 생길 수 있으므로, 경로 객체를 직접 조합하는 `pathlib`을 자주 사용하는 편이 좋습니다.

환경 변수는 프로그램 설정을 외부에서 주입할 때 유용합니다.

```python
api_environment = os.environ.get("TRADING_ENV", "development")
print(f"실행 환경: {api_environment}")
```

민감한 API 키나 비밀번호를 소스 코드에 직접 쓰지 않고 환경 변수로 관리할 수 있습니다. 실제 거래 프로그램에서는 키를 로그나 화면에 출력하지 않도록 주의해야 합니다.

### `pathlib`로 경로 다루기

Python 공식 튜토리얼은 `os`를 소개하지만, 현대 Python 코드에서는 객체 방식의 `pathlib`도 자주 사용합니다.

```python
from pathlib import Path

project_dir = Path.cwd()
doc_dir = project_dir / "doc"

print(project_dir)
print(doc_dir)
print(doc_dir.exists())
```

운영체제별 경로 구분자를 직접 문자열로 조합하는 대신 `/` 연산자로 경로를 합치면 Windows와 Unix 계열에서 모두 읽기 쉬운 코드가 됩니다.

### `shutil`로 파일 작업하기

`shutil`은 파일 복사, 이동, 디렉터리 작업을 위한 높은 수준의 인터페이스를 제공합니다.

```python
import shutil

print(shutil.which("python"))
```

`shutil.copyfile()`이나 `shutil.move()`를 사용할 때는 원본과 대상 경로를 정확히 확인해야 합니다. 교육용 코드에서는 실제 프로젝트 파일을 덮어쓰지 않도록 임시 디렉터리에서 테스트하세요.

---

## 2. 파일 목록 검색: `glob`

`glob`은 와일드카드 패턴으로 파일 목록을 찾습니다.

```python
import glob

python_files = glob.glob("src/*.py")
for path in python_files:
    print(path)
```

주요 패턴은 다음과 같습니다.

- `*`: 길이에 관계없이 모든 문자열
- `?`: 한 글자
- `[abc]`: 괄호 안 문자 중 하나

하위 디렉터리까지 검색하려면 `recursive=True`와 `**`를 사용할 수 있습니다.

```python
all_markdown = glob.glob("**/*.md", recursive=True)
print(f"Markdown 파일 수: {len(all_markdown)}")
```

단순한 파일 이름 검색에는 `glob`, 경로를 객체로 다루며 상세하게 순회할 때는 `pathlib.Path.glob()`을 사용할 수 있습니다.

```python
from pathlib import Path

for path in Path("doc").glob("*.md"):
    print(path.name)
```

---

## 3. 명령줄 인자: `sys.argv`

실행할 때 값을 전달하는 스크립트의 인자는 `sys.argv` 리스트에 저장됩니다. 첫 번째 항목은 실행 파일 이름입니다.

```python
import sys

print("실행 파일:", sys.argv[0])
print("전달된 인자:", sys.argv[1:])
```

다음처럼 실행하면 인자가 문자열로 전달됩니다.

```bash
python price_report.py BTC 105000000
```

`sys.argv`에서 숫자를 사용하려면 직접 변환해야 합니다.

```python
import sys

symbol = sys.argv[1] if len(sys.argv) > 1 else "BTC"
price_text = sys.argv[2] if len(sys.argv) > 2 else "0"
price = float(price_text)

print(f"{symbol}: {price:,.0f}원")
```

인자가 많거나 선택 옵션이 필요하면 `argparse`를 사용하는 것이 좋습니다.

### `argparse`

```python
import argparse

parser = argparse.ArgumentParser(description="코인 가격을 표시합니다.")
parser.add_argument("symbol", help="코인 심볼")
parser.add_argument("--price", type=float, default=0, help="현재 가격")
args = parser.parse_args()

print(f"{args.symbol}: {args.price:,.0f}원")
```

`argparse`는 도움말, 타입 변환, 필수 인자, 기본값을 자동으로 처리합니다. 실제 스크립트에서는 `sys.argv`를 직접 해석하기보다 `argparse`를 사용하면 오류가 줄어듭니다.

---

## 4. 오류 출력과 프로그램 종료

`sys.stdout`은 일반 출력, `sys.stderr`는 오류와 경고를 출력하는 스트림입니다.

```python
import sys

print("정상 결과입니다.")
sys.stderr.write("경고: 가격 데이터가 오래되었습니다.\n")
```

출력과 오류를 서로 다른 파일로 리다이렉트할 수 있어 배치 작업이나 서버 로그에 유용합니다.

프로그램을 종료하려면 `sys.exit()`을 사용합니다.

```python
import sys

price = -1
if price < 0:
    sys.stderr.write("가격은 음수일 수 없습니다.\n")
    # 실제 스크립트에서 종료하려면 다음 줄을 사용합니다.
    # sys.exit(1)

print("검증을 계속합니다.")
```

`sys.exit(0)`은 일반적인 정상 종료, 0이 아닌 값은 오류 종료를 나타내는 관례로 사용합니다. 라이브러리 함수에서는 프로그램 전체를 종료하기보다 예외를 발생시키는 것이 좋습니다.

---

## 5. 문자열 패턴 검색: `re`

간단한 문자열 검색에는 `in`, `find()`, `replace()` 같은 문자열 메서드가 읽기 쉽습니다.

```python
message = "BTC price increased"
print("BTC" in message)
print(message.replace("increased", "changed"))
```

복잡한 패턴을 찾을 때는 정규 표현식 모듈인 `re`를 사용합니다.

```python
import re

text = "BTC:105000000 ETH:3500000 XRP:800"
prices = re.findall(r"[A-Z]+:\d+", text)
print(prices)
```

자주 사용하는 정규 표현식 기호는 다음과 같습니다.

- `\d`: 숫자 한 글자
- `\w`: 문자, 숫자, 밑줄
- `+`: 앞 패턴이 한 번 이상 반복
- `*`: 앞 패턴이 0번 이상 반복
- `[]`: 문자 집합
- `^`, `$`: 문자열의 시작과 끝

그룹을 사용하면 필요한 부분을 추출할 수 있습니다.

```python
import re

record = "symbol=BTC price=105000000"
match = re.search(r"symbol=(\w+) price=(\d+)", record)

if match:
    symbol, price = match.groups()
    print(symbol, int(price))
```

정규 표현식은 강력하지만 복잡해지면 읽기 어려워집니다. 단순한 작업에는 문자열 메서드를 우선 사용하세요.

---

## 6. 수학: `math`

`math`는 부동소수점 계산을 위한 C 라이브러리 함수를 제공합니다.

```python
import math

print(math.pi)
print(math.sqrt(16))
print(math.cos(math.pi / 4))
print(math.log(1024, 2))
```

가격 계산에서 반올림이나 올림이 필요할 때도 사용할 수 있습니다.

```python
price = 105.67
print(math.floor(price))
print(math.ceil(price))
print(math.isclose(0.1 + 0.2, 0.3))
```

부동소수점은 표현 방식 때문에 정확히 같은 값 비교가 어려울 수 있으므로, 오차를 허용하는 비교에는 `math.isclose()`를 고려합니다.

### 난수: `random`

`random`은 모의 데이터나 테스트용 무작위 선택에 사용합니다.

```python
import random

random.seed(42)
print(random.choice(["BTC", "ETH", "XRP"]))
print(random.sample(range(100), 5))
print(random.randrange(6))
print(random.random())
```

`seed()`를 지정하면 같은 실행에서 같은 난수 순서를 재현할 수 있어 테스트에 유용합니다. `random`은 보안용 난수나 실제 인증 토큰 생성에 사용하면 안 됩니다.

### 통계: `statistics`

```python
import statistics

returns = [1.2, -0.5, 2.1, 0.8, -1.0]

print(statistics.mean(returns))
print(statistics.median(returns))
print(statistics.pvariance(returns))
```

기본 통계 계산에는 `statistics`를 사용할 수 있습니다. 대규모 수치 분석이나 고급 금융 계산에는 별도의 전문 라이브러리가 필요할 수 있지만, 간단한 실습에는 표준 모듈로 충분합니다.

---

## 7. 인터넷 접근: `urllib.request`

`urllib.request`는 URL에서 데이터를 읽을 수 있는 표준 모듈입니다. 다음 예제는 공개된 Python 문서의 응답 헤더를 읽습니다.

```python
from urllib.request import urlopen

url = "https://docs.python.org/3/"

with urlopen(url, timeout=10) as response:
    print("상태 코드:", response.status)
    print("콘텐츠 유형:", response.headers.get("Content-Type"))
```

응답 본문은 `bytes`로 읽히므로 텍스트로 사용하려면 디코딩합니다.

```python
from urllib.request import urlopen

with urlopen("https://docs.python.org/3/", timeout=10) as response:
    for line in response:
        text = line.decode("utf-8", errors="replace")
        if "Python" in text:
            print(text.strip())
            break
```

네트워크 요청에는 항상 timeout을 지정하고, 오류와 응답 상태를 처리해야 합니다. 거래 API를 호출할 때는 인증, 요청 제한, 네트워크 오류, 응답 검증을 추가로 고려해야 합니다.

SMTP 메일 전송도 표준 라이브러리의 `smtplib`로 가능하지만, 실제 메일 서버 설정이 필요하므로 여기서는 다루지 않습니다.

---

## 8. 날짜와 시간: `datetime`

`datetime`은 날짜와 시간의 생성, 포맷팅, 계산을 지원합니다.

```python
from datetime import date, datetime, timedelta

today = date.today()
now = datetime.now()

print(today)
print(now)
print(today + timedelta(days=7))
```

날짜와 시간은 타임존을 고려해야 하는 경우가 많습니다. 서버와 거래소의 시간 기준이 다를 수 있으므로 실제 데이터 분석에서는 시간대 정보를 명시적으로 관리하세요.

문자열과 날짜 사이를 변환할 때는 `strftime()`과 `strptime()`을 사용합니다.

```python
from datetime import datetime

now = datetime.now()
formatted = now.strftime("%Y-%m-%d %H:%M:%S")
print(formatted)

parsed = datetime.strptime("2026-07-31 09:30:00", "%Y-%m-%d %H:%M:%S")
print(parsed)
```

자주 쓰는 포맷 코드는 다음과 같습니다.

- `%Y`: 네 자리 연도
- `%m`: 월
- `%d`: 일
- `%H`: 24시간 형식의 시
- `%M`: 분
- `%S`: 초

두 날짜를 빼면 `timedelta`가 반환됩니다.

```python
from datetime import date

start = date(2026, 7, 1)
end = date(2026, 7, 31)
print((end - start).days)
```

---

## 9. 데이터 압축: `zlib`와 `zipfile`

`zlib`은 바이트 데이터를 압축하고 복원합니다.

```python
import zlib

raw_data = b"BTC,105000000\nETH,3500000\n" * 10
compressed = zlib.compress(raw_data)
restored = zlib.decompress(compressed)

print(len(raw_data))
print(len(compressed))
print(restored == raw_data)
print(zlib.crc32(raw_data))
```

텍스트를 압축할 때는 먼저 인코딩해 바이트로 만들고, 복원한 뒤 다시 디코딩합니다.

```python
import zlib

text = "코인 가격 데이터입니다." * 10
compressed = zlib.compress(text.encode("utf-8"))
restored_text = zlib.decompress(compressed).decode("utf-8")

print(restored_text == text)
```

여러 파일을 하나의 ZIP 파일로 묶을 때는 `zipfile`을 사용합니다.

```python
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

source = Path("sample_prices.txt")
source.write_text("BTC,105000000\nETH,3500000\n", encoding="utf-8")

with ZipFile("sample_prices.zip", "w", compression=ZIP_DEFLATED) as archive:
    archive.write(source, arcname=source.name)

with ZipFile("sample_prices.zip") as archive:
    print(archive.namelist())
```

실습 후 생성된 `sample_prices.txt`와 `sample_prices.zip`은 필요하면 삭제하세요. 압축 파일에 외부에서 받은 파일을 넣거나 풀 때는 경로 조작으로 원하지 않는 위치에 파일이 생성되지 않는지 확인해야 합니다.

---

## 10. 성능 측정: `timeit`

두 구현 방식의 성능을 비교할 때는 단순히 한 번 실행한 시간을 보는 것보다 `timeit`을 사용하는 것이 좋습니다.

```python
import timeit

loop_time = timeit.timeit(
    "result = []\nfor value in range(100):\n    result.append(value * value)",
    number=1_000,
)
comprehension_time = timeit.timeit(
    "result = [value * value for value in range(100)]",
    number=1_000,
)

print(f"반복문: {loop_time:.5f}초")
print(f"컴프리헨션: {comprehension_time:.5f}초")
```

실행 시간은 Python 버전, 컴퓨터, 현재 부하에 따라 달라집니다. `timeit` 결과를 절대적인 성능 순위로 받아들이기보다 같은 환경에서 여러 구현을 비교하는 자료로 사용하세요.

큰 프로그램의 어느 함수가 느린지 찾을 때는 `profile`과 `pstats`를 사용할 수 있습니다.

---

## 11. 품질 관리: `doctest`

`doctest`는 독스트링 안에 작성한 대화형 예제를 실제로 실행해 결과가 맞는지 확인합니다.

```python
import doctest


def average(values):
    """숫자 목록의 평균을 반환합니다.

    >>> average([20, 30, 70])
    40.0
    >>> average([1, 5, 7])
    4.333333333333333
    """
    return sum(values) / len(values)


result = doctest.testmod()
print(result)
```

독스트링이 문서이면서 테스트가 되므로 예제와 구현이 어긋나는 문제를 줄일 수 있습니다. 함수가 많아지면 별도의 테스트 파일을 사용하는 `unittest`가 더 적합합니다.

### `unittest`

```python
import unittest


def calculate_fee(amount, fee_rate=0.0004):
    return amount * fee_rate


class TestTradingFunctions(unittest.TestCase):
    def test_fee(self):
        self.assertEqual(calculate_fee(10_000), 4.0)

    def test_invalid_amount(self):
        with self.assertRaises(ValueError):
            if -1 < 0:
                raise ValueError("금액은 음수일 수 없습니다.")


suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestTradingFunctions)
result = unittest.TextTestRunner(verbosity=0).run(suite)
print(f"성공: {result.wasSuccessful()}")
```

실제 프로젝트에서는 테스트 함수가 끝난 뒤 `unittest.main()`을 명령줄에서 실행하는 방식도 사용할 수 있습니다. 노트북에서는 현재처럼 테스트 스위트를 직접 실행하는 편이 편리합니다.

---

## 12. 배터리 포함 철학

Python은 자주 필요한 기능을 표준 라이브러리로 넓게 제공합니다. 이를 “batteries included” 철학이라고 부릅니다.

예를 들어 다음 기능들이 기본으로 포함됩니다.

- `json`, `csv`: 데이터 교환과 표 형식 파일
- `sqlite3`: 별도 서버 없이 사용하는 SQLite 데이터베이스
- `xml.etree.ElementTree`: XML 처리
- `email`: 이메일 메시지 생성과 해석
- `urllib`: 인터넷 프로토콜 접근
- `logging`: 프로그램 로그 관리
- `unittest`, `doctest`: 테스트
- `locale`, `gettext`: 국제화

표준 라이브러리의 모듈을 먼저 확인하면 작은 작업을 위해 외부 패키지를 추가로 설치하지 않아도 됩니다. 다만 데이터 분석, 시각화, 머신러닝처럼 전문 영역에서는 프로젝트 목적에 맞는 외부 라이브러리를 사용하는 것이 합리적입니다.

---

## 13. 코인 프로젝트에 적용하기

표준 라이브러리만 이용해 가격 기록을 탐색하고 평균과 최신 시간을 표시하는 작은 함수를 만들어 보겠습니다.

```python
from datetime import datetime
from statistics import mean
from pathlib import Path
import re


def summarize_price_file(path):
    path = Path(path)
    prices = []

    for line in path.read_text(encoding="utf-8").splitlines():
        match = re.fullmatch(r"([A-Z]+),([0-9.]+)", line.strip())
        if match:
            symbol, price_text = match.groups()
            prices.append((symbol, float(price_text)))

    if not prices:
        return {"count": 0, "average": None, "checked_at": datetime.now()}

    return {
        "count": len(prices),
        "average": mean(price for _, price in prices),
        "checked_at": datetime.now(),
    }


sample_path = Path("price_records.txt")
sample_path.write_text(
    "BTC,105000000\nETH,3500000\nXRP,800\n",
    encoding="utf-8",
)
print(summarize_price_file(sample_path))
```

이 예제는 `pathlib`, `re`, `statistics`, `datetime`을 한 프로그램에서 조합합니다. 각 모듈은 한 가지 역할에 집중하고, 함수는 그 기능을 연결합니다.

---

## ✅ 이번 챕터 요약 과제

1. `pathlib`과 `glob`을 이용해 `doc` 폴더의 Markdown 파일 목록을 출력하세요.
2. `argparse`를 사용해 코인 심볼과 가격을 입력받는 스크립트를 작성하세요.
3. 정규 표현식으로 `SYMBOL,PRICE` 형식의 가격 기록만 추출하세요.
4. `statistics`로 수익률의 평균, 중앙값, 분산을 계산하세요.
5. `datetime`으로 백테스팅 시작일과 종료일 사이의 날짜 수를 계산하세요.
6. 가격 데이터 문자열을 `zlib`으로 압축했다가 복원하세요.
7. `timeit`으로 일반 반복문과 리스트 컴프리헨션의 실행 시간을 비교하세요.
8. `doctest` 또는 `unittest`로 수수료 계산 함수를 테스트하세요.
9. 표준 라이브러리에서 거래 기록을 JSON, CSV, SQLite 중 하나로 저장하는 방법을 조사해 보세요.

---

## 참고 자료

- [Python 공식 문서: Brief tour of the standard library](https://docs.python.org/3/tutorial/stdlib.html)
- [Python 공식 문서: Python Standard Library](https://docs.python.org/3/library/)
- [Python 공식 문서: Module Index](https://docs.python.org/3/py-modindex.html)

다음 장에서는 Python 표준 라이브러리의 네트워크, 파일 형식, 동시성 관련 기능을 더 살펴봅니다.
