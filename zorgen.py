import shutil
import os
import sys

def create_app_directory(app_name):
    source_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app')
    
    destination_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), app_name)

    if not os.path.exists(source_dir):
        exit(1)

    if os.path.exists(destination_dir):
        shutil.rmtree(destination_dir)
    
    shutil.copytree(source_dir, destination_dir, dirs_exist_ok=True)
    
    update_apps_file(destination_dir, app_name)

def update_apps_file(app_dir, app_name):
    apps_file_path = os.path.join(app_dir, 'apps.py')
    
    if not os.path.exists(apps_file_path):
        return
    
    with open(apps_file_path, 'r') as file:
        content = file.read()


    content = content.replace('class AppNameConfig(AppConfig):', f'class {app_name}Config(AppConfig):')
    content = content.replace('name = "appname"', f'name = "{app_name}"')

    with open(apps_file_path, 'w') as file:
        file.write(content)
    
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python zorgen.py createapp <nome>")
        sys.exit(1)
    
    command = sys.argv[1]
    app_name = sys.argv[2]
    
    if command == "createapp":
        create_app_directory(app_name)
        print(f"APP {app_name} criado com sucesso!")
    else:
        print("Comando inválido. Use: python zorgen.py createapp <nome>")
        sys.exit(1)
