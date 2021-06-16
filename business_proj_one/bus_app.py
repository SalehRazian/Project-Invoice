from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mah_db.db'
db = SQLAlchemy(app)

class Database_Model(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(256), nullable=False)
    qty_type = db.Column(db.String(10))
    price = db.Column(db.Float)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form['btn'] == 'Create Table':
            items_list = request.form.getlist('item') 
            return redirect(url_for('results', items=items_list))
        elif request.form['btn'] == 'ADD ITEM':
            item_description = request.form.get('description')
            item_qty_type = request.form.get('qty_type')
            item_price = request.form.get('price')
            new_item = Database_Model(description=item_description, qty_type=item_qty_type, price=item_price)

            try:
                db.session.add(new_item)
                db.session.commit()
                return redirect('/')
            except:
                return 'There was an issue adding your task'
    
    items = Database_Model.query.order_by(Database_Model.id).all()
    return render_template('index.html', items=items)

@app.route('/results')
def results():
    items_data = []
    id_list = request.args.getlist('items', None)
    for item_id in id_list:
        items_data.append(Database_Model.query.get_or_404(int(item_id)))
    return render_template('results.html', items=items_data)

if __name__ == "__main__":
    app.run(debug=True)