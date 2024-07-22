import shutil
import os
import sys

def is_ignored_directory(path):
    ignored_dirs = {'VENV', 'venv', 'env', 'ENV', 'virtualenv', 'VIRTUALENV', 'ENVIROMENT'}
    # Check if the path or any of its parent directories is in the ignored_dirs list
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

def create_app_directory(app_name):
    try:
        base_dir = find_manage_py()
        base_dir = base_dir.split('/manage.py')[0]
    except FileNotFoundError as e:
        print(e)
        exit(1)
    
    # print(base_dir)
    source_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app')
    destination_dir = os.path.join(base_dir, app_name)

    if not os.path.exists(source_dir):
        # print(f"Source directory {source_dir} does not exist.")
        exit(1)

    if os.path.exists(destination_dir):
        # print("existia foi exlcuido")
        shutil.rmtree(destination_dir)
    # else:
    #     os.makedirs(destination_dir, exist_ok=True)
    #     print("Diretório de destino criado:", destination_dir)

    try:
        shutil.copytree(source_dir, destination_dir, dirs_exist_ok=True)
    except Exception as e:
        # print(f"Error copying directory: {e}")
        exit(1)
    
    update_apps_file(destination_dir, app_name)

    pycache_dir = os.path.join(destination_dir, '__pycache__')
    if os.path.exists(pycache_dir):
        # print(f"Deleting __pycache__ directory at {pycache_dir}")
        shutil.rmtree(pycache_dir)

        for root, dirs, files in os.walk(destination_dir, topdown=False):
            if '__pycache__' in dirs:
                pycache_dir = os.path.join(root, '__pycache__')
                # print(f"Deleting __pycache__ directory at {pycache_dir}")
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

# Example usage:
# create_app_directory('my_new_app')
