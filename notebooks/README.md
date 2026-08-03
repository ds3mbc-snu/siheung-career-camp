# 시흥 진로캠프 강의용 노트북

이 폴더는 시흥 진로캠프의 network 분석 강의용 Jupyter Notebook 배포본입니다.
API를 호출하지 않고, 함께 포함된 `output/` 산출물만 읽어서 실행합니다.

## 파일 구성

| 파일 | 내용 |
|---|---|
| `02_candidate_scenario.ipynb` | W1~W4 복합 비용으로 후보 network 확인 |
| `03_structure_alternatives.ipynb` | MST, t-spanner, degree-limited Kruskal 비교 |
| `04_weight_sensitivity.ipynb` | weight 조합별 구조 민감도와 route 안정성 확인 |
| `05_route_geometry_and_interactive_weights.ipynb` | 저장 route geometry 기반 구조별 지도 확인 |
| `output/` | 노트북 실행에 필요한 CSV, JSON, PNG, HTML 산출물 |

## 실행 방법

처음 실행하는 학생은 아래 순서대로 진행하면 됩니다.

### 1. 파일 내려받기

1. GitHub 저장소 화면에서 초록색 `Code` 버튼을 누릅니다.
2. `Download ZIP`을 누릅니다.
3. 내려받은 ZIP 파일의 압축을 풉니다.
4. 압축을 풀면 `siheung-career-camp-main` 같은 이름의 폴더가 생깁니다.
5. 그 안의 `notebooks` 폴더가 이번 실습 폴더입니다.

### 2. Jupyter 설치하기

노트북을 실행하려면 Python과 Jupyter가 필요합니다.
처음 설치하는 경우에는 Anaconda를 사용하는 것이 가장 쉽습니다.

1. Anaconda 다운로드 페이지에 접속합니다: <https://www.anaconda.com/download>
2. 본인 컴퓨터에 맞는 설치 파일을 내려받습니다.
   - Windows: Windows용 installer
   - Mac: macOS용 installer
3. 설치 과정에서는 기본 설정을 그대로 두고 진행합니다.
4. 설치가 끝나면 다음 프로그램을 실행합니다.
   - Windows: `Anaconda Prompt`
   - Mac: `Terminal`

### 3. 실습 폴더로 이동하기

터미널에서 `notebooks` 폴더로 이동해야 합니다.
가장 쉬운 방법은 아래와 같습니다.

1. 압축을 푼 폴더 안의 `notebooks` 폴더를 찾습니다.
2. 터미널에 `cd `를 입력하고, 마지막에 한 칸을 띄웁니다.
3. `notebooks` 폴더를 터미널 창으로 끌어다 놓습니다.
4. Enter를 누릅니다.

예시는 다음과 비슷합니다. 컴퓨터마다 경로는 다를 수 있습니다.

```bash
cd /Users/yourname/Downloads/siheung-career-camp-main/notebooks
```

Windows에서는 다음과 비슷하게 보일 수 있습니다.

```bash
cd C:\Users\yourname\Downloads\siheung-career-camp-main\notebooks
```

### 4. JupyterLab 실행하기

`notebooks` 폴더로 이동한 뒤 아래 명령을 입력합니다.

```bash
jupyter lab
```

잠시 기다리면 웹 브라우저가 열리고 JupyterLab 화면이 나타납니다.
왼쪽 파일 목록에서 아래 노트북을 순서대로 열어 실행합니다.

1. `02_candidate_scenario.ipynb`
2. `03_structure_alternatives.ipynb`
3. `04_weight_sensitivity.ipynb`
4. `05_route_geometry_and_interactive_weights.ipynb`

노트북을 연 뒤에는 상단 메뉴에서 `Run` → `Run All Cells`를 누르면 전체 셀이 순서대로 실행됩니다.

### 5. 실행이 안 될 때

- `jupyter: command not found` 또는 `'jupyter'은(는) 내부 또는 외부 명령...`이라고 나오면 Anaconda가 설치되지 않았거나 터미널을 새로 열어야 합니다.
- `output` 폴더를 찾을 수 없다는 오류가 나오면 `notebooks` 폴더 안에서 Jupyter를 실행했는지 확인합니다.
- ZIP 압축을 풀지 않고 실행하면 파일을 제대로 읽지 못할 수 있습니다. 반드시 압축을 푼 뒤 실행합니다.
- 실행 중 경고가 떠도 결과 표와 그림이 보이면 수업 진행에는 문제가 없습니다.

## 주의

- 이 배포본은 강의 실습용입니다.
- 네이버 API나 외부 데이터 API를 호출하지 않습니다.
- `output/` 폴더를 삭제하면 노트북이 실행되지 않습니다.
- W3는 보호구역 시설점 buffer proxy 예비값이고, W4는 90m DEM 예비값입니다.
- 결과는 알고리즘 비교 수업용 자료이며 최종 트램 노선안이 아닙니다.
