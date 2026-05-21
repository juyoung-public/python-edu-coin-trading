# Chapter 04. 데이터 시각화: 내 코인 차트 그리기

단순히 숫자로만 보는 시세는 흐름을 파악하기 어렵습니다. 이번 장에서는 **Jupyter Notebook**을 활용해 빗썸에서 가져온 데이터를 멋진 그래프로 그려보는 방법을 배웁니다.

---

## 1. Jupyter Notebook이란? 📒

주피터 노트북은 코드를 **'셀(Cell)'** 단위로 실행하고, 그 결과를 즉시 확인할 수 있는 도구입니다.

*   **실시간 확인:** 코드를 실행하자마자 아래에 숫자나 그래프가 나타납니다. 
*   **데이터 분석의 필수품:** 전 세계 데이터 과학자들이 실험실처럼 사용하는 가장 대중적인 도구입니다.
*   **부분 실행:** 전체 코드를 다시 실행할 필요 없이, 수정하고 싶은 부분만 골라 실행할 수 있어 매우 편리합니다.

---

## 2. 환경 설정 (설치 및 실행) 🛠️

### (1) 라이브러리 설치
먼저 데이터를 다루는 `pandas`와 그래프를 그리는 `matplotlib`, 그리고 주피터 기능을 터미널(CMD)에서 설치합니다.
```bash
pip install jupyter pandas matplotlib pybithumb
```

### (2) VS Code에서 실행하기
1.  VS Code 왼쪽 확장(Extensions) 아이콘에서 **`Jupyter`**를 검색하여 설치합니다.
2.  새 파일을 만드는데, 이때 확장자를 반드시 **`.ipynb`**로 저장합니다. (예: `analysis.ipynb`)
3.  파일을 열면 상단에 `+ Code` 버튼이 생기며, 셀 단위로 코드를 입력할 수 있게 됩니다.

---

## 3. 시세 데이터 가져오기 (Pandas) 📈

먼저 빗썸에서 비트코인의 과거 시세(일봉) 데이터를 가져와 보겠습니다. 

**첫 번째 셀에 입력:**
```python
import pybithumb
import pandas as pd

# 비트코인 과거 시세 데이터 가져오기 (최근 100일 기준)
df = pybithumb.get_ohlcv("BTC")

# 데이터 확인 (상위 5개 행 출력)
df.head()
```
> **설명:** `get_ohlcv` 함수는 시가(Open), 고가(High), 저가(Low), 종가(Close), 거래량(Volume)이 포함된 **DataFrame(표 형태의 데이터)**을 반환합니다.

---

## 4. 시각화 시작하기 (Matplotlib) 🎨

가져온 데이터를 바탕으로 비트코인의 가격 변화를 한눈에 보여주는 선 그래프를 그려봅시다.

**두 번째 셀에 입력:**
```python
import matplotlib.pyplot as plt

# 그래프의 크기 설정 (가로 10, 세로 5)
plt.figure(figsize=(10, 5))

# 종가(close) 데이터를 그래프로 그리기
plt.plot(df.index, df['close'], label='BTC Close Price', color='orange')

# 그래프 꾸미기 (한글 폰트 설정이 안 되어 있을 경우 영어 권장)
plt.title('Bitcoin Price Chart') # 제목
plt.xlabel('Date')               # x축 이름
plt.ylabel('Price (KRW)')        # y축 이름
plt.legend()                     # 범례 표시
plt.grid(True)                   # 격자 표시

# 화면에 출력
plt.show()
```

---

## 5. 심화 분석: 이동평균선(MA) 추가하기 📉

주식이나 코인 투자자들이 가장 많이 보는 **이동평균선(Moving Average)**을 그려봅시다. 이동평균선은 가격의 흐름을 부드럽게 보여줍니다.

**세 번째 셀에 입력:**
```python
# 5일 이동평균선 계산 (최근 5일간의 평균 가격)
df['MA5'] = df['close'].rolling(window=5).mean()

plt.figure(figsize=(10, 5))

# 실제 종가 그래프
plt.plot(df.index, df['close'], label='Close Price')

# 5일 이동평균선 그래프 (빨간색 점선)
plt.plot(df.index, df['MA5'], label='5-Day Moving Average', color='red', linestyle='--')

plt.title('Bitcoin Price with MA5')
plt.legend()
plt.show()
```

---

## 💡 분석 포인트 (고등학생을 위한 팁)

1.  **데이터의 힘:** 숫자로만 나열된 표를 볼 때보다 그래프로 볼 때 하락세와 상승세가 훨씬 명확하게 보이죠? 이것이 데이터 시각화의 목적입니다.
2.  **색상 커스텀:** `color='green'`, `color='blue'` 등으로 색상을 바꿔 나만의 차트를 만들어보세요.
3.  **단축키 활용:** 주피터 노트북에서 셀을 실행할 때는 `Shift + Enter`를 누르면 아주 빠릅니다.

---

## ✅ 이번 챕터 요약 과제

1.  비트코인(`BTC`)이 아닌 **이더리움(`ETH`)**의 데이터를 가져와서 그래프를 그려보세요.
2.  5일 이동평균선이 아니라 **20일 이동평균선(MA20)**을 추가해 보세요. (어떤 그래프가 더 부드러운가요?)
3.  그래프의 제목을 자신의 이름이 들어간 제목(예: `K-Student's Bitcoin Chart`)으로 수정해 보세요.

---
**다음 장 예고:** 시각화로 차트를 분석했다면, 이제 이 데이터를 이용해 "과거에 샀다면 얼마를 벌었을까?"를 수학적으로 계산하는 **백테스팅(Backtesting)**을 배워보겠습니다!
