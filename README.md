# 1141 資料庫系統
- 姓名: 邱鈺婷
- 學號: 41271124H
- 系級: 科技116

# 課程筆記
## 快速連結區
1. [MySQL 實作程式碼連結](https://github.com/MocuAcqu/1141DB/tree/main/ex.1)
2. [Mongodb 實作程式碼連結](https://github.com/MocuAcqu/1141DB/tree/main/ex.2)
3. [作業一 - 影片解說](https://youtu.be/GURVYD-b9EQ?si=pIod6bg15WtA4c0h)
4. [作業二 - 影片解說](https://www.youtube.com/watch?v=av6wAkeqLvA)

<details>
<summary>實作一 + 作業一</summary>

## 一、實作一 + 作業一
<img src="https://github.com/MocuAcqu/1141DB/blob/main/readme_images/ex.1_1.png" width="500">

- 安裝環境: Flask、MySQL
- 安裝資訊可參考: 安裝 [Flask](https://flask.palletsprojects.com/en/stable/installation/#install-flask)、[MySQL](https://dev.mysql.com/downloads/installer/)
- 實作說明
  
  課堂實作希望嘗試將 Flask 和 MySQL 結合。我製作了一個簡易「留言板」，其中，實際操作一次資料庫 table 建立的過程，並串接到 flask。用簡易的前端介面，讓使用者可以輸入「姓名」、「留言內容」，並從資料庫抓取資料顯示在介面下方。
  
  - 重點安裝: `from flask_mysqldb import MySQL`
  
- 作業要求
  1. Create a table in MySQL (CREATE TABLE).
  2. Build an Insert web page that allows you to input a record from the web.
  3. Ensure that the inserted data is visible in the MySQL database.

- 作業影片說明: https://youtu.be/GURVYD-b9EQ?si=pIod6bg15WtA4c0h

重要程式碼 (連接 Flask + MySQL 的關鍵)
```
# 主頁路由，同時處理顯示留言 (GET) 和新增留言 (POST)
@app.route('/', methods=['GET', 'POST'])
def index():
    if 'user_id' not in session:
        flash('請先登入才能查看或發表留言', 'warning')
        return redirect(url_for('login'))

    #新增留言
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
    
    # 在網頁上顯示留言
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT m.id, m.content, m.created_at, u.username, u.id AS user_id
        FROM messages AS m
        JOIN users AS u ON m.user_id = u.id
        ORDER BY m.created_at DESC
    """)
    messages = cur.fetchall()
    cur.close()

    return render_template('index.html', messages=messages)

```
- 資料結構

  ```
  my-flask-app/
  ├── app.py   
  └── templates/
      └── index.html 
  ```
- 啟動方式
  ```
  .venv\Scripts\activate
  python app.py
  ```

</details>

<details>
<summary>實作二</summary>
  
## 二、實作二

|<img src="https://github.com/MocuAcqu/1141DB/blob/main/readme_images/ex.1_2.png" width="500">|<img src="https://github.com/MocuAcqu/1141DB/blob/main/readme_images/ex.1_3.png" width="500">|<img src="https://github.com/MocuAcqu/1141DB/blob/main/readme_images/ex.1_4.png" width="500">|
|:--:|:--:|:--:|

- 實作說明
  
  接續實作一，這次把重點放在 `Use SELECT with a conditional filter, sort, and join. (Read)` ，我延伸製作了使用者登入/註冊介面。

- 資料結構
```
my-flask-app/
├── app.py
└── templates/
    ├── index.html     # 主頁 (顯示留言)
    ├── login.html     # 登入頁面
    ├── register.html  # 註冊頁面
    └── layout.html 
```
</details>

<details>
<summary>實作三 + 作業二</summary>
  
## 三、實作三 + 作業二
|<img src="https://github.com/MocuAcqu/1141DB/blob/main/readme_images/ex.1_5.png" width="500">|<img src="https://github.com/MocuAcqu/1141DB/blob/main/readme_images/ex.1_6.png" width="500">|
|:--:|:--:|

- 實作說明: 完成 CRUD

  基於前面的實作，我增加了 Update 修改(更新)資料的功能，以及 Delete 刪除資料的功能。同時，我也增加了 CSS 去美化這個留言板。並且為了使用到三個 table，我增加了劉由「回覆」功能，增加一個 comments 的 table 去紀錄使用者的回覆。

- 作業要求:
  1. Connecting your Python Flask application to MySQL
  2. Adding data to the MySQL database
  3. Draw an ERD model that includes three tables
  4. Ensure that these three tables contain at least one type of JOIN operation
  5. Implement full CRUD functionality (Create, Read, Update, Delete) for the tables.
     
- 解說影片: https://www.youtube.com/watch?v=av6wAkeqLvA
- 資料結構
```
my-flask-app/
├── static/
│   └── css/
│       └── style.css 
├── templates/
│   ├── index.html
│   ├── layout.html
│   ├── login.html
│   ├── register.html
│   └── profile.html
└── app.py
```

---

- ERD
<img src="https://github.com/MocuAcqu/1141DB/blob/main/readme_images/ex.1_ERD.png" width="500">

1. users: 代表註冊此系統的使用者。每一筆記錄就是一個獨立的使用者帳號。
    - id: 主鍵 (Primary Key, PK)，用底線標示。它是每個使用者的唯一識別碼，絕不重複。
    - username, email, password: 使用者的基本資料。
    - registered_at: 記錄使用者註冊時間的時間戳。
    
2. messages: 代表使用者發表的主留言。每一筆記錄就是一則獨立的留言。
    - id: 主鍵 (PK)，每則主留言的唯一識別碼。
    - content, created_at: 留言的內容和發表時間。
    - fk: user_id: 外鍵 (Foreign Key, FK)。這個欄位儲存了發表此留言的使用者 ID，它參照到 users 表的 id 欄位。

3. comments: 代表針對主留言的回覆。每一筆記錄就是一則回覆。
    - id: 主鍵 (PK)，每則回覆的唯一識別碼。
    - content, created_at: 回覆的內容和發表時間。
    - fk: user_id: 外鍵 (FK)。記錄了發表此回覆的使用者 ID，參照到 users 表的 id。
    - fk: message_id: 外鍵 (FK)。記錄了這則回覆是針對哪一則主留言的，參照到 messages 表的 id。

---

- CRUD 對應內容
  #### 【C - Create (新增)】
  - 使用者註冊 (/register)：將新的使用者名稱、Email 和密碼 INSERT 到 users 表中。
  - 發表新留言 (主頁 /)：將留言內容和當前登入者的 user_id INSERT 到 messages 表中。
  - 新增回覆 (/add_comment)：將留言內容、被留言的 message_id、user_id INSERT 到 comments 表中。
  
  #### 【R - Read (讀取)】
  - 顯示所有留言 (主頁 /)：首先 SELECT 所有留言，並 JOIN users 表來獲得留言者的 username，ORDER BY 發表時間來顯示。再來 SELECT 所有回覆，JOIN users 表來獲得留言者的 username。
  - 登入驗證 (/login)：SELECT 使用者資料 WHERE username 符合輸入值，以比對密碼。
  - 顯示個人資料頁 (/profile)：讀取當前使用者的名稱與 email。
  
  #### 【U - Update (更新)】
  - 修改個人資料 (/profile)：UPDATE users 表，SET 新的 username 和 email，WHERE id 等於當前登入者的 user_id。
  
  #### 【D - Delete (刪除)】
  - 刪除自己的留言 (/delete_message/...)：DELETE FROM messages WHERE id 等於指定的 message_id，並且在執行前先驗證操作者是否為留言者。

</details>

<details>
<summary>實作四</summary>
  
  ## 四、實作四
  <img src="https://github.com/MocuAcqu/1141DB/blob/main/readme_images/ex.2_1.png" width="500">

  
- 安裝環境: Mongodb
- 安裝資訊可參考: [Mongodb](https://www.mongodb.com/try/download/community)
- 實作說明:
  
   課堂實作希望嘗試將 Flask 和 Mongodb 結合。我製作了一個「活動排隊系統」，首先在使用者登入/註冊的部分，除了基本資訊，還需要選擇身分是參加者、活動方，如果使用者是活動方，可以輸入要開放排對等號的活動，包含(活動名稱、簡述、時間、地點)，該活動除了會顯示在註冊活動的活動方介面，也會顯示在所有參加者的介面。

  - 重點安裝: `pip install Flask Flask-PyMongo`
- 啟動方式:
  ```
  venv\Scripts\activate
  python app.py
  ```
</details>

<details>
<summary>實作五 + 作業三</summary>
  
 ## 五、實作五 + 作業三
  
  <img src="https://github.com/MocuAcqu/1141DB/blob/main/readme_images/ex.2_2.png" width="500">

- 實作說明:
  
   基於活動方登記活動的部分，我們藉由 `insert_many()` 去增加「批次新增」、「csv 新增」的功能。並使用 render 部屬上雲端，獲得一個可公開存取的線上連結。

  - render 操作可參考: https://render.com/docs/deploy-mongodb

- 作業要求:
  1. Build a New Database with a User Interface for Multiple Data Entry
  2. 部屬上 Render

- 解說影片: (預期放影片)
- Render 部屬連結: https://one141db-event-queue.onrender.com
- 資料結構
```
my-flask-app/
├── templates/
│   ├── base.html
│   ├── logout.html
│   ├── login.html
│   ├── register.html
│   └── profile.html
└── app.py
```
</details>
