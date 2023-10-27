from datetime import datetime
import time
import bcrypt
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from geoalchemy2 import Geography
import requests
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)

load_dotenv()


# from pymongo.mongo_client import MongoClient
# from pymongo.server_api import ServerApi


app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'your-secret-key'

jwt = JWTManager(app)

CORS(app)

# Configurações do banco de dados PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('url_heroku')
db = SQLAlchemy(app)

# Defina o modelo para a tabela "table"

#############################
##### Define Functions ######
#############################


# def mongo_connection():
#     uri = "mongodb+srv://phantom:<password>@cluster0.yxkoek8.mongodb.net/?retryWrites=true&w=majority"
#     client = MongoClient(uri)

#     # Nome da coleção
#     collection = client.GeoForesight.User

#     return collection


#############################
##### Database Classes ######
#############################


# class Table(db.Model):
#     tablename = 'table'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(255), nullable=False)

# class clima(db.Model):
#     idClima = db.Column(db.Integer, primary_key=True, nullable=False)
#     descricao = db.Column(db.String(255))
#     operacao_credito_estadual = db.relationship(
#         'operacao_credito_estadual', backref='clima')


# class irrigacao(db.Model):
#     idirrigacao = db.Column(db.Integer, primary_key=True,
#                             nullable=False,  autoincrement=False)
#     descricao = db.Column(db.String(255))
#     operacao_credito_estadual = db.relationship(
#         'operacao_credito_estadual', backref='irrigacao')

# class solo(db.Model):
#     idSolo = db.Column(db.Integer, primary_key=True, nullable=False)
#     descricao = db.Column(db.String(255))
#     operacao_credito_estadual = db.relationship(
#         'operacao_credito_estadual', backref='solo')


# class ciclo_producao(db.Model):
#     idciclo = db.Column(db.Integer, primary_key=True,
#                         nullable=False,  autoincrement=False)
#     descricao = db.Column(db.String(255))
#     operacao_credito_estadual = db.relationship(
#         'operacao_credito_estadual', backref='ciclo_producao')


# class grao(db.Model):
#     idgrao = db.Column(db.Integer, primary_key=True,
#                        nullable=False,  autoincrement=False)
#     descricao = db.Column(db.String(255))
#     operacao_credito_estadual = db.relationship(
#         'operacao_credito_estadual', backref='grao')


# class evento_climatico(db.Model):
#     idEvento = db.Column(db.Integer, primary_key=True, nullable=False)
#     descricao = db.Column(db.String(255))
#     operacao_credito_estadual = db.relationship(
#         'operacao_credito_estadual', backref='evento_climatico')


# class produtos(db.Model):
#     idproduto = db.Column(db.Integer, primary_key=True,
#                           nullable=False,  autoincrement=False)
#     nome = db.Column(db.String(255))
#     Empreendimento = db.Relationship('empreendimento', backref='produtos')


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
    aceitacao_padrao = db.Column(db.Boolean, nullable=False)
    aceitacao_email = db.Column(db.Boolean, nullable=False)
    data_aceitacao = db.Column(db.Date, nullable=False)

class user(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)

    rel_ace_user  = db.relationship('aceitacao_usuario', backref='user', lazy=True)

class termos(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
    data = db.Column(db.String(255), unique=True, nullable=False)
    termo = db.Column(db.String(255), unique=True, nullable=False)

    rel_ace_user = db.relationship('aceitacao_usuario', backref='termos', lazy=True)


with app.app_context():
    db.create_all()




#############################
######## cadastro  ##########
#############################

@app.route('/cadastro/', methods=['POST'])
def cadastro():
    data = request.get_json()

    id = data.get('id')
    nome = data.get('nome')
    email = data.get('email')
    senha = data.get('senha')
    # aceitacao = data.get('aceitacao')
    # data_atual = datetime.now()

    termos_id = data.get('termos_id') # definir como o sistema vai funcionar para ver como será o id do termo, ex.: se sera puxado de forma dinamica
    
   
    # Gerar um salt aleatório
    salt = bcrypt.gensalt()

    # Criptografar a senha com o salt
    hashed_password = bcrypt.hashpw(senha.encode('utf-8'), salt)
    hashed_password = hashed_password.decode('utf-8')

    # Imprimir o valor de hash
    print(hashed_password)

    novo_dado = user(id=id, nome=nome, email=email, senha=hashed_password)

    try:
        db.session.add(novo_dado)
        db.session.commit()
        # Atrasar o login por 30 segundos
        time.sleep(3)

        return jsonify({'mensagem': 'Dado salvo com sucesso!'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': 'Falha ao salvar os dados.'}), 500

    


#############################
###### login routes #########
#############################


@app.route('/login/', methods=['POST'])
def login(email_in=None, senha_in=None):
    
    if email_in != None or senha_in != None:
        email = email_in
        senha = senha_in
    else: 
        data = request.get_json()
        email = data.get('email')
        senha = data.get('senha')

    # email padrão -> admin@admin.com, senha padrão -> admin123
    user = user.query.filter_by(email=email).first()

    if user and bcrypt.checkpw(senha.encode('utf-8'), user.senha.encode('utf-8')):
        # Credenciais válidas, crie um token JWT
        access_token = create_access_token(identity=email)
        return jsonify({'access_token': access_token}), 200
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



#############################
###### General Routes #######
#############################


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
                    JOIN grao ON grao.idgrao = oce.idgrao
                    JOIN ciclo_producao ON ciclo_producao.idciclo = oce.idciclo
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
            query += f" AND oce.inicio_plantio = '{data['inicio_plantio']}'"
        if data['descricao_solo'] is not None:
            query += f" AND solo.descricao = '{data['descricao_solo']}'"
        if data['descricao_evento'] is not None:
            query += f" AND evento_climatico.descricao = '{data['descricao_evento']}'"
        if data['descricao_cultiva'] is not None:
            query += f" AND ciclo_cultivar.descricao = '{data['descricao_cultiva']}'"
        if data['final_plantio'] is not None:
            query += f" AND oce.final_plantio = '{data['final_plantio']}'"
        if data['inicio_colheita'] is not None:
            query += f" AND oce.inicio_colheita = '{data['inicio_colheita']}'"
        if data['final_colheita'] is not None:
            query += f" AND oce.final_colheita = '{data['final_colheita']}'"
        if data['descricao_grao'] is not None:
            query += f" AND grao.descricao = '{data['descricao_grao']}'"
        if data['descricao_producao'] is not None:
            query += f" AND ciclo_producao.descricao = '{data['descricao_producao']}'"
        if data['descricao_irrigacao'] is not None:
            query += f" AND irrigacao.descricao = {data['descricao_irrigacao']}"

        group = """ 
                    GROUP BY 
                        sub.ref_bacen,
                        oce.inicio_plantio, 
                        oce.final_plantio,
                        oce.data_vencimento,
                        oce.inicio_colheita,
                        oce.final_colheita,
                        irrigacao.descricao,
                        ciclo_producao.descricao ,
                        grao.descricao,
                        sub.nu_identificador,
						solo.descricao,
						evento_climatico.descricao,
						ciclo_cultivar.descricao"""
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
        "descricao_cultiva": resultado.descricao_cultiva  
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