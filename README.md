# Django Zorgen Templator

Django Zorgen Templator é uma biblioteca projetada para criar aplicativos e projetos Django de maneira padronizada Zorgen. Utilizando comandos simples, você pode iniciar novos projetos e aplicativos Django com uma estrutura predefinida e consistente. Esta biblioteca facilita a configuração inicial e garante que todos os projetos sigam as melhores práticas e padrões de codificação Zorgenática.

## Instalação

Para instalar o Django Zorgen Templator, você pode usar o pip:

```bash
pip install git+https://github.com/Bohredd/zorgen-manager.git
```

<h1> Uso </h1>
<h3> Criando um Novo Projeto </h3>
Para criar um novo projeto Django usando Django Zorgen Templator, use o comando zorgen-admin startproject seguido pelo nome do projeto:

```bash
zorgen-admin startproject nome_do_projeto
```

<h3> Criando um Novo APP </h3>
Para criar um novo projeto Django usando Django Zorgen Templator, use o comando zorgen-admin startproject seguido pelo nome do projeto:

```bash
zorgen-admin startapp nome_do_projeto
```

<h3> Organizando Composes do Docker, DockerFile e Arquivos Python </h3>

Por padrão, nossa estruturação vem com inúmeros locais onde há o nome: '< projeto >'

Para isso temos o comando que você altera todas as referências de < projeto > para o nome do seu projeto real.

Use o comando zorgen-admin compose seguido pelo nome do seu projeto:

```bash
zorgen-admin compose nome_do_projeto
```


##
<h3> Estrutura do Projeto </h3>

```base
seuProjeto/
├── manage.py
├── seuProjeto/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
└── seuApp/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── tests/
        ├── unit/
            ├── tests.py
        ├── integration/
            ├── tests.py
    └── views.py
```