import pandas as pd
import os
import argparse

def map_type(dtype):
    if pd.api.types.is_integer_dtype(dtype):
        return 'BIGINT'
    elif pd.api.types.is_float_dtype(dtype):
        return 'FLOAT'
    elif pd.api.types.is_bool_dtype(dtype):
        return 'BOOLEAN'
    elif pd.api.types.is_datetime64_any_dtype(dtype):
        return 'DATETIME'
    else:
        return 'VARCHAR(255)'

def gerar_script_sql(csv_file, sql_file, chunksize=1000):
    # Verifica se o arquivo SQL já existe e o remove se existir
    if os.path.exists(sql_file):
        os.remove(sql_file)

    # Início da criação do script SQL
    print(f"Iniciando criação do script SQL para {csv_file}...")

    # Lê o arquivo CSV com codificação latin-1 em chunks
    try:
        chunks = pd.read_csv(csv_file, encoding='latin-1', delimiter=';', chunksize=chunksize)
    except FileNotFoundError:
        print(f"Erro: O arquivo '{csv_file}' não foi encontrado.")
        return  # Sai da função se o arquivo não for encontrado
    except Exception as e:
        print(f"Erro ao ler o arquivo '{csv_file}': {e}")
        return  # Sai da função se ocorrer outro erro

    # Obtém o nome do arquivo sem a extensão
    base_name = os.path.basename(csv_file)  # Nome do arquivo com extensão
    table_name = os.path.splitext(base_name)[0]  # Remove a extensão
    table_name = table_name.replace(' ', '_')  # Substitui espaços por underscores

    # Obtém os tipos de dados e gera a query de criação da tabela
    columns_with_types = []

    # Lê o primeiro chunk para definir a estrutura da tabela
    first_chunk = next(chunks)
    for column in first_chunk.columns:
        sql_type = map_type(first_chunk[column].dtype)
        columns_with_types.append(f"`{column}` {sql_type}")  # Usar crase para nomes de coluna com caracteres especiais

    create_table_query = f"CREATE TABLE `{table_name}` (\n    " + ",\n    ".join(columns_with_types) + "\n);\n\n"

    # Prepara para armazenar as instruções INSERT
    insert_queries = []

    # Adiciona os inserts do primeiro chunk    
    for index, row in first_chunk.iterrows():
        values = []
        for column in first_chunk.columns:
            value = row[column]
            if pd.isnull(value):
                values.append("NULL")
            elif isinstance(value, str):
                value = value.replace("'", "''")
                values.append(f"'{value}'")
            else:
                values.append(str(value))

        insert_query = f"INSERT INTO `{table_name}` (" + ", ".join(f"`{col}`" for col in first_chunk.columns) + ") VALUES (" + ", ".join(values) + ");"
        insert_queries.append(insert_query)

    # Processa os demais chunks
    total_chunks = sum(1 for _ in pd.read_csv(csv_file, encoding='latin-1', delimiter=';', chunksize=chunksize))  # Conta total de chunks
    print(f"Total de chunks: {total_chunks}")
    print("Processando chunk 1...")

    for i, chunk in enumerate(chunks, start=2):
        print(f"Processando parte {i} de {total_chunks}...")
        for index, row in chunk.iterrows():
            values = []
            for column in chunk.columns:
                value = row[column]
                if pd.isnull(value):
                    values.append("NULL")
                elif isinstance(value, str):
                    value = value.replace("'", "''")
                    values.append(f"'{value}'")
                else:
                    values.append(str(value))

            insert_query = f"INSERT INTO `{table_name}` (" + ", ".join(f"`{col}`" for col in chunk.columns) + ") VALUES (" + ", ".join(values) + ");"
            insert_queries.append(insert_query)

    # Junta tudo em um único script SQL
    full_script = create_table_query + "\n".join(insert_queries) + "\n"

    # Certifica-se de que o diretório de destino existe
    os.makedirs(os.path.dirname(sql_file), exist_ok=True)

    with open(sql_file, 'w') as f:
        f.write(full_script)

    print(f"Script SQL criado com sucesso em {sql_file}!")

def main():
    caminho_da_pasta = 'data'
    
    pastas = [nome for nome in os.listdir(caminho_da_pasta) if os.path.isdir(os.path.join(caminho_da_pasta, nome))]

    # Configura o parser de argumentos
    parser = argparse.ArgumentParser(description='Gerar scripts SQL a partir de arquivos CSV.')
    parser.add_argument('-estado', type=str, required=True, help='Estado dos dados a serem processados (ex: SP)')
    args = parser.parse_args()
    
    for ano in pastas:           
        # Chama a função para gerar o script SQL
        gerar_script_sql(
            os.path.join('data', ano, 'candidato', f'votacao_candidato_munzona_{ano}_{args.estado}.csv'),
            os.path.join('sql', ano, 'candidato', f'votacao_candidato_munzona_{ano}_{args.estado}.sql')
        )
        gerar_script_sql(
            os.path.join('data', ano, 'secao', f'detalhe_votacao_secao_{ano}_{args.estado}.csv'),
            os.path.join('sql', ano, 'secao', f'detalhe_votacao_secao_{ano}_{args.estado}.sql')
        )
        gerar_script_sql(
            os.path.join('data', ano, 'zona', f'detalhe_votacao_munzona_{ano}_{args.estado}.csv'),
            os.path.join('sql', ano, 'zona', f'detalhe_votacao_munzona_{ano}_{args.estado}.sql')
        )

if __name__ == "__main__":
    main()