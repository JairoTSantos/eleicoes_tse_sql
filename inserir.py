import os
import mysql.connector

# Configurações do banco de dados
config = {
    'user': 'jairo',
    'password': 'intell01',
    'host': 'localhost',  # ou o IP do seu servidor MySQL
    'database': 'api',
}

def executar_sql_arquivo(caminho_arquivo):
    """Executa um arquivo SQL no banco de dados."""
    try:
        with open(caminho_arquivo, 'r') as arquivo:
            sql = arquivo.read()

        # Conectando ao banco de dados
        conexao = mysql.connector.connect(**config)
        cursor = conexao.cursor()

        # Executando os comandos SQL
        for comando in sql.split(';'):  # Divide os comandos pelo ponto e vírgula
            if comando.strip():  # Ignora comandos vazios
                cursor.execute(comando)

        # Comita as mudanças
        conexao.commit()
        print(f"Arquivo '{caminho_arquivo}' inserido com sucesso.")

    except mysql.connector.Error as err:
        print(f"Erro ao executar o arquivo {caminho_arquivo}: {err}")
    except Exception as e:
        print(f"Ocorreu um erro ao executar o arquivo {caminho_arquivo}: {e}")
    finally:
        cursor.close()
        conexao.close()

def importar_sql_da_pasta(pasta):
    """Importa todos os arquivos SQL de uma pasta."""
    arquivos_sql = [f for f in os.listdir(pasta) if f.endswith('.sql')]
    total_arquivos = len(arquivos_sql)

    if total_arquivos == 0:
        print("Nenhum arquivo SQL encontrado na pasta.")
        return

    print(f"Encontrados {total_arquivos} arquivos SQL na pasta '{pasta}'.")

    for i, arquivo in enumerate(arquivos_sql, start=1):
        caminho_completo = os.path.join(pasta, arquivo)
        print(f"Iniciando a inserção do arquivo {i} de {total_arquivos}: '{caminho_completo}'")
        executar_sql_arquivo(caminho_completo)

if __name__ == "__main__":
    pasta_sql = 'sql'  # Substitua pelo caminho da sua pasta
    importar_sql_da_pasta(pasta_sql)
