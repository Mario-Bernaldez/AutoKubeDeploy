import unittest
import requests
import utils

BASE_URL = f"http://{utils.get_internal_url("generator-engine")}"


class TestGenerateEndpoint(unittest.TestCase):

    def test_generate_namespace(self):
        payload = {
            "namespace": {"namespace_name": "test-namespace", "labels": "app=test"}
        }
        response = requests.post(f"{BASE_URL}/generate", json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn("kind: Namespace", response.text)

    def test_generate_service(self):
        payload = {
            "service": {
                "service_name": "test-service",
                "service_type": "ClusterIP",
                "selector": "app=test",
                "ports": [{"port": 80, "target_port": 8080, "protocol": "TCP"}],
            }
        }
        response = requests.post(f"{BASE_URL}/generate", json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn("kind: Service", response.text)

    def test_generate_configmap(self):
        payload = {
            "configmap": {
                "configmap_name": "test-config",
                "namespace": "default",
                "keys": [
                    {
                        "key_name": "config.json",
                        "is_multiline": True,
                        "value": '{\n  "env": "prod"\n}',
                    }
                ],
            }
        }
        response = requests.post(f"{BASE_URL}/generate", json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn("kind: ConfigMap", response.text)

    def test_generate_secret_opaque(self):
        payload = {
            "secret": {
                "secret_name": "test-secret",
                "namespace": "default",
                "secret_type": "Opaque",
                "data": [
                    {"key_name": "username", "value": "admin"},
                    {"key_name": "password", "value": "secret"},
                ],
            }
        }
        response = requests.post(f"{BASE_URL}/generate", json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn("kind: Secret", response.text)

    def test_generate_pvc(self):
        payload = {
            "pvc": {
                "pvc_name": "test-pvc",
                "namespace": "default",
                "storage_request": "1Gi",
                "access_modes": ["ReadWriteOnce"],
                "storage_class_name": "standard",
            }
        }
        response = requests.post(f"{BASE_URL}/generate", json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn("kind: PersistentVolumeClaim", response.text)

    def test_generate_hpa(self):
        payload = {
            "hpa": {
                "hpa_name": "test-hpa",
                "namespace": "default",
                "target_deployment": "test-deployment",
                "min_replicas": 1,
                "max_replicas": 3,
                "metrics": [
                    {
                        "resource_name": "cpu",
                        "target_type": "Utilization",
                        "target_value": 75,
                    }
                ],
            }
        }
        response = requests.post(f"{BASE_URL}/generate", json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn("kind: HorizontalPodAutoscaler", response.text)

    def test_generate_ingress(self):
        payload = {
            "ingress": {
                "ingress_name": "test-ingress",
                "namespace": "default",
                "host": "example.com",
                "paths": [
                    {"path": "/", "service_name": "test-service", "service_port": 80}
                ],
            }
        }
        response = requests.post(f"{BASE_URL}/generate", json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn("kind: Ingress", response.text)

    def test_generate_serviceaccount(self):
        payload = {
            "serviceaccount": {
                "service_account_name": "test-sa",
                "namespace": "default",
                "imagePullSecrets": ["my-secret"],
            }
        }
        response = requests.post(f"{BASE_URL}/generate", json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn("kind: ServiceAccount", response.text)

    def test_generate_role(self):
        payload = {
            "role": {
                "type": "Role",
                "name": "test-role",
                "namespace": "default",
                "rules": [
                    {
                        "apiGroups": [""],
                        "resources": ["pods"],
                        "verbs": ["get", "watch", "list"],
                    }
                ],
                "binding": {
                    "name": "test-role-binding",
                    "namespace": "default",
                    "subjects": [{"kind": "ServiceAccount", "name": "default"}],
                },
            }
        }
        response = requests.post(f"{BASE_URL}/generate", json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn("kind: Role", response.text)
        self.assertIn("kind: RoleBinding", response.text)

    def test_invalid_json_format(self):
        invalid_json = '{"namespace": {"namespace_name": "test", "labels": app=test}}'

        headers = {"Content-Type": "application/json"}
        response = requests.post(
            f"{BASE_URL}/generate", data=invalid_json, headers=headers
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("Error parsing JSON", response.text)

    def test_missing_valid_object(self):
        payload = {"foo": {"bar": "baz"}}
        response = requests.post(f"{BASE_URL}/generate", json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("No valid Kubernetes object provided", response.text)


if __name__ == "__main__":
    unittest.main()
