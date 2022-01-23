from flask import Flask, request, jsonify, json
from flask_sqlalchemy import SQLAlchemy
import data

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///orders.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(200))
    last_name = db.Column(db.String(200))
    age = db.Column(db.Integer)
    email = db.Column(db.String(200))
    role = db.Column(db.String(200))
    phone = db.Column(db.String(200))

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'age': self.age,
            'email': self.email,
            'role': self.role,
            'phone': self.phone,
        }


class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    description = db.Column(db.String(200))
    start_date = db.Column(db.String(100))
    end_date = db.Column(db.String(100))
    address = db.Column(db.String(200))
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'address': self.address,
            'price': self.price,
            'customer_id': self.customer_id,
            'executor_id': self.executor_id,
        }


class Offer(db.Model):
    __tablename__ = 'offer'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def to_dict(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'executor_id': self.executor_id,

        }

db.drop_all()
db.create_all()

for user in data.users:
    new_user = User(
        id=user['id'],
        first_name=user['first_name'],
        last_name=user['last_name'],
        age=user['age'],
        email=user['email'],
        role=user['role'],
        phone=user['phone'],
    )
    db.session.add(new_user)
    db.session.commit()

for order in data.orders:
    new_order = Order(
        id=order['id'],
        name=order['name'],
        description=order['description'],
        start_date=order['start_date'],
        end_date=order['end_date'],
        address=order['address'],
        price=order['price'],
        customer_id=order['customer_id'],
        executor_id=order['executor_id'],
    )
    db.session.add(new_order)
    db.session.commit()

for offer in data.offers:
    new_offer = Offer(
        id=offer['id'],
        order_id=offer['order_id'],
        executor_id=offer['executor_id'],

    )
    db.session.add(new_offer)
    db.session.commit()


@app.route("/users/", methods=['GET', 'POST'])
def users():
    user_list = []
    if request.method == 'GET':
        for i in User.query.all():
            user_list.append(i.to_dict())
        return jsonify(user_list)
    elif request.method == 'POST':
        data = json.loads(request.data)
        new_user = User(
            first_name=data['first_name'],
            last_name=data['last_name'],
            age=data['age'],
            email=data['email'],
            role=data['role'],
            phone=data['phone'],
        )
        db.session.add(new_user)
        db.session.commit()
        return 'Создан новый пользователь', 201


@app.route("/orders/", methods=['GET', 'POST'])
def orders():
    order_list = []
    if request.method == 'GET':
        for i in Order.query.all():
            order_list.append(i.to_dict())
        return jsonify(order_list)
    elif request.method == 'POST':
        data = json.loads(request.data)
        new_order = Order(
            name=data['name'],
            description=data['description'],
            start_date=data['start_date'],
            end_date=data['end_date'],
            address=data['address'],
            price=data['price'],
            customer_id=data['customer_id'],
            executor_id=data['executor_id'],
        )
        db.session.add(new_order)
        db.session.commit()
        return 'Создан новый заказ', 201


@app.route("/offers/", methods=['GET', 'POST'])
def offers():
    offer_list = []
    if request.method == 'GET':
        for i in Offer.query.all():
            offer_list.append(i.to_dict())
        return jsonify(offer_list)
    elif request.method == 'POST':
        data = json.loads(request.data)
        new_offer = Offer(
            order_id=data['order_id'],
            executor_id=data['executor_id'],
        )
        db.session.add(new_offer)
        db.session.commit()
        return 'Создано новое предложение', 201



@app.route('/users/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def user_id(id):
    if request.method == 'GET':
        try:
            user_id = User.query.get(id)
            return jsonify(user_id.to_dict())
        except:
            return f"Пользователь с id:{id} не найден"
    elif request.method == 'DELETE':
        user_del = User.query.get(id)
        db.session.delete(user_del)
        db.session.commit()
        return f"Пользователь{user_del} удален"
    elif request.method == 'PUT':
        data = json.loads(request.data)
        user_put = User.query.get(id)
        user_put.first_name = data['first_name']
        user_put.last_name = data['last_name']
        user_put.age = data['age']
        user_put.email = data['email']
        user_put.role = data['role']
        user_put.phone = data['phone']
        db.session.add(user_put)
        db.session.commit()
        return 'Пользователь исправлен', 201


@app.route('/orders/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def order_id(id):
    if request.method == 'GET':
        try:
            order_id = Order.query.get(id)
            return jsonify(order_id.to_dict())
        except:
            return f"Заказ с id:{id} не найден"
    elif request.method == 'DELETE':
        order_del = Order.query.get(id)
        db.session.delete(order_del)
        db.session.commit()
        return f"Заказ{order_del} удален"
    elif request.method == 'PUT':
        data = json.loads(request.data)
        order_put = Order.query.get(id)
        order_put.name = data['name']
        order_put.description = data['description']
        order_put.start_date = data['start_date']
        order_put.end_date = data['end_date']
        order_put.address = data['address']
        order_put.price = data['price']
        order_put.customer_id = data['customer_id']
        order_put.executor_id = data['executor_id']

        db.session.add(order_put)
        db.session.commit()
        return 'Заказ исправлен', 201


@app.route('/offers/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def offer_id(id):
    if request.method == 'GET':
        try:
            offer_id = Offer.query.get(id)
            return jsonify(offer_id.to_dict())
        except:
            return f"Предложение с id:{id} не найдено"
    elif request.method == 'DELETE':
        offer_del = Offer.query.get(id)
        db.session.delete(offer_del)
        db.session.commit()
        return f"Предложение{offer_del} удалено"
    elif request.method == 'PUT':
        data = json.loads(request.data)
        offer_put = Offer.query.get(id)
        offer_put.order_id = data['order_id']
        offer_put.executor_id = data['executor_id']

        db.session.add(offer_put)
        db.session.commit()
        return 'Предложение исправлено', 201




if __name__ == '__main__':
    app.run(debug=True)
