from flask import Flask
import os
import requests

app = Flask(__name__)

@app.route("/")
def index():
    bg_color = os.environ.get("BG_COLOR", "#000000")
    pod_name = os.environ.get("HOSTNAME", "Unknown")
    try:
        with open("/etc/config/CONFIG_TEXT") as f:
            config_text = f.read()
    except:
        config_text = "No config text"
    try:
        with open("/etc/secret/my_secret.txt") as f:
            secret_text = f.read()
    except:
        secret_text = "No secret found"

    try:
        with open("/mnt/data/volume_data.txt") as f:
            volume_text = f.read()
    except:
        volume_text = "No volume data found"

    try:
        with open("/var/run/secrets/kubernetes.io/serviceaccount/namespace") as f:
            namespace = f.read()
    except:
        namespace = "Unknown"

    # Probar conexión saliente
    try:
        response = requests.get("https://example.com", timeout=3)
        external_status = f"Acceso permitido (status {response.status_code})"
    except Exception as e:
        external_status = f"❌ Bloqueado: {e}"

    return f"""
    <html>
    <body style='background-color:{bg_color}; font-family: sans-serif;'>
        <div style='padding: 2rem; max-width: 800px; margin: auto; background: #fff; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1);'>
            <h1>Demo Kubernetes Visual</h1>
            <p><strong>Texto desde ConfigMap:</strong> {config_text}</p>
            <p><strong>Texto desde Secret:</strong> {secret_text}</p>
            <p><strong>Contenido de volumen PVC:</strong> {volume_text}</p>
            <p><strong>Pod:</strong> {pod_name}</p>
            <p><strong>Namespace:</strong> {namespace}</p>
            <p><strong>Conexión externa:</strong> {external_status}</p>
        </div>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
