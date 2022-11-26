import praw
import re
from time import sleep
import os
from dotenv import load_dotenv
load_dotenv("bot.env")
key=os.getenv("key")
bekleme=1
reddit = praw.Reddit(
client_id=os.getenv("id"),
client_secret=os.getenv("secret"),
user_agent="<console:LOL:1.0>",
username=os.getenv("username"),
password=os.getenv("password"),
ratelimit_seconds=1200,
)
from cryptography.fernet import Fernet
import requests as r
from bs4 import BeautifulSoup as bs
from urllib.parse import quote_plus
from random import sample
cevap_ls=[]
k_defter=reddit.submission("x1krdg")
a_defter=reddit.submission("x1kv05")
d=False
fernet = Fernet(key)
def temizmi(s):
    if ";" in s:
        return False
    elif "|" in s:
        return False
    elif "&" in s:
        return False
    elif "rm" in s:
        return False
    elif "sudo" in s:
        return False
    else:
        return True


while True:
    try:
        ls=[]
        for l in reddit.inbox.mentions(limit=10):
            if l in cevap_ls:
                continue
            else:
                ls.append(l)
        if len(ls)==0:
            print("Bot çağrılmamış")
            sleep(bekleme)
        else:
            for x in ls:
                bakılmışmı=False
                post=x.submission
                post_id=post.id
                title=post.title
                title=title.replace(" ","_")
                title=title.replace('"',"_")
                title=title.replace("'","_")
                title=title.replace("|","")
                title=title.replace("&","")
                title=title.replace(";","")
                title=title.replace(":","")
                title=title.replace("#","")
                title=title.replace("/","")
                title=title.replace("<","")
                title=title.replace(">","")
                title=title.replace("?","")
                url=post.url
                id=url.split("/",3)[3]
                print(id)
                komut=""
                kalite=""
                txt=x.body.lower()

                if "end:" in x.body.lower():
                    a=txt.find("end:")
                    kriter=x.body[a+4:]
                    argüman=kriter.split(" ",1)[0]
                    if temizmi(argüman)==True:
                        pass
                    else:
                        x.reply("I found some 'dangerous' words/symbols in your command.Please remove them and call the bot again.")
                        cevap_ls.append(x)
                        continue
                    komut=komut+" -to {}".format(argüman)
                if "start:" in x.body.lower():
                    a=txt.find("start:")
                    kriter=x.body[a+6:]
                    argüman=kriter.split(" ",1)[0]
                    if temizmi(argüman)==True:
                        pass
                    else:
                        x.reply("I found some 'dangerous' words/symbols in your command.Please remove them and call the bot again.")
                        cevap_ls.append(x)
                        continue
                    komut=komut+" -ss {}".format(argüman)
                
                if "quality:" in x.body.lower():
                    a=txt.find("quality:")
                    kriter=x.body[a+8:]
                    argüman=kriter.split(" ",1)[0]
                    if temizmi(argüman)==True:
                        pass
                    else:
                        x.reply("I found some 'dangerous' words/symbols in your command.Please remove them and call the bot again.")
                        cevap_ls.append(x)
                        continue
                    kalite=argüman
                if "speed:" in x.body.lower():
                    a=txt.find("speed:")
                    kriter=x.body[a+6:]
                    argüman=kriter.split(" ",1)[0]
                    if temizmi(argüman)==True:
                        pass
                    else:
                        x.reply("I found some 'dangerous' words/symbols in your command.Please remove them and call the bot again.")
                        cevap_ls.append(x)
                        continue
                    komut=komut+" -vf 'setpts=(PTS-STARTPTS)/{}' -af atempo={}".format(argüman,argüman)
                if komut=="":
                    komut="None"
                else:
                    komut=fernet.encrypt(komut.encode())
                if kalite=="":
                    kalite="None"
                title=fernet.encrypt(title.encode())
                id=fernet.encrypt(id.encode())
                link="https://saveit.gq/d/{}/{}/{}/{}/{}/".format(id,komut,kalite,title,post_id)
                x.reply("#[Download]({})".format(link)+"\n\n"+"^([Donate](https://www.buymeacoffee.com/semihaslan)) "+" ^([Commands](https://saveit.gq))")
                try:
                    x.author.message(subject="Your Download Link",message="#[Download]({})".format(link)+"\n\n"+"[Donate](https://www.buymeacoffee.com/semihaslan) "+" [Commands](https://saveit.gq)")
                except:
                    pass
                print("Link dönüldü!")
                cevap_ls.append(x)
    except Exception as e:
        print("Hata dondü:{}".format(e))
        cevap_ls.append(x)
    if len(cevap_ls) > 100:
        for i in range(0,21):
            cevap_ls.pop(i) 