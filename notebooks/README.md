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

1. GitHub에서 이 저장소를 ZIP으로 내려받아 압축을 풉니다.
2. 터미널 또는 Anaconda Prompt에서 `notebooks` 폴더로 이동합니다.
3. Jupyter Notebook 또는 JupyterLab을 실행합니다.

```bash
cd notebooks
jupyter lab
```

4. 순서대로 `02`부터 `05`까지 노트북을 열어 실행합니다.

## 주의

- 이 배포본은 강의 실습용입니다.
- 네이버 API나 외부 데이터 API를 호출하지 않습니다.
- `output/` 폴더를 삭제하면 노트북이 실행되지 않습니다.
- W3는 보호구역 시설점 buffer proxy 예비값이고, W4는 90m DEM 예비값입니다.
- 결과는 알고리즘 비교 수업용 자료이며 최종 트램 노선안이 아닙니다.
