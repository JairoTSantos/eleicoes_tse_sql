import pandas as pd
import argparse
import os
import math

# Função para gerar a criação da tabela SQL
def gerar_comando_criacao_tabela(nome_tabela, tipos_dados):
    comando_criacao = f"CREATE TABLE {nome_tabela} (\n"
    for coluna, tipo in tipos_dados.items():
        if tipo == 'object':
            tipo_sql = 'VARCHAR(255)'  # Tipo SQL para strings
        elif tipo == 'int64':
            tipo_sql = 'BIGINT'
        elif tipo == 'float64':
            tipo_sql = 'FLOAT'
        else:
            tipo_sql = 'TEXT'  # Tipo padrão
        comando_criacao += f"    {coluna} {tipo_sql},\n"
    comando_criacao = comando_criacao.rstrip(',\n') + "\n);\n"
    return comando_criacao

# Função para gerar o comando de inserção
def gerar_comandos_insercao(nome_tabela, chunk):
    comandos_insercao = []
    for index, row in chunk.iterrows():
        valores = []
        for v in row:
            if isinstance(v, str) and v == "":  # Verifica se o valor é uma string vazia
                valores.append('NULL')  # Substitui por NULL
            else:
                valores.append(f"'{str(v).replace('\'', '\'\'')}'" if pd.notnull(v) else 'NULL')
        comandos_insercao.append(f"INSERT INTO {nome_tabela} VALUES ({', '.join(valores)});\n")
    return comandos_insercao

# Função para processar grandes arquivos CSV em chunks
def processar_csv_grande(arquivo_csv, nome_tabela, sep=';', enc='latin1', dec=',', chunksize=10000):
    # Criar diretório sql se não existir
    os.makedirs('sql', exist_ok=True)

    print("Aguarde, gerando arquivo SQL, essa operação pode demorar....")

    # Calcular o número total de chunks
    total_linhas = sum(1 for _ in open(arquivo_csv, encoding=enc)) - 1  # menos 1 para o cabeçalho
    total_chunks = math.ceil(total_linhas / chunksize)

    # Iterar sobre o CSV em chunks
    for i, chunk in enumerate(pd.read_csv(arquivo_csv, sep=sep, encoding=enc, decimal=dec, chunksize=chunksize)):
        # Na primeira iteração, gerar o comando de criação da tabela
        if i == 0:
            tipos_dados = chunk.dtypes
            comando_criacao = gerar_comando_criacao_tabela(nome_tabela, tipos_dados)
            with open(f'sql/{nome_tabela}.sql', 'w', encoding='utf-8') as f:
                f.write(comando_criacao)

        # Gerar os comandos de inserção para o chunk atual
        comandos_insercao = gerar_comandos_insercao(nome_tabela, chunk)
        
        # Escrever os comandos de inserção no arquivo SQL
        with open(f'sql/{nome_tabela}.sql', 'a', encoding='utf-8') as f:
            f.writelines(comandos_insercao)
        
        # Informar o progresso
        print(f"Processando chunk {i + 1} de {total_chunks}...")

    print("Arquivo SQL gerado com sucesso!")

def main():
    # Configurando o parser de argumentos
    parser = argparse.ArgumentParser(description='Processar arquivos CSV e gerar arquivos SQL.')
    parser.add_argument('-ano', type=int, required=True, help='Ano inicial para o arquivo CSV')
    parser.add_argument('-estado', type=str, required=True, help='Estado para o arquivo CSV')
    parser.add_argument('-tipo', choices=['candidato', 'detalhe'], required=True, help='Tipo de dados a serem processados: "candidato" ou "detalhe".')
    parser.add_argument('-ano_final', type=int, help='Ano final para processamento em intervalos de 2 anos (opcional).')

    args = parser.parse_args()

    # Parâmetros
    estado = args.estado
    ano_inicial = args.ano
    ano_final = args.ano_final
    tipo = args.tipo

    # Verifica se ano_final foi fornecido
    if ano_final is None:
        # Apenas processa o ano específico
        anos_para_processar = [ano_inicial]
    else:
        # Verifica se o ano_final é maior que o ano_inicial
        if ano_final < ano_inicial:
            print("Erro: O ano final deve ser maior ou igual ao ano inicial.")
            return
        anos_para_processar = list(range(ano_inicial, ano_final + 1, 2))  # Pula de 2 em 2 anos

    for ano in anos_para_processar:
        # Define o caminho do arquivo CSV com base no tipo
        if tipo == 'candidato':
            arquivo_csv = f'./data/{ano}/candidato/votacao_candidato_munzona_{ano}_{estado}.csv'
            nome_tabela = f'votacao_candidato_munzona_{ano}_{estado}'
        elif tipo == 'detalhe':
            arquivo_csv = f'./data/{ano}/detalhe/detalhe_votacao_secao_{ano}_{estado}.csv'
            nome_tabela = f'votacao_secao_{ano}_{estado}'

        # Verifica se o arquivo CSV existe
        if not os.path.isfile(arquivo_csv):
            print(f"Erro: O arquivo {arquivo_csv} não foi encontrado.")
            continue  # Continua para o próximo ano

        # Processar o CSV
        processar_csv_grande(arquivo_csv, nome_tabela)

if __name__ == '__main__':
    main()
