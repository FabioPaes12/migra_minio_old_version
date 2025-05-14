import os
import boto3
from botocore.exceptions import BotoCoreError, ClientError
# pip3 install boto3


def enviar_arquivos_minio(diretorio_base, bucket_name, endpoint_url, access_key, secret_key):
    '''COM BASE EM UMA PASTA, VERIFICA E ENVIA TODOS OS ARQUIVOS AO MINIO
        diretorio_base: RECEBE O CAMINHO ABSOLUTO DA PASTA
        bucket_name: RECEBE O NOME DA PASTA BASE QUE SERÁ CRIADA NO MINIO, SE NAO EXISTIR
        endpoint_url: URL DO MINIO:PORTA
        access_key e secret_key: SÃO AS CREDENCIAIS DE ACESSO AO MINIO.
    '''
    # Criando cliente S3 para MinIO
    s3 = boto3.client(
        's3',
        endpoint_url=endpoint_url,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key
    )

    # Verifica se o bucket existe, e cria se não existir
    try:
        s3.head_bucket(Bucket=bucket_name)
        print(f'[✔]  ----> Bucket "{bucket_name}" já existe.')
    except ClientError as e:
        error_code = int(e.response['Error']['Code'])
        if error_code == 404:
            try:
                s3.create_bucket(Bucket=bucket_name)
                print(f'------->Bucket "{bucket_name}" criado com sucesso.')
            except ClientError as ce:
                print(f'[✔] Erro ao criar bucket "{bucket_name}": {ce}')
                return
        else:
            print(f'[✔] Erro ao acessar bucket "{bucket_name}": {e}')
            return

    pasta = 0
    arq = 0
    falha = []
    for raiz, _, arquivos in os.walk(diretorio_base):
        pasta += 1
        total_files = len(arquivos)
        print(f"[✔]               ----> Encontrado: {total_files} na pasta!!!")
        for i, arquivo in enumerate(arquivos, start=1):
            arq += 1
            caminho_absoluto = os.path.join(raiz, arquivo)
            caminho_relativo = os.path.relpath(
                caminho_absoluto, diretorio_base)
            chave_s3 = caminho_relativo.replace(os.sep, '/')
            lg = f"{chave_s3[:15]}...{chave_s3[-10:]} F: {i}/{total_files}"
            # Verifica se o arquivo Existe
            try:
                s3.head_object(Bucket=bucket_name, Key=chave_s3)
                print(
                    f"[✔]               ----> Arquivo existe: {lg}")
            except ClientError as e:
                if e.response['Error']['Code'] == '404':
                    print(
                        f'[✘]                -------> Arquivo NÃO encontrado no Minio: {lg}')
                    print(f"------> Enviando: {lg}")
                    try:
                        s3.upload_file(caminho_absoluto, bucket_name, chave_s3)
                        print(f"[✔]                  Sucesso: {lg}")
                    except (BotoCoreError, ClientError) as e:
                        falha.append(chave_s3)
                        print(f'[!]   ==============> Erro ao enviar {lg}: {e}')
                else:
                    print(f'[!]         Erro ao verificar {chave_s3}: {e}')
    print(f'=========>Processo Terminado.... {pasta}/{arq} pastas/arquivos')

    if falha:
        print(f'[!] -------->Arquivos com Falha: {len(falha)}', falha)


# === Exemplo de uso ===
bucket = 'log'
folder_base = f'/home/usuario/minio_data/{bucket}'

endpoint = 'http://10.10.0.10:9000'  # Endpoint do MinIO
access_key = 'root_minio'            # MINIO_ROOT_USER
secret_key = 'SuperSenhaRootM'       # MINIO_ROOT_PASSWORD

enviar_arquivos_minio(folder_base, bucket, endpoint,
                      access_key, secret_key)
