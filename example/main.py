import requests
import json
import os
from datetime import datetime

class DiscordWebhook:
    def __init__(self, WebhookUrl=None):
        """
        如果是單純生成Embed訊息，可以不用填入
        WebhookUrl : 要填入Webhook網址
        """
        self.WebhookUrl = WebhookUrl
        self.colors = {
            "red": 0xFF0000,
            "blue": 0x000079,
            "yellow": 0xF9F900,
            "white": 0xFDFFFF,
            "black": 0x000000
        }
        self.content = ""
        self.avatar_url = None
        self.username = None
        self.embed = {}
        self.file_paths = []
        self.image_path = {"image" : None}
        self.message_id = None

    def send_webhook__(self , arg = None):
        files = {}
        data = {
            "username": self.username,
            "avatar_url": self.avatar_url,
        }
        
        if self.content:
            data["content"] = self.content
            
        embeds = []
        if isinstance(arg, list):
            embeds = arg
        elif self.embed:
            embeds = [self.embed]

        if not data.get("content") and not embeds:
            raise ValueError("無法發送空消息，請設置content或有效的embeds")

        for embed in embeds:
            if "image_path" in embed:
                image_path = embed["image_path"]
                if os.path.isfile(image_path):
                    file_name = os.path.basename(image_path)
                    img_file = open(image_path, "rb")
                    files[file_name] = (file_name, img_file, "image/jpeg")
                    embed["image"] = {"url": f"attachment://{file_name}"}
                del embed["image_path"]

            if not isinstance(arg, list) and self.image_path['image']:
                if os.path.isfile(self.image_path['image']):
                    file_name = os.path.basename(self.image_path['image'])
                    img_file = open(self.image_path['image'], "rb")
                    files[file_name] = (file_name, img_file, "image/jpeg")
                    embed["image"] = {"url": f"attachment://{file_name}"}

        if self.file_paths:
            for file_path in self.file_paths:
                file_name = os.path.basename(file_path)
                file = open(file_path, "rb")
                files[file_name] = (file_name, file, "application/octet-stream")

        data["embeds"] = embeds
        
        response = requests.post(self.WebhookUrl+"?wait=true", data={"payload_json": json.dumps(data)}, files=files)

        for file in files.values():
            file[1].close()

        if response.status_code in [200, 204]:
            message_id = None
            if response.status_code == 200:
                try:
                    message_id = response.json().get('id')
                except ValueError:
                    pass
            return {"code": response.status_code, 'message': 'done', 'message_id': message_id}
        else:
            return {"code": response.status_code, 'message': response.text}

    def set_content(self, message):
        """
        功能 : 設置一般訊息
        message : 訊息
        """
        self.content = message

    def set_image(self, image):
        """
        功能 : 嵌入訊息_設置照片
        image : 檔案路徑或網址
        """
        if isinstance(image, str):
            if image.startswith("http"):
                self.embed["image"] = {"url": image}
            elif os.path.isfile(image):
                self.image_path['image'] = image 
                file_name = os.path.basename(image)
                self.embed["image"] = {"url": f"attachment://{file_name}"}
            else:
                raise ValueError("無效的圖片路徑或網址")
        else:
            raise TypeError("圖片參數必須是字串，表示本地路徑或網址")

    def set_files(self, file_paths):
        """
        功能 : 發送檔案
        file_paths : 檔案路徑
        """
        if isinstance(file_paths, list):
            for file_path in file_paths:
                if not os.path.isfile(file_path):
                    raise ValueError(f"檔案不存在: {file_path}")
            self.file_paths = file_paths
        else:
            raise TypeError("檔案參數必須是列表")

    def set_title(self, title):
        """
        功能 : 嵌入訊息_設置標題
        title : 訊息
        """
        self.embed["title"] = title

    def set_description(self, description):
        """
        功能 : 嵌入訊息_設置描述
        description : 訊息
        """
        self.embed["description"] = description

    def set_avatar(self, avatar_url):
        """
        功能 : 設置使用者頭貼
        avatar_url : 網址
        """
        self.avatar_url = avatar_url

    def set_username(self, username):
        """
        功能 : 設置使用者名稱
        username : 名字
        """
        self.username = username

    def set_color(self, color):
        """
        功能 : 嵌入訊息_設置顏色
        color : 名稱
        value : 訊息
        inline : 是否在同一行，但要使用bool
        """
        if color in self.colors:
            self.embed["color"] = self.colors[color]
        elif isinstance(color, str) and color.startswith('0x'):
            try:
                color_int = int(color, 16)
                if 0x000000 <= color_int <= 0xFFFFFF:
                    self.embed["color"] = color_int
                else:
                    raise ValueError("顏色值出錯瞜")
            except ValueError:
                raise ValueError("顏色格式出錯必須 0x000000")
        elif isinstance(color, int):
            if 0x000000 <= color <= 0xFFFFFF:
                self.embed["color"] = color
            else:
                raise ValueError("顏色值出錯瞜")
        else:
            raise TypeError("顏色無效請用16進位字串或整數")

    def set_value(self, name, value, inline=True):
        """
        功能 : 嵌入訊息_設置value
        name : 名稱
        value : 訊息
        inline : 是否在同一行，但要使用bool值
        """
        if "fields" not in self.embed.keys():
            self.embed["fields"] = []
        self.embed["fields"].append({"name": name, "value": value, "inline": inline})

    def set_footer(self, text, icon_url=None):
        """
        功能 : 嵌入訊息_設置頁尾
        text : 資訊
        icon_url : 填入網址
        """
        if "footer" not in self.embed.keys():
            self.embed["fields"] = {}
        self.embed["footer"]["text"] = text
        if icon_url:
            self.embed["footer"]["icon_url"] = icon_url

    def set_author(self, name, icon_url=None):
        """
        功能 : 嵌入訊息_設置作者訊息
        name : 名稱
        icon_url : 填入網址
        """
        if "author" not in self.embed.keys():
            self.embed["author"] = {}
        self.embed["author"]["name"] = name
        if icon_url:
            self.embed["author"]["icon_url"] = icon_url

    def set_thumbnail(self, url):
        """
        功能 : 嵌入訊息_設置縮圖
        url : 填入網址
        """
        self.embed["thumbnail"] = {"url": url}

    def set_timestamp(self, timestamp=None):
        """
        功能 : 嵌入訊息_設置時間戳
        timestamp : 填入時間戳 或 不填會給現在時間
        """
        if timestamp is not None:
            self.embed["timestamp"] = timestamp.isoformat()
        else:
            self.embed["timestamp"] = datetime.utcnow().isoformat()

    def send(self, arg = None):
        """
        功能 : 發送訊息
        arg : 可以發送多則embed訊息，但需使用 [] list 
        """
        return self.send_webhook__(arg)
    
    def dataembed(self):
        """
        功能 : 獲取Embed資訊
        """
        data = self.embed.copy()
        if self.image_path['image']:
            data["image_path"] = self.image_path['image']
        return data

    def delete(self, message_id):
        """
        功能 : 刪除訊息
        message_id : 訊息ID
        """
        url = f"{self.WebhookUrl}/messages/{message_id}"
        response = requests.delete(url)
        if response.status_code == 204:
            return {"message" : 'done'}
        else:
            return {"code" : response.status_code , "message" : response.text}
        
    def edit(self, message_id, new_content=None, new_embeds=None):
        """
        功能 : 編輯訊息
        message_id : 訊息ID
        new_content : 文字訊息
        new_embeds : 嵌入訊息，如果多則請記得使用 dataembed()調用資料 包成[]
        """
        url = f"{self.WebhookUrl}/messages/{message_id}"
        
        files = {}
        data = {
            "username": self.username,
            "avatar_url": self.avatar_url,
        }
        
        if self.content:
            data["content"] = self.content
            
        embeds = []
        if new_content:
            data["content"] = new_content

        if isinstance(new_embeds, list):
            embeds = new_embeds

        if not data.get("content") and not embeds:
            raise ValueError("無法發送空消息，請設置content或有效的embeds")

        for embed in embeds:
            if "image_path" in embed:
                image_path = embed["image_path"]
                if os.path.isfile(image_path):
                    file_name = os.path.basename(image_path)
                    img_file = open(image_path, "rb")
                    files[file_name] = (file_name, img_file, "image/jpeg")
                    embed["image"] = {"url": f"attachment://{file_name}"}
                del embed["image_path"]

            if not isinstance(new_embeds, list) and self.image_path['image']:
                if os.path.isfile(self.image_path['image']):
                    file_name = os.path.basename(self.image_path['image'])
                    img_file = open(self.image_path['image'], "rb")
                    files[file_name] = (file_name, img_file, "image/jpeg")
                    embed["image"] = {"url": f"attachment://{file_name}"}

        if self.file_paths:
            for file_path in self.file_paths:
                file_name = os.path.basename(file_path)
                file = open(file_path, "rb")
                files[file_name] = (file_name, file, "application/octet-stream")

        data["embeds"] = embeds

        response = requests.patch(url, data={"payload_json": json.dumps(data)}, files=files)

        for file in files.values():
            file[1].close()

        if response.status_code in [200, 204]:
            message_id = None
            if response.status_code == 200:
                try:
                    message_id = response.json().get('id')
                except ValueError:
                    pass
            return {"code": response.status_code, 'message': 'done', 'message_id': message_id}
        else:
            return {"code": response.status_code, 'message': response.text}
    

    def set_clear(self):
        """
        恢復初始狀態
        """
        self.content = ""
        self.avatar_url = None
        self.username = None
        self.embed = {}
        self.file_paths = []
        self.image_path = {"image" : None}
        self.message_id = None
        return {'message' : 'done'}