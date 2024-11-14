from flask import Flask, request, jsonify
import boto3
import uuid
import os
import json
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configurações do S3
S3_BUCKET = 'api-iot-estacio'
S3_REGION = 'sa-east'  # Ex: us-east-1
S3_ACCESS_KEY = 'AKIAW3MEDVA6ASTQFPLM'
S3_SECRET_KEY = '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'

# Inicializar o cliente S3
s3_client = boto3.client(
    's3',
    aws_access_key_id=S3_ACCESS_KEY,
    aws_secret_access_key=S3_SECRET_KEY,
    region_name=S3_REGION
)

@app.route('/register', methods=['POST'])
def create_user():
  # Receber dados do JSON
  data = request.get_json()
  nome = data.get('nome')
  email = data.get('email')
  telefone = data.get('telefone')
  
  # Gerar UUID para o usuário
  user_id = str(uuid.uuid4())
  
  # Verificar se o arquivo foi enviado com a requisição
  if 'foto' not in request.files:
    return jsonify({'error': 'Nenhuma foto enviada'}), 400
  
  foto = request.files['foto']
  
  # Salvar o arquivo com um nome seguro e único usando o UUID
  filename = f"{user_id}_{secure_filename(foto.filename)}"
  foto_path = os.path.join('/tmp', filename)
  foto.save(foto_path)

  # Fazer upload da foto para o S3
  try:
    s3_client.upload_file(
      foto_path,
      S3_BUCKET,
      f"usuarios/{filename}",
      ExtraArgs={'ACL': 'public-read'}  # Permite acesso público ao arquivo
    )
    
    # Gerar a URL pública da foto
    foto_url = f"https://{S3_BUCKET}.s3.{S3_REGION}.amazonaws.com/usuarios/{filename}"
    
    # Dados do novo usuário
    new_user_data = {
      'id': user_id,
      'nome': nome,
      'email': email,
      'telefone': telefone,
      'foto_url': foto_url
    }
    # Converter dados do usuário para JSON
    json_filename = f"{user_id}_dados.json"
    json_path = os.path.join('/tmp', json_filename)
    with open(json_path, 'w') as json_file:
      json.dump(new_user_data, json_file)
    
    # Fazer upload do arquivo JSON para o S3
    s3_client.upload_file(
      json_path,
      S3_BUCKET,
      f"usuarios/{json_filename}",
      ExtraArgs={'ACL': 'public-read'}  # Permite acesso público ao arquivo
    )
    
    # URL pública do arquivo JSON
    json_url = f"https://{S3_BUCKET}.s3.{S3_REGION}.amazonaws.com/usuarios/{json_filename}"
    
    # Retornar a resposta com a URL do JSON e da foto
    response_data = {
      'user_data': new_user_data,
      'json_url': json_url
    }
    
    # Remover arquivos temporários
    os.remove(foto_path)
    os.remove(json_path)
    
    return jsonify(response_data), 201
  
  except Exception as e:
    return jsonify({'error': str(e)}), 500

app.run(port=5000, host='localhost', debug=True)
