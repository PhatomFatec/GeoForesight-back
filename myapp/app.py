from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from geoalchemy2 import Geography
import requests

app = Flask(__name__)

# Configurações do banco de dados PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:A@996739786@localhost/geoforesight'
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


with app.app_context():
    db.create_all()


@app.route('/table', methods=['GET'])
def get_table_data():
    try:
        data = Table.query.all()
        response = [{'id': item.id, 'name': item.name} for item in data]
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/ciclo_producao/<int:id>', methods=['GET'])
def obter_ciclo_producao(id):
    try:
        ciclo = ciclo_producao.query.get(id)
        if ciclo is None:
            return jsonify({"mensagem": "Ciclo não encontrado"}), 404

        # Você pode retornar os dados do ciclo como JSON
        return jsonify({
            "idciclo": ciclo.idciclo,
            "descricao": ciclo.descricao
        }), 200
    except Exception as e:
        return jsonify({"mensagem": "Erro interno do servidor"}), 500
    
@app.route('/consulta/<int:ref_bacen>/<int:nu_ordem>/<string:coordenadas>/<int:altitude>/<string:inicio_plantio>/<string:final_plantio>/<string:inicio_colheita>/<string:final_colheita>/<string:descricao_grao>/<string:descricao_producao>/<string:descricao_irrigacao>', methods=['GET'])
def consulta_dinamica(ref_bacen, nu_ordem, coordenadas, altitude, inicio_plantio, final_plantio, inicio_colheita, final_colheita, descricao_grao, descricao_producao, descricao_irrigacao):
    
    try:
        
            query = ''' select glebas.ref_bacen, glebas.nu_ordem, glebas.coordenadas, operacao_credito_estadual.inicio_plantio, operacao_credito_estadual.final_plantio, operacao_credito_estadual.data_liberacao, operacao_credito_estadual.data_vencimento,
                                            operacao_credito_estadual.inicio_colheita, operacao_credito_estadual.final_colheita, irrigacao.descricao, ciclo_producao.descricao, produtos.nome
                                            from glebas
                                            join operacao_credito_estadual on glebas.ref_bacen = operacao_credito_estadual.ref_bacen
                                            join irrigacao on irrigacao.idirrigacao = operacao_credito_estadual.idirrigacao
                                            join ciclo_producao on ciclo_producao.idciclo = operacao_credito_estadual.idciclo
                                            join empreendimento on empreendimento.idteste = operacao_credito_estadual.idempreendimento
                                            join produtos on produtos.idproduto = empreendimento.idproduto
                                            where 1
                                        '''
        
            if ref_bacen != "NULL":
                query += f''' and ref_bacen = {ref_bacen}'''
            if nu_ordem != "NULL":
                query += f''' and ref_bacen = {ref_bacen}'''
            if coordenadas != "NULL":
                query += f''' and ref_bacen = {ref_bacen}'''
            if altitude != "NULL":
                query += f''' and ref_bacen = {ref_bacen}'''
            if inicio_plantio != "NULL":
                query += f''' and ref_bacen = {ref_bacen}'''
            if final_plantio != "NULL":
                query += f''' and ref_bacen = {ref_bacen}'''
            if inicio_colheita != "NULL":
                query += f''' and ref_bacen = {ref_bacen}'''   
            if final_colheita != "NULL":
                query += f''' and ref_bacen = {ref_bacen}'''
                
            if descricao_grao != "NULL":
                query += f''' and ref_bacen = {ref_bacen}'''
                
            if descricao_producao != "NULL":
                query += f''' and ref_bacen = {ref_bacen}'''
                
            if descricao_irrigacao != "NULL":
                query += f''' and ref_bacen = {ref_bacen}'''

    except Exception as e:
        # Tratamento de erro: retorna uma mensagem de erro genérica em caso de exceção

        return jsonify({'error': 'Ocorreu um erro no processamento da solicitação.'}), 500


if __name__ == '__main__':
    app.run(debug=True)