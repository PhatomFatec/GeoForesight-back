from bson import ObjectId
from geoalchemy2 import Geography
from dotenv import load_dotenv
from datetime import datetime
import requests
import bcrypt
import json
import os

from sqlalchemy import TEXT,DateTime, func
from sqlalchemy import create_engine, text
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import string

from email.message import EmailMessage
import smtplib

from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)

load_dotenv()

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'your-secret-key'

jwt = JWTManager(app)

CORS(app)

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Configurações do banco de dados PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('url_heroku')

db = SQLAlchemy(app)


#############################
##### Database Classes ######
#############################


# class operacao_credito_estadual(db.Model):
#     ref_bacen = db.Column(db.Integer, primary_key=True,
#                           unique=True, nullable=False,  autoincrement=False)
#     nu_ordem = db.Column(db.Integer, primary_key=True,
#                          unique=True, nullable=False,  autoincrement=False)
#     inicio_plantio = db.Column(db.Date, nullable=False)
#     final_plantio = db.Column(db.Date, nullable=False)
#     final_colheita = db.Column(db.Date, nullable=False)
#     inicio_colheita = db.Column(db.Date, nullable=False)
#     data_liberacao = db.Column(db.Date, nullable=False)
#     data_vencimento = db.Column(db.Date, nullable=False)
#     idciclo = db.Column(db.Integer, db.ForeignKey('ciclo_producao.idciclo'))
#     idteste = db.Column(
#         db.Integer, db.ForeignKey('empreendimento.idteste'))
#     idClima = db.Column(db.Integer, db.ForeignKey('clima.idClima'))
#     idEvento = db.Column(db.Integer, db.ForeignKey('evento_climatico.idEvento'))
#     idgrao = db.Column(db.Integer, db.ForeignKey('grao.idgrao'))
#     idSolo = db.Column(db.Integer, db.ForeignKey('solo.idSolo'))
#     idirrigacao = db.Column(db.Integer, db.ForeignKey('irrigacao.idirrigacao'))
#     idempreendimento = db.Column(
#         db.Integer, db.ForeignKey('empreendimento.idempreendimento'))
#     glebas = db.relationship('glebas', backref='operacao_credito_estadual')

#     table_args = (
#         db.PrimaryKeyConstraint('ref_bacen', 'nu_ordem'),
#     )


# class glebas(db.Model):
#     idgleba = db.Column(db.Integer, primary_key=True,
#                         nullable=False,  autoincrement=False)
#     coordenadas = db.Column(
#         Geography(geometry_type='POINT', srid=4326), nullable=False)
#     altitude = db.Column(db.Double)
#     nu_ponto = db.Column(db.Integer, nullable=False)
#     ref_bacen = db.Column(db.Integer, db.ForeignKey(
#         'operacao_credito_estadual.ref_bacen'))
#     nu_ordem = db.Column(db.Integer, db.ForeignKey(
#         'operacao_credito_estadual.nu_ordem'))


# class empreendimento(db.Model):
#     idteste = db.Column(db.Integer, primary_key=True, nullable=False)
#     idempreendimento = db.Column(db.BigInteger, nullable=False)
#     finalidade = db.Column(db.String(255))
#     cesta = db.Column(db.String(255), nullable=False)
#     modalidade = db.Column(db.String(255), nullable=False)
#     idproduto = db.Column(db.Integer, db.ForeignKey(
#         'produtos.idproduto'), nullable=False)
    
# class cooperados(db.Model):
#      ref_bacen = db.Column(db.Integer, primary_key=True,unique=True, nullable=False,  autoincrement=False)
#      nu_ordem = db.Column(db.Integer, primary_key=True,unique=True, nullable=False,  autoincrement=False)
#      valor_parcela = db.Column(db.Double)
#      cpf = db.Column(db.String(255))
class aceitacao_usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id')) 
    id_termo = db.Column(db.Integer, db.ForeignKey('termos.id')) 
    aceite = db.Column(db.Boolean, nullable=False)
    data_aceitacao = db.Column(db.DateTime,default=datetime.utcnow, nullable=False)

class user(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    telefone = db.Column(db.String(14))

    rel_ace_user  = db.relationship('aceitacao_usuario', backref='user', lazy=True)

class tipo_termos(db.Model):
    id_tipo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tipo_desc = db.Column(db.String(255), nullable=False) 
    termos_rel = db.relationship('termos', backref='tipo_termos', lazy=True)
    
class termos(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    data = db.Column(DateTime, default=datetime.utcnow, nullable=False)  
    termo = db.Column(TEXT, unique=True, nullable=False)
    
    id_tipo = db.Column(db.Integer, db.ForeignKey('tipo_termos.id_tipo'))
    rel_ace_user = db.relationship('aceitacao_usuario', backref='termos', lazy=True)


with app.app_context():
    db.create_all()



#############################
######## cadastro  ##########
#############################

@app.route('/cadastro', methods=['POST'])
def cadastro():
    data = request.get_json()

    nome = data.get('nome')
    email = data.get('email')
    senha = data.get('senha')
    telefone = data.get('telefone')
    aceites = data.get('aceites', [])   
    data_aceitacao = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Gerar um salt aleatório
    salt = bcrypt.gensalt()

    # Criptografar a senha com o salt
    hashed_password = bcrypt.hashpw(senha.encode('utf-8'), salt)
    hashed_password = hashed_password.decode('utf-8')

    # Imprimir o valor de hash
    print(hashed_password)

    novo_dado = user(nome=nome, email=email, telefone=telefone, senha=hashed_password)

    try:
        db.session.add(novo_dado)
        db.session.commit()

        # Obter o ID do usuário recém-criado
        id_user = user.query.filter_by(email=email).first()

        for aceite in aceites:
            id_termo = aceite.get('id_termo')
            valor_aceite = aceite.get('aceite')

            # Verificar se o termo e o usuário são válidos
            termo_valido = termos.query.filter_by(id=id_termo).first()
            if not termo_valido:
                return jsonify({'erro': 'Termo inválido'}), 400

            # Verificar se o usuário já aceitou este termo
            termo_aceito = aceitacao_usuario.query.filter_by(id_user=id_user.id, id_termo=id_termo).first()

            if not termo_aceito:
                # Adicionar o aceite para o termo específico
                new_aceite = aceitacao_usuario(id_termo=id_termo, id_user=id_user.id, aceite=valor_aceite, data_aceitacao=data_aceitacao)
                db.session.add(new_aceite)
            else:
                # Se o usuário já aceitou, atualizar o valor do aceite
                termo_aceito.aceite = valor_aceite
                termo_aceito.data_aceitacao = data_aceitacao

        db.session.commit()
        return jsonify({'mensagem': 'Dado salvo com sucesso!'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': 'Falha ao salvar os dados.'}), 500


#############################
###### login routes #########
#############################


@app.route('/login', methods=['POST'])
def login(email_in=None, senha_in=None):
    
    if email_in != None or senha_in != None:
        email = email_in
        senha = senha_in
    else: 
        data = request.get_json()
        email = data.get('email')
        senha = data.get('senha')

    # email padrão -> admin@admin.com, senha padrão -> admin123
    User = user.query.filter_by(email=email).first()

    if User and bcrypt.checkpw(senha.encode('utf-8'), User.senha.encode('utf-8')):
        # Credenciais válidas, crie um token JWT
        access_token = create_access_token(identity=User.id)
        return jsonify({'access_token': access_token, 'user_id': User.id, 'nome': User.nome}), 200
    else:
        return jsonify({'message': 'Credenciais inválidas.'}), 401
        # Se as credenciais não forem válidas (email incorreto, senha incorreta ou ambos),
        # retorna uma resposta JSON com uma mensagem de "Credenciais inválidas" e um código de status HTTP 401 (Não Autorizado).


# @app.route('/loginmongo/', methods=['POST'])
# def login_mongo():
#     data = request.get_json()
#     email = data.get('email')
#     senha = data.get('senha')

#     collection = mongo_connection()

#     # Encontre o usuário com o email fornecido
#     user = collection.find_one({"email": email})

#     # Recupere o hash da senha do documento MongoDB
#     hashed_password = user.get("senha")

#     if user and bcrypt.checkpw(senha.encode('utf-8'), hashed_password.encode('utf-8')):
#         # Credenciais válidas, crie um token JWT
#         access_token = create_access_token(identity=email)
#         return jsonify({'access_token': access_token}), 200
#     else:
#         return jsonify({'message': 'Credenciais inválidas.'}), 401
#         # Se as credenciais não forem válidas (email incorreto, senha incorreta ou ambos),
#         # retorna uma resposta JSON com uma mensagem de "Credenciais inválidas" e um código de status HTTP 401 (Não Autorizado).

#     # Feche a conexão com o MongoDB
#     client.close()

def mongo_connection():
    uri = "mongodb+srv://phantom:<password>@cluster0.yxkoek8.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(uri)

    # Nome da coleção
    collection = client.GeoForesight.NewUser

    return collection

def generate_random_email():
    # Gerar uma string aleatória de comprimento 8
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    # Concatenar a string aleatória com um domínio de e-mail fictício
    email = f"{random_string}@excluido.com"
    return email


@app.route('/usuario/atualizar/<int:id>', methods=['POST'])
def atualizar_usuario(id):
    data = request.get_json()

    # Recuperar o usuário pelo ID
    usuario = user.query.get(id)

    if usuario:
        # Atualizar os campos desejados
        usuario.nome = "****"
        usuario.email = generate_random_email()
        usuario.senha = "******"
        usuario.telefone = '********'

        try:
            db.session.commit()
            login_mongo(usuario.id),
            return jsonify({'mensagem': 'Dados salvos no MongoDB com sucesso!'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'erro': 'Falha ao atualizar o usuário.'}), 500
    else:
        return jsonify({'erro': 'Usuário não encontrado.'}), 404




def login_mongo(user_id):
    try:
        # Função para salvar o ID e a data no MongoDB
        collection = mongo_connection()

        # Verificar se o usuário existe
        usuario = user.query.get(user_id)

        if usuario:
            # Inserindo apenas a data e o id_user no MongoDB
            user_data = {
                '_id': ObjectId(),
                'id_user': usuario.id,
                'data': datetime.now()
            }

            # Inserindo os dados no MongoDB
            collection.insert_one(user_data)

            # Fechar a conexão com o MongoDB (opcional dependendo da sua lógica de aplicação)
            # client.close()

            return jsonify({'mensagem': 'Dados salvos no MongoDB com sucesso!'}), 200
        else:
            return jsonify({'erro': 'Usuário não encontrado.'}), 404

    except Exception as e:
        return jsonify({'erro': f'Erro ao inserir dados no MongoDB: {str(e)}'}), 500

#############################
###### General Routes #######
#############################

@app.route('/infousers', methods=['GET'])
@jwt_required()
def get_user():
        try:
            current_user = get_jwt_identity()
            current_user = user.query.filter_by(id=current_user).first()

            if current_user:
                resposta = {
                    'nome': current_user.nome,
                    'email': current_user.email,
                    'telefone': current_user.telefone,
                }
                return jsonify(resposta), 200
            else:
                return jsonify({'mensagem': 'Usuário não encontrado'}), 404

        except Exception as e:
            return jsonify({'mensagem': 'Erro interno'}), 500


@app.route('/attuser', methods=['PUT'])
@jwt_required()
def update_user_info():
    current_user = get_jwt_identity()
    current_user = user.query.filter_by(id=current_user).first()

    if not current_user:
        return jsonify({'error': 'User not found'}), 404

    data = request.get_json()
    nome = data.get('nome')
    email = data.get('email')
    telefone = data.get('telefone')

    if nome:
        current_user.nome = nome
    if email:
        current_user.email = email
    if telefone:
        current_user.telefone = telefone

    db.session.commit()

    return jsonify({'mensagem': 'Informações atualizadas com sucesso!'}), 200


@app.route('/create_tipo_termos', methods=['POST'])
def create_tipo_termos():
    dados = request.get_json()
    tipo_desc = dados.get('tipo_desc')
    new_tipo_termo = tipo_termos( tipo_desc=tipo_desc)
    db.session.add(new_tipo_termo)
    db.session.commit()

    return jsonify({'message': 'tipo termo criado com sucesso!'}), 201


@app.route('/create_termos', methods=['POST'])
def create_termos():
    dados = request.get_json()
    id_tipo = dados.get('id_tipo')
    data = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
    termo = dados.get('termo')

    new_termo = termos(data=data, termo=termo, id_tipo=id_tipo)
    db.session.add(new_termo)
    db.session.commit()

    return jsonify({'message': 'termo criado com sucesso!'}), 201

@app.route('/aceitar_termo', methods=['POST'])
def aceitar_termo():
    dados = request.get_json()

    id_user = dados.get('id_user')
    aceites = dados.get('aceites')  # aceites é uma lista de dicionários contendo id_termo e aceite

    data_aceitacao = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
    
    if id_user is None or aceites is None:
        return jsonify({'message': 'Parâmetros inválidos'}), 400

    try:
        for aceite in aceites:
            id_termo = aceite.get('id_termo')
            aceitacao = aceitacao_usuario(id_user=id_user, id_termo=id_termo, aceite=aceite['aceite'], data_aceitacao=data_aceitacao)
            db.session.add(aceitacao)
        
        db.session.commit()
        return jsonify({'message': 'Aceitação dos termos salva com sucesso'}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Termo ou usuário não encontrado'}), 404



@app.route('/termo_mais_recente', methods=['GET'])
def termo_mais_recente():
    subquery = db.session.query(
        termos.id_tipo,
        func.max(termos.data).label('max_data')
    ).group_by(termos.id_tipo).subquery()

    query = db.session.query(termos).join(
        subquery,
        (termos.id_tipo == subquery.c.id_tipo) &
        (termos.data == subquery.c.max_data)
    )

    resultados = query.all()

    if resultados:
        termos_mais_recentes = []
        for resultado in resultados:
            termos_mais_recentes.append({
                'id': resultado.id,
                'data': resultado.data.strftime('%Y-%m-%d'),
                'id_tipo': resultado.id_tipo,
                'termo': resultado.termo
            })

        return jsonify(termos_mais_recentes), 200
    else:
        return jsonify({'message': 'Nenhum termo encontrado'}), 404
    

@app.route('/verificar_aceitacao', methods=['GET'])
@jwt_required()
def verificar_aceitacao():
    current_user = get_jwt_identity()

    query = text(f"""
        SELECT id_user, au.id_termo , data_aceitacao, au.aceite
            FROM aceitacao_usuario AS au
            join public.user as u on u.id = au.id_user 
            WHERE au.aceite = True
            AND au.data_aceitacao = ( SELECT MAX(data_aceitacao)
            FROM aceitacao_usuario
            WHERE id_user =:current_user);
    """)

    result = db.session.execute(query, {'current_user': current_user})

    
    termos_aceitos = []
    for row in result:
        termos_aceitos.append({
            'id_user': row[0],
            'id_termo': row[1],
            'data_aceitacao': row[2].isoformat(),
            'aceite': row[3]
        })
    print(termos_aceitos)

    if termos_aceitos:
        return jsonify({'termos_aceitos': termos_aceitos})
    else:
        return jsonify({'message': 'Nenhum termo aceito encontrado'}), 404


@app.route('/verificar_aceitacao_email', methods=['GET'])
@jwt_required() 
def aceitou_email():
    current_user = get_jwt_identity()

    query = text("""  SELECT id_user, au.id_termo, tt.tipo_desc, data_aceitacao, au.aceite
        FROM aceitacao_usuario AS au
        JOIN public.user AS u ON u.id = au.id_user
        JOIN termos AS t ON t.id = au.id_termo
        JOIN tipo_termos AS tt ON tt.id_tipo = t.id_tipo
        WHERE au.id_user = :current_user
        AND au.aceite = true
        AND tt.tipo_desc LIKE '%Email%'
        AND au.data_aceitacao = (
            SELECT MAX(data_aceitacao)
            FROM aceitacao_usuario
            WHERE id_user = au.id_user
        );""")

    result = db.session.execute(query, {'current_user': current_user})
    termos_aceitos_email = list(result.fetchall())

    if termos_aceitos_email:
        return jsonify({'message': 'Envio de email permitido'}), 200
    else:
        return jsonify({'message': 'Envio de email não permitido'}), 403
    


@app.route('/verificar_aceitacao_whatsapp', methods=['GET'])
@jwt_required()
def aceitou_envio_whatsapp():
    current_user = get_jwt_identity()

    query = text("""
        SELECT id_user, au.id_termo, tt.tipo_desc, data_aceitacao, au.aceite, u.telefone
        FROM aceitacao_usuario AS au
        JOIN public.user AS u ON u.id = au.id_user
        JOIN termos AS t ON t.id = au.id_termo
        JOIN tipo_termos AS tt ON tt.id_tipo = t.id_tipo
        WHERE au.id_user = :current_user
        AND au.aceite = true
        AND tt.tipo_desc LIKE '%WhatsApp%'
        AND au.data_aceitacao = (
            SELECT MAX(data_aceitacao)
            FROM aceitacao_usuario
            WHERE id_user = au.id_user
        );
    """)

    result = db.session.execute(query, {'current_user': current_user})
    termos_aceitos_wpp = list(result.fetchall())

    if termos_aceitos_wpp:
        return jsonify({'message': 'Envio de WhatsApp permitido'}), 200
    else:
        return jsonify({'message': 'Envio de WhatsApp não permitido'}), 403
    
@app.route('/enviar-emails', methods=['GET'])
def enviar_emails():
    with db.engine.connect() as connection:
            query = text('''
                SELECT id_user, au.id_termo ,tt.tipo_desc , data_aceitacao, au.aceite, u.email 
                FROM aceitacao_usuario AS au
                join public.user as u on u.id = au.id_user 
                join termos as t on t.id = au.id_termo 
                join tipo_termos as tt on tt.id_tipo = t.id_tipo 
                WHERE au.aceite = true
                AND tt.tipo_desc like '%Email%'
                AND au.data_aceitacao = (
                    SELECT
                        MAX(data_aceitacao)
                    FROM
                        aceitacao_usuario
                    WHERE
                        id_user = au.id_user
                );
            ''')
            aceitacoes = connection.execute(query)
        
            results = aceitacoes.fetchall()
        
        # Verifica se a lista de resultados está vazia
            if not results:
                return jsonify({'message': 'Nenhum e-mail a ser enviado'}), 404

            output = []
            for row in results:
                row_dict = {
                    'id_user': row[0],
                    'id_termo': row[1],
                    'data_aceitacao': row[2],
                    'aceite': row[3]
                }
                output.append(row_dict)

    lista_de_emails = []
    for item in output:
        if 'u.email' in item:
            lista_de_emails.append(item['u.email'])

    smtp_server = 'smtp.office365.com'
    smtp_port = 587  # Porta SMTP (normalmente 587 para TLS)
    smtp_username = 'geoforesight-api@outlook.com'   # Seu endereço de e-mail
    smtp_password = 'Abc@2023'  # Sua senha de e-mail

    with open('data/config.json', 'r') as config_file:
        config_data = json.load(config_file)

    assunto = config_data.get('assunto_email', 'GeoForesight Project')
    corpo_da_mensagem = config_data.get('corpo_da_mensagem', 'Corpo do e-mail padrão.')

    # Itera sobre a lista de e-mails e envia e-mails
    for email in lista_de_emails:
        msg = EmailMessage()
        msg.set_content(corpo_da_mensagem)
        msg['Subject'] = assunto
        msg['From'] = smtp_username
        msg['To'] = email

        # Estabelece a conexão com o servidor SMTP e envia o e-mail
        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()  # Inicia uma conexão segura
            server.login(smtp_username, smtp_password)
            server.send_message(msg)
            server.quit()
            print(f'E-mail enviado para {email}')
        except Exception as e:
            print(f'Falha ao enviar e-mail para {email}: {str(e)}')
    
    return jsonify({'message': 'E-mail enviados com sucesso'}), 201

@app.route('/enviar-whatsapp', methods=['GET'])
def enviar_whatsapp():
    with db.engine.connect() as connection:
            query = text('''
                SELECT id_user, au.id_termo ,tt.tipo_desc , data_aceitacao, au.aceite, u.telefone 
                FROM aceitacao_usuario AS au
                join public.user as u on u.id = au.id_user 
                join termos as t on t.id = au.id_termo 
                join tipo_termos as tt on tt.id_tipo = t.id_tipo 
                WHERE au.aceite = true
                AND tt.tipo_desc like '%Whats%'
                AND au.data_aceitacao = (
                    SELECT
                        MAX(data_aceitacao)
                    FROM
                        aceitacao_usuario
                    WHERE
                        id_user = au.id_user
                );
            ''')
            aceitacoes = connection.execute(query)
        
            results = aceitacoes.fetchall()
        
        # Verifica se a lista de resultados está vazia
            if not results:
                return jsonify({'message': 'Nenhuma mensagem a ser enviado'}), 404

            output = []
            for row in results:
                row_dict = {
                    'id_user': row[0],
                    'id_termo': row[1],
                    'data_aceitacao': row[2],
                    'aceite': row[3]
                }
                output.append(row_dict)

    lista_de_whatsapp = []
    for item in output:
        if 'u.telefone' in item:
            lista_de_whatsapp.append(item['u.telefone'])
    for tel in lista_de_whatsapp:
        try:
            print(f'Mensagem enviada para {tel}')
        except Exception as e:
            print(f'Falha ao enviar mensagem para {tel}: {str(e)}')
    
    return jsonify({'message': 'Mensagens enviadas com sucesso'}), 201





# # nova consulta
@app.route('/consultaTeste/', methods=['POST'])
@jwt_required()
def consulta_teste():
    current_user = get_jwt_identity()
    data = request.json

    # adicionar os seguintes campos no filtro da query dinamica:
    # Solo ok
    # Clima ok
    # Ciclo do cultivo
    # Estado

    print(data)
    try:

        query = ''' SELECT 
                        sub.ref_bacen,
                        sub.nu_identificador,
                        ARRAY_TO_STRING(ARRAY_AGG(concat(sub.latitude, ',', sub.longitude) ORDER BY sub.nu_ponto), '/') as coordenadas,
                        oce.inicio_plantio,
                        oce.final_plantio,
                        oce.data_vencimento,
                        oce.inicio_colheita,
                        oce.final_colheita,
						oce.estado,
						mg.nome as municipio,
                        pr.nome as produto,
                        irrigacao.descricao as descricao_irrigacao,
                        ciclo_producao.descricao as descricao_producao,
                        grao.descricao as descricao_grao,
						solo.descricao as descricao_solo,
						evento_climatico.descricao as descricao_evento,
						ciclo_cultivar.descricao as descricao_cultiva
                    FROM (
                        SELECT 
                            glebas.ref_bacen,
                            glebas.nu_identificador,
                            glebas.latitude,
                            glebas.longitude,
                            glebas.nu_ponto
                        FROM 
                            glebas
                            JOIN operacao_credito_estadual ON glebas.ref_bacen = operacao_credito_estadual.ref_bacen
                            JOIN irrigacao ON irrigacao.idirrigacao = operacao_credito_estadual.idirrigacao
                            JOIN grao ON grao.idgrao = operacao_credito_estadual.idgrao
                            JOIN ciclo_producao ON ciclo_producao.idciclo = operacao_credito_estadual.idciclo
                        WHERE 
                            1=1
                        ORDER BY 
                            glebas.nu_ponto ASC
                    ) as sub
                    JOIN operacao_credito_estadual oce ON sub.ref_bacen = oce.ref_bacen
                    JOIN irrigacao ON irrigacao.idirrigacao = oce.idirrigacao
					LEFT JOIN municipio_glebas mg ON mg.ref_bacen = oce.ref_bacen
                    JOIN grao ON grao.idgrao = oce.idgrao
                    JOIN ciclo_producao ON ciclo_producao.idciclo = oce.idciclo
                    LEFT JOIN empreendimento em on oce.idempreendimento = em.idempreendimento
					LEFT JOIN produtos pr on em.idproduto = pr.idproduto
					LEFT JOIN solo on solo.idsolo = oce.idsolo
					LEFT JOIN evento_climatico ON evento_climatico.idevento = oce.idevento
					LEFT JOIN ciclo_cultivar on ciclo_cultivar.idcultivar = oce.idcultivar
                    WHERE 1=1
                             '''
        if data['ref_bacen'] is not None:
            query += f" AND sub.ref_bacen = {data['ref_bacen']}"
        if data['nu_identificador'] is not None:
            query += f" AND sub.nu_identificador = {data['nu_identificador']}"
        if data['altitude'] is not None:
            query += f" AND glebas.altitude = {data['altitude']}"
        if data['inicio_plantio'] is not None:
            query += f" AND oce.inicio_plantio >= '{data['inicio_plantio']}'"
        if data['descricao_solo'] is not None:
            query += f" AND solo.descricao = '{data['descricao_solo']}'"
        if data['descricao_evento'] is not None:
            query += f" AND evento_climatico.descricao = '{data['descricao_evento']}'"
        if data['descricao_cultiva'] is not None:
            query += f" AND ciclo_cultivar.descricao = '{data['descricao_cultiva']}'"
        if data['final_plantio'] is not None:
            query += f" AND oce.final_plantio <= '{data['final_plantio']}'"
        if data['inicio_colheita'] is not None:
            query += f" AND oce.inicio_colheita >= '{data['inicio_colheita']}'"
        if data['final_colheita'] is not None:
            query += f" AND oce.final_colheita <= '{data['final_colheita']}'"
        if data['descricao_grao'] is not None:
            query += f" AND grao.descricao = '{data['descricao_grao']}'"
        if data['descricao_producao'] is not None:
            query += f" AND ciclo_producao.descricao = '{data['descricao_producao']}'"
        if data['municipio'] is not None:
            query += f" AND mg.nome = '{data['municipio']}'"
        if data['estado'] is not None:
           query += f" AND oce.estado = '{data['estado']}'"
        if data['produto'] is not None:
           query += f" AND pr.nome = '{data['produto']}'"
        if data['descricao_irrigacao'] is not None:
            query += f" AND irrigacao.descricao = '{data['descricao_irrigacao']}'"

        group = """ 
                    GROUP BY 
                        sub.ref_bacen,
                        oce.inicio_plantio, 
                        oce.final_plantio,
                        oce.data_vencimento,
                        oce.inicio_colheita,
                        oce.final_colheita,
						oce.estado,
						mg.nome,
                        irrigacao.descricao,
                        ciclo_producao.descricao ,
                        grao.descricao,
                        sub.nu_identificador,
						solo.descricao,
						evento_climatico.descricao,
						ciclo_cultivar.descricao,
                        pr.nome"""
        # Criar uma conexão com o banco de dados
        # Substitua pela sua string de conexão


        engine = create_engine(os.getenv('url_heroku'))

        conn = engine.connect()

        # Executar a query
        resultados = conn.execute(text(query + group)).fetchall()

        # Montar a lista de resultados
        lista_resultados = []
        for resultado in resultados:
            resultado_dict = {
        "ref_bacen": resultado.ref_bacen,
        "nu_identificador": resultado.nu_identificador,
        "coordenadas": resultado.coordenadas,
        "inicio_plantio": resultado.inicio_plantio,
        "final_plantio": resultado.final_plantio,
        "data_vencimento": resultado.data_vencimento, 
        "inicio_colheita": resultado.inicio_colheita,
        "final_colheita": resultado.final_colheita,
        "descricao_grao": resultado.descricao_grao,
        "descricao_irrigacao": resultado.descricao_irrigacao,
        "descricao_producao": resultado.descricao_producao,
        "descricao_solo": resultado.descricao_solo, 
        "descricao_evento": resultado.descricao_evento, 
        "descricao_cultiva": resultado.descricao_cultiva,
        "estado": resultado.estado,
        "municipio": resultado.municipio,
        "produto": resultado.produto
    }
            lista_resultados.append(resultado_dict)

        #  Fechar a conexão
        conn.close()

        return jsonify(lista_resultados), 200

    except Exception as e:
        # Tratamento de erro: retorna uma mensagem de erro genérica em caso de exceção

        return jsonify({'error': 'Ocorreu um erro no processamento da solicitação.'}), 500
    

@app.route('/consultaNova', methods=['POST'])
@jwt_required()
def consulta_nova():
    current_user = get_jwt_identity()
    data = request.json

    print(data)
    try:

        query = ''' SELECT distinct * from 
                public.vw_previsoes
                    WHERE 1=1
                '''

        if data['ref_bacen'] is not None:
            query += f" AND ref_bacen = '{data['ref_bacen']}'"
        if data['nu_identificador'] is not None:
            query += f" AND nu_identificador = {data['nu_identificador']}"
        if data['inicio_plantio'] is not None:
            query += f" AND inicio_plantio >= '{data['inicio_plantio']}'"
        if data['descricao_solo'] is not None:
            query += f" AND descricao_solo = '{data['descricao_solo']}'"
        if data['descricao_evento'] is not None:
            query += f" AND descricao_evento = '{data['descricao_evento']}'"
        if data['descricao_cultiva'] is not None:
            query += f" AND descricao_cultiva = '{data['descricao_cultiva']}'"
        if data['final_plantio'] is not None:
            query += f" AND final_plantio <= '{data['final_plantio']}'"
        if data['inicio_colheita'] is not None:
            query += f" AND inicio_colheita >= '{data['inicio_colheita']}'"
        if data['final_colheita'] is not None:
            query += f" AND final_colheita <= '{data['final_colheita']}'"
        if data['descricao_grao'] is not None:
            query += f" AND descricao_grao = '{data['descricao_grao']}'"
        if data['descricao_producao'] is not None:
            query += f" AND descricao_producao = '{data['descricao_producao']}'"
        if data['municipio'] is not None:
            query += f" AND municipio = '{data['municipio']}'"
        if data['estado'] is not None:
           query += f" AND estado = '{data['estado']}'"
        if data['produto'] is not None:
           query += f" AND produto = '{data['produto']}'"
        if data['descricao_irrigacao'] is not None:
            query += f" AND descricao_irrigacao = '{data['descricao_irrigacao']}'"
        
        query2 = ' order by date ASC'
        
        engine = create_engine(os.getenv('url_heroku'))

        conn = engine.connect()

        # Executar a query
        resultados = conn.execute(text(query+query2)).fetchall()

        # Montar a lista de resultados
        lista_resultados = []
        for resultado in resultados:
            resultado_dict = {
        "ref_bacen": resultado.ref_bacen,
        "nu_identificador": resultado.nu_identificador,
        "coordenadas": resultado.coordenadas,
        "inicio_plantio": resultado.inicio_plantio,
        "final_plantio": resultado.final_plantio,
        "inicio_colheita": resultado.inicio_colheita,
        "final_colheita": resultado.final_colheita,
        "descricao_grao": resultado.descricao_grao,
        "descricao_irrigacao": resultado.descricao_irrigacao,
        "descricao_producao": resultado.descricao_producao,
        "descricao_solo": resultado.descricao_solo, 
        "descricao_evento": resultado.descricao_evento, 
        "descricao_cultiva": resultado.descricao_cultiva,
        "estado": resultado.estado,
        "municipio": resultado.municipio,
        "produto": resultado.produto,
        "previsao": resultado.previsao,
        "date": resultado.date,
        "indice": resultado.indice
    }
            lista_resultados.append(resultado_dict)

        #  Fechar a conexão
        conn.close()

        return jsonify(lista_resultados), 200

    except Exception as e:
        # Tratamento de erro: retorna uma mensagem de erro genérica em caso de exceção

        return jsonify({'error': 'Ocorreu um erro no processamento da solicitação.'}), 500
    
# main
if __name__ == '__main__':
    app.run(debug=True)
