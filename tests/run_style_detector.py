import sys
from pathlib import Path

# 프로젝트 루트(C_style_detector_final)를 Python 경로에 추가
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.ad_inspector.style_detector import detect_style


TEST_CASES = [
    {
        "name": "T03 opacity: 0",
        "element": {
            "id": "e1",
            "computed_style": {
                "opacity": "0"
            }
        },
    },
    {
        "name": "T03 color: transparent",
        "element": {
            "id": "e2",
            "computed_style": {
                "color": "transparent"
            }
        },
    },
    {
        "name": "T03 글자색 = 배경색",
        "element": {
            "id": "e3",
            "computed_style": {
                "color": "rgb(255, 255, 255)",
                "background_color": "rgb(255, 255, 255)"
            }
        },
    },
    {
        "name": "T04 font-size: 0~1px",
        "element": {
            "id": "e4",
            "computed_style": {
                "font_size_px": 0
            }
        },
    },
    {
        "name": "T04 position:absolute + left <= -9999px",
        "element": {
            "id": "e5",
            "computed_style": {
                "position": "absolute",
                "left": "-9999px"
            }
        },
    },
    {
        "name": "T04 display:none",
        "element": {
            "id": "e6",
            "computed_style": {
                "display": "none"
            }
        },
    },
]


def main():
    print("=" * 60)
    print("           C 스타일 탐지기 확인 결과")
    print("=" * 60)

    success_count = 0

    for index, case in enumerate(TEST_CASES, start=1):
        result = detect_style(case["element"])

        print(f"\n[{index}] {case['name']}")
        print(f"  요소 ID : {result['element_id']}")

        if result["suspicious"]:
            success_count += 1

            print("  상태    : [발견]")
            print(f"  점수    : {result['score']:.2f}")

            if result["reasons"]:
                print("  이유    :")
                for reason in result["reasons"]:
                    print(f"             - {reason}")

            print(
                f"  탐지기법: "
                f"{', '.join(result['evidence']['techniques'])}"
            )
        else:
            print("  상태    : [미발견]")

    print("\n" + "=" * 60)
    print("                    최종 결과")
    print("=" * 60)
    print(f"확인 기준 : {len(TEST_CASES)}개")
    print(f"탐지 성공 : {success_count}/{len(TEST_CASES)}")

    if success_count == len(TEST_CASES):
        print("결과      : 모든 기준 탐지 성공")
    else:
        print("결과      : 일부 기준 탐지 실패")

    print("=" * 60)


if __name__ == "__main__":
    main()