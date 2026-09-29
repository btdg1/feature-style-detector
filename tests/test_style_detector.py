import unittest

from src.ad_inspector.style_detector import detect_style


class StyleDetectorTest(unittest.TestCase):

    def test_t03_opacity_zero(self):
        result = detect_style({
            "id": "e1",
            "computed_style": {"opacity": "0"}
        })
        self.assertTrue(result["suspicious"])
        self.assertIn("T03", result["evidence"]["techniques"])

    def test_t03_transparent(self):
        result = detect_style({
            "id": "e2",
            "computed_style": {"color": "transparent"}
        })
        self.assertTrue(result["suspicious"])
        self.assertIn("T03", result["evidence"]["techniques"])

    def test_t03_same_color(self):
        result = detect_style({
            "id": "e3",
            "computed_style": {
                "color": "rgb(255, 255, 255)",
                "background_color": "rgb(255, 255, 255)"
            }
        })
        self.assertTrue(result["suspicious"])
        self.assertIn("T03", result["evidence"]["techniques"])

    def test_t04_font_size_zero(self):
        result = detect_style({
            "id": "e4",
            "computed_style": {"font_size_px": 0}
        })
        self.assertTrue(result["suspicious"])
        self.assertIn("T04", result["evidence"]["techniques"])

    def test_t04_font_size_one(self):
        result = detect_style({
            "id": "e5",
            "computed_style": {"font_size_px": 1}
        })
        self.assertTrue(result["suspicious"])
        self.assertIn("T04", result["evidence"]["techniques"])

    def test_t04_offscreen(self):
        result = detect_style({
            "id": "e6",
            "computed_style": {
                "position": "absolute",
                "left": "-9999px"
            }
        })
        self.assertTrue(result["suspicious"])
        self.assertIn("T04", result["evidence"]["techniques"])

    def test_t04_display_none(self):
        result = detect_style({
            "id": "e7",
            "computed_style": {"display": "none"}
        })
        self.assertTrue(result["suspicious"])
        self.assertIn("T04", result["evidence"]["techniques"])

    def test_normal_element(self):
        result = detect_style({
            "id": "normal",
            "computed_style": {
                "display": "block",
                "visibility": "visible",
                "opacity": "1",
                "font_size_px": 16,
                "color": "rgb(0, 0, 0)",
                "background_color": "rgb(255, 255, 255)"
            }
        })

        self.assertFalse(result["suspicious"])
        self.assertEqual(result["score"], 0.0)
        self.assertEqual(result["evidence"]["techniques"], [])

    def test_team_sample_element(self):
        result = detect_style({
            "id": "e1",
            "frame_path": [],
            "selector": "body > main > div:nth-of-type(1)",
            "tag": "div",
            "text": "예시 광고 문구",
            "html": "<div>예시 광고 문구</div>",
            "computed_style": {
                "display": "block",
                "visibility": "visible",
                "opacity": "1",
                "font_size_px": 16,
                "color": "rgb(0, 0, 0)",
                "background_color": "rgb(255, 255, 255)"
            },
            "bounding_box": {
                "x": 20,
                "y": 40,
                "width": 100,
                "height": 20
            }
        })

        self.assertFalse(result["suspicious"])


if __name__ == "__main__":
    unittest.main()
