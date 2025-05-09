import subprocess


def get_internal_url(service_name):
    "Retrieve the clusterIP URL of a Kubernetes service using 'kubectl'."
    return subprocess.check_output(
        [
            "kubectl",
            "get",
            "svc",
            service_name,
            "-o",
            "jsonpath={.spec.clusterIP}:{.spec.ports[0].port}",
        ],
        text=True,
    ).strip()
