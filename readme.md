# Sistema de Download e Conversão de Dados de Votação

Este repositório contém dois scripts em Python que permitem baixar e processar dados de votação do Tribunal Superior Eleitoral (TSE) do Brasil. O primeiro script (`download.py`) faz o download dos dados de votação para candidatos ou detalhes de seções eleitorais, enquanto o segundo script (`conversor.py`) converte os arquivos CSV baixados em comandos SQL para criação e inserção em um banco de dados.

## Estrutura do Repositório

```
.
├── download.py
├── conversor.py
└── README.md
```

## Requisitos

- Python 3.x
- Bibliotecas:
  - `requests`
  - `pandas`

Você pode instalar as bibliotecas necessárias usando pip:

```bash
pip install requests pandas
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

## Contribuição

Sinta-se à vontade para contribuir com melhorias, correções ou novas funcionalidades. Para isso, basta fazer um fork deste repositório, realizar suas alterações e enviar um pull request.

## Licença

Este projeto não possui uma licença específica. Sinta-se à vontade para usar o código como desejar.
