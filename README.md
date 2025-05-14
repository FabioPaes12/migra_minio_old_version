# Migração de Arquivos de Versões Antigas do MinIO
Responsável por migrar todos os arquivos do Minio S3 da versão antiga (até **RELEASE.2021-11-05T09-16-26Z**), para a versão atual.

A Finalidade desse Código é com base em uma Pasta do computador, realizar o envio de todos os arquivos de forma recursiva, mantendo a mesma extrutura.

Após a versão **RELEASE.2021-11-05T09-16-26Z**, o Minio mudou a forma de armazenamento dos arquivos, de forma a nao manter o formato tradicional de visualização dos sistemas operacionais. Sendo assim não existe a compatibilidade entre versões menores ou iguais a **RELEASE.2021-11-05T09-16-26Z**, e as versões posteriores. Sendo necessário a migração dos dados.
Para quem busca um método seguro e Prático de migração dos dados, segue o Código em Python3 para realizar essa tarefa.

# Requisitos:
1.  - *Python3*; e
2.  - *Boto3*

# Como Rodar o projeto:
1. - Crie um projeto python de sua preferência;
2. - Copie o arquivo main.py;
3. - Instale o pré requisito em seu projeto através do comando pip3 install boto3
4. - Altere as Variáveis de acordo com o seu ambiente de trabalho, sendo:
     
        4.1. diretorio_base: RECEBE O CAMINHO ABSOLUTO DA PASTA
     
        4.2. bucket_name: RECEBE O NOME DA PASTA BASE QUE SERÁ CRIADA NO MINIO, SE NAO EXISTIR
     
        4.3. endpoint_url: URL DO MINIO:PORTA
     
        4.4. access_key e secret_key: SÃO AS CREDENCIAIS DE ACESSO AO MINIO.


# Conclusão
A Função irá mapear todos os arquivos e diretórios posteriores a diretorio_base/bucket_name, e realizará a verificação, em busca de saber se o arquivo já se encontra na sua nova instalação minio. Caso o arquivo não esteja lá, será realizado o envio dele mantendo a mesma hierarquia.
Em caso de falha em algum arquivo, basta rodar novamente a função, python3 main.py, que ela se encarrega de enviar apenas os arquivos que ainda não foram enviadoa ao servidor.

# python3 main.py
