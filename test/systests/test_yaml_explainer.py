import unittest
import requests
import utils

BASE_URL = f"http://{utils.get_internal_url("yaml-explainer")}"


class TestYAMLExplainerIntegration(unittest.TestCase):

    def test_1_explain_valid_yaml(self):
        payload = {
            "yaml": """
apiVersion: v1
kind: Namespace
metadata:
  name: test-ns
""",
            "model": "openchat/openchat-7b:free",
        }
        response = requests.post(f"{BASE_URL}/explain", json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn("explanation", response.json())

    def test_2_explain_invalid_yaml(self):
        payload = {
            "yaml": "kind: Pod\nmetadata: [invalid",
            "model": "openchat/openchat-7b:free",
        }
        response = requests.post(f"{BASE_URL}/explain", json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid YAML", response.text)

    def test_3_explain_missing_body(self):
        response = requests.post(
            f"{BASE_URL}/explain",
            data="not-json",
            headers={"Content-Type": "application/json"},
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("Error reading request body", response.text)

    def test_4_explain_wrong_method(self):
        response = requests.get(f"{BASE_URL}/explain")
        self.assertEqual(response.status_code, 405)
        self.assertIn("Method not allowed", response.text)

    def test_5_get_models(self):
        response = requests.get(f"{BASE_URL}/models")
        self.assertEqual(response.status_code, 200)
        models = response.json()
        self.assertTrue(isinstance(models, list))
        self.assertTrue(any("id" in m and "name" in m for m in models))

    def test_6_get_models_filter_free(self):
        response = requests.get(f"{BASE_URL}/models?free=true")
        self.assertEqual(response.status_code, 200)
        models = response.json()
        self.assertTrue(all(m.get("free", False) for m in models))


if __name__ == "__main__":
    unittest.main()
