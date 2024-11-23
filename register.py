from flask import Flask, request, jsonify
from flask_cors import CORS
import boto3
import uuid
import os
import json
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

# Configurações do S3
S3_BUCKET = 'api-iot-estacio'
S3_REGION = 'sa-east-1'  # Ex: us-east-1
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
  try:
    # Receber dados do formulário
    nome = request.form.get('nome')
    email = request.form.get('email')
    telefone = request.form.get('telefone')



    # Verificar se os campos obrigatórios foram enviados
    if not all([nome, email, telefone]):
      return jsonify({'error': 'Nome, email e telefone são obrigatórios'}), 400

    # Verificar se o arquivo foi enviado com a requisição
    if 'foto' not in request.files:
      return jsonify({'error': 'Nenhuma foto enviada'}), 400

    foto = request.files['foto']

    print(nome)
    print(email)
    print(telefone)
    print(foto)


    # Gerar UUID para o usuário
    user_id = str(uuid.uuid4())


    # Salvar o arquivo com um nome seguro e único usando o UUID
    filename = f"{user_id}_{secure_filename(foto.filename)}"
    foto_path = os.path.join('./tmp', filename)
    foto.save(foto_path)

    # Fazer upload da foto para o S3
    try:
      s3_client.upload_file(
          foto_path,
          S3_BUCKET,
          f"usuarios/{filename}"
      )
      print('Upload para S3 bem-sucedido')
    except Exception as e:
      print(f"Erro ao fazer upload para o S3: {str(e)}")
      return jsonify({'error': f"Erro ao fazer upload para o S3: {str(e)}"}), 500
    
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
    json_path = os.path.join('./tmp', json_filename)
    with open(json_path, 'w') as json_file:
      json.dump(new_user_data, json_file)
    
    # Fazer upload do arquivo JSON para o S3
    s3_client.upload_file(
      json_path,
      S3_BUCKET,
      f"usuarios/{json_filename}"
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
