# Sistema de Download e Conversão de Dados de Votação

Este repositório contém três scripts em Python que permitem baixar e processar dados de votação do Tribunal Superior Eleitoral (TSE) do Brasil. O primeiro script (`download.py`) faz o download dos dados de votação para candidatos ou detalhes de seções eleitorais, o segundo script (`conversor.py`) converte os arquivos CSV baixados em comandos SQL para criação e inserção em um banco de dados, e o terceiro script (`inserir.py`) insere os comandos SQL gerados no banco de dados MySQL.

## Estrutura do Repositório

```
.
├── /data
├── /sql
├── download.py
├── conversor.py
├── inserir.py
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
- `-ano_final`: O ano final para download em intervalos de 2 anos.
- `-tipo`: (opcional) O tipo de dados a serem baixados (candidato, secao ou zona).

#### Exemplos

- Para baixar dados os anos de 2022 ate 2024:

```bash
python download.py -ano 2022 -ano_final 2024
```

### 2. `conversor.py`

O script `conversor.py` é usado para processar os arquivos CSV baixados e gerar um arquivo SQL correspondente. Ele aceita os seguintes argumentos:

- `-estado`: O estado para o arquivo CSV (ex: SP).
- `-ano`: O ano para o arquivo CSV.


#### Exemplos

- Para processar dados de votação de candidatos para o estado de São Paulo em 2022:

```bash
python conversor.py -estado SP
```

- Para processar dados de detalhes de votação para o estado do Rio de Janeiro em 2020:

```bash
python conversor.py 2020 -estado RJ
```

### 3. `inserir.py`

O script `inserir.py` é usado para inserir no banco os arquivos SQL gerados:

- `-apagar`: Apagar os arquivos sql após a inserção (s ou n)

#### Exemplos

- Para inserir os arquivos gerados rode:

```bash
python inserir.py
```

## Contribuição

Sinta-se à vontade para contribuir com melhorias, correções ou novas funcionalidades. Para isso, basta fazer um fork deste repositório, realizar suas alterações e enviar um pull request.

## Licença

Este projeto não possui uma licença específica. Sinta-se à vontade para usar o código como desejar.