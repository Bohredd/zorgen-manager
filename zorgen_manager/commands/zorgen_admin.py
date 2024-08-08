import subprocess
import shutil
import os
import sys
import re

def is_ignored_directory(path):
    ignored_dirs = {'VENV', 'venv', 'env', 'ENV', 'virtualenv', 'VIRTUALENV', 'ENVIROMENT', 'enviroment'}
    while path != os.path.dirname(path):
        if os.path.basename(path) in ignored_dirs:
            return True
        path = os.path.dirname(path)
    return False

def find_manage_py():
    start_dir = os.getcwd()

    for root, dirs, files in os.walk(start_dir):
        if 'manage.py' in files and not is_ignored_directory(root):
            return os.path.join(root, 'manage.py')
    raise FileNotFoundError("manage.py not found in non-ignored directories.")

def find_settings_py(base_dir):
    for root, dirs, files in os.walk(base_dir):
        if 'settings.py' in files:
            return os.path.join(root, 'settings.py')
    raise FileNotFoundError("settings.py not found")

def add_app_to_installed_apps(settings_path, app_name):
    try:
        with open(settings_path, 'r') as file:
            lines = file.readlines()
        
        with open(settings_path, 'w') as file:
            in_installed_apps = False
            for line in lines:
                if line.strip() == 'INSTALLED_APPS = [':
                    in_installed_apps = True
                if in_installed_apps and line.strip() == ']':
                    file.write(f"    '{app_name}',\n")
                    in_installed_apps = False
                file.write(line)
                
    except Exception as e:
        print(f"Error updating {settings_path}: {e}")

def create_app_directory(app_name):
    try:
        base_dir = find_manage_py()
        base_dir = base_dir.split('/manage.py')[0]
    except FileNotFoundError as e:
        print(e)
        exit(1)

    try:
        settings_path = find_settings_py(base_dir)
        print(f"Found settings.py at: {settings_path}")
        add_app_to_installed_apps(settings_path, app_name)
    except FileNotFoundError as e:
        print(e)
        exit(1)
    
    source_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'app')
    destination_dir = os.path.join(base_dir, app_name)

    if os.path.exists(destination_dir):
        shutil.rmtree(destination_dir)

    shutil.copytree(source_dir, destination_dir, dirs_exist_ok=True)
    
    update_apps_file(destination_dir, app_name)

    pycache_dir = os.path.join(destination_dir, '__pycache__')
    if os.path.exists(pycache_dir):
        shutil.rmtree(pycache_dir)

    for root, dirs, files in os.walk(destination_dir, topdown=False):
        if '__pycache__' in dirs:
            pycache_dir = os.path.join(root, '__pycache__')
            shutil.rmtree(pycache_dir)

def update_apps_file(app_dir, app_name):
    apps_file_path = os.path.join(app_dir, 'apps.py')
    
    if not os.path.exists(apps_file_path):
        return
    
    try:
        with open(apps_file_path, 'r') as file:
            content = file.read()
        
        content = content.replace('class AppNameConfig(AppConfig):', f'class {app_name.capitalize()}Config(AppConfig):')
        content = content.replace('name = "appname"', f'name = "{app_name}"')

        with open(apps_file_path, 'w') as file:
            file.write(content)
    except Exception as e:
        print(f"Error updating apps file: {e}")

def custom_startapp():
    if len(sys.argv) < 3:
        print("Por favor, forneça o nome do aplicativo.")
        sys.exit(1)

    app_name = sys.argv[2]
    create_app_directory(app_name)
    print(f"Criado APP de maneira personalizada: {app_name}")

def replace_project_references(project_name):
    pattern = re.compile(r'<\s*projeto\s*>', re.IGNORECASE)
    
    for root, dirs, files in os.walk(os.getcwd()):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            if not is_ignored_directory(root):
                print("FILE PATH PARA ARRUMAR: ", file_path)
                try:
                    with open(file_path, 'r') as file:
                        content = file.read()

                    if pattern.search(content):
                        updated_content = pattern.sub(project_name, content)

                        with open(file_path, 'w') as file:
                            file.write(updated_content)

                        print(f'Sucesso ao atualizar {file_path}')
                except (UnicodeDecodeError, FileNotFoundError):
                    continue
def custom_compose():
    if len(sys.argv) < 3:
        print("Por favor, forneça o nome do projeto.")
        sys.exit(1)

    project_name = sys.argv[2]
    replace_project_references(project_name)
    print(f"Substituições para o projeto '{project_name}' concluídas.")

def main():
    if len(sys.argv) < 2:
        print("Por favor, forneça um comando.")
        sys.exit(1)

    command = sys.argv[1]

    if command == 'startapp':
        custom_startapp()
    elif command =='compose':
        custom_compose()
    else:
        django_command = ['django-admin'] + sys.argv[1:]
        result = subprocess.run(django_command, capture_output=True, text=True)
        print(result.stdout)
        print(result.stderr, file=sys.stderr)
        sys.exit(result.returncode)

if __name__ == "__main__":
    main()
