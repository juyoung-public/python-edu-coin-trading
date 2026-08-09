# Appendix. 파이썬 실행을 위한 기본적인 윈도우 터미널 사용법 및 커맨드

이 문서는 Python 코드를 실행하고 프로젝트를 관리할 때 자주 사용하는 Windows 터미널(명령 프롬프트, PowerShell) 기본 명령을 정리한 실습용 참조 자료입니다.

Python 학습을 하다 보면 코드가 잘 실행되지 않는 이유가 경로 문제, 인터프리터 선택, 가상 환경 활성화, 설치 패키지와 연결되는 경우가 많습니다. 이 문서를 활용하면 기본적인 터미널 사용 흐름을 익히고, 이후 실습 환경을 빠르게 점검할 수 있습니다.

---

## 1. 파일과 디렉터리(File, Directory)란?

컴퓨터에서 작업을 할 때 가장 먼저 알아야 할 개념은 파일과 폴더(디렉터리)입니다.

- 파일(file): 문서, 코드, 이미지, 데이터와 같이 실제 내용을 담는 단위입니다.
  - 예: `hello.py`, `README.md`, `data.csv`
- 디렉터리(directory, 폴더): 파일을 정리하는 상자 같은 개념입니다.
  - 예: `src/`, `doc/`, `.venv/`

예를 들어 이 프로젝트는 보통 다음 구조를 가집니다.

```text
python-edu-coin-trading/
    README.md
    doc/
        Chapter 01. ...md
    src/
        hello.py
        chapter_02.py
    .venv/
```

여기서 `README.md`는 파일이고, `doc`와 `src`는 디렉터리입니다. 파일은 내용을 담고, 디렉터리는 파일을 담아 구조를 정리하는 역할을 합니다.

Python을 실행할 때는 보통 특정 파일을 선택해서 실행합니다. 예를 들면 `python src\hello.py`처럼 "이 디렉터리 안의 이 파일을 실행해라"는 의미를 터미널에 전달하는 것입니다.

이 개념을 이해하면 다음 단계인 `cd`와 `ls` 같은 경로 명령이 훨씬 자연스럽게 느껴집니다.

---

## 2. 터미널이란?

터미널은 컴퓨터의 명령을 직접 입력하고 결과를 확인하는 창입니다. Windows에서는 보통 다음 두 가지를 사용합니다.

- Command Prompt (`cmd`)
- PowerShell (`powershell`)
- VS Code의 내장 터미널

Python 실습에서는 보통 VS Code의 터미널을 열어 작업하는 경우가 가장 편합니다.

---

## 3. 터미널 열기

### VS Code에서 열기

1. VS Code를 엽니다.
2. 상단 메뉴의 Terminal → New Terminal을 선택합니다.
3. 기본 쉘은 PowerShell 또는 Command Prompt가 열립니다.

### 직접 실행

PowerShell에서:

```powershell
powershell
```

명령 프롬프트에서:

```cmd
cmd
```

---

## 4. 기본 경로 이동 명령

프로젝트 폴더에 들어가려면 `cd`(change directory)를 사용합니다.

### 현재 위치 확인

```powershell
pwd
```

혹은 PowerShell에서는:

```powershell
Get-Location
```

### 폴더 이동

```powershell
cd C:\path\to\project
```

예를 들어 이 프로젝트 폴더에 들어간다면:

```powershell
cd "C:\Users\juyoung\python\python-edu-coin-trading"
```

상위 폴더로 이동:

```powershell
cd ..
```

### 현재 폴더의 내용 보기

```powershell
Get-ChildItem
```

또는 간단히:

```powershell
dir
```

---

## 5. Python 설치 확인

Python이 설치되어 있는지 확인합니다.

```powershell
python --version
```

버전이 안 나오면 Windows에서 Python Launcher를 시도해 봅니다.

```powershell
py --version
```

Python 실행 경로 확인:

```powershell
python -c "import sys; print(sys.executable)"
```

또는 PowerShell에서:

```powershell
Get-Command python
```

---

## 6. Python 실행 명령

### 간단한 Python 코드 실행

```powershell
python -c "print('Hello, Python!')"
```

### 스크립트 실행

```powershell
python src\hello.py
```

실행 파일이 현재 폴더에 있다고 가정하면:

```powershell
python .\hello.py
```

### Python Launcher 사용

```powershell
py .\src\hello.py
```

---

## 7. 가상 환경 만들기

프로젝트별로 패키지를 분리하기 위해 가상 환경을 만듭니다.

```powershell
python -m venv .venv
```

가상 환경 생성 후 활성화합니다.

### PowerShell에서 활성화

```powershell
.\.venv\Scripts\Activate.ps1
```

활성화되면 프롬프트 앞에 `(.venv)`가 보입니다.

### 비활성화

```powershell
deactivate
```

---

## 8. pip 사용법

`pip`는 Python 패키지를 설치할 때 사용하는 도구입니다.

### 패키지 설치

```powershell
python -m pip install pandas
```

### 패키지 확인

```powershell
python -m pip list
```

### 특정 버전 설치

```powershell
python -m pip install requests==2.32.3
```

### 패키지 업그레이드

```powershell
python -m pip install --upgrade pip
```

### 패키지 삭제

```powershell
python -m pip uninstall pandas
```

### 설치된 패키지 목록 저장

```powershell
python -m pip freeze > requirements.txt
```

다른 환경에서 복원할 때:

```powershell
python -m pip install -r requirements.txt
```

---

## 9. 자주 쓰는 Windows 터미널 명령

### 폴더 생성

```powershell
mkdir my_project
```

### 폴더 삭제

```powershell
Remove-Item -Recurse my_project
```

### 파일 삭제

```powershell
Remove-Item example.txt
```

### 파일 내용 보기

```powershell
Get-Content example.txt
```

### 파일 복사

```powershell
Copy-Item source.txt target.txt
```

### 파일 이동

```powershell
Move-Item source.txt backup\source.txt
```

---

## 10. 프로젝트 실습 흐름 예시

다음은 Python 프로젝트를 시작할 때 자주 쓰는 흐름입니다.

```powershell
cd "C:\Users\juyoung\python\python-edu-coin-trading"
python --version
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install pandas matplotlib jupyter requests
python src\hello.py
```

이 흐름은 다음을 한 번에 보여줍니다.

- 프로젝트 폴더 이동
- Python 버전 확인
- 가상 환경 생성
- 환경 활성화
- 패키지 설치
- 코드 실행

---

## 11. 실습 과제

다음 명령을 직접 순서대로 입력해 보세요.

1. 현재 폴더 확인

```powershell
Get-Location
```

2. 프로젝트 폴더로 이동

```powershell
cd "C:\Users\juyoung\python\python-edu-coin-trading"
```

3. Python 버전 확인

```powershell
python --version
```

4. 가상 환경 생성

```powershell
python -m venv .venv
```

5. 가상 환경 활성화

```powershell
.\.venv\Scripts\Activate.ps1
```

6. 현재 파이썬 경로 확인

```powershell
python -c "import sys; print(sys.executable)"
```

7. 패키지 설치 예시

```powershell
python -m pip install requests
```

8. 간단한 문자열 출력

```powershell
python -c "print('윈도우 터미널 실습 완료')"
```

9. 비활성화

```powershell
deactivate
```

---

## 12. 실습 체크리스트

아래 항목을 모두 확인하면 기본 환경 구성이 정상적으로 이루어진 것입니다.

- Python이 설치되어 있다.
- 터미널에서 `python --version`이 동작한다.
- 프로젝트 폴더로 이동할 수 있다.
- `.venv`를 만들 수 있다.
- 가상 환경을 활성화할 수 있다.
- `python -m pip install`이 동작한다.
- `python script.py`로 스크립트를 실행할 수 있다.
- 필요하면 `deactivate`로 환경을 종료할 수 있다.

---

## 13. 정리

Windows 터미널에서 Python을 실행하는 기본은 매우 단순합니다. 핵심은 다음 세 가지입니다.

1. 프로젝트 폴더로 이동한다.
2. 올바른 Python 인터프리터를 선택한다.
3. 필요한 패키지는 가상 환경에서 설치하고 실행한다.

이 기본 습관을 익히면 이후 Jupyter Notebook, 프로젝트 실행, 패키지 설치, 가상 환경 관리가 훨씬 쉬워집니다.

이 프로젝트에서는 특히 다음 명령이 자주 사용됩니다.

```powershell
cd "C:\Users\juyoung\python\python-edu-coin-trading"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install pandas matplotlib jupyter requests
python src\hello.py
```

이 문서는 Python을 실제로 실행할 때 가장 기본적인 터미널 사용법을 빠르게 익히는 데 목적이 있습니다.
