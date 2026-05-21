# Chapter 03. 코드의 재사용: 함수, 객체, 라이브러리

단순히 코드를 위에서 아래로 순서대로 적는 것을 넘어, 이제는 효율적으로 코드를 관리하고 외부의 강력한 도구들을 가져와 사용하는 방법을 배웁니다.

---

## 1. 함수(Function): 반복되는 로직을 하나로 묶기 📦

함수는 특정 작업을 수행하는 **'마법 상자'**와 같습니다. 매번 같은 계산식을 적는 대신, 상자에 이름을 붙이고 필요할 때마다 꺼내 씁니다.

*   **구조:**
    ```python
    def 함수이름(입력값):
        # 실행할 내용
        return 결과값
    ```

*   **실습: 코인 매수 목표가 계산 함수**
    ```python
    def get_target_price(open_price, last_range):
        """시가와 전일 변동폭을 넣으면 목표가를 계산해줌"""
        target = open_price + (last_range * 0.5)
        return target

    # 함수 사용
    btc_target = get_target_price(90000000, 2000000)
    print(f"비트코인 매수 목표가: {btc_target}원")
    ```

---

## 2. 라이브러리와 pip: "남이 만든 도구 가져오기" 🛠️

프로그래밍의 매력은 모든 것을 직접 만들 필요가 없다는 점입니다. 전 세계 개발자들이 미리 만들어둔 도구 상자를 **'라이브러리(Library)'**라고 합니다.

*   **pip란?** 파이썬의 '앱스토어' 같은 프로그램입니다. 외부 라이브러리를 내 컴퓨터에 설치할 때 사용합니다.
*   **라이브러리 설치하기 (터미널에서 입력):**
    ```bash
    # 터미널 창에 입력하세요
    pip install requests
    pip install pybithumb
    ```
*   **라이브러리 사용하기 (import):**
    ```python
    import time           # 파이썬 기본 내장 라이브러리
    import pybithumb      # 방금 설치한 라이브러리

    print("3초 뒤에 시세를 조회합니다...")
    time.sleep(3)         # 3초 대기
    print(pybithumb.get_current_price("BTC"))
    ```

---

## 3. 클래스(Class)와 객체(Object): 데이터와 기능을 하나로 묶기 🏗️

클래스는 **'설계도'**이고, 객체는 그 설계도로 만든 **'실제 물건'**입니다. 데이터를 관리하기 위한 구조를 짤 때 매우 유용합니다.

*   **실습: 간단한 계좌 관리 클래스**
    ```python
    class TradingBot:
        def __init__(self, name, balance):
            self.name = name        # 봇의 이름
            self.balance = balance  # 초기 잔고
        
        def buy(self, amount):
            if self.balance >= amount:
                self.balance -= amount
                print(f"[{self.name}] {amount}원 매수 완료. 남은 잔고: {self.balance}원")
            else:
                print(f"[{self.name}] 잔고가 부족합니다!")

    # 객체 생성 (설계도에서 실제 봇을 찍어냄)
    my_bot = TradingBot("고딩트레이더1호", 1000000)
    my_bot.buy(300000)
    ```

---

## 4. 종합: 라이브러리 속의 객체 활용하기 🧩

우리가 직접 클래스를 만들지 않더라도, 설치한 `pybithumb` 라이브러리 내부에는 전문가들이 이미 만들어둔 클래스들이 가득합니다.

*   **실전 예시 (Bithumb API 객체 사용):**
    ```python
    import pybithumb

    # Bithumb 클래스를 사용해 'my_account'라는 객체를 만듭니다.
    # (실제 계정 키는 추후 Chapter 07에서 발급받습니다)
    my_account = pybithumb.Bithumb("CONNECT_KEY", "SECRET_KEY")

    # 객체 안에 있는 'get_balance'라는 기능을 점(.)을 찍어 사용합니다.
    balance = my_account.get_balance("BTC")
    print(f"내 비트코인 잔고: {balance}")
    ```

---

## ✅ 이번 챕터 요약 과제

1.  터미널에 `pip install pandas`를 입력하여 데이터 분석 라이브러리를 설치해 보세요.
2.  두 숫자를 더해서 2로 나누는 `get_average(a, b)` 함수를 직접 만들어 보세요.
3.  왜 우리가 직접 빗썸 접속 코드를 다 짜지 않고 `pybithumb` 같은 라이브러리를 쓰는지 생각해 보세요. (힌트: 시간 절약, 오류 감소)

---
**다음 장 예고:** 이제 라이브러리 사용법을 익혔으니, 본격적으로 데이터를 가져와서 시각화하는 **데이터 분석(Jupyter Notebook)** 단계로 넘어갑니다!
