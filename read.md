## 必須使用套件

```py
pip install requests
```

## 套件參數

# 創建 Webhook:
```py
DiscordWebhook(填入Discord WebHook網址)
```

# 參數列表:

設定一般訊息
```py
set_content("") < 文字 
```

設置圖片
```py
set_image("") < 填入網址或檔案路徑
```

設置檔案
```py
set_files("") < 檔案路徑
```

設置使用者頭貼
```py
set_avatar("") < 網址
```

設置使用者名稱
```py
set_username("") < 文字
```

設置嵌入訊息 title
```py
set_title("") < 文字
```

設置嵌入訊息 description
```py
set_description("") < 文字
```

設置嵌入訊息 顏色
```py
set_color("") < 設置顏色
```

設置嵌入訊息 value
```py
set_value("name" , "value" , inline=True) < inline 一定要填入bool
```

設置嵌入訊息 footer
```py
set_footer("test", icon_url=None) < icon_url可不用填寫，但如要填寫請設置網址
```

設置嵌入訊息 author
```py
set_author("name" , icon_url=None) < icon_url可不用填寫，但如要填寫請設置網址
```

設置嵌入訊息 thumbnail
```py
set_thumbnail("") < 填入網址
```

設置嵌入訊息 時間
```py
set_timestamp("") < 填入時間戳 或 不填會給現在時間
```

獲取embed資料 < 用於發送多則embed訊息
```py
dataembed()
```

發送webhook訊息
```py
send() < 如果要傳多則embed 請使用[] 可參考下方範例
```

刪除訊息
```py
delete('message_id') < 只能刪除指定的webhook發送過的訊息
```

編輯訊息
```py
edit('message_id' , 'new_content' , [new_embeds]) < 只能更改指定的webhook發送過的訊息
預設 new_content 和 new_embeds 為 None
```

清楚所有設定
```py
set_clear() < 會回傳 {'message' : 'done'}
```

回傳值只有 send 和 embedssend 有格式為
```py
{"code" : code , "message" : message , message_id : message_id} 
```


## 範例1

# 發送單則embed

```py
webhook_url = "" < 填入 webhook網址
webhook = DiscordWebhook(webhook_url)
webhook.set_content("不好")
webhook.set_title("你好")
webhook.set_color("0xFF0000")
webhook.set_value("早安" , "午安")
webhook.set_value("早安" , "午安" , True)
webhool.set_timestamp()
webhook.set_author("author" , "https://m.media-amazon.com/images/I/51y8GUVKJoL.jpg")
webhook.send()
```

## 範例2

# 發送多則embed
```py
webhook_url = "" < 填入 webhook網址
webhook = DiscordWebhook(webhook_url)
webhook.set_title("你好")
webhook.set_files(['awa.txt' , 'AAA.png'])
webhook_data = webhook.dataembed()

webhook2 = DiscordWebhook()
webhook2.set_title("不好")
webhook2.set_image("www.png")
webhook_data2 = webhook2.dataembed()

webhook.send([webhook_data , webhook_data2])
```

## 範例三

# 編輯訊息
```py
webhook_url = "" < 填入 webhook網址
webhook = DiscordWebhook(webhook_url)
webhook.set_title("不好")
webhook.edit('訊息ID',new_embeds=[webhook.dataembed()])
```

# 刪除訊息
```py
webhook_url = "" < 填入 webhook網址
webhook = DiscordWebhook(webhook_url)
webhook.delete('訊息ID')
```