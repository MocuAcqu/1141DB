from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# --- MySQL 設定 ---
# 請根據你的 MySQL 設定修改以下資訊
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
    # 如果是 POST 請求，表示使用者提交了表單
    if request.method == 'POST':
        # 從表單中獲取資料
        userDetails = request.form
        username = userDetails['username']
        content = userDetails['content']

        # 建立一個 cursor 物件來執行 SQL 指令
        cur = mysql.connection.cursor()
        
        # 執行 INSERT 指令將新留言存入資料庫
        # 注意：使用 %s 作為佔位符可以防止 SQL Injection 攻擊
        cur.execute("INSERT INTO messages(username, content) VALUES(%s, %s)", (username, content))
        
        # 提交變更到資料庫
        mysql.connection.commit()
        
        # 關閉 cursor
        cur.close()
        
        # 完成後重新導向回主頁，這樣可以避免重新整理時重複提交表單
        return redirect(url_for('index'))

    # 如果是 GET 請求，就從資料庫讀取所有留言並顯示
    cur = mysql.connection.cursor()
    # 執行 SELECT 指令來抓取所有留言，並依照 id 降序排列 (最新的在最上面)
    cur.execute("SELECT * FROM messages ORDER BY id DESC")
    messages = cur.fetchall()
    cur.close()

    # 將留言資料傳遞給 index.html 模板並渲染頁面
    return render_template('index.html', messages=messages)

# 啟動伺服器
if __name__ == '__main__':
    app.run(debug=True)