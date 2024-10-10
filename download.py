import os
import requests
import zipfile
import argparse
import shutil



def baixar_arquivo_zip(ano, tipo):
    if tipo == "candidato":
        url = f"https://cdn.tse.jus.br/estatistica/sead/odsele/votacao_candidato_munzona/votacao_candidato_munzona_{ano}.zip"
    elif tipo == "secao":
        url = f"https://cdn.tse.jus.br/estatistica/sead/odsele/detalhe_votacao_secao/detalhe_votacao_secao_{ano}.zip"
    elif tipo == "zona":
        url = f"https://cdn.tse.jus.br/estatistica/sead/odsele/detalhe_votacao_munzona/detalhe_votacao_munzona_{ano}.zip"
    else:
        raise ValueError("Tipo inválido. Use 'candidato', 'zona' ou 'secao'.")

    print(f"Fazendo download dos arquivos zip para o ano {ano}")

    try:
        # Fazendo o download com stream
        response = requests.get(url, stream=True, timeout=10)

        # Verifica se a requisição foi bem-sucedida
        response.raise_for_status()

        # Obtendo o tamanho total do arquivo
        total_size = int(response.headers.get('content-length', 0))
        downloaded_size = 0

        # Definir a pasta de destino apenas após o download ser bem-sucedido
        pasta_destino = f"data/{ano}/{tipo}"
        caminho_zip = os.path.join(pasta_destino, f"{tipo}_votacao_{ano}.zip")

        # Apaga a pasta primeiro depois criar a pasta de destino após a resposta ser verificada
        if os.path.exists(pasta_destino):
            if os.path.isdir(pasta_destino):
                shutil.rmtree(pasta_destino)
        os.makedirs(pasta_destino, exist_ok=True)

        # Salvando o arquivo zip
        with open(caminho_zip, "wb") as zip_file:
            for data in response.iter_content(chunk_size=1024):
                downloaded_size += len(data)
                zip_file.write(data)
                # Converte para MB e exibe o progresso
                mb_downloaded = downloaded_size / (1024 * 1024)
                mb_total = total_size / (1024 * 1024)
                print(f"Baixando {mb_downloaded:.2f} MB de {mb_total:.2f} MB", end='\r')

        print("\nDownload concluído.")

        # Extraindo o arquivo ZIP
        with zipfile.ZipFile(caminho_zip, 'r') as zip_ref:
            total_files = len(zip_ref.namelist())
            for i, arquivo in enumerate(zip_ref.namelist(), start=1):
                zip_ref.extract(arquivo, pasta_destino)
                print(f"Arquivo {i} de {total_files} descompactado com sucesso: {arquivo}")

        # Apagando o arquivo ZIP
        os.remove(caminho_zip)
        print("Arquivo ZIP apagado.")

    except requests.exceptions.HTTPError as http_err:
        print(f"Erro HTTP: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Erro de Conexão: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Erro de Timeout: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Erro na requisição: {req_err}")
    except zipfile.BadZipFile as zip_err:
        print(f"Erro ao descompactar o arquivo ZIP: {zip_err}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")


def calcular_tamanho_pasta(pasta):
    tamanho_total = 0
    for dirpath, dirnames, filenames in os.walk(pasta):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            tamanho_total += os.path.getsize(fp)
    return tamanho_total


def main():
    # Configura o parser de argumentos
    parser = argparse.ArgumentParser(description='Baixar e descompactar dados de votação por ano.')
    parser.add_argument('-ano', type=int, required=True, help='Ano dos dados a serem baixados (ex: 2022)')
    parser.add_argument('-tipo', choices=['candidato', 'secao', 'zona'], help='Tipo de dados a serem baixados: "candidato", "zona" ou "secao".')
    parser.add_argument('-ano_final', type=int, help='Ano final para download em intervalos de 2 anos (opcional).')

    # Obtém os argumentos fornecidos na linha de comando
    args = parser.parse_args()

    tipos = ['candidato', 'secao', 'zona'] if args.tipo is None else [args.tipo]

    # Se ano_final não for fornecido, apenas baixa o ano específico
    if args.ano_final is None:
        for tipo in tipos:
            baixar_arquivo_zip(args.ano, tipo)
    else:
        # Verifica se os anos estão em um intervalo válido
        if args.ano_final < args.ano:
            print("Erro: O ano final deve ser maior ou igual ao ano inicial.")
            return

        for ano in range(args.ano, args.ano_final + 1, 2):  # Baixa de 2 em 2 anos
            for tipo in tipos:
                baixar_arquivo_zip(ano, tipo)

    # Calcula o tamanho total da pasta /data e exibe
    pasta_data = "data"
    tamanho_pasta = calcular_tamanho_pasta(pasta_data)
    tamanho_pasta_mb = tamanho_pasta / (1024 * 1024 * 1024)  # Converte para MB
    print(f"Tamanho total da pasta '{pasta_data}': {tamanho_pasta_mb:.2f} GB")


if __name__ == "__main__":
    main()