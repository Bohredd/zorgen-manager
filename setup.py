from setuptools import setup, find_packages

PACKAGE_DATA = list()
setup(
    name="zorgen-manager",
    version="0.0.5",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    license="MIT License",
    description="Um pacote que auxília na criação de APPs Django no Padrão da Zorgen",
    long_description=open("README.md").read(),
    author="Diogo Antonio",
    author_email="bohreddev@gmail.com",
    classifiers=[
        "Framework :: Django Zorgen Template APP",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
    ],
    install_requires=[
        "Django==4.2.13",
        "python-decouple==3.8",
        "django-extensions==3.2.3",
        "requests==2.32.3",
        "psycopg2==2.9.9",
        "sentry-sdk==2.11.0",
    ],
    entry_points={
        'console_scripts': [
            'zorgen-admin=zorgen_manager.commands.zorgen_admin:main',
        ],
    },
)
