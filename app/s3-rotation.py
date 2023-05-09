import boto3, os
from envyaml import EnvYAML
from datetime import datetime, timedelta

# Valores defaults
DEFAULT_FILE_AGE = 15

# Ajustando o local da configuracao do bucket.yaml
script_dir = os.path.dirname(__file__)
rel_path = "config/bucket.yaml"
abs_path = os.path.join(script_dir, rel_path)
env = EnvYAML(abs_path)

if "DEBUG" in os.environ :
    debug = bool(os.environ["FILE_AGE"])
else :
    debug= False
if debug :
    print(env['config'])    
if "FILE_AGE" in os.environ :
    file_age = int(os.environ["FILE_AGE"])
else :
    file_age = DEFAULT_FILE_AGE

# Obtém as credenciais e a região do S3 das variáveis de ambiente como descrito no bucket.yaml







if 'config.access_key' in env :
    aws_access_key_id = env['config.access_key']
else:    
    raise ValueError("AWS_ACCESS_KEY_ID is not defined")

if 'config.secret_key' in env :
    aws_secret_access_key = env['config.secret_key']
else:    
    raise ValueError("AWS_SECRET_ACCESS_KEY is not defined")

if 'config.region' in env :
    region_name = env['config.region']
else:    
    raise ValueError("AWS_REGION is not defined")

if 'config.endpoint' in env :
    endpoint_url= env['config.endpoint']
else:    
    raise ValueError("AWS_ENDPOINT_URL is not defined")

if 'config.bucket' in env :
    bucket_name= env['config.bucket']    
else:    
    raise ValueError("AWS_BUCKET_NAME is not defined")

if 'config.insecure' in env :
    insecure= env['config.insecure']    
else:    
    insecure= False
    
if 'config.signature_version2' in env :
    signature_version= env['config.signature_version2']
else:
    signature_version= False


# Cria uma sessão com as suas credenciais
# session = boto3.Session(
#     aws_access_key_id=aws_access_key_id,
#     aws_secret_access_key=aws_secret_access_key,
#     region_name=region_name
# )

# Crie um cliente S3
if signature_version :
    s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=region_name, endpoint_url=endpoint_url, verify=insecure, config=boto3.session.Config(signature_version="v2"))
else:
    s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=region_name, endpoint_url=endpoint_url, verify=insecure)
# s3 = boto3.client('s3', endpoint_url=endpoint_url, verify=insecure)    

# Obtém a data atual
now = datetime.now()

# Lista todos os objetos no bucket
objects = s3.list_objects(Bucket=bucket_name)

if debug :    
    print(objects)

if 'Contents' in objects:
# Percorre cada objeto e verifica se ele tem mais de 15 dias de idade
    for obj in objects['Contents']:
        # Obtém a data de criação do objeto
        create_date = obj['LastModified'].replace(tzinfo=None)
        
        # Calcula a diferença entre a data atual e a data de criação do objeto
        age = now - create_date
        
        # Se o objeto tiver mais de 15 dias de idade, apaga ele
        if age > timedelta(file_age):
            s3.delete_object(Bucket=bucket_name, Key=obj['Key'])
            print(f'O objeto {obj["Key"]} com mais de ',file_age,' dias de idade foi apagado com sucesso!')
        else: 
            print('Não tem objetos com mais de ',file_age,' dias no bucket:',bucket_name)
    # print('Todos os objetos com mais de ',file_age,' dias de idade foram apagados com sucesso!')
else :
    print('Não há objetos no bucket:',bucket_name)        
