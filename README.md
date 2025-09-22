# 1141 資料庫系統
- 姓名: 邱鈺婷
- 學號: 41271124H
- 系級: 科技116

# 課程筆記
## [實作程式碼連結](https://github.com/MocuAcqu/1141DB/tree/main/ex.1)
## 實作一 + 作業一
<img src="https://github.com/MocuAcqu/1141DB/blob/main/readme_images/ex.1_1.png" width="500">

- 安裝環境: Flask、MySQL
- 安裝資訊可參考: 安裝 [Flask](https://flask.palletsprojects.com/en/stable/installation/#install-flask)、[MySQL](https://dev.mysql.com/downloads/installer/)
- 實作說明
  
  課堂實作希望嘗試將 Flask 和 MySQL 結合。我製作了一個簡易「留言板」，其中，實際操作一次資料庫 table 建立的過程，並串接到 flask。用簡易的前端介面，讓使用者可以輸入「姓名」、「留言內容」，並從資料庫抓取資料顯示在介面下方。

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

---

## 實作二

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

---

## 實作三 + 作業二
作業介紹: 完成 CRUD
基於前面的實作，我增加了 Update 修改(更新)資料的功能，以及 Delete 刪除資料的功能。同時，我也增加了 CSS 去美化這個留言板。
|<img src="https://github.com/MocuAcqu/1141DB/blob/main/readme_images/ex.1_5.png" width="500">|<img src="https://github.com/MocuAcqu/1141DB/blob/main/readme_images/ex.1_6.png" width="500">|
|:--:|:--:|

