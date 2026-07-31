# Chapter 14. 파이썬 가상 환경과 패키지 관리

Python 프로젝트는 여러 외부 패키지를 사용할 수 있습니다. 프로젝트마다 필요한 패키지와 버전이 다르면 하나의 전역 Python 환경에 모두 설치하기 어렵습니다.

예를 들어 프로젝트 A는 `requests`의 이전 버전을 필요로 하고, 프로젝트 B는 최신 버전을 필요로 할 수 있습니다. 전역 환경에 한 버전만 설치하면 다른 프로젝트가 동작하지 않을 수 있습니다.

이 문제를 해결하는 방법이 **가상 환경(virtual environment)**입니다. 가상 환경은 특정 Python 실행 파일과 패키지를 프로젝트별로 분리해 관리하는 독립된 디렉터리입니다.

이번 장에서는 Python 공식 튜토리얼의 [Virtual Environments and Packages](https://docs.python.org/3/tutorial/venv.html)를 바탕으로 다음 내용을 학습합니다.

- 가상 환경이 필요한 이유
- `venv`로 가상 환경 만들기
- Windows와 macOS/Linux에서 활성화하기
- 가상 환경 비활성화하기
- `python -m pip`으로 패키지 설치·업그레이드·삭제하기
- 설치된 패키지 확인하기
- `pip freeze`와 `requirements.txt`
- 다른 컴퓨터에서 같은 환경 재현하기
- `.venv`와 의존성 파일을 프로젝트에서 관리하는 방법

---

## 1. 가상 환경이 필요한 이유

전역 환경에 모든 패키지를 설치하면 다음과 같은 문제가 생길 수 있습니다.

- 프로젝트마다 필요한 패키지 버전이 다릅니다.
- 한 프로젝트의 업그레이드가 다른 프로젝트를 망가뜨릴 수 있습니다.
- 어떤 패키지가 프로젝트에 필요한지 확인하기 어렵습니다.
- 다른 컴퓨터나 팀원이 같은 실행 환경을 만들기 어렵습니다.

가상 환경을 사용하면 프로젝트별로 패키지를 분리할 수 있습니다.

```text
프로젝트 A
  .venv-a/
    Python
    requests 2.x

프로젝트 B
  .venv-b/
    Python
    requests 3.x
```

한 프로젝트의 패키지를 설치하거나 업그레이드해도 다른 가상 환경에는 영향을 주지 않습니다.

이 프로젝트처럼 코인 데이터를 다루는 프로그램은 `pandas`, `matplotlib`, 거래소 API 패키지 등 여러 의존성을 사용할 수 있으므로, 전역 환경보다 가상 환경에서 관리하는 것이 안전합니다.

---

## 2. Python 버전 확인하기

가상 환경을 만들기 전에 현재 사용 중인 Python 버전을 확인합니다.

Windows PowerShell에서는 다음 명령을 실행합니다.

```powershell
python --version
python -c "import sys; print(sys.executable)"
```

macOS/Linux에서는 `python3` 명령을 사용하는 경우가 많습니다.

```bash
python3 --version
python3 -c "import sys; print(sys.executable)"
```

가상 환경은 명령을 실행한 Python 버전을 기반으로 만들어집니다. 여러 Python 버전이 설치되어 있다면 원하는 인터프리터로 명시해야 합니다.

Windows Python Launcher를 사용하는 경우 다음처럼 버전을 지정할 수 있습니다.

```powershell
py -3.13 --version
py -3.13 -m venv .venv
```

중요한 것은 가상 환경 생성과 패키지 설치에 같은 Python 인터프리터를 사용하는 것입니다.

---

## 3. 가상 환경 만들기

가상 환경을 만들 프로젝트의 루트 디렉터리로 이동한 뒤 `venv` 모듈을 실행합니다.

Windows PowerShell:

```powershell
cd "C:\path\to\python-edu-coin-trading"
python -m venv .venv
```

macOS/Linux:

```bash
cd /path/to/python-edu-coin-trading
python3 -m venv .venv
```

`.venv`는 가상 환경을 저장하는 디렉터리 이름으로 널리 사용하는 관례입니다. 이름 앞에 점이 있어 Unix 계열에서 숨김 디렉터리처럼 보이고, 프로젝트의 환경 파일이라는 의미도 분명합니다.

생성 후 프로젝트 구조는 대략 다음과 같습니다.

```text
python-edu-coin-trading/
    .venv/
    doc/
    src/
    README.md
```

`.venv` 안에는 Python 실행 파일과 패키지 설치 위치가 들어 있습니다. 이 폴더의 내부 파일을 직접 수정하기보다 `python -m venv`와 `pip` 명령으로 관리하세요.

가상 환경을 다시 만들고 싶다면 기존 `.venv`를 삭제한 뒤 같은 명령을 실행할 수 있습니다. 가상 환경은 `requirements.txt`로 재현할 수 있으므로 일반적으로 `.venv` 폴더 자체를 저장소에 올리지 않습니다.

---

## 4. 가상 환경 활성화하기

가상 환경을 활성화하면 `python`과 `pip` 명령이 해당 환경을 가리키도록 셸 설정이 바뀝니다.

### Windows PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
```

활성화되면 프롬프트 앞에 보통 `(.venv)`가 표시됩니다.

```text
(.venv) PS C:\path\to\python-edu-coin-trading>
```

### Windows 명령 프롬프트

```bat
.venv\Scripts\activate.bat
```

### macOS/Linux

```bash
source .venv/bin/activate
```

활성화된 뒤 Python 실행 파일 위치를 확인하면 `.venv` 아래의 경로가 표시됩니다.

```powershell
python -c "import sys; print(sys.executable)"
```

PowerShell에서 실행 정책 오류가 발생하면 조직이나 컴퓨터의 보안 정책을 확인해야 합니다. 무작정 정책을 변경하기보다 VS Code의 Python 인터프리터 선택 기능이나 명령 프롬프트를 사용하는 방법도 고려하세요.

---

## 5. 가상 환경에서 Python 사용하기

활성화된 상태에서 Python을 실행하면 가상 환경의 인터프리터가 사용됩니다.

```powershell
python
```

Python 안에서 `sys.prefix`와 `sys.base_prefix`를 비교하면 가상 환경 여부를 확인할 수 있습니다.

```python
import sys

print(sys.executable)
print(sys.prefix)
print(sys.base_prefix)
print(sys.prefix != sys.base_prefix)
```

마지막 값이 `True`이면 일반적으로 가상 환경 안에서 실행 중입니다.

활성화하지 않고도 가상 환경의 Python을 직접 지정할 수 있습니다.

Windows:

```powershell
.\.venv\Scripts\python.exe -m pip list
```

macOS/Linux:

```bash
.venv/bin/python -m pip list
```

이 방식은 자동화 스크립트나 IDE 설정에서 어떤 인터프리터를 사용하는지 명확히 하고 싶을 때 유용합니다.

---

## 6. 가상 환경 비활성화하기

작업이 끝났다면 다음 명령으로 현재 셸에서 가상 환경을 빠져나옵니다.

```powershell
deactivate
```

macOS/Linux도 같은 `deactivate` 명령을 사용합니다.

비활성화하면 `python`과 `pip` 명령은 다시 원래의 전역 환경 또는 상위 환경을 가리킵니다. 가상 환경 폴더가 삭제되는 것은 아니므로 나중에 다시 활성화할 수 있습니다.

```powershell
.\.venv\Scripts\Activate.ps1
```

가상 환경은 셸 세션마다 활성화해야 합니다. 터미널을 새로 열었다면 다시 활성화하세요.

---

## 7. `pip`로 패키지 설치하기

`pip`는 Python 패키지를 설치·업그레이드·삭제하는 도구입니다. 공식 튜토리얼처럼 `pip`를 직접 실행하는 대신 `python -m pip` 형식을 사용하는 것이 좋습니다.

```powershell
python -m pip install requests
```

`python -m pip`는 현재 `python` 명령이 가리키는 인터프리터의 pip를 사용합니다. 여러 Python이 설치된 컴퓨터에서 다른 환경의 pip를 잘못 실행하는 문제를 줄일 수 있습니다.

설치할 버전을 지정할 수도 있습니다.

```powershell
python -m pip install requests==2.32.3
```

버전 지정 형식은 다음과 같습니다.

- `package`: 최신 버전 설치
- `package==1.2.3`: 특정 버전 설치
- `package>=1.2`: 특정 버전 이상
- `package>=1.2,<2.0`: 허용 범위 지정

설치된 패키지는 현재 활성화된 가상 환경 안에만 설치됩니다.

---

## 8. 패키지 업그레이드와 삭제

설치된 패키지를 최신 버전으로 업그레이드하려면 `--upgrade` 또는 `-U`를 사용합니다.

```powershell
python -m pip install --upgrade requests
```

패키지를 삭제하려면 `uninstall`을 사용합니다.

```powershell
python -m pip uninstall requests
```

pip가 삭제 여부를 묻는 경우 확인 입력을 해야 합니다. 자동화 환경에서는 명시적으로 확인할 수 있습니다.

```powershell
python -m pip uninstall -y requests
```

패키지를 업그레이드하거나 삭제하기 전에 해당 프로젝트의 코드와 다른 패키지 호환성을 확인하세요. 운영 중인 프로젝트에서는 무조건 최신 버전으로 올리기보다 변경 기록과 테스트 결과를 먼저 확인하는 편이 안전합니다.

---

## 9. 설치된 패키지 확인하기

현재 환경에 설치된 패키지를 보려면 `pip list`를 실행합니다.

```powershell
python -m pip list
```

특정 패키지의 상세 정보는 `pip show`로 확인합니다.

```powershell
python -m pip show requests
```

출력에는 패키지 버전, 설치 위치, 의존 패키지 등이 포함됩니다.

패키지를 import할 수 있는지 Python 코드로도 확인할 수 있습니다.

```python
import sys

print(sys.executable)
try:
    import requests
except ImportError:
    print("requests가 설치되지 않았습니다.")
else:
    print(requests.__version__)
```

패키지 이름과 import 이름이 항상 같은 것은 아닙니다. 설치 문서와 패키지의 사용법을 확인하세요.

---

## 10. `pip freeze`와 `requirements.txt`

현재 가상 환경에 설치된 패키지와 정확한 버전을 기록하려면 `pip freeze`를 사용합니다.

```powershell
python -m pip freeze
```

결과는 보통 다음과 같은 형식입니다.

```text
matplotlib==3.9.2
pandas==2.2.3
requests==2.32.3
```

이 결과를 `requirements.txt`에 저장할 수 있습니다.

```powershell
python -m pip freeze > requirements.txt
```

`requirements.txt`는 프로젝트를 실행하는 데 필요한 패키지 목록을 기록하는 파일입니다. 버전까지 고정하면 다른 컴퓨터에서 비슷한 환경을 만들기 쉽습니다.

파일 예시는 다음과 같습니다.

```text
pandas==2.2.3
matplotlib==3.9.2
requests==2.32.3
```

프로젝트의 직접 의존성만 관리하려면 실제로 필요한 패키지를 직접 작성하는 방법도 있습니다. `pip freeze`는 현재 환경의 모든 설치 패키지를 기록하므로, 개발 도구나 간접 의존성까지 포함될 수 있습니다.

---

## 11. `requirements.txt`로 환경 재현하기

새 가상 환경을 만들고 requirements 파일의 모든 패키지를 설치할 수 있습니다.

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

설치가 끝난 뒤 패키지 목록을 확인합니다.

```powershell
python -m pip list
```

다른 컴퓨터의 Python 버전이나 운영체제가 다르면 일부 패키지가 설치되지 않을 수 있습니다. `requirements.txt`만으로 모든 시스템 차이가 해결되는 것은 아니므로 Python 버전, 운영체제, 시스템 라이브러리도 함께 기록하는 것이 좋습니다.

---

## 12. 이 프로젝트에 적용하기

이 저장소의 학습 코드를 실행하기 위한 기본 가상 환경을 만들 수 있습니다.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install pandas matplotlib jupyter requests
```

설치한 패키지를 기록합니다.

```powershell
python -m pip freeze > requirements.txt
```

그 뒤 Jupyter Notebook을 실행합니다.

```powershell
jupyter notebook
```

VS Code에서는 명령 팔레트에서 Python 인터프리터를 선택하고 프로젝트의 다음 경로를 지정할 수 있습니다.

```text
.venv\Scripts\python.exe
```

선택한 인터프리터가 `src/chapter_04.ipynb`, `src/chapter_05.ipynb`, `src/chapter_06.ipynb`의 커널로 사용되는지 확인하세요.

---

## 13. `.venv`를 저장소에 올리지 않기

가상 환경은 컴퓨터와 Python 설치에 종속된 생성물입니다. 일반적으로 `.venv` 폴더 전체를 Git 저장소에 커밋하지 않고, 필요한 패키지 목록만 저장합니다.

`.gitignore`에 다음 항목을 추가할 수 있습니다.

```gitignore
.venv/
__pycache__/
*.py[cod]
```

저장소에 포함할 파일:

- `requirements.txt`
- 프로젝트 소스 코드
- 문서와 설정 파일
- 필요한 경우 Python 버전 안내

저장소에 보통 포함하지 않을 파일:

- `.venv/`
- `__pycache__/`
- 비밀번호와 API 키가 들어 있는 `.env`
- 운영체제나 편집기가 생성한 임시 파일

가상 환경 자체를 공유하는 대신, 누구나 새 환경을 만들고 requirements 파일로 패키지를 설치할 수 있게 만드는 것이 재현 가능한 방식입니다.

---

## 14. 활성화하지 않고 패키지 설치하기

활성화는 편리한 셸 기능일 뿐 필수 조건은 아닙니다. 가상 환경의 Python 실행 파일을 직접 호출할 수 있습니다.

Windows:

```powershell
.\.venv\Scripts\python.exe -m pip install requests
.\.venv\Scripts\python.exe src\hello.py
```

macOS/Linux:

```bash
.venv/bin/python -m pip install requests
.venv/bin/python src/hello.py
```

자동화 도구나 VS Code 설정에서는 이 방식이 어떤 환경을 사용하는지 더 명확하게 보여줄 수 있습니다.

---

## 15. 가상 환경 문제 해결

### `python`과 `pip`가 서로 다른 환경을 가리키는 경우

다음 명령으로 실행 파일 위치를 각각 확인합니다.

```powershell
python -c "import sys; print(sys.executable)"
python -m pip --version
```

두 출력 모두 `.venv` 경로를 가리켜야 합니다. `pip`만 단독으로 실행하기보다 항상 `python -m pip`를 사용하세요.

### 패키지를 찾을 수 없는 경우

1. 가상 환경이 활성화되어 있는지 확인합니다.
2. VS Code의 선택된 인터프리터가 `.venv`인지 확인합니다.
3. `python -m pip show package_name`으로 설치 위치를 확인합니다.
4. 패키지의 import 이름과 설치 이름이 다른지 문서를 확인합니다.
5. Python 버전과 패키지 지원 범위를 확인합니다.

### 가상 환경이 손상된 경우

가상 환경은 재생성할 수 있습니다.

```powershell
deactivate
Remove-Item -Recurse -Force .venv
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

삭제하기 전에 필요한 패키지가 `requirements.txt`에 기록되어 있는지 확인하세요.

---

## ✅ 이번 챕터 요약 과제

1. 프로젝트 루트에 `.venv` 가상 환경을 생성하세요.
2. 가상 환경을 활성화하고 `sys.executable`의 경로를 확인하세요.
3. `requests` 또는 `pandas`를 가상 환경에 설치하세요.
4. `pip show`, `pip list`, `pip freeze`의 결과 차이를 확인하세요.
5. 설치된 패키지 목록을 `requirements.txt`에 저장하세요.
6. 새 가상 환경을 만든 뒤 `pip install -r requirements.txt`로 환경을 재현하세요.
7. `.gitignore`에 `.venv/`와 `__pycache__/`를 추가하세요.
8. `python -m pip`을 사용하는 이유를 자신의 말로 정리하세요.

---

## 참고 자료

- [Python 공식 문서: Virtual Environments and Packages](https://docs.python.org/3/tutorial/venv.html)
- [Python 공식 문서: `venv`](https://docs.python.org/3/library/venv.html)
- [Python 공식 문서: Installing Python Modules](https://docs.python.org/3/installing/index.html)
- [Python Packaging User Guide](https://packaging.python.org/)

다음 장에서는 Python 프로그램을 배포 가능한 패키지로 구성하고 프로젝트 메타데이터를 작성하는 방법을 배웁니다.
