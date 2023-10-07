from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from geoalchemy2 import Geography
import requests
from sqlalchemy import create_engine, text

app = Flask(__name__)

CORS(app)

# Configurações do banco de dados PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost/geoforesight'
db = SQLAlchemy(app)

# Defina o modelo para a tabela "table"

class Table(db.Model):
    __tablename__ = 'table'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

# class clima(db.Model):
#     idClima = db.Column(db.Integer, primary_key=True, nullable=False)
#     descricao = db.Column(db.String(255))
#     operacao_credito_estadual = db.relationship(
#         'operacao_credito_estadual', backref='clima')

class irrigacao(db.Model):
    idirrigacao = db.Column(db.Integer, primary_key=True,
                            nullable=False,  autoincrement=False)
    descricao = db.Column(db.String(255))
    operacao_credito_estadual = db.relationship(
        'operacao_credito_estadual', backref='irrigacao')

# class solo(db.Model):
#     idSolo = db.Column(db.Integer, primary_key=True, nullable=False)
#     descricao = db.Column(db.String(255))
#     operacao_credito_estadual = db.relationship(
#         'operacao_credito_estadual', backref='solo')


class ciclo_producao(db.Model):
    idciclo = db.Column(db.Integer, primary_key=True,
                        nullable=False,  autoincrement=False)
    descricao = db.Column(db.String(255))
    operacao_credito_estadual = db.relationship(
        'operacao_credito_estadual', backref='ciclo_producao')


class grao(db.Model):
    idgrao = db.Column(db.Integer, primary_key=True,
                       nullable=False,  autoincrement=False)
    descricao = db.Column(db.String(255))
    operacao_credito_estadual = db.relationship(
        'operacao_credito_estadual', backref='grao')


# class evento_climatico(db.Model):
#     idEvento = db.Column(db.Integer, primary_key=True, nullable=False)
#     descricao = db.Column(db.String(255))
#     operacao_credito_estadual = db.relationship(
#         'operacao_credito_estadual', backref='evento_climatico')


class produtos(db.Model):
    idproduto = db.Column(db.Integer, primary_key=True,
                          nullable=False,  autoincrement=False)
    nome = db.Column(db.String(255))
    Empreendimento = db.Relationship('empreendimento', backref='produtos')


class operacao_credito_estadual(db.Model):
    ref_bacen = db.Column(db.Integer, primary_key=True,
                          unique=True, nullable=False,  autoincrement=False)
    nu_ordem = db.Column(db.Integer, primary_key=True,
                         unique=True, nullable=False,  autoincrement=False)
    inicio_plantio = db.Column(db.Date, nullable=False)
    final_plantio = db.Column(db.Date, nullable=False)
    final_colheita = db.Column(db.Date, nullable=False)
    inicio_colheita = db.Column(db.Date, nullable=False)
    data_liberacao = db.Column(db.Date, nullable=False)
    data_vencimento = db.Column(db.Date, nullable=False)
    idciclo = db.Column(db.Integer, db.ForeignKey('ciclo_producao.idciclo'))
    idteste = db.Column(
        db.Integer, db.ForeignKey('empreendimento.idteste'))
    # idClima = db.Column(db.Integer, db.ForeignKey('clima.idClima'))
    # idEvento = db.Column(db.Integer, db.ForeignKey('evento_climatico.idEvento'))
    idgrao = db.Column(db.Integer, db.ForeignKey('grao.idgrao'))
    # idSolo = db.Column(db.Integer, db.ForeignKey('solo.idSolo'))
    idirrigacao = db.Column(db.Integer, db.ForeignKey('irrigacao.idirrigacao'))
    idempreendimento = db.Column(
        db.Integer, db.ForeignKey('empreendimento.idempreendimento'))
    # glebas = db.relationship('glebas', backref='operacao_credito_estadual')

    __table_args__ = (
        db.PrimaryKeyConstraint('ref_bacen', 'nu_ordem'),
    )


class glebas(db.Model):
    idgleba = db.Column(db.Integer, primary_key=True,
                        nullable=False,  autoincrement=False)
    coordenadas = db.Column(
        Geography(geometry_type='POINT', srid=4326), nullable=False)
    altitude = db.Column(db.Double)
    nu_ponto = db.Column(db.Integer, nullable=False)
    ref_bacen = db.Column(db.Integer, db.ForeignKey(
        'operacao_credito_estadual.ref_bacen'))
    nu_ordem = db.Column(db.Integer, db.ForeignKey(
        'operacao_credito_estadual.nu_ordem'))


class empreendimento(db.Model):
    idteste = db.Column(db.Integer, primary_key=True, nullable=False)
    idempreendimento = db.Column(db.BigInteger, nullable=False)
    finalidade = db.Column(db.String(255))
    cesta = db.Column(db.String(255), nullable=False)
    modalidade = db.Column(db.String(255), nullable=False)
    idproduto = db.Column(db.Integer, db.ForeignKey(
        'produtos.idproduto'), nullable=False)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)

with app.app_context():
    db.create_all()
   
@app.route('/consulta_dinamica/', methods=['POST'])
def consulta_dinamica():
    data = request.json
    print(data)
    try:
        
        query = ''' SELECT 
            glebas.ref_bacen,
            glebas.nu_ordem,
            glebas.coordenadas,
            operacao_credito_estadual.inicio_plantio,
            operacao_credito_estadual.final_plantio,
            operacao_credito_estadual.data_liberacao,
            operacao_credito_estadual.data_vencimento,
            operacao_credito_estadual.inicio_colheita,
            operacao_credito_estadual.final_colheita,
            irrigacao.descricao as descricao_irrigacao,
            ciclo_producao.descricao as descricao_producao,
            grao.descricao as descricao_grao
            FROM 
            glebas
            JOIN 
                operacao_credito_estadual ON glebas.ref_bacen = operacao_credito_estadual.ref_bacen
            JOIN 
                irrigacao ON irrigacao.idirrigacao = operacao_credito_estadual.idirrigacao
			JOIN 
				grao ON grao.idgrao = operacao_credito_estadual.idgrao
            JOIN 
                ciclo_producao ON ciclo_producao.idciclo = operacao_credito_estadual.idciclo
            WHERE 
                1=1 '''
            
        if data['ref_bacen'] != "NULL":
            query += f" AND glebas.ref_bacen = {data['ref_bacen']}"
        if data['nu_ordem'] != "NULL":
            query += f" AND glebas.nu_ordem = {data['nu_ordem']}"
        if data['altitude'] != "NULL":
            query += f" AND glebas.altitude = {data['altitude']}"
        if data['inicio_plantio'] != "NULL":
            query += f" AND operacao_credito_estadual.inicio_plantio = '{data['inicio_plantio']}'"
        if data['final_plantio'] != "NULL":
            query += f" AND operacao_credito_estadual.final_plantio = '{data['final_plantio']}'"
        if data['inicio_colheita'] != "NULL":
            query += f" AND operacao_credito_estadual.inicio_colheita = '{data['inicio_colheita']}'"   
        if data['final_colheita'] != "NULL":
            query += f" AND operacao_credito_estadual.final_colheita = '{data['final_colheita']}'"
        if data['descricao_grao'] != "NULL":
            query += f" AND grao.descricao = '{data['descricao_grao']}'"
        if data['descricao_producao'] != "NULL":
            query += f" AND ciclo_producao.descricao = '{data['descricao_producao']}'"
        if data['descricao_irrigacao'] != "NULL":
            query += f" AND irrigacao.descricao= '{data['descricao_irrigacao']}'"


        # Criar uma conexão com o banco de dados
        engine = create_engine('postgresql://postgres:123@localhost/geoforesight')  # Substitua pela sua string de conexão
        conn = engine.connect()

        # Executar a query
        resultados = conn.execute(text(query)).fetchall()

        # Montar a lista de resultados
        lista_resultados = []
        for resultado in resultados:
            resultado_dict = {
                 "ref_bacen": resultado.ref_bacen,
                "nu_ordem": resultado.nu_ordem,
                "coordenadas": resultado.coordenadas,
                "inicio_plantio": resultado.inicio_plantio,
                "final_plantio": resultado.final_plantio,
                "data_liberacao": resultado.data_liberacao,
                "data_vencimento": resultado.data_vencimento,
                "inicio_colheita": resultado.inicio_colheita,
                "final_colheita": resultado.final_colheita,
                "descricao_grao": resultado.descricao_grao,
                "descricao_irrigacao": resultado.descricao_irrigacao,
                "descricao_producao": resultado.descricao_producao,
            }
            lista_resultados.append(resultado_dict)

        #  Fechar a conexão
        conn.close()

        return jsonify(lista_resultados), 200

    except Exception as e:
        # Tratamento de erro: retorna uma mensagem de erro genérica em caso de exceção

        return jsonify({'error': 'Ocorreu um erro no processamento da solicitação.'}), 500




@app.route('/login/', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    senha = data.get('senha')

    user = User.query.filter_by(email=email, senha=senha).first() # email padrão -> admin@admin.com, senha 

    if user:
        return jsonify({'message': 'Login bem-sucedido!'})
    else:
        return jsonify({'message': 'Credenciais inválidas.'}), 401


if __name__ == '__main__':
    app.run(debug=True)