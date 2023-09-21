from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from geoalchemy2 import Geography

app = Flask(__name__)

# Configurações do banco de dados PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost/postgres'
db = SQLAlchemy(app)

# Defina o modelo para a tabela "table"
class Table(db.Model):
    __tablename__ = 'table'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
 



class Clima(db.Model):
    idClima = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(30))
    operacao_credito_estadual = db.relationship('Operacao_credito_estadual', backref='clima')


class Irrigacao(db.Model):
    idIrrigacao = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(30))
    operacao_credito_estadual = db.relationship('Operacao_credito_estadual', backref='irrigacao')


class Solo(db.Model):
    idSolo = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(30))
    operacao_credito_estadual = db.relationship('Operacao_credito_estadual', backref='solo')

class Ciclo_producao(db.Model):
    idCiclo = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(30))
    operacao_credito_estadual = db.relationship('Operacao_credito_estadual', backref='ciclo_producao')


class Grao(db.Model):
    idGrao = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(30))
    operacao_credito_estadual = db.relationship('Operacao_credito_estadual', backref='grao')


class Evento_climatico(db.Model):
    idEvento = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(30))
    operacao_credito_estadual = db.relationship('Operacao_credito_estadual', backref='evento_climatico')


class Produtos(db.Model):
    idProduto = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(30))
    Empreendimento = db.Relationship('Empreendimento',backref='produtos')

class Operacao_credito_estadual(db.Model):
    ref_bacen = db.Column(db.Integer, primary_key=True)
    nu_ordem = db.Column(db.Integer, primary_key=True)
    inicio_plantio = db.Column(db.Date)
    final_plantio = db.Column(db.Date)
    final_colheita = db.Column(db.Date)
    inicio_colheita = db.Column(db.Date)
    data_liberacao = db.Column(db.Date)
    data_vencimento = db.Column(db.Date)
    idCiclo = db.Column(db.Integer, db.ForeignKey('ciclo_producao.idCiclo'))
    idClima = db.Column(db.Integer, db.ForeignKey('clima.idClima'))
    idEvento = db.Column(db.Integer, db.ForeignKey('evento_climatico.idEvento'))
    idGrao = db.Column(db.Integer, db.ForeignKey('grao.idGrao'))
    idSolo = db.Column(db.Integer, db.ForeignKey('solo.idSolo'))
    idIrrigacao = db.Column(db.Integer, db.ForeignKey('irrigacao.idIrrigacao'))

    gleba = db.relationship('Glebas', back_populates='operacao', uselist=False)
    



class Glebas(db.Model):
    idGleba = db.Column(db.Integer, primary_key=True)
    ref_bacen = db.Column(db.Integer, primary_key=True)
    nu_ordem = db.Column(db.Integer, primary_key=True)
    coordenadas = db.Column(Geography(geometry_type='POINT', srid=4326))
    altitude = db.Column(db.Double)
    nu_ponto = db.Column(db.Integer)

    operacao = db.relationship('Operacao_credito_estadual', back_populates='gleba')



class Empreendimento(db.Model):
    idEmpreendimento = db.Column(db.Integer, primary_key=True)
    finalidade = db.Column(db.String(30))
    cesta = db.Column(db.String(30))
    modalidade = db.Column(db.String(30))
    idProduto = db.Column(db.Integer, db.ForeignKey('produtos.idProduto'))



# Crie as tabelas no banco de dados se elas não existirem
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

if __name__ == '__main__':
    app.run(debug=True)