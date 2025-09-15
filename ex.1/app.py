from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
# --- MySQL 設定 ---
# 請根據你的 MySQL 設定修改以下資訊
app.config['SECRET_KEY'] = 'a_really_long_and_random_string_for_security_!@#$%' 
app.config['MYSQL_HOST'] = 'localhost'         # MySQL 伺服器主機
app.config['MYSQL_USER'] = 'root'              # MySQL 使用者名稱
app.config['MYSQL_PASSWORD'] = '#Vul3wu0g3' # 你的 MySQL 密碼
app.config['MYSQL_DB'] = 'flask_message_board' # 你要連接的資料庫名稱
app.config['MYSQL_CURSORCLASS'] = 'DictCursor' # 設定 cursor 回傳的資料為字典形式

# 初始化 MySQL
mysql = MySQL(app)

# --- 路由 (Routes) ---

# 主頁路由，同時處理顯示留言 (GET) 和新增留言 (POST)
@app.route('/', methods=['GET', 'POST'])
def index():
    # 檢查使用者是否登入
    if 'user_id' not in session:
        flash('請先登入才能查看或發表留言', 'warning')
        return redirect(url_for('login'))

    if request.method == 'POST':
        content = request.form['content']
        user_id = session['user_id'] # 從 session 獲取當前登入的使用者 ID

        if not content:
            flash('留言內容不可為空！', 'danger')
        else:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO messages(content, user_id) VALUES(%s, %s)", (content, user_id))
            mysql.connection.commit()
            cur.close()
            flash('留言成功！', 'success')
        
        return redirect(url_for('index'))
    
    # 使用 JOIN 查詢來獲取留言和對應的使用者名稱
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT m.content, m.created_at, u.username
        FROM messages AS m
        JOIN users AS u ON m.user_id = u.id
        ORDER BY m.created_at DESC
    """)
    messages = cur.fetchall()
    cur.close()

    return render_template('index.html', messages=messages)

# 註冊頁面
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # 將密碼進行雜湊處理，絕不儲存明文密碼！
        hashed_password = generate_password_hash(password)

        cur = mysql.connection.cursor()
        # 檢查使用者名稱或 email 是否已存在
        cur.execute("SELECT * FROM users WHERE username = %s OR email = %s", (username, email))
        user = cur.fetchone()

        if user:
            flash('使用者名稱或 Email 已被註冊！', 'danger')
        else:
            cur.execute("INSERT INTO users(username, email, password) VALUES(%s, %s, %s)", 
                        (username, email, hashed_password))
            mysql.connection.commit()
            flash('註冊成功！請登入。', 'success')
            return redirect(url_for('login'))
        
        cur.close()

    return render_template('register.html')

# 登入頁面
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        cur.close()

        if user and check_password_hash(user['password'], password):
            # 登入成功，將使用者資訊存入 session
            session['loggedin'] = True
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash('登入成功！', 'success')
            return redirect(url_for('index'))
        else:
            flash('使用者名稱或密碼錯誤！', 'danger')

    return render_template('login.html')

# 登出
@app.route('/logout')
def logout():
    # 清除 session 中的使用者資訊
    session.pop('loggedin', None)
    session.pop('user_id', None)
    session.pop('username', None)
    flash('你已成功登出。', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)