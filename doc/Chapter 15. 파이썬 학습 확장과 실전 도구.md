# Chapter 15. 파이썬 학습 확장과 실전 도구

지금까지 Python의 기본 문법, 자료구조, 함수, 모듈, 파일 입출력, 예외, 클래스, 표준 라이브러리, 가상 환경과 패키지 관리를 배웠습니다. 이제 배운 내용을 실제 개발 흐름에 적용하고, Python을 더 효율적으로 사용하는 방법을 살펴볼 차례입니다.

이번 장은 다음 네 공식 문서를 바탕으로 구성했습니다.

- [What Now?](https://docs.python.org/3/tutorial/whatnow.html)
- [Interactive Input Editing and History Substitution](https://docs.python.org/3/tutorial/interactive.html)
- [Floating-Point Arithmetic: Issues and Limitations](https://docs.python.org/3/tutorial/floatingpoint.html)
- [Appendix](https://docs.python.org/3/tutorial/appendix.html)

이번 장에서는 다음 내용을 학습합니다.

- Python 공식 문서를 이용한 다음 학습 경로
- 대화형 인터프리터의 자동 완성, 히스토리, 도움말
- IPython과 다른 대화형 도구
- 부동소수점의 표현 오차와 안전한 비교
- `Decimal`, `Fraction`, `math.isclose()`, `math.fsum()`
- Python 스크립트 실행과 인터프리터 오류 처리
- Unix 실행 권한과 Windows의 `.py` 파일 실행
- `PYTHONSTARTUP`, `sitecustomize`, `usercustomize`

---

## 1. 튜토리얼 이후의 학습 경로

Python 공식 튜토리얼은 문법과 기본 사용법을 익히기 위한 출발점입니다. 그 다음에는 목적에 따라 다음 자료를 찾아보는 것이 좋습니다.

- **표준 라이브러리 문서**: 모듈, 함수, 클래스의 정확한 사용법을 확인합니다.
- **Python 언어 레퍼런스**: 문법과 실행 의미를 깊이 이해합니다.
- **Python Packaging User Guide**: 패키지 제작과 배포 방법을 학습합니다.
- **PyPI**: 다른 개발자가 만든 패키지를 검색합니다.
- **FAQ와 커뮤니티**: 자주 발생하는 문제와 해결 방법을 찾습니다.
- **전문 라이브러리 문서**: 데이터 분석, 시각화, 과학 계산 등 목표에 맞는 도구를 배웁니다.

코인 트레이딩 프로젝트를 계속 발전시키려면 다음 순서로 확장할 수 있습니다.

1. 작은 함수에 테스트를 작성합니다.
2. 가격 수집, 지표 계산, 전략, 주문 처리를 모듈로 분리합니다.
3. 가상 환경과 `requirements.txt`로 실행 환경을 고정합니다.
4. 로그와 예외 처리를 추가합니다.
5. 과거 데이터 백테스트와 모의 주문으로 결과를 검증합니다.
6. API 키와 실제 주문 기능을 추가하기 전에 보안과 위험 제한을 점검합니다.

문서를 읽을 때는 제목만 훑기보다 다음 정보를 확인하세요.

- 함수의 매개변수와 반환값
- 발생할 수 있는 예외
- 버전별 변경 사항
- 입력 자료형과 단위
- 예제 코드와 제한 사항

---

## 2. 대화형 인터프리터 사용하기

Python을 인자 없이 실행하면 대화형 인터프리터(REPL)를 사용할 수 있습니다.

Windows:

```powershell
python
```

macOS/Linux:

```bash
python3
```

프롬프트에서 코드를 입력하고 즉시 결과를 확인할 수 있습니다.

```text
>>> price = 105_000_000
>>> price * 1.05
110250000.0
>>> exit()
```

대화형 모드는 다음 상황에 유용합니다.

- 짧은 표현식의 결과를 확인할 때
- 모듈의 함수 사용법을 시험할 때
- 자료형과 메서드를 탐색할 때
- 정규 표현식이나 포맷 문자열을 실험할 때

반복해서 사용할 코드는 파일이나 노트북에 저장해야 합니다. REPL에만 입력한 정의는 인터프리터를 종료하면 사라집니다.

---

## 3. 탭 자동 완성과 객체 탐색

대화형 인터프리터에서는 Tab 키로 이름과 속성을 자동 완성할 수 있습니다.

```text
>>> import statistics
>>> statistics.me<Tab>
```

실제 터미널에서는 Tab을 누르면 `statistics.mean`, `statistics.median`처럼 가능한 이름이 표시됩니다. 객체 뒤에 점을 입력한 뒤 Tab을 누르면 해당 객체의 속성과 메서드를 탐색할 수 있습니다.

```text
>>> prices = [100, 105, 110]
>>> prices.<Tab>
```

자동 완성은 편리하지만, 속성 조회 과정에서 사용자 정의 `__getattr__()`가 실행될 수 있습니다. 신뢰할 수 없는 객체를 탐색할 때는 부작용이 있는 속성 접근에 주의하세요.

`dir()`은 객체가 제공하는 이름을 목록으로 보여줍니다.

```text
>>> prices = [100, 105, 110]
>>> [name for name in dir(prices) if not name.startswith("_")]
['append', 'clear', 'copy', 'count', 'extend', 'index', 'insert', 'pop', 'remove', 'reverse', 'sort']
```

`help()`는 문서 문자열과 사용법을 보여줍니다.

```text
>>> help(str.split)
```

노트북에서는 `?`나 `help()`를 사용할 수 있고, VS Code에서는 객체 위에 마우스를 올리거나 자동 완성 목록을 확인할 수 있습니다.

---

## 4. 입력 히스토리와 새 대화형 셸

대화형 인터프리터는 입력 히스토리를 저장해 다음 세션에서 다시 사용할 수 있습니다. 기본 히스토리 파일 이름은 보통 사용자 디렉터리의 `.python_history`입니다.

히스토리는 다음 작업을 빠르게 할 때 유용합니다.

- 직전에 실행한 계산을 다시 사용하기
- 긴 함수 호출을 수정해 재실행하기
- 이전에 확인한 변수나 모듈 탐색 명령을 다시 실행하기

Python 3.13부터 새로운 대화형 셸이 기본으로 사용됩니다. 환경에 따라 색상, 여러 줄 편집, 히스토리 탐색, 붙여넣기 모드를 제공합니다.

```powershell
python
```

새 셸에서는 다음 기능을 사용할 수 있습니다.

- F1: 도움말 브라우저
- F2: 명령 히스토리 보기
- F3: 여러 줄 붙여넣기 모드 전환
- `exit` 또는 `quit`: 셸 종료

환경에 따라 새 셸을 사용하지 않으려면 `PYTHON_BASIC_REPL` 환경 변수를 확인할 수 있습니다.

```powershell
$env:PYTHON_BASIC_REPL = "1"
python
```

환경 변수 동작은 Python 버전에 따라 달라질 수 있으므로, 현재 버전의 공식 문서를 확인하세요.

---

## 5. 향상된 대화형 도구

기본 인터프리터 외에도 IPython과 bpython 같은 도구가 있습니다.

- **IPython**: 자동 완성, 객체 탐색, 풍부한 출력, 매직 명령, 노트북과의 연동
- **bpython**: 터미널 안에서의 자동 완성과 간결한 인터페이스
- **Jupyter Notebook**: Markdown 설명, 코드, 출력, 시각화를 하나의 문서에 저장

가상 환경 안에서 IPython을 설치할 수 있습니다.

```powershell
python -m pip install ipython
ipython
```

Jupyter를 사용한다면 다음 명령으로 노트북을 실행합니다.

```powershell
python -m pip install jupyter
jupyter notebook
```

대화형 도구는 탐색과 실험에 유용하지만, 재현 가능한 프로그램은 `.py` 파일과 테스트로 관리하는 것이 좋습니다. 실험 결과를 다른 사람이 다시 실행해야 한다면 입력 데이터, Python 버전, 패키지 버전도 함께 기록하세요.

---

## 6. 부동소수점은 왜 정확하지 않을까?

컴퓨터의 `float`는 일반적으로 이진수 기반의 부동소수점으로 저장됩니다. 십진수 `0.1`은 이진수로 무한히 반복되므로 유한한 비트로 정확히 표현할 수 없습니다.

```python
print(0.1)
print(format(0.1, ".17f"))
print(0.1 + 0.1 + 0.1 == 0.3)
```

화면에 `0.1`이라고 표시되어도 실제 내부에는 `0.1`에 가장 가까운 이진 부동소수점 값이 저장됩니다. 이것은 Python의 버그가 아니라 대부분의 프로그래밍 언어와 하드웨어가 사용하는 표현 방식의 한계입니다.

`repr()`과 `format()`으로 표현 차이를 확인할 수 있습니다.

```python
value = 0.1
print(repr(value))
print(value.as_integer_ratio())
print(value.hex())
```

`as_integer_ratio()`는 저장된 값을 정확한 분수로 나타내고, `hex()`는 저장된 부동소수점 값을 16진수 형태로 보여줍니다.

---

## 7. 부동소수점 비교하기

부동소수점 계산 결과를 `==`로 바로 비교하면 예상과 다를 수 있습니다.

```python
value = 0.1 + 0.1 + 0.1
print(value == 0.3)
```

허용 가능한 오차 안에서 비교하려면 `math.isclose()`를 사용합니다.

```python
import math

value = 0.1 + 0.1 + 0.1
print(math.isclose(value, 0.3))
print(math.isclose(value, 0.3, rel_tol=1e-12, abs_tol=0.0))
```

- `rel_tol`: 상대 오차 허용 범위
- `abs_tol`: 절대 오차 허용 범위

값이 0에 가까운지 확인할 때는 `abs_tol`을 명시하는 것이 도움이 됩니다.

```python
print(math.isclose(0.0000001, 0.0, abs_tol=1e-6))
```

반올림된 표시가 필요하면 `round()`나 형식 지정자를 사용합니다.

```python
import math

print(round(math.pi, 2))
print(f"{math.pi:.2f}")
```

표시를 반올림하는 것과 내부 계산값을 정확한 십진수로 바꾸는 것은 다른 작업입니다. 화면 출력만 필요한 경우에는 반올림으로 충분하지만, 금융 계산의 저장과 비교에는 별도의 자료형을 고려해야 합니다.

---

## 8. `Decimal`과 `Fraction`

정확한 십진수 계산이 필요하면 `Decimal`을 사용합니다.

```python
from decimal import Decimal

float_total = 0.1 + 0.1 + 0.1
Decimal_total = Decimal("0.1") + Decimal("0.1") + Decimal("0.1")

print(float_total)
print(Decimal_total)
print(Decimal_total == Decimal("0.3"))
```

`Decimal`을 만들 때는 `Decimal(0.1)`보다 `Decimal("0.1")`처럼 문자열을 전달하는 것이 좋습니다. 이미 오차가 포함된 float를 Decimal로 변환하면 그 오차까지 가져오기 때문입니다.

```python
from decimal import Decimal

print(Decimal("0.1"))
print(Decimal(0.1))
```

분수 자체를 정확하게 표현하려면 `fractions.Fraction`을 사용합니다.

```python
from fractions import Fraction

third = Fraction(1, 3)
print(third + third + third)
print(third == Fraction(1, 3))
print(Fraction.from_float(0.1))
```

용도별 선택 기준은 다음과 같습니다.

- `float`: 일반적인 과학 계산과 근사값 계산
- `Decimal`: 회계, 수수료, 가격처럼 십진 자릿수가 중요한 계산
- `Fraction`: 분수의 정확한 값과 비율을 유지해야 하는 계산

---

## 9. 합계의 정밀도: `sum()`과 `math.fsum()`

많은 실수를 더하면 반올림 오차가 누적될 수 있습니다.

```python
import math

values = [0.1] * 10
print(sum(values))
print(math.fsum(values))
```

`math.fsum()`은 중간 계산에서 잃어버린 자릿수를 추적해 일반적인 `sum()`보다 정확한 합계를 계산합니다. 대신 계산 비용이 더 클 수 있습니다.

```python
import math

returns = [0.0001, -0.0001, 0.0002, -0.0002]
print(sum(returns))
print(math.fsum(returns))
```

정확한 화폐 계산에는 `Decimal`이 더 적절할 수 있고, 많은 float 측정값의 합계에는 `math.fsum()`이 유용합니다.

---

## 10. 인터프리터 오류 처리

대화형 모드에서 처리되지 않은 예외가 발생하면 traceback이 출력되고, 인터프리터는 다시 프롬프트로 돌아갑니다.

```text
>>> 10 / 0
Traceback (most recent call last):
    ...
ZeroDivisionError: division by zero
>>> print("계속 실행할 수 있습니다.")
계속 실행할 수 있습니다.
```

스크립트에서 처리되지 않은 예외가 발생하면 traceback을 출력한 뒤 0이 아닌 종료 상태로 끝납니다.

```powershell
python failing_script.py
$LASTEXITCODE
```

오류 메시지는 `stderr`, 정상 출력은 `stdout`으로 전달됩니다. 예외를 직접 처리하려면 `try`와 `except`를 사용합니다.

```python
try:
    price = float("not-a-price")
except ValueError as error:
    print(f"입력 오류: {error}")
```

Ctrl+C로 실행 중인 프로그램을 중단하면 `KeyboardInterrupt`가 발생할 수 있습니다.

```python
try:
    while True:
        pass
except KeyboardInterrupt:
    print("사용자가 실행을 중단했습니다.")
```

무한 루프 예제는 실행할 때 Ctrl+C가 필요하므로, 실제로 실행하기보다 구조만 이해하세요.

---

## 11. Python 스크립트 실행하기

Unix 계열에서는 스크립트 첫 줄에 shebang을 작성하고 실행 권한을 부여할 수 있습니다.

```python
#!/usr/bin/env python3

print("Python 스크립트입니다.")
```

파일을 실행 가능하게 만든 뒤 실행합니다.

```bash
chmod +x hello.py
./hello.py
```

shebang은 파일의 첫 두 문자가 `#!`이어야 하며, Unix 계열에서 주로 사용합니다.

Windows에는 Unix의 실행 권한 개념이 없지만 Python 설치 프로그램이 `.py` 파일과 `python.exe`를 연결할 수 있습니다.

```powershell
python hello.py
```

콘솔 창 없이 실행하려는 Windows 스크립트는 `.pyw` 확장자를 사용할 수 있지만, 오류 메시지를 확인하기 어려울 수 있으므로 프로그램을 개발할 때는 `.py` 파일과 터미널 실행을 권장합니다.

---

## 12. 대화형 시작 파일: `PYTHONSTARTUP`

대화형 Python을 시작할 때 공통으로 실행할 명령을 파일에 저장하고 `PYTHONSTARTUP` 환경 변수로 지정할 수 있습니다.

예를 들어 `python_startup.py`를 만듭니다.

```python
from pathlib import Path

PROJECT_ROOT = Path.cwd()
print(f"대화형 시작: {PROJECT_ROOT}")
```

Windows PowerShell:

```powershell
$env:PYTHONSTARTUP = "C:\path\to\python_startup.py"
python
```

macOS/Linux:

```bash
export PYTHONSTARTUP=/path/to/python_startup.py
python3
```

이 파일은 대화형 세션에서만 읽힙니다. Python 스크립트를 실행할 때 자동으로 실행되는 것은 아닙니다.

시작 파일에는 부작용이 큰 코드나 민감한 정보를 넣지 마세요. 다른 컴퓨터나 자동화 환경에서는 해당 환경 변수가 설정되지 않을 수 있습니다.

---

## 13. `sitecustomize`와 `usercustomize`

Python은 시작 과정에서 `sitecustomize`와 `usercustomize` 모듈을 자동으로 찾을 수 있습니다.

- `sitecustomize`: 시스템 관리자 수준의 사용자 지정
- `usercustomize`: 개별 사용자의 Python 환경 사용자 지정

사용자 사이트 패키지 위치는 다음처럼 확인할 수 있습니다.

```python
import site

print(site.getusersitepackages())
```

이 기능은 모든 Python 실행에 영향을 줄 수 있으므로 프로젝트 설정에는 신중하게 사용해야 합니다. 일반적인 프로젝트 설정은 가상 환경, `.env` 파일, 명시적인 설정 모듈, IDE 설정으로 관리하는 편이 예측 가능합니다.

`-s` 옵션은 사용자 사이트 패키지 자동 처리를 끄는 데 사용할 수 있습니다.

```powershell
python -s
```

---

## 14. 실전 수치 계산 패턴

코인 가격과 수익률을 다룰 때는 다음처럼 계산 목적에 맞는 도구를 선택합니다.

```python
import math
from decimal import Decimal

buy_price = Decimal("100.00")
sell_price = Decimal("100.30")
quantity = Decimal("0.75")
fee_rate = Decimal("0.0004")

gross_return = (sell_price - buy_price) * quantity
fee = sell_price * quantity * fee_rate
net_return = gross_return - fee

print(f"총 손익: {net_return:.2f}")

estimated_rate = float(net_return / (buy_price * quantity))
print(math.isclose(estimated_rate, 0.003, rel_tol=0.2))
```

- 금액과 수수료 계산: `Decimal`
- 외부 계산 결과와 근사 비교: `math.isclose()`
- 많은 float 데이터의 합계: `math.fsum()`
- 비율이나 분수의 정확한 표현: `Fraction`

실제 거래 시스템에서는 거래소가 제공하는 가격 단위, 수량 단위, 수수료 반올림 규칙을 확인해야 합니다. 자료형을 선택하는 것만으로 거래 결과의 정확성이 보장되지는 않습니다.

---

## ✅ 이번 챕터 요약 과제

1. 대화형 인터프리터에서 `dir()`, `help()`, Tab 자동 완성을 사용해 `datetime` 모듈을 탐색하세요.
2. Python 명령 히스토리에서 이전 가격 계산을 다시 실행해 보세요.
3. `0.1 + 0.1 + 0.1 == 0.3`이 왜 `False`인지 `as_integer_ratio()`로 확인하세요.
4. `float`, `Decimal`, `Fraction`으로 같은 수익률 계산을 비교하세요.
5. `math.isclose()`의 `rel_tol`과 `abs_tol`을 바꿔 결과를 비교하세요.
6. `sum()`과 `math.fsum()`으로 많은 수익률의 합계를 비교하세요.
7. 처리되지 않은 예외가 대화형 모드와 스크립트에서 어떻게 다르게 보이는지 확인하세요.
8. `PYTHONSTARTUP` 파일에 자주 쓰는 프로젝트 경로와 함수를 등록하세요.
9. Python 공식 표준 라이브러리 문서에서 코인 프로젝트에 사용할 새 모듈 하나를 찾아 간단한 예제를 작성하세요.

---

## 참고 자료

- [Python 공식 문서: What Now?](https://docs.python.org/3/tutorial/whatnow.html)
- [Python 공식 문서: Interactive Input Editing and History Substitution](https://docs.python.org/3/tutorial/interactive.html)
- [Python 공식 문서: Floating-Point Arithmetic](https://docs.python.org/3/tutorial/floatingpoint.html)
- [Python 공식 문서: Appendix](https://docs.python.org/3/tutorial/appendix.html)
- [Python 공식 문서: The Python Standard Library](https://docs.python.org/3/library/index.html)

다음 단계에서는 지금까지 작성한 챕터를 바탕으로 프로젝트를 정리하고, 실험 가능한 작은 프로그램을 완성해 보세요.
