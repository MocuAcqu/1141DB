import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId

load_dotenv()

app = Flask(__name__)

app.config["MONGO_URI"] = os.getenv("MONGO_URI")
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

mongo = PyMongo(app)

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('profile'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # 從表單接收資料
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')

        if not name or not email or not password or not role:
            flash("所有欄位都是必填的！")
            return redirect(url_for('register'))

        # 檢查信箱是否已被註冊
        existing_user = mongo.db.users.find_one({'email': email})
        if existing_user:
            flash("這個信箱已經被註冊過了！")
            return redirect(url_for('register'))

        # 將密碼進行雜湊處理
        hashed_password = generate_password_hash(password)

        # 將新使用者資料存入資料庫
        mongo.db.users.insert_one({
            'name': name,
            'email': email,
            'password': hashed_password,
            'role': role
        })

        flash("註冊成功！請登入。")
        return redirect(url_for('login'))

    # 如果是 GET 請求，就顯示註冊頁面
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # 根據 email 尋找使用者
        user = mongo.db.users.find_one({'email': email})

        # 檢查使用者是否存在，且密碼是否正確
        if user and check_password_hash(user['password'], password):
            # 登入成功，將使用者資訊存入 session
            session['user_id'] = str(user['_id']) 
            session['name'] = user['name']
            session['role'] = user['role']
            flash("登入成功！")
            return redirect(url_for('profile'))
        else:
            flash("信箱或密碼錯誤！")
            return redirect(url_for('login'))

    # 如果是 GET 請求，就顯示登入頁面
    return render_template('login.html')

# 個人資料頁面 (需要登入才能訪問)
@app.route('/profile')
def profile():
    if 'user_id' not in session:
        flash("請先登入！")
        return redirect(url_for('login'))

    # 根據不同身分，從資料庫讀取不同的活動資料
    if session['role'] == 'organizer':
        user_id_obj = ObjectId(session['user_id'])
        my_events = list(mongo.db.events.find({'organizer_id': user_id_obj}))
        return render_template('profile.html', my_events=my_events)
    else:
        all_events = list(mongo.db.events.find({}))
        return render_template('profile.html', all_events=all_events)

@app.route('/logout', methods=['GET'])
def show_logout_page():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('logout.html')

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    flash("您已成功登出。")
    return redirect(url_for('login'))

@app.route('/create_event', methods=['POST'])
def create_event():
    if 'user_id' not in session or session.get('role') != 'organizer':
        flash("權限不足！")
        return redirect(url_for('profile'))

    event_name = request.form.get('event_name')
    description = request.form.get('description')
    event_time = request.form.get('event_time')
    location = request.form.get('location')

    if not all([event_name, description, event_time, location]):
        flash("所有欄位都是必填的！")
        return redirect(url_for('profile'))

    mongo.db.events.insert_one({
        'organizer_id': ObjectId(session['user_id']),
        'organizer_name': session['name'],
        'name': event_name,
        'description': description,
        'time': event_time,
        'location': location,
        'current_number': 0,
        'queue': []
    })

    flash("活動建立成功！")
    return redirect(url_for('profile'))

if __name__ == '__main__':
    app.run(debug=True)