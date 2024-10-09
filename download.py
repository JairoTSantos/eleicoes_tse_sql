import os
import requests
import zipfile
import argparse

def baixar_e_descompactar(ano, tipo):
    # Define a URL com base no tipo escolhido
    if tipo == "candidato":
        url = f"https://cdn.tse.jus.br/estatistica/sead/odsele/votacao_candidato_munzona/votacao_candidato_munzona_{ano}.zip"
        pasta_destino = f"data/{ano}/candidato"
    elif tipo == "detalhe":
        url = f"https://cdn.tse.jus.br/estatistica/sead/odsele/detalhe_votacao_secao/detalhe_votacao_secao_{ano}.zip"
        pasta_destino = f"data/{ano}/detalhe"
    else:
        raise ValueError("Tipo inválido. Use 'candidato' ou 'detalhe'.")

    # Caminho do arquivo ZIP a ser salvo
    caminho_zip = os.path.join(pasta_destino, f"{tipo}_votacao_{ano}.zip")

    # Cria a pasta se não existir
    os.makedirs(pasta_destino, exist_ok=True)

    # Faz o download do arquivo ZIP
    print(f"Fazendo download de {tipo} para o ano {ano}...")
    response = requests.get(url, stream=True)

    # Obtém o tamanho total do arquivo
    total_size = int(response.headers.get('content-length', 0))
    downloaded_size = 0

    with open(caminho_zip, "wb") as zip_file:
        for data in response.iter_content(chunk_size=1024):
            downloaded_size += len(data)
            zip_file.write(data)
            # Converte para MB e exibe o progresso
            mb_downloaded = downloaded_size / (1024 * 1024)
            mb_total = total_size / (1024 * 1024)
            print(f"Baixando {mb_downloaded:.2f} MB de {mb_total:.2f} MB", end='\r')

    print("\nDownload concluído.")

    # Descompacta o arquivo ZIP
    with zipfile.ZipFile(caminho_zip, 'r') as zip_ref:
        total_files = len(zip_ref.namelist())
        for i, arquivo in enumerate(zip_ref.namelist(), start=1):
            zip_ref.extract(arquivo, pasta_destino)
            print(f"Arquivo {i} de {total_files} descompactado com sucesso: {arquivo}")

    # Apaga o arquivo ZIP
    os.remove(caminho_zip)
    print("Arquivo ZIP apagado.")

def main():
    # Configura o parser de argumentos
    parser = argparse.ArgumentParser(description='Baixar e descompactar dados de votação por ano.')
    parser.add_argument('-ano', type=int, required=True, help='Ano dos dados a serem baixados (ex: 2022)')
    parser.add_argument('-tipo', choices=['candidato', 'detalhe'], required=True, help='Tipo de dados a serem baixados: "candidato" ou "detalhe".')
    parser.add_argument('-ano_final', type=int, help='Ano final para download em intervalos de 2 anos (opcional).')

    # Obtém os argumentos fornecidos na linha de comando
    args = parser.parse_args()

    # Se ano_final não for fornecido, apenas baixa o ano específico
    if args.ano_final is None:
        baixar_e_descompactar(args.ano, args.tipo)
    else:
        # Verifica se os anos estão em um intervalo válido
        if args.ano_final < args.ano:
            print("Erro: O ano final deve ser maior ou igual ao ano inicial.")
            return

        for ano in range(args.ano, args.ano_final + 1, 2):  # Baixa de 2 em 2 anos
            baixar_e_descompactar(ano, args.tipo)

if __name__ == "__main__":
    main()
