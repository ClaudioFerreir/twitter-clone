# Twitter Clone

Um projeto simples de clone do Twitter utilizando Django.

## Pré-requisitos

Antes de começar, você precisará ter instalado o seguinte:

- [Python](https://www.python.org/downloads/) (versão 3.10 ou superior)
- [Poetry](https://python-poetry.org/docs/#installation) (para gerenciar as dependências)

## Configuração do Ambiente

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/ClaudioFerreir/twitter-clone.git
   cd twitter-clone/twitter_clone
   ```

2. **Crie um ambiente virtual:**

   Você pode criar um ambiente virtual com o `venv` ou usar o Poetry:

   ```bash
   # Usando venv
   python3 -m venv venv
   source venv/bin/activate  # No Linux ou Mac
   venv\Scripts\activate  # No Windows

   # Usando Poetry
   poetry install
   ```

3. **Instale as dependências:**

   Se você estiver usando o Poetry, use o comando:

   ```bash
   poetry install
   ```

   Se você exportou suas dependências para um `requirements.txt`, você pode usar:

   ```bash
   pip install -r requirements.txt
   ```

## Gerenciando o Projeto com Poetry

Este projeto utiliza o [Poetry](https://python-poetry.org/) para gerenciamento de dependências e ambiente virtual. Aqui estão as instruções para usar o Poetry:

### Comandos do Poetry

Aqui estão alguns comandos úteis do Poetry que você pode usar para gerenciar o projeto:

- **Instalar as dependências do projeto:**
  
   ```bash
   poetry install
   ```

- **Adicionar uma nova dependência:**
  
   ```bash
   poetry add <nome-do-pacote>
   ```

- **Remover uma dependência:**
  
   ```bash
   poetry remove <nome-do-pacote>
   ```

- **Atualizar as dependências:**
  
   ```bash
   poetry update
   ```

- **Executar um comando dentro do ambiente virtual do projeto:**
  
   ```bash
   poetry run <comando>
   ```

### Executando o Projeto

Para iniciar o projeto, você pode usar o seguinte comando:

```bash
poetry run python manage.py runserver
```

Agora você pode acessar o projeto em [http://127.0.0.1:8000](http://127.0.0.1:8000).

### Exportando Dependências

Se você precisar de um arquivo `requirements.txt`, você pode exportar as dependências do Poetry usando:

```bash
poetry export -f requirements.txt --output requirements.txt
```

### Desativando Avisos

Se você desejar desativar os avisos sobre o plugin de exportação do Poetry, você pode usar o seguinte comando:

```bash
poetry config warnings.export false
```

## Contribuindo

Sinta-se à vontade para contribuir! Abra um issue ou envie um pull request.

## Licença

Este projeto é opensource produzido por Claudio Ferreira como projeto final do curso Full Stack Python.
