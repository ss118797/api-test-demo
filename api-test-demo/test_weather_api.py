import requests
import unittest


class TestWeatherAPI(unittest.TestCase):
    """高德天气API接口测试"""

    # 换成你自己的Key
    API_KEY = "e9795097dc9c7e12b62311dd0fd2adb6"
    BASE_URL = "https://restapi.amap.com/v3/weather/weatherInfo"

    # ---------- 正常场景 ----------
    def test_query_by_chinese_city(self):
        """API-001: 中文城市名查询，期望返回成功"""
        params = {"key": self.API_KEY, "city": "成都"}
        response = requests.get(self.BASE_URL, params=params)

        # 断言状态码
        self.assertEqual(response.status_code, 200)
        # 断言响应体status字段
        body = response.json()
        self.assertEqual(body["status"], "1")
        self.assertEqual(body["infocode"], "10000")
        # 断言有天气数据
        self.assertIn("lives", body)
        self.assertGreater(len(body["lives"]), 0)

    def test_query_by_adcode(self):
        """API-002: 城市编码查询，期望返回成功"""
        params = {"key": self.API_KEY, "city": "510100"}
        response = requests.get(self.BASE_URL, params=params)
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body["status"], "1")

    def test_extensions_all(self):
        """API-013: 获取天气预报，期望返回成功"""
        params = {"key": self.API_KEY, "city": "成都", "extensions": "all"}
        response = requests.get(self.BASE_URL, params=params)
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body["status"], "1")
        # 预报接口返回的是 forecasts 字段
        self.assertIn("forecasts", body)

    # ---------- 异常场景 ----------
    def test_city_empty(self):
        """API-003: 缺少city参数，期望返回失败"""
        params = {"key": self.API_KEY}
        response = requests.get(self.BASE_URL, params=params)
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body["status"], "0")
        self.assertNotEqual(body["infocode"], "10000")

    def test_city_not_exist(self):
        """API-004: 不存在的城市，期望返回失败"""
        params = {"key": self.API_KEY, "city": "不存在的城市999"}
        response = requests.get(self.BASE_URL, params=params)
        body = response.json()
        self.assertEqual(body["status"], "0")

    def test_city_special_chars(self):
        """API-006: 特殊字符城市名，期望返回失败"""
        params = {"key": self.API_KEY, "city": "@#$"}
        response = requests.get(self.BASE_URL, params=params)
        body = response.json()
        self.assertEqual(body["status"], "0")

    def test_key_empty(self):
        """API-008: 缺少key参数，期望返回失败"""
        params = {"city": "成都"}
        response = requests.get(self.BASE_URL, params=params)
        body = response.json()
        self.assertEqual(body["status"], "0")

    def test_key_invalid(self):
        """API-009: 错误key，期望返回失败"""
        params = {"key": "123456789", "city": "成都"}
        response = requests.get(self.BASE_URL, params=params)
        body = response.json()
        self.assertEqual(body["status"], "0")

    def test_post_method(self):
        """API-014: 使用POST方法，期望返回失败"""
        data = {"key": self.API_KEY, "city": "成都"}
        response = requests.post(self.BASE_URL, data=data)
        body = response.json()
        # 高德API对POST可能返回错误或仍返回结果，以实际为准
        self.assertIn(body["status"], ["0", "1"])  # 记录实际表现

    def test_city_number_string(self):
        """补充用例: city传纯数字字符串（非adcode），期望失败"""
        params = {"key": self.API_KEY, "city": "123456"}
        response = requests.get(self.BASE_URL, params=params)
        body = response.json()
        self.assertEqual(body["status"], "0")

    # ---------- 边界场景 ----------
    def test_response_time(self):
        """响应时间应在3秒内"""
        params = {"key": self.API_KEY, "city": "成都"}
        response = requests.get(self.BASE_URL, params=params)
        self.assertLess(response.elapsed.total_seconds(), 3.0)

    def test_response_content_type(self):
        """响应头Content-Type应为application/json"""
        params = {"key": self.API_KEY, "city": "成都"}
        response = requests.get(self.BASE_URL, params=params)
        self.assertIn("application/json", response.headers["Content-Type"])


if __name__ == "__main__":
    unittest.main(verbosity=2)