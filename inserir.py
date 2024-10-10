import os
import mysql.connector

# Configurações do banco de dados
config = {
    'user': 'jairo',
    'password': 'intell01',
    'host': 'localhost',
    'database': 'api',
}

def verificar_e_remover_tabela(cursor, nome_tabela):
    """Verifica se a tabela existe e a remove, se existir."""
    cursor.execute(f"SHOW TABLES LIKE '{nome_tabela}';")
    resultado = cursor.fetchone()
    
    if resultado:
        print(f"Tabela '{nome_tabela}' encontrada. Removendo...")
        cursor.execute(f"DROP TABLE {nome_tabela};")
        print(f"Tabela '{nome_tabela}' removida com sucesso.")

def executar_sql_arquivo(caminho_arquivo):
    """Executa um arquivo SQL no banco de dados."""
    try:
        with open(caminho_arquivo, 'r') as arquivo:
            sql = arquivo.read()

        # Conectando ao banco de dados
        conexao = mysql.connector.connect(**config)
        cursor = conexao.cursor()

        # Dividindo o SQL em comandos
        comandos = sql.split(';')

        for comando in comandos:
            comando = comando.strip()
            if comando:  # Ignora comandos vazios
                # Verifica se o comando é um CREATE TABLE e obtém o nome da tabela
                if comando.startswith("CREATE TABLE"):
                    # Extrai o nome da tabela da consulta
                    nome_tabela = comando.split()[2]  # Ajuste se necessário

                    # Verifica e remove a tabela se existir
                    verificar_e_remover_tabela(cursor, nome_tabela)

                # Executa o comando
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

    # Pergunta de confirmação
    resposta = input("Essa operação pode levar vários minutos. Você deseja continuar? (s/n): ").strip().lower()
    if resposta != 's':
        print("Operação cancelada.")
        return

    for i, arquivo in enumerate(arquivos_sql, start=1):
        caminho_completo = os.path.join(pasta, arquivo)
        print(f"Iniciando a inserção do arquivo {i} de {total_arquivos}: '{caminho_completo}'")
        executar_sql_arquivo(caminho_completo)

if __name__ == "__main__":
    pasta_sql = 'sql'  # Substitua pelo caminho da sua pasta
    importar_sql_da_pasta(pasta_sql)