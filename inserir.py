import os
import mysql.connector
import argparse

def conectar_banco(host, user, password, database, port):
    """Conecta ao banco de dados MySQL e retorna a conexão."""
    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=port  # Adicionando o parâmetro da porta
        )
        print("Conexão com o banco de dados estabelecida com sucesso.")
        return conn
    except mysql.connector.Error as err:
        print(f"Erro ao conectar ao banco de dados: {err}")
        return None

def executar_sql(conn, arquivo_sql):
    """Executa os comandos SQL contidos no arquivo fornecido."""
    try:
        with open(arquivo_sql, 'r', encoding='utf-8') as f:
            sql_commands = f.read()
        
        cursor = conn.cursor()
        for command in sql_commands.split(';'):
            command = command.strip()
            if command:  # Executa apenas comandos não vazios
                cursor.execute(command)

        conn.commit()  # Confirma as alterações
        print(f"Arquivo {arquivo_sql} processado com sucesso.")
    except Exception as e:
        print(f"Erro ao executar comandos de {arquivo_sql}: {e}")

def main():
    # Configurando o parser de argumentos
    parser = argparse.ArgumentParser(description='Inserir arquivos SQL no banco de dados MySQL.')
    parser.add_argument('-pasta', type=str, required=True, help='Caminho da pasta com arquivos SQL.')
    parser.add_argument('-host', type=str, required=True, help='Host do banco de dados MySQL.')
    parser.add_argument('-user', type=str, required=True, help='Usuário do banco de dados MySQL.')
    parser.add_argument('-password', type=str, required=True, help='Senha do banco de dados MySQL.')
    parser.add_argument('-database', type=str, required=True, help='Nome do banco de dados.')
    parser.add_argument('-port', type=int, default=8889, help='Porta do banco de dados.')  # Definindo a porta padrão

    args = parser.parse_args()

    # Conecta ao banco de dados
    conn = conectar_banco(args.host, args.user, args.password, args.database, args.port)
    if conn is None:
        return

    # Processa todos os arquivos SQL na pasta especificada
    for arquivo in os.listdir(args.pasta):
        if arquivo.endswith('.sql'):
            caminho_arquivo = os.path.join(args.pasta, arquivo)
            executar_sql(conn, caminho_arquivo)

    # Fecha a conexão com o banco de dados
    conn.close()
    print("Conexão com o banco de dados fechada.")

if __name__ == '__main__':
    main()
