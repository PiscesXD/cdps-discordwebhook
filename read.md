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
set_content("") 
```

設定title
```py
set_title("")
```

設定description
```py
set_description("")
```

設定color
```py
set_color("")
```

設定image
```py
set_image("") < 填入圖片網址
```

設定avatar
```py
set_avatar("") < 填入圖片網址
```

設定username
```py
set_username("")
```

設定value
```py
set_value(name="" , value="" , inline=bool) < bool預設False
```

設定footer
```py
set_footer(test="",icon_url="") < icon_url 圖片網址
```

設定author
```py
set_author(test="",icon_url="") < icon_url 圖片網址
```

設定thumbnail
```py
set_thumbnail("")< 填入圖片網址
```

設定timestamp
```py
set_timestamp() < 可填寫 也可不填寫 請記住要使用utc來表示
```

發送訊息
```py
send()
```

獲取Embed資料 < 用於發送多則embed
```py
dataembed()
```

發送多則embed
```py
embedssend([])
```

回傳值只有 send 和 embedssend 有格式為
```py
{"code" : code , "message" : message} 
```

## 範例1

# 發送單則embed

```py
webhook_url = ""
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
webhook_url = ""
webhook = DiscordWebhook(webhook_url)
webhook.set_title("你好")

webhook_data = webhook.dataembed()

webhook2 = DiscordWebhook()
webhook2.set_title("不好")
webhook_data2 = webhook.dataembed()

webhook.embedssend([a , b])
```
