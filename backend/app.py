from datetime import datetime
from flask import Flask, request, json, jsonify, render_template
from flask_cors import CORS, cross_origin
from sqlalchemy.exc import IntegrityError

from config import Config
from . import main
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity

from flask import Flask
from models import db, Meeting

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meetings.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)



@main.route('/')
def index():
    # reset()
    # insert_all()
    return render_template('index.html')



@main.route('/postData', methods=['POST'])
@jwt_required()
def postData():

    user_id = get_jwt_identity()
    data = request.get_json()
    # TODO: add user_id

    new_rider = Rider(start=data['start'], end=data['end'], content=data['content'], time=datetime.utcnow(), user_id=user_id)
    db.session.add(new_rider)
    db.session.commit()
    return jsonify({"message": "Post Successful"})


@main.route('/testGetPost', methods=['GET', 'POST'])
def testGetPost():
    # get all post data from database
    # find the nearest posts for start and end position
    # start, end = form_start, form_end
    # data1 = distance.match(start, end)
    # print("Print Matched Data", data1)
    data1 = {
        "post_id": 1,
        "start": [47.625168, -122.337751],
        "end": [47.625168, -122.3378]
    }

    bodydata = request.json
    print(bodydata)
    if bodydata is None:
        print("no body data")

    return jsonify(data1)
    # return json.dumps(data)


@main.route('/json')
def send_json():
    data = {
        "name": "John",
        "age": 30,
        "city": "New York"
    }
    return json.dumps(data)


@main.route('/SignUp', methods=['POST', 'OPTIONS'])
@cross_origin()
def register():
    if request.method == 'OPTIONS':
        return jsonify({"message": "Prelight check successful"})
    data = request.json

    try:
        new_user = User(name=data['name'], email=data['email'], password_hash=generate_password_hash(data['password']),
                        age=data['age'], gender=data['gender'], city=data['city'])
        db.session.add(new_user)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"message": "Please Try Again"}), 401
    return jsonify({"message": "Sign Up Successful"}), 200

@main.route('/SignIn', methods=['POST', 'OPTIONS'])
@cross_origin()
def login():
    data = request.json

    user = User.query.filter_by(email=data['email']).first()
    if user:
        # 创建JWT令牌
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token, message="Sign In Successful")
    else:
        return jsonify({"message": "Wrong Username or Password"}), 401
