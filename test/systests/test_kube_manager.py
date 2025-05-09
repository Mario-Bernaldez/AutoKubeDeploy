import unittest
import requests
import time
import utils

BASE_URL = f"http://{utils.get_internal_url("kube-manager")}"


class TestKubeManagerIntegration(unittest.TestCase):

    def test_1_deploy_valid_yaml(self):
        yaml = """
apiVersion: v1
kind: ConfigMap
metadata:
  name: test-configmap
  namespace: default
data:
  key: value
"""
        response = requests.post(
            f"{BASE_URL}/deploy",
            data=yaml,
            headers={"Content-Type": "application/yaml"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("YAML successfully deployed", response.text)

    def test_2_list_existing_resource(self):
        time.sleep(2)
        params = {"resource": "ConfigMap", "namespace": "default"}
        response = requests.get(f"{BASE_URL}/list", params=params)
        self.assertEqual(response.status_code, 200)
        names = response.json()
        self.assertIn("test-configmap", names)

    def test_3_delete_existing_resource(self):
        params = {"type": "ConfigMap", "name": "test-configmap", "namespace": "default"}
        response = requests.delete(f"{BASE_URL}/resource", params=params)
        self.assertEqual(response.status_code, 204)

    def test_4_list_missing_resource_type(self):
        response = requests.get(f"{BASE_URL}/list")
        self.assertEqual(response.status_code, 400)
        self.assertIn("Missing 'resource' parameter", response.text)

    def test_5_deploy_invalid_yaml(self):
        invalid_yaml = "invalid_yaml: ["
        response = requests.post(f"{BASE_URL}/deploy", data=invalid_yaml)
        self.assertEqual(response.status_code, 500)
        self.assertIn("Error applying YAML", response.text)

    def test_6_delete_missing_parameters(self):
        response = requests.delete(f"{BASE_URL}/resource")
        self.assertEqual(response.status_code, 400)
        self.assertIn("Missing 'type' or 'name'", response.text)


if __name__ == "__main__":
    unittest.main()
