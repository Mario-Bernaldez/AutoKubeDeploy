#!/usr/bin/env python3
import subprocess
import sys
import os
import getpass
import argparse
import time
import yaml


def load_modules_config():
    """Loads the modules.yaml file to get module configuration."""
    config_path = os.path.join(os.path.dirname(__file__), "modules.yaml")
    try:
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
        return config.get("modules", {})
    except Exception as e:
        print(f"❌ Error loading modules.yaml: {e}")
        sys.exit(1)


def is_command_available(command):
    """Checks if a command is available in the system."""
    result = subprocess.run(
        ["which", command], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    return result.returncode == 0


def install_microk8s():
    """Installs MicroK8s using Snap if not installed and enables the local registry."""
    print("Installing MicroK8s...")
    try:
        subprocess.run(["sudo", "snap", "install", "microk8s", "--classic"], check=True)
    except subprocess.CalledProcessError:
        print("❌ Failed to install MicroK8s.")
        sys.exit(1)

    print("✅ MicroK8s installed successfully.")

    print("Adding user to microk8s group...")
    try:
        subprocess.run(["sudo", "usermod", "-aG", "microk8s", "$USER"], check=True)
    except subprocess.CalledProcessError:
        print(
            "⚠️ Failed to add user to microk8s group. You may need to log out and back in."
        )

    print("🔧 Enabling MicroK8s built-in registry...")
    try:
        subprocess.run(["microk8s", "enable", "registry"], check=True)
    except subprocess.CalledProcessError:
        print("❌ Failed to enable MicroK8s registry.")
        sys.exit(1)

    print("✅ MicroK8s registry enabled on localhost:32000.")

    print("♻️ Restarting MicroK8s to apply changes...")
    try:
        subprocess.run(["microk8s", "stop"], check=True)
        subprocess.run(["microk8s", "start"], check=True)
    except subprocess.CalledProcessError:
        print("❌ Failed to restart MicroK8s.")
        sys.exit(1)

    print("✅ MicroK8s is ready to use.")


def start_microk8s():
    """Starts MicroK8s."""
    print("Starting MicroK8s...")
    try:
        subprocess.run(["sudo", "microk8s", "start"], check=True)
    except subprocess.CalledProcessError:
        print("Failed to start MicroK8s.")
        sys.exit(1)


def configure_kubectl():
    """Sets up kubectl alias if not installed."""
    if is_command_available("kubectl"):
        print("kubectl is already installed.")
    else:
        print("Creating alias for kubectl...")
        try:
            subprocess.run(
                ["sudo", "snap", "alias", "microk8s.kubectl", "kubectl"], check=True
            )
        except subprocess.CalledProcessError:
            print("Failed to create alias for kubectl.")
            sys.exit(1)


def configure_permissions():
    """Sets permissions and adds the user to the microk8s group."""
    user = getpass.getuser()
    print(f"Adding user '{user}' to microk8s group...")

    try:
        subprocess.run(["sudo", "usermod", "-a", "-G", "microk8s", user], check=True)
    except subprocess.CalledProcessError:
        print(f"Failed to add user '{user}' to microk8s group.")
        sys.exit(1)

    kube_dir = os.path.expanduser("~/.kube")
    if not os.path.exists(kube_dir):
        os.makedirs(kube_dir, exist_ok=True)

    print(f"Changing ownership of {kube_dir} to user '{user}'...")
    try:
        subprocess.run(["sudo", "chown", "-R", user, kube_dir], check=True)
    except subprocess.CalledProcessError:
        print(f"Failed to change ownership of {kube_dir}.")
        sys.exit(1)

    print("Permissions configured successfully.")


def apply_group_changes():
    """Applies group changes without requiring a logout."""
    print("Applying group changes without logging out...")

    try:
        subprocess.run(["newgrp", "microk8s"], check=True)
    except subprocess.CalledProcessError:
        print("Failed to apply microk8s group. Try logging out or rebooting.")
        sys.exit(1)


def configure_kubeconfig():
    """Sets the ~/.kube/config file with MicroK8s configuration."""
    kube_config_path = os.path.expanduser("~/.kube/config")
    print("Configuring Kubernetes config...")

    try:
        result = subprocess.run(
            ["microk8s", "config"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )
        with open(kube_config_path, "w") as f:
            f.write(result.stdout)

        print(f"Kubernetes configuration saved at {kube_config_path}")

    except subprocess.CalledProcessError:
        print("Failed to get Kubernetes config from MicroK8s.")
        sys.exit(1)


def build_and_push_docker_image(modules):
    """Builds Docker images with unique tags and pushes them to the local registry."""
    tags = {}

    for module in modules:
        tag = str(int(time.time()))
        image_name = f"localhost:32000/{module}:{tag}"
        print(f"\n🔧 Building Docker image {image_name}...")

        try:
            subprocess.run(["docker", "build", "-t", image_name, module], check=True)
        except subprocess.CalledProcessError:
            print("❌ Failed to build Docker image.")
            sys.exit(1)

        print("\n📤 Pushing image to local MicroK8s registry...")
        try:
            subprocess.run(["docker", "push", image_name], check=True)
        except subprocess.CalledProcessError:
            print("❌ Failed to push Docker image to local registry.")
            sys.exit(1)

        print(f"\n✅ Image '{image_name}' pushed successfully.")
        tags[module] = tag

    return tags


def deploy_helm_chart(modules, tags):
    """Installs or updates the Helm chart in Kubernetes."""
    modules_config = load_modules_config()

    for module in modules:
        release_name = module
        chart_path = f"{module}/helm"
        module_type = modules_config.get(module, {}).get("type", "internal")

        print(f"\n🚀 Deploying '{module}' ({module_type}) with Helm...")

        helm_cmd = ["helm", "upgrade", "--install", release_name, chart_path]

        if module_type == "internal":
            helm_cmd += [
                "--set",
                f"image.repository=localhost:32000/{module}",
                "--set",
                f"image.tag={tags[module]}",
            ]

        try:
            subprocess.run(helm_cmd, check=True)
        except subprocess.CalledProcessError:
            print(f"❌ Failed to deploy '{module}' with Helm.")
            sys.exit(1)

        print(f"✅ '{module}' deployed successfully.")


def main():
    parser = argparse.ArgumentParser(
        description="Script to install and configure MicroK8s, build Docker images, and deploy using Helm."
    )

    parser.add_argument(
        "--install", action="store_true", help="Install and configure MicroK8s."
    )
    parser.add_argument(
        "--build",
        action="store_true",
        help="Build and push Docker images for the specified modules.",
    )
    parser.add_argument(
        "--deploy",
        action="store_true",
        help="Deploy the application using Helm with the specified modules.",
    )
    parser.add_argument(
        "--all", action="store_true", help="Run all: install, build, and deploy."
    )
    parser.add_argument(
        "-m",
        "--modules",
        action="append",
        help="List of modules to process.",
        default=[],
    )

    args = parser.parse_args()

    if args.all or args.install:
        if not is_command_available("microk8s"):
            print("MicroK8s is not installed. Proceeding with installation...")
            install_microk8s()
        else:
            print("✅ MicroK8s is already installed.")

        start_microk8s()
        configure_kubectl()
        configure_permissions()
        apply_group_changes()
        configure_kubeconfig()

    modules_config = load_modules_config()
    module_tags = {}

    if not args.modules:
        args.modules = list(modules_config.keys())

    if args.all or args.build:
        to_build = []
        for module in args.modules:
            module_type = modules_config.get(module, {}).get("type", "internal")
            if module_type == "external":
                print(f"🔹 '{module}' is external, skipping build.")
                module_tags[module] = None
            else:
                to_build.append(module)

        if to_build:
            tags = build_and_push_docker_image(to_build)
            module_tags.update(tags)

    if args.all or args.deploy:
        deploy_helm_chart(args.modules, module_tags)

    print("\n✅ Process completed successfully.")


if __name__ == "__main__":
    main()
