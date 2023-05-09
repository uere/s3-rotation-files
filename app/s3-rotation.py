import boto3, os
from envyaml import EnvYAML
from datetime import datetime, timedelta

# Ajustando o local da configuracao do bucket.yaml
script_dir = os.path.dirname(__file__)
rel_path = "config/bucket.yaml"
abs_path = os.path.join(script_dir, rel_path)
env = EnvYAML(abs_path)
print(env['config'])

# Obtém as credenciais e a região do S3 das variáveis de ambiente como descrito no bucket.yaml
aws_access_key_id = env['config.access_key']
aws_secret_access_key = env['config.secret_key']
region_name = env['config.region']
endpoint_url= env['config.endpoint']
bucket_name= env['config.bucket']
insecure= env['config.insecure']
signature_version= env['config.signature_version2']
insecure=env['config.insecure']

# Cria uma sessão com as suas credenciais
session = boto3.Session(
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=region_name
)

# Crie um cliente S3
if signature_version :
    s3 = boto3.client('s3', endpoint_url=endpoint_url, verify=insecure, config=boto3.session.Config(signature_version="v2"))
else:
    s3 = boto3.client('s3', endpoint_url=endpoint_url, verify=insecure)
# s3 = boto3.client('s3', endpoint_url=endpoint_url, verify=insecure)    

# Obtém a data atual
now = datetime.now()

# Lista todos os objetos no bucket
objects = s3.list_objects(Bucket=bucket_name)

# Percorre cada objeto e verifica se ele tem mais de 15 dias de idade
for obj in objects['Contents']:
    # Obtém a data de criação do objeto
    create_date = obj['LastModified'].replace(tzinfo=None)
    
    # Calcula a diferença entre a data atual e a data de criação do objeto
    age = now - create_date
    
    # Se o objeto tiver mais de 15 dias de idade, apaga ele
    if age < timedelta(days=15):
        # s3.delete_object(Bucket=bucket_name, Key=obj['Key'])
        print(f'O objeto {obj["Key"]} com mais de 15 dias de idade foi apagado com sucesso!')
        
print('Todos os objetos com mais de 15 dias de idade foram apagados com sucesso!')
