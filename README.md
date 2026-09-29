# C Style Detector 최종본

## 역할

A 크롤러가 수집한 HTML 요소의 `computed_style`을 받아
스타일 기반 은닉 요소를 탐지한다.

C는 직접 웹사이트를 크롤링하지 않는다.

## 탐지 항목

### T03
- `opacity: 0`
- `color: transparent`
- 글자색과 배경색이 동일

### T04
- `font-size: 0~1px`
- `position: absolute` + `left <= -9999px`
- `display: none`

## 파일

```text
C_style_detector_final/
├── src/
│   ├── __init__.py
│   └── ad_inspector/
│       ├── __init__.py
│       └── style_detector.py
├── tests/
│   ├── test_style_detector.py
│   └── run_style_detector.py
└── README.md
```

## 1. 자동 테스트

프로젝트 루트에서:

```powershell
python -m pytest
```

정상 결과:

```text
9 passed
```

## 2. 상세 테스트 결과

프로젝트 루트에서:

```powershell
python tests\run_style_detector.py
```

`[발견]`, `[정상]`, 탐지 기법, 이유, 점수를 보여준다.

## 통합 시 주의

A 크롤러의 `computed_style`에 T04 offscreen 탐지를 위한
`position`과 `left`가 포함되어야 한다.

현재 C 모듈은 이 값이 들어오면 탐지할 수 있도록 준비되어 있다.

`detect_style()`의 반환값은 팀 통합용 데이터로 사용하며,
상세 출력의 `[발견]` 문구는 테스트 실행 화면에만 사용한다.
