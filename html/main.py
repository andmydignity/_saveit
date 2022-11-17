import re
from crypt import methods
from fileinput import filename
from requests import get as g
from unicodedata import name
from os import system as s
import os
from flask import Flask, current_app,render_template,redirect,request, send_file, send_from_directory
from cryptography.fernet import Fernet
import random 
import string
from bs4 import BeautifulSoup as bs
import requests as r
from os.path import isfile

key = "TM9659kT1RReo022ha4pSWTwSOZ96o2jD0QEeC-WY7w="
fernet = Fernet(key)
site=Flask(__name__)
def deEmojify(text):
    regrex_pattern = re.compile(pattern = "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags = re.UNICODE)
    return regrex_pattern.sub(r'',text)
def temizmi(s):
    if ";" in s:
        return False
    elif "|" in s:
        return False
    elif "&" in s:
        return False
    else:
        return True
#HTML:Sayfa başına nav bar ekle.Ordan 'How to Use' tıklayınca sayfadaki ilgili bölümü göstersin mesela.✔
#HTML:'Command' kısmında bir <code> eksik kalmış✔
#HTML:Küçük düzeltmeler✔
#HTML:Mobil versiyon yap (Responsive)✔
#HTML:FAQ yaz✔
#HTML:Contact yaz✔
#HTML:Download page'den ana sayfasaya dönülebilsin.✔
#HTML:404 ve hata sitesi✔
#PY:Hız komudu çalışmıyor.✔
#PY:RedGIFS desteği(Direk RedGIFS se yallah)
#PY:Resim indirmede indirme başlamıyor(Valla banene)
#PY:GIF te sıkıntı var.(Valla banane)
#Bot:start ve end birlikte kullanıldığındaki uyumsuzluğu çöz✔
#Bot:Komutlar için siteye yönlendir.✔
#Bot ve PY:İndirilecek şeyin başına başlık koy.✔
@site.route("/",methods=["GET","POST"])
def ana():
    return render_template("main.html")
@site.route("/d/<link>/<komut>/<quality>/",methods=["GET","POST"])
def indir(link,komut,quality):
    try:
        link=bytes(link,"utf-8")
        link=link[2:]
        link=fernet.decrypt(link).decode()
    except:
        link=link.decode("utf-8")
        if temizmi(link)==False:
            link="Nice try buddy."
        #Link temizlemesi yap komutlara karşın✔(Zaten korumalıymış)
    test=[]
    uz = 10
    has_audio=True
    if komut=="None":
        komut=""
    else:
        komut=bytes(komut,"utf-8")
        komut=komut[2:]
        komut=fernet.decrypt(komut).decode("utf-8")
    if quality!="None":
        quality=bytes(quality,"utf-8")
        quality=quality[2:]
        quality=fernet.decrypt(quality).decode("utf-8")
        if "a" in quality:
            has_audio=False
            quality=quality[-1]
            test.append(quality)
    normal="ffmpeg -i files/{}.mp4 -i files/{}.mp4 {} -c copy files/{}.mp4"
    no_audio="ffmpeg -i files/{}.mp4 {} -c copy files/{}.mp4"
    speed="ffmpeg -i files/{}.mp4 -i files/{}.mp4 {} files/{}.mp4"
    speed_wa="ffmpeg -i files/{}.mp4 {} 'files/{}.mp4'"
    if link.startswith("watch/")==True:
        link="https://www.redgifs.com/{}".format(link)
        return render_template("reggifs.html",l=link)
    if link.endswith(".gif")==True:
        link="https://i.redd.it/{}".format(link)
        return render_template("special.html",l=link)
    elif link.endswith(".jpg")==True:
        link="https://i.redd.it/{}".format(link)
        return render_template("special.html",l=link)
    elif link.endswith(".jpg")==True:
        link="https://i.redd.it/{}".format(link)
        return render_template("special.html",l=link)
    elif link.endswith(".png")==True:
        link="https://i.redd.it/{}".format(link)
        return render_template("special.html",l=link)   
    elif link.endswith(".gifv")==True:
        link="https://i.imgur.com/{}".format(link)
        return render_template("special.html",l=link)
    else:
        link="https://v.redd.it/{}".format(link)
        test_m=["1080","720","480","360","240","220"]
        for i in test_m:
            test.append(i)
        dw=None
        for i in test:
            status=os.popen("curl -I {}/DASH_{}.mp4".format(link,i)).read()
            print(status)
            if status.startswith("HTTP/2 403")==False and status.startswith("HTTP/1.1 403")==False and status.startswith("HTTP/1 403")==False and status.startswith("HTTP/0.9 403")==False:
                if has_audio==True:
                    status=os.popen("curl -I {}/DASH_audio.mp4".format(link)).read()
                    if status.startswith("HTTP/2 403")==False and status.startswith("HTTP/1.1 403")==False and status.startswith("HTTP/1 403")==False and status.startswith("HTTP/0.9 403")==False:
                        has_audio=True
                    else:
                        has_audio=False
                    print("{}/DASH_{}.mp4".format(link,i))
                    dw = ''.join(random.choices(string.ascii_letters+string.digits, k = uz))    
                    au = ''.join(random.choices(string.ascii_letters+string.digits, k = uz))
                    çk = ''.join(random.choices(string.ascii_letters+string.digits, k = uz))
                    if has_audio==True:
                        s("curl {}/DASH_{}.mp4 -o files/{}.mp4".format(link,i,dw))
                        s("curl {}/DASH_audio.mp4 -o files/{}.mp4".format(link,au))
                        if "-vf" in komut:
                            try:
                                s(speed.format(dw,au,komut,çk))
                            except:
                                s(normal.format(dw,au,"",çk))
                        else:    
                            try:
                                s(normal.format(dw,au,komut,çk))
                            except:
                                s(normal.format(dw,au,"",çk))
                else:
                    if  komut=="":
                        return render_template("special.html",l="{}/DASH_{}.mp4".format(link,i))
                        
                    else:
                        s("curl {}/DASH_{}.mp4 -o files/{}.mp4".format(link,i,dw))
                        if "-vf" in komut:
                            try:
                                s(speed_wa.format(dw,komut,çk))
                            except:
                                s(no_audio.format(dw,"",çk))    
                        try:
                            s(no_audio.format(dw,komut,çk))
                        except:
                            s(no_audio.format(dw,"",çk))
                break
            else:
                print("olmadı")
                continue
        if dw==None:
            return render_template("hata.html",id=link)
        else:
            return render_template("download.html",l="{}.mp4".format(çk))
@site.route("/d/<link>/<komut>/<quality>/<title>/",methods=["GET","POST"])
def indirt(link,komut,quality,title):
    title=bytes(title,"utf-8")
    title=title[2:]
    title=fernet.decrypt(title).decode()
    title=title.replace("|","")
    title=title.replace("&","")
    title=title.replace(";","")
    title=title.replace(":","")
    title=title.replace("#","")
    title=title.replace("/","")
    title=title.replace("<","")
    title=title.replace(">","")
    title=title.replace("?","")

    title=deEmojify(title)


    try:
        link=bytes(link,"utf-8")
        link=link[2:]
        link=fernet.decrypt(link).decode()
    except:
        link=link.decode("utf-8")
        if temizmi(link)==False:
            link="Nice try buddy."
        #Link temizlemesi yap komutlara karşın✔(Zaten korumalıymış)
    test=[]
    uz = 10
    has_audio=True
    if komut=="None":
        komut=""
    else:
        komut=bytes(komut,"utf-8")
        komut=komut[2:]
        komut=fernet.decrypt(komut).decode("utf-8")
    if quality!="None":
        quality=bytes(quality,"utf-8")
        quality=quality[2:]
        quality=fernet.decrypt(quality).decode("utf-8")
        if "a" in quality:
            has_audio=False
            quality=quality[-1]
            test.append(quality)
    if quality=="None" and has_audio==True and komut=="" and isfile("files/{}_None.mp4".format(title))==True:
        print("Zaten olan dosya gönderiliyor...")
        try:
            return render_template("download.html",l="{}_None.mp4".format(title))
        except:
            normal="ffmpeg -i files/{}.mp4 -i files/{}.mp4 {} -c copy 'files/{}.mp4'"
        no_audio="ffmpeg -i files/{}.mp4 {} -c copy 'files/{}.mp4'"
        speed="ffmpeg -i files/{}.mp4 -i files/{}.mp4 {} 'files/{}.mp4'"
        speed_wa="ffmpeg -i files/{}.mp4 {} 'files/{}.mp4'"
        if link.startswith("watch/")==True:
            link="https://www.redgifs.com/{}".format(link)
            return render_template("reggifs.html",l=link)
        elif link.endswith(".gif")==True:
            link="https://i.redd.it/{}".format(link)
            return render_template("special.html",l=link)
        elif link.endswith(".jpg")==True:
            link="https://i.redd.it/{}".format(link)
            return render_template("special.html",l=link)
        elif link.endswith(".jpg")==True:
            link="https://i.redd.it/{}".format(link)
            return render_template("special.html",l=link)
        elif link.endswith(".png")==True:
            link="https://i.redd.it/{}".format(link)
            return render_template("special.html",l=link)   
        elif link.endswith(".gifv")==True:
            link="https://i.imgur.com/{}".format(link)
            return render_template("special.html",l=link)
        else:
            link="https://v.redd.it/{}".format(link)
            test_m=["1080","720","480","360","240","220"]
            for i in test_m:
                test.append(i)
            dw=None
            for i in test:
                status=os.popen("curl -I {}/DASH_{}.mp4".format(link,i)).read()
                print(status)
                if status.startswith("HTTP/2 403")==False and status.startswith("HTTP/1.1 403")==False and status.startswith("HTTP/1 403")==False and status.startswith("HTTP/0.9 403")==False:
                    if has_audio==True:
                        status=os.popen("curl -I {}/DASH_audio.mp4".format(link)).read()
                        if status.startswith("HTTP/2 403")==False and status.startswith("HTTP/1.1 403")==False and status.startswith("HTTP/1 403")==False and status.startswith("HTTP/0.9 403")==False:
                            has_audio=True
                        else:
                            has_audio=False
                        print("{}/DASH_{}.mp4".format(link,i))
                        dw = ''.join(random.choices(string.ascii_letters+string.digits, k = uz))    
                        au = ''.join(random.choices(string.ascii_letters+string.digits, k = uz))
                        çk=title+"_"
                        if komut=="":
                            çk=çk+"None"
                        else:
                            çk =çk+ ''.join(random.choices(string.ascii_letters+string.digits, k = uz))
                        if has_audio==True:
                            s("curl {}/DASH_{}.mp4 -o files/{}.mp4".format(link,i,dw))
                            s("curl {}/DASH_audio.mp4 -o files/{}.mp4".format(link,au))
                            if "-vf" in komut:
                                try:
                                    s(speed.format(dw,au,komut,çk))
                                except:
                                    s(normal.format(dw,au,"",çk))
                            else:    
                                try:
                                    s(normal.format(dw,au,komut,çk))
                                except:
                                    s(normal.format(dw,au,"",çk))
                    else:
                        if  komut=="":
                            return render_template("special.html",l="{}/DASH_{}.mp4".format(link,i))
                            
                        else:
                            s("curl {}/DASH_{}.mp4 -o files/{}.mp4".format(link,i,dw))
                            if "-vf" in komut:
                                try:
                                    s(speed_wa.format(dw,komut,çk))
                                except:
                                    s(no_audio.format(dw,"",çk))    
                            try:
                                s(no_audio.format(dw,komut,çk))
                            except:
                                s(no_audio.format(dw,"",çk))
                    break
                else:
                    print("olmadı")
                    continue
            if dw==None:
                return render_template("hata.html",id=link)
            else:
                return render_template("download.html",l="{}.mp4".format(çk))
    else:  
        
        normal="ffmpeg -i files/{}.mp4 -i files/{}.mp4 {} -c copy 'files/{}.mp4'"
        no_audio="ffmpeg -i files/{}.mp4 {} -c copy 'files/{}.mp4'"
        speed="ffmpeg -i files/{}.mp4 -i files/{}.mp4 {} 'files/{}.mp4'"
        speed_wa="ffmpeg -i files/{}.mp4 {} 'files/{}.mp4'"
        if link.startswith("watch/")==True:
            link="https://www.redgifs.com/{}".format(link)
            return render_template("reggifs.html",l=link)
        elif link.endswith(".gif")==True:
            link="https://i.redd.it/{}".format(link)
            return render_template("special.html",l=link)
        elif link.endswith(".jpg")==True:
            link="https://i.redd.it/{}".format(link)
            return render_template("special.html",l=link)
        elif link.endswith(".jpg")==True:
            link="https://i.redd.it/{}".format(link)
            return render_template("special.html",l=link)
        elif link.endswith(".png")==True:
            link="https://i.redd.it/{}".format(link)
            return render_template("special.html",l=link)   
        elif link.endswith(".gifv")==True:
            link="https://i.imgur.com/{}".format(link)
            return render_template("special.html",l=link)
        else:
            link="https://v.redd.it/{}".format(link)
            test_m=["1080","720","480","360","240","220"]
            for i in test_m:
                test.append(i)
            dw=None
            for i in test:
                status=os.popen("curl -I {}/DASH_{}.mp4".format(link,i)).read()
                print(status)
                if status.startswith("HTTP/2 403")==False and status.startswith("HTTP/1.1 403")==False and status.startswith("HTTP/1 403")==False and status.startswith("HTTP/0.9 403")==False:
                    if has_audio==True:
                        status=os.popen("curl -I {}/DASH_audio.mp4".format(link)).read()
                        if status.startswith("HTTP/2 403")==False and status.startswith("HTTP/1.1 403")==False and status.startswith("HTTP/1 403")==False and status.startswith("HTTP/0.9 403")==False:
                            has_audio=True
                        else:
                            has_audio=False
                        print("{}/DASH_{}.mp4".format(link,i))
                        dw = ''.join(random.choices(string.ascii_letters+string.digits, k = uz))    
                        au = ''.join(random.choices(string.ascii_letters+string.digits, k = uz))
                        çk=title+"_"
                        if komut=="":
                            çk=çk+"None"
                        else:
                            çk =çk+ ''.join(random.choices(string.ascii_letters+string.digits, k = uz))
                        if has_audio==True:
                            s("curl {}/DASH_{}.mp4 -o files/{}.mp4".format(link,i,dw))
                            s("curl {}/DASH_audio.mp4 -o files/{}.mp4".format(link,au))
                            if "-vf" in komut:
                                try:
                                    s(speed.format(dw,au,komut,çk))
                                except:
                                    s(normal.format(dw,au,"",çk))
                            else:    
                                try:
                                    s(normal.format(dw,au,komut,çk))
                                except:
                                    s(normal.format(dw,au,"",çk))
                    else:
                        if  komut=="":
                            return render_template("special.html",l="{}/DASH_{}.mp4".format(link,i))
                            
                        else:
                            s("curl {}/DASH_{}.mp4 -o files/{}.mp4".format(link,i,dw))
                            if "-vf" in komut:
                                try:
                                    s(speed_wa.format(dw,komut,çk))
                                except:
                                    s(no_audio.format(dw,"",çk))    
                            try:
                                s(no_audio.format(dw,komut,çk))
                            except:
                                s(no_audio.format(dw,"",çk))
                    break
                else:
                    print("olmadı")
                    continue
            if dw==None:
                return render_template("hata.html",id=link)
            else:
                return render_template("download.html",l="{}.mp4".format(çk))
@site.route("/z/<file>",methods=["GET","POST"])
def last(file):
    path="/home/ubuntu/website/files/{}".format(file)
    return send_file(path, as_attachment=True)
    
@site.route('/py', methods=['GET', 'POST'])
def server():
    if request.method == 'POST':
        # Then get the data from the form
        tag = request.form['tag']

        # Get the username/password associated with this tag
        user=tag

        # Generate just a boring response
        print(tag) 
        # Or you could have a custom template for displaying the info
        # return render_template('asset_information.html',
        #                        username=user, 
        #                        password=password)

    # Otherwise this was a normal GET request
    else:   
        return render_template('main.html')
@site.route("/ads.txt",methods=['GET', 'POST'])
def ads():
    return send_file("ads.txt",as_attachment=False)
@site.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404
@site.errorhandler(500)
def page_not_found(e):
    return render_template('hata.html'), 500
if __name__=="__main__":
    site.run()