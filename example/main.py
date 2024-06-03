import requests
import json
import time
from datetime import datetime 

class DiscordWebhook:
    def __init__(self, WebhookUrl = None):
        self.WebhookUrl = WebhookUrl
        self.colors = {
            "red": 0xFF0000,
            "blue": 0x000079,
            "yellow": 0xF9F900,
            "white": 0xFDFFFF,
            "black": 0x000000
        }
        self.content = None
        self.avatar_url = None
        self.username = None
        self.embed = {"fields": [] , "footer" : {} , "author" : {}}

    def __send_webhook__(self):
        headers = {
            "Content-Type": "application/json"
        }

        senddata = {"username" : self.username,
                   "avatar_url" : self.avatar_url,
                   "embeds": [self.embed]}
        
        if self.content:
            senddata["content"] = self.content

        response = requests.post(self.WebhookUrl, headers=headers, data=json.dumps(senddata))
        
        if response.status_code == 204:
            return {"code" : response.status_code , 'message' : 'done'}
        else:
            return {"code" : response.status_code , 'message' : {response.text}}
    
    def dataembed(self):
        return self.embed

    def set_content(self, message):
        self.content = message

    def set_image(self, url):
        self.embed["image"] = {"url": url}

    def set_title(self, title):
        self.embed["title"] = title

    def set_description(self, description):
        self.embed["description"] = description

    def set_avatar(self, avatar_url):
        self.avatar_url = avatar_url

    def set_username(self, username):
        self.username = username

    def set_color(self, color):
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

    def set_value(self, name, value, inline=False):
        self.embed["fields"].append({"name" : name , "value" : value , "inline" : inline})

    def set_footer(self, text, icon_url=None):
        self.embed["footer"]["text"] = text
        if icon_url:
            self.embed["footer"]["icon_url"] = icon_url

    def set_author(self, name, icon_url=None):
        self.embed["author"]["name"] = name
        if icon_url:
            self.embed["author"]["icon_url"] = icon_url

    def set_thumbnail(self, url):
        self.embed["thumbnail"] = {"url": url}

    def set_timestamp(self, timestamp=None):
        if timestamp is not None:
            self.embed["timestamp"] = timestamp.isoformat()
        else:
            self.embed["timestamp"] = datetime.utcnow().isoformat()

    def send(self):
        return self.__send_webhook__()

    def embedssend(self , lists):
        if not isinstance(lists, list):
            raise TypeError("傳入參數型態必須是List")

        if (len(lists) < 11):
            raise ValueError("傳入的List數量不能超過10")

        headers = {
            "Content-Type": "application/json"
        }

        senddata = {"username" : self.username,
                   "avatar_url" : self.avatar_url,
                   "embeds": lists}
        
        if self.content:
            senddata["content"] = self.content

        response = requests.post(self.WebhookUrl, headers=headers, data=json.dumps(senddata))
        
        if response.status_code == 204:
            return {"code" : response.status_code , 'message' : 'done'}
        else:
            return {"code" : response.status_code , 'message' : {response.text}}