import subprocess
import sys
from ..zorgen import create_app_directory

def custom_startapp():
    if len(sys.argv) < 3:
        print("Por favor, forneça o nome do aplicativo.")
        sys.exit(1)

    app_name = sys.argv[2]
    create_app_directory(app_name)
    print(f"Criado APP de maneira personalizada: {app_name}")


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
