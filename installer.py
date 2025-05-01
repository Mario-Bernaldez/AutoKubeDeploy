#!/usr/bin/env python3
import subprocess
import sys
import os
import getpass
import argparse
import time

def is_command_available(command):
    """Verifica si un comando está disponible en el sistema."""
    result = subprocess.run(["which", command], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result.returncode == 0

import subprocess
import sys

def install_microk8s():
    """Instala MicroK8s usando Snap si no está instalado y habilita el registro local."""
    print("Instalando MicroK8s...")
    try:
        subprocess.run(["sudo", "snap", "install", "microk8s", "--classic"], check=True)
    except subprocess.CalledProcessError:
        print("❌ Error al instalar MicroK8s.")
        sys.exit(1)

    print("✅ MicroK8s instalado correctamente.")

    # Agregar el usuario al grupo microk8s para evitar usar sudo constantemente
    print("Añadiendo el usuario al grupo microk8s...")
    try:
        subprocess.run(["sudo", "usermod", "-aG", "microk8s", "$USER"], check=True)
    except subprocess.CalledProcessError:
        print("⚠️ Error al añadir el usuario al grupo microk8s. Es posible que necesites reiniciar tu sesión.")
    
    # Habilitar el registro local en MicroK8s
    print("🔧 Habilitando el registro interno de MicroK8s...")
    try:
        subprocess.run(["microk8s", "enable", "registry"], check=True)
    except subprocess.CalledProcessError:
        print("❌ Error al habilitar el registro local de MicroK8s.")
        sys.exit(1)

    print("✅ Registro de MicroK8s habilitado correctamente en localhost:32000.")

    # Reiniciar MicroK8s para aplicar los cambios
    print("♻️ Reiniciando MicroK8s para aplicar cambios...")
    try:
        subprocess.run(["microk8s", "stop"], check=True)
        subprocess.run(["microk8s", "start"], check=True)
    except subprocess.CalledProcessError:
        print("❌ Error al reiniciar MicroK8s.")
        sys.exit(1)

    print("✅ MicroK8s listo para usar.")


def start_microk8s():
    """Inicia MicroK8s."""
    print("Iniciando MicroK8s...")
    try:
        subprocess.run(["sudo", "microk8s", "start"], check=True)
    except subprocess.CalledProcessError:
        print("Error al iniciar MicroK8s.")
        sys.exit(1)

def configure_kubectl():
    """Configura el alias de kubectl si no está instalado."""
    if is_command_available("kubectl"):
        print("kubectl ya está instalado.")
    else:
        print("Creando alias para kubectl...")
        try:
            subprocess.run(["sudo", "snap", "alias", "microk8s.kubectl", "kubectl"], check=True)
        except subprocess.CalledProcessError:
            print("Error al crear alias para kubectl.")
            sys.exit(1)

def configure_permissions():
    """Configura permisos y agrega el usuario al grupo microk8s."""
    user = getpass.getuser()
    print(f"Añadiendo el usuario '{user}' al grupo microk8s...")
    
    try:
        subprocess.run(["sudo", "usermod", "-a", "-G", "microk8s", user], check=True)
    except subprocess.CalledProcessError:
        print(f"Error al añadir el usuario '{user}' al grupo microk8s.")
        sys.exit(1)

    kube_dir = os.path.expanduser("~/.kube")
    if not os.path.exists(kube_dir):
        os.makedirs(kube_dir, exist_ok=True)

    print(f"Cambiando la propiedad de {kube_dir} al usuario '{user}'...")
    try:
        subprocess.run(["sudo", "chown", "-R", user, kube_dir], check=True)
    except subprocess.CalledProcessError:
        print(f"Error al cambiar la propiedad de {kube_dir}.")
        sys.exit(1)

    print("Permisos configurados correctamente.")

def apply_group_changes():
    """Recarga los grupos del usuario actual sin necesidad de cerrar sesión."""
    print("Aplicando cambios de grupo sin cerrar sesión...")
    
    try:
        subprocess.run(["newgrp", "microk8s"], check=True)
    except subprocess.CalledProcessError:
        print("Error al aplicar el grupo microk8s. Intenta cerrar sesión o reiniciar.")
        sys.exit(1)

def configure_kubeconfig():
    """Configura el archivo ~/.kube/config con la configuración de MicroK8s."""
    kube_config_path = os.path.expanduser("~/.kube/config")
    print("Configurando Kubernetes config...")

    try:
        result = subprocess.run(["microk8s", "config"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        with open(kube_config_path, "w") as f:
            f.write(result.stdout)
        
        print(f"Configuración de Kubernetes guardada en {kube_config_path}")

    except subprocess.CalledProcessError:
        print("Error al obtener la configuración de Kubernetes desde MicroK8s.")
        sys.exit(1)

def build_and_push_docker_image(modules):
    """Construye imágenes con tag único y las sube al registro local."""
    tags = {}

    for module in modules:
        tag = str(int(time.time()))
        image_name = f"localhost:32000/{module}:{tag}"
        print(f"\n🔧 Construyendo imagen Docker {image_name}...")

        try:
            subprocess.run(["docker", "build", "-t", image_name, module], check=True)
        except subprocess.CalledProcessError:
            print("❌ Error al construir la imagen Docker.")
            sys.exit(1)

        print("\n📤 Subiendo la imagen al registro local de MicroK8s...")
        try:
            subprocess.run(["docker", "push", image_name], check=True)
        except subprocess.CalledProcessError:
            print("❌ Error al subir la imagen Docker al registro local.")
            sys.exit(1)

        print(f"\n✅ Imagen '{image_name}' subida correctamente.")
        tags[module] = tag

    return tags
def deploy_helm_chart(modules, tags):
    """Instala o actualiza el paquete Helm en Kubernetes."""
    for module in modules:
        release_name = module
        chart_path = f"{module}/helm"

        print("\n🚀 Desplegando aplicación con Helm...")

        result = subprocess.run(["helm", "list", "-q"], stdout=subprocess.PIPE, text=True)
        installed_releases = result.stdout.splitlines()

        if release_name in installed_releases:
            print("\n🔄 Actualizando el despliegue existente con Helm...")
            try:
                subprocess.run([
                    "helm", "upgrade", release_name, chart_path,
                    "--install",
                    "--set", f"image.repository=localhost:32000/{module}",
                    "--set", f"image.tag={tags[module]}"
                ], check=True)
            except subprocess.CalledProcessError:
                print("❌ Error al actualizar el despliegue con Helm.")
                sys.exit(1)
        else:
            print("\n📦 Instalando el paquete Helm...")
            try:
                subprocess.run(["helm", "install", release_name, chart_path], check=True)
            except subprocess.CalledProcessError:
                print("❌ Error al instalar el paquete Helm.")
                sys.exit(1)

        print("\n✅ Despliegue exitoso con Helm.")

def main():
    parser = argparse.ArgumentParser(description="Script para instalar y configurar MicroK8s, construir imágenes Docker y desplegar con Helm.")
    
    parser.add_argument("--install", action="store_true", help="Instala y configura MicroK8s.")
    parser.add_argument("--build", action="store_true", help="Construye y sube imágenes Docker para los módulos especificados.")
    parser.add_argument("--deploy", action="store_true", help="Despliega la aplicación con Helm usando los módulos especificados.")
    parser.add_argument("--all", action="store_true", help="Ejecuta todas las opciones: instalación, construcción y despliegue.")
    parser.add_argument("-m", "--modules", action="append", help="Lista de módulos a procesar.", default=[])

    args = parser.parse_args()

    if args.all or args.install:
        if not is_command_available("microk8s"):
            print("MicroK8s no está instalado. Procediendo con la instalación...")
            install_microk8s()
        else:
            print("✅ MicroK8s ya está instalado.")

        start_microk8s()
        configure_kubectl()
        configure_permissions()
        apply_group_changes()
        configure_kubeconfig()

    if args.all or args.build:
        if not args.modules:
            print("⚠️ Debes especificar al menos un módulo con -m para construir.")
            sys.exit(1)
        module_tags = build_and_push_docker_image(args.modules)
    else:
        module_tags = {}

    if args.all or args.deploy:
        if not args.modules:
            print("⚠️ Debes especificar al menos un módulo con -m para desplegar.")
            sys.exit(1)
        deploy_helm_chart(args.modules, module_tags)

    print("\n✅ Proceso completado correctamente.")

if __name__ == "__main__":
    main()