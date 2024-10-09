
# Sistema de Download e Conversão de Dados de Votação

Este repositório contém três scripts em Python que permitem baixar e processar dados de votação do Tribunal Superior Eleitoral (TSE) do Brasil. O primeiro script (`download.py`) faz o download dos dados de votação para candidatos ou detalhes de seções eleitorais, o segundo script (`conversor.py`) converte os arquivos CSV baixados em comandos SQL para criação e inserção em um banco de dados, e o terceiro script (`inserir.py`) insere os comandos SQL gerados no banco de dados MySQL.

## Estrutura do Repositório

```
.
├── /data
├── /sql
├── download.py
├── conversor.py
├── inserir_sql.py
└── README.md
```

## Requisitos

- Python 3.x
- Bibliotecas:
  - `requests`
  - `pandas`
  - `mysql-connector-python`

Você pode instalar as bibliotecas necessárias usando pip:

```bash
pip install requests pandas mysql-connector-python
```

## Uso

### 1. `download.py`

O script `download.py` é usado para baixar os dados de votação. Ele aceita os seguintes argumentos:

- `-ano`: O ano dos dados a serem baixados (ex: 2022).
- `-tipo`: O tipo de dados a serem baixados (`candidato` ou `detalhe`).
- `-ano_final`: (opcional) O ano final para download em intervalos de 2 anos.

#### Exemplos

- Para baixar dados de candidatos para o ano de 2022:

```bash
python download.py -ano 2022 -tipo candidato
```

- Para baixar dados de detalhes para o ano de 2020 a 2024 (de 2 em 2 anos):

```bash
python download.py -ano 2020 -ano_final 2024 -tipo detalhe
```

### 2. `conversor.py`

O script `conversor.py` é usado para processar os arquivos CSV baixados e gerar um arquivo SQL correspondente. Ele aceita os seguintes argumentos:

- `-ano`: O ano para o arquivo CSV.
- `-estado`: O estado para o arquivo CSV.
- `-tipo`: O tipo de dados a serem processados (`candidato` ou `detalhe`).

#### Exemplos

- Para processar dados de votação de candidatos para o estado de São Paulo em 2022:

```bash
python conversor.py -ano 2022 -estado SP -tipo candidato
```

- Para processar dados de detalhes de votação para o estado do Rio de Janeiro em 2020:

```bash
python conversor.py -ano 2020 -estado RJ -tipo detalhe
```

### 3. `inserir.py`

O script `inserir.py` é usado para inserir os comandos SQL gerados no banco de dados MySQL. Ele aceita os seguintes argumentos:

- `-pasta`: O caminho da pasta com arquivos SQL.
- `-host`: O host do banco de dados MySQL.
- `-user`: O usuário do banco de dados MySQL.
- `-password`: A senha do banco de dados MySQL.
- `-database`: O nome do banco de dados.
- `-port`: A porta do banco de dados (padrão: `8889`).

#### Exemplos

- Para inserir os comandos SQL de arquivos na pasta `sql` no banco de dados:

```bash
python inserir_sql.py -pasta sql -host localhost -user seu_usuario -password sua_senha -database seu_banco -port 8889
```

## Contribuição

Sinta-se à vontade para contribuir com melhorias, correções ou novas funcionalidades. Para isso, basta fazer um fork deste repositório, realizar suas alterações e enviar um pull request.

## Licença

Este projeto não possui uma licença específica. Sinta-se à vontade para usar o código como desejar.
