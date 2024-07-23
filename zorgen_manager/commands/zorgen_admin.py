import subprocess
import shutil
import os
import sys

def is_ignored_directory(path):
    ignored_dirs = {'VENV', 'venv', 'env', 'ENV', 'virtualenv', 'VIRTUALENV', 'ENVIROMENT', 'enviroment'}
    while path != os.path.dirname(path):
        if os.path.basename(path) in ignored_dirs:
            return True
        path = os.path.dirname(path)
    return False

def find_settings_directory():
    start_path = os.getcwd()

    # Caminho para iniciar a busca
    for root, dirs, files in os.walk(start_path):
        # Arquivos que estamos procurando
        required_files = {"settings.py", "urls.py", "wsgi.py", "asgi.py"}
        # Verifica se todos os arquivos requeridos estão presentes no diretório atual
        if required_files.issubset(set(files)):
            print(f'Diretório encontrado: {root}')
            return root
    raise FileNotFoundError("settings.py not found.")

def find_manage_py():
    start_dir = os.getcwd()

    for root, dirs, files in os.walk(start_dir):
        if 'manage.py' in files and not is_ignored_directory(root):
            return os.path.join(root, 'manage.py')
    raise FileNotFoundError("manage.py not found in non-ignored directories.")

def create_app_directory(app_name):
    try:
        base_dir = find_manage_py()
        base_dir = base_dir.split('/manage.py')[0]
    except FileNotFoundError as e:
        print(e)
        exit(1)
    
    source_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app')
    destination_dir = os.path.join(base_dir, app_name)

    if not os.path.exists(source_dir):
        exit(1)

    if os.path.exists(destination_dir):
        shutil.rmtree(destination_dir)

    try:
        shutil.copytree(source_dir, destination_dir, dirs_exist_ok=True)
    except Exception as e:
        exit(1)
    
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
        
        content = content.replace('class AppNameConfig(AppConfig):', f'class {app_name}Config(AppConfig):')
        content = content.replace('name = "appname"', f'name = "{app_name}"')

        with open(apps_file_path, 'w') as file:
            file.write(content)
    except Exception as e:
        print(f"Error updating apps file: {e}")

def display_settings_file():
    try:
        settings_dir = find_settings_directory()
        settings_file_path = os.path.join(settings_dir, 'settings.py')

        if os.path.exists(settings_file_path):
            with open(settings_file_path, 'r') as file:
                print(file.read())
        else:
            print("settings.py não encontrado.")
    except FileNotFoundError as e:
        print(e)

def custom_startapp():
    if len(sys.argv) < 3:
        print("Por favor, forneça o nome do aplicativo.")
        sys.exit(1)

    app_name = sys.argv[2]
    create_app_directory(app_name)
    print(f"Criado APP de maneira personalizada: {app_name}")
    display_settings_file()

def main():
    if len(sys.argv) < 2:
        print("Por favor, forneça um comando.")
        sys.exit(1)

    command = sys.argv[1]

    if command == 'startapp':
        custom_startapp()
    else:
        django_command = ['django-admin'] + sys.argv[1:]
        result = subprocess.run(django_command, capture_output=True, text=True)
        print(result.stdout)
        print(result.stderr, file=sys.stderr)
        sys.exit(result.returncode)

if __name__ == "__main__":
    main()
