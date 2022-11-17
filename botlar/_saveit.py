
import praw
import re
from time import sleep
bekleme=1
reddit = praw.Reddit(
client_id="tFMaWlhwtIKUSjFGDtCwXg",
client_secret="d5DhwvIlElddiw1wnGJe2rd0jPuTQQ",
user_agent="<console:LOL:1.0>",
username="_saveit",
password="Ahmetse12",
ratelimit_seconds=1200,
)
#TODO:Reply #1 ve Mesajı ayır,yorum kaldırılsa mesaj at.
key = "TM9659kT1RReo022ha4pSWTwSOZ96o2jD0QEeC-WY7w="
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
        #for z in reddit.inbox.comment_replies(limit=25):
           # if z in yorum_ls:
               # continue
            #txt=z.body.lower()
            #print(txt)
            #if "good bot" in txt:
               # z.reply("teşekkürler")
               # d=True
               # print("Cevap dönüldü")
               # yorum_ls.append(z)
            #if d==False:
               # for f in sxtng:
                  #  if f in txt:
                      #  z.reply("hayır")
                        #d=True
                        #yorum_ls.append(z)
                        #print("Cevap dönüldü")
                        #break
            #if d==False:
               # for f in niye:
                   # if f in txt:
                       # cevap=sample(niye_c, 1)[0]
                        #z.reply(cevap)
                      #  d#=True
                        #print("Cevap dönüldü")
                        #yorum_ls.append(z)
                        #break
            #if d==False:
               # cevap=sample(niye_c, 1)[0]
                #z.reply(cevap)
                #print("Cevap dönüldü")
                #yorum_ls.append(z)
           # txt=''
            #kelime=[]
            #d=False

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
                link="https://saveit.gq/d/{}/{}/{}/{}/".format(id,komut,kalite,title)
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
    

                
        '''
        for z in dön_ls:
            if z.banned_by==None:
                pass
            else:
                if z in ban_ls:
                    pass
                else:
                    nu=dön_ls.index(z)
                    y=cevap_ls[nu]
                    kişi=kayıt_kişi[nu]
                    p=kayıt_post[nu]
                    sub=kayıt_sub[nu]
                    post=y.submission
                    main_url= main_url="https://reddit.com{}".format(post.permalink)
                    url=quote_plus(main_url)
                    resp=r.get("https://redditsave.com/info?url={}".format(url))
                    html=resp.content
                    soup=bs(html,"html.parser")
                    lnks=soup.find_all("a",{"class":"downloadbutton"})
                    if len(lnks)==0:
                        continue
                    elif len(lnks)==1:
                        sonuç=lnks[0].get("href")
                        if "https://" in sonuç:
                            pass
                        else:
                            sonuç="https://redditsave.com{}".format(sonuç)
                        dön=a_defter.reply("u/{} | {} | {}".format(kişi,p.sub)+"\n\n"+"#[İNDİR]({})".format(sonuç)+"\n\n"+"^(Resim indirmek istiyorsanız yeni sekmede Ctrl+S veya sağ click/uzun süre basktıktan sonra resmi farklı kaydet/resmi indir e basın)"+"\n\n"+"[Bağış](https://www.buymeacoffee.com/semihaslan)")
                        print("Link düzgün dönüldü!")
                        ban_ls.append(z)

                    else:
                        sonuç_hd=lnks[0].get("href")
                        sonuç_sd=lnks[1].get("href")
                        if "https://" in sonuç_hd:
                            pass
                        else:
                            sonuç_hd="https://redditsave.com{}".format(sonuç_hd)
                        if "https://" in sonuç_sd:
                            pass
                        else:
                            sonuç_sd="https://redditsave.com{}".format(sonuç_sd)
                        dön=a_.reply("u/{} | {} | {}".format(kişi,p.sub)+"\n\n"+"#[HD İNDİR]({})".format(sonuç_hd)+"\n\n"+"\n\n"+"#[SD İNDİR]({})".format(sonuç_sd)+"\n\n"+"^(Resim indirmek istiyorsanız yeni sekmede Ctrl+S veya sağ click/uzun süre basktıktan sonra resmi farklı kaydet/resmi indir e basın)"+"\n\n"+"[Bağış](https://www.buymeacoffee.com/semihaslan)")
                        print("Link düzgün dönüldü!")
                        ban_ls.append(z)
                   '''