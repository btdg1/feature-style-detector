"""C 스타일 탐지 모듈.

A 크롤러가 제공하는 공통 element 데이터를 받아
스타일 기반 은닉(T03/T04)을 탐지한다.

이 모듈은 웹 크롤링을 직접 수행하지 않는다.
"""

import re


def _normalize(value):
    if value is None:
        return ""
    return str(value).strip().lower().replace(" ", "")


def _parse_px(value):
    if value is None:
        return None

    if isinstance(value, (int, float)):
        return float(value)

    text = str(value).strip().lower()
    match = re.fullmatch(r"-?\d+(?:\.\d+)?px", text)

    if match:
        return float(text[:-2])

    return None


def _add_reason(reasons, reason):
    if reason not in reasons:
        reasons.append(reason)


def detect_style(element):
    """공통 element 1개를 검사한다.

    반환 형식:
    {
        "element_id": str,
        "detector": "style",
        "suspicious": bool,
        "score": float,
        "reasons": list[str],
        "evidence": {
            "techniques": list[str],
            ...
        }
    }
    """
    computed = element.get("computed_style", {}) or {}
    inline = element.get("style", {}) or {}

    # computed_style을 우선 사용하고, 없는 값은 style에서 보완
    css = {**inline, **computed}

    opacity = _normalize(css.get("opacity"))
    color = _normalize(css.get("color"))
    background = _normalize(
        css.get("background_color", css.get("background-color"))
    )
    display = _normalize(css.get("display"))
    position = _normalize(css.get("position"))

    font_size = _parse_px(
        css.get(
            "font_size_px",
            css.get("font-size", css.get("font_size"))
        )
    )

    left = _parse_px(css.get("left"))

    t03_reasons = []
    t04_reasons = []
    evidence = {}

    # -------------------------
    # T03: 투명/은닉 스타일
    # -------------------------

    if opacity == "0":
        _add_reason(t03_reasons, "opacity=0")
        evidence["opacity"] = css.get("opacity")

    if color == "transparent":
        _add_reason(t03_reasons, "color=transparent")
        evidence["color"] = css.get("color")

    if color and background and color == background:
        _add_reason(
            t03_reasons,
            "color와 background_color가 동일"
        )
        evidence["color"] = css.get("color")
        evidence["background_color"] = css.get(
            "background_color",
            css.get("background-color")
        )

    # -------------------------
    # T04: 화면상 보이지 않게 숨김
    # -------------------------

    if font_size is not None and 0 <= font_size <= 1:
        _add_reason(
            t04_reasons,
            f"font-size={font_size}px"
        )
        evidence["font_size_px"] = font_size

    if position == "absolute" and left is not None and left <= -9999:
        _add_reason(
            t04_reasons,
            f"position=absolute, left={left}px"
        )
        evidence["position"] = css.get("position")
        evidence["left"] = left

    if display == "none":
        _add_reason(t04_reasons, "display=none")
        evidence["display"] = css.get("display")

    techniques = []
    reasons = []

    if t03_reasons:
        techniques.append("T03")
        reasons.extend(
            f"T03: {reason}" for reason in t03_reasons
        )

    if t04_reasons:
        techniques.append("T04")
        reasons.extend(
            f"T04: {reason}" for reason in t04_reasons
        )

    suspicious = bool(techniques)

    # 1주차/초기 통합용 휴리스틱 점수
    if not suspicious:
        score = 0.0
    elif len(techniques) == 1:
        score = 0.8
    else:
        score = 0.95

    return {
        "element_id": element.get("id", ""),
        "detector": "style",
        "suspicious": suspicious,
        "score": score,
        "reasons": reasons,
        "evidence": {
            "techniques": techniques,
            **evidence,
        },
    }
