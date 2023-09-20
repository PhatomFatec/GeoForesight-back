from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configurações do banco de dados PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost/postgres'
db = SQLAlchemy(app)

# Defina o modelo para a tabela "table"
class Table(db.Model):
    __tablename__ = 'table'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

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