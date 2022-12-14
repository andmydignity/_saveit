#IMPORTANT:ONLY WORKS IN LINUX!
from redgifdl import download
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
from dotenv import load_dotenv
from werkzeug.utils import secure_filename

load_dotenv("site.env")
key=os.getenv("key")
fernet = Fernet(key)
site=Flask(__name__)
from flask_sqlalchemy import SQLAlchemy
from flask_statistics import Statistics
site.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

#For statistics:
db = SQLAlchemy(site)
class Request(db.Model):
    __tablename__ = "request"

    index = db.Column(db.Integer, primary_key=True, autoincrement=True)
    response_time = db.Column(db.Float)
    date = db.Column(db.DateTime)
    method = db.Column(db.String)
    size = db.Column(db.Integer)
    status_code = db.Column(db.Integer)
    path = db.Column(db.String)
    user_agent = db.Column(db.String)
    remote_address = db.Column(db.String)
    exception = db.Column(db.String)
    referrer = db.Column(db.String)
    browser = db.Column(db.String)
    platform = db.Column(db.String)
    mimetype = db.Column(db.String)
with site.app_context():
    db.create_all()
statistics = Statistics(site, db, Request)
def deEmojify(text):
    regrex_pattern = re.compile(pattern = "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags = re.UNICODE)
    return regrex_pattern.sub(r'',text)
def temizmi(s):#Does nothing?
    if ";" in s:
        return False
    elif "|" in s:
        return False
    elif "&" in s:
        return False
    else:
        return True
@site.route("/",methods=["GET","POST"])
def ana():
    return render_template("main.html")
@site.route("/d/<link>/<komut>/<quality>/",methods=["GET","POST"])#Old link system support.
def indir(link,komut,quality):
    try:
        link=bytes(link,"utf-8")
        link=link[2:]
        link=fernet.decrypt(link).decode()
    except:
        #Useless thing i left
        link=link.decode("utf-8")
        if temizmi(link)==False:
            link="Nice try buddy."
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
    if komut!="":
        number = int(filter(str.isdigit, komut))
    else:
        number=""
    normal="ffmpeg -i files/{}.mp4 -i files/{}.mp4 {} -c copy files/{}.mp4"
    no_audio="ffmpeg -i files/{}.mp4 {} -c copy files/{}.mp4"
    speed="ffmpeg -i files/{}.mp4 -i files/{}.mp4 {} files/{}.mp4"
    speed_wa="ffmpeg -i files/{}.mp4 {} 'files/{}.mp4'"
    #Check if it's a image/gif.
    if link.startswith("watch/")==True:
        url="https://www.redgifs.com/{}".format(link)
        fname=link.split("/",1)[1]
        if komut=="":
            if isfile("files/{}.mp4".format(fname))==True:
                print("Sending the same RedGIF.")
                return render_template("download.html",l="{}.mp4".format(fname))   
            else:
                download.url_file(redgifs_url=url, filename="files/{}.mp4".format(fname))
                return render_template("download.html",l="{}.mp4".format(fname))
        else:
            if isfile("files/{}_{}.mp4".format(fname,number))==True:
                print("Sending the same RedGIF.")
                return render_template("download.html",l="{}_{}.mp4".format(fname,number))   
            else:
                download.url_file(redgifs_url=url, filename="files/{}_{}.mp4".format(fname,number))
                return render_template("download.html",l="{}_{}.mp4".format(fname,number))

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
        ex=False
        status=os.popen("curl -I {}/DASH_audio.mp4".format(link)).read()
        print(status)
        if status.startswith("HTTP/2 403")==False and status.startswith("HTTP/1.1 403")==False and status.startswith("HTTP/1 403")==False and status.startswith("HTTP/0.9 403")==False:
            has_audio=True
        else:
            has_audio=False
        for i in test:
            status=os.popen("curl -I {}/DASH_{}.mp4".format(link,i)).read()
            print(status)
            if status.startswith("HTTP/2 403")==False and status.startswith("HTTP/1.1 403")==False and status.startswith("HTTP/1 403")==False and status.startswith("HTTP/0.9 403")==False:
                if has_audio==True:
                    print("{}/DASH_{}.mp4".format(link,i))
                    #Create random strings to rename the files.
                    dw = ''.join(random.choices(string.ascii_letters+string.digits, k = uz))    
                    au = ''.join(random.choices(string.ascii_letters+string.digits, k = uz))
                    ??k = ''.join(random.choices(string.ascii_letters+string.digits, k = uz))
                    ??k=secure_filename(??k)
                    if has_audio==True:
                        s("curl {}/DASH_{}.mp4 -o files/{}.mp4".format(link,i,dw))
                        try:
                            s("curl {}/DASH_audio.mp4 -o files/{}.mp4".format(link,au))
                        except:
                            ex=True
                        if "-vf" in komut:
                                if ex==True:
                                    try:
                                        s(speed_wa.format(dw,komut,??k))
                                    except:
                                        s(no_audio.format(dw,"",??k))
                                else:
                                    try:
                                        s(speed.format(dw,au,komut,??k))
                                    except:
                                        s(normal.format(dw,au,"",??k))
                        else:
                            if ex==True:
                                try:
                                    s(no_audio.format(dw,komut,??k))
                                except:
                                    s(no_audio.format(dw,"",??k))
                            else:   
                                try:
                                    s(normal.format(dw,au,komut,??k))
                                except:
                                    s(normal.format(dw,au,"",??k))
                    else:
                        if komut=="":
                            dw="Successful"
                            s("curl {}/DASH_{}.mp4 -o files/{}.mp4".format(link,i,??k))
                        else:
                            s("curl {}/DASH_{}.mp4 -o files/{}.mp4".format(link,i,dw))
                            if "-vf" in komut:
                                try:
                                    s(speed_wa.format(dw,komut,??k))
                                except:
                                    s(no_audio.format(dw,"",??k))    
                            try:
                                s(no_audio.format(dw,komut,??k))
                            except:
                                s(no_audio.format(dw,"",??k))
                    break
            else:
                print("olmad??")
                continue
        if dw==None:
            return render_template("hata.html",id=link)
        else:
            return render_template("download.html",l="{}.mp4".format(??k))
@site.route("/d/<link>/<komut>/<quality>/<title>/",methods=["GET","POST"])
def indirt(link,komut,quality,title):
    #Clean the title
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
    title=title.replace("??","u")
    title=title.replace("??","o")
    title=title.replace("??","g")
    title=title.replace("??","c")
    title=deEmojify(title)
    title=secure_filename(title)


    try:
        link=bytes(link,"utf-8")
        link=link[2:]
        link=fernet.decrypt(link).decode()
    except:
        #Useless
        link=link.decode("utf-8")
        if temizmi(link)==False:
            link="Nice try buddy."
    test=[]
    uz = 10
    has_audio=True
    ex=False
    if komut=="None":
        komut=""
    else:
        komut=bytes(komut,"utf-8")
        komut=komut[2:]
        komut=fernet.decrypt(komut).decode()
    if quality!="None":
        quality=bytes(quality,"utf-8")
        quality=quality[2:]
        quality=fernet.decrypt(quality).decode()
        if "a" in quality:
            has_audio=False
            quality=quality[-1]
            test.append(quality)
    if komut!="":
        number=int(''.join(i for i in komut if i.isdigit()))
        number=str(number)
    else:
        number=""
    if quality=="None" and has_audio==True and komut=="" and isfile("files/{}_None.mp4".format(title))==True:
        print("Returning the same file...")
        try:
            return render_template("download.html",l="{}_None.mp4".format(title))
        except:
            pass
    elif isfile("files/{}_{}.mp4".format(title,number))==True and number!="" :
        print("Returning the same file...")
        try:
            return render_template("download.html",l="{}_{}.mp4".format(title,number))
        except:
            pass    
            
    else:  
        normal="ffmpeg -i files/{}.mp4 -i files/{}.mp4 {} -c copy 'files/{}.mp4'"
        no_audio="ffmpeg -i files/{}.mp4 {} -c copy 'files/{}.mp4'"
        speed="ffmpeg -i files/{}.mp4 -i files/{}.mp4 {} 'files/{}.mp4'"
        speed_wa="ffmpeg -i files/{}.mp4 {} 'files/{}.mp4'"
        if link.startswith("watch/")==True:
            url="https://www.redgifs.com/{}".format(link)
            fname=link.split("/",1)[1]
            if komut=="":
                if isfile("files/{}.mp4".format(fname))==True:
                    print("Sending the same RedGIF.")
                    return render_template("download.html",l="{}.mp4".format(fname))   
                else:
                    download.url_file(redgifs_url=url, filename="files/{}.mp4".format(fname))
                    return render_template("download.html",l="{}.mp4".format(fname))
            else:
                if isfile("files/{}_{}.mp4".format(fname,number))==True:
                    print("Sending the same RedGIF.")
                    return render_template("download.html",l="{}_{}.mp4".format(fname,number))   
                else:
                    download.url_file(redgifs_url=url, filename="files/{}_{}.mp4".format(fname,number))
                    return render_template("download.html",l="{}_{}.mp4".format(fname,number))
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
            status=os.popen("curl -I {}/DASH_audio.mp4".format(link)).read()
            print(status)
            if status.startswith("HTTP/2 403")==False and status.startswith("HTTP/1.1 403")==False and status.startswith("HTTP/1 403")==False and status.startswith("HTTP/0.9 403")==False:
                has_audio=True
            else:
                has_audio=False
            for i in test:
                status=os.popen("curl -I {}/DASH_{}.mp4".format(link,i)).read()
                print(status)
                if status.startswith("HTTP/2 403")==False and status.startswith("HTTP/1.1 403")==False and status.startswith("HTTP/1 403")==False and status.startswith("HTTP/0.9 403")==False:
                    if has_audio==True:
                        print("{}/DASH_{}.mp4".format(link,i))
                        dw = ''.join(random.choices(string.ascii_letters+string.digits, k = uz))    
                        au = ''.join(random.choices(string.ascii_letters+string.digits, k = uz))
                        ??k=title+"_"
                        if komut=="":
                            ??k=??k+"None"
                        else:
                            ??k =??k+number
                        if has_audio==True:
                            s("curl {}/DASH_{}.mp4 -o files/{}.mp4".format(link,i,dw))
                            try:
                                s("curl {}/DASH_audio.mp4 -o files/{}.mp4".format(link,au))
                            except:
                                ex=True
                            if "-vf" in komut:
                                if ex==True:
                                    try:
                                        s(speed_wa.format(dw,komut,??k))
                                    except:
                                        s(no_audio.format(dw,"",??k))
                                else:
                                    try:
                                        s(speed.format(dw,au,komut,??k))
                                    except:
                                        s(normal.format(dw,au,"",??k))
                            else:
                                if ex==True:
                                    try:
                                        s(no_audio.format(dw,komut,??k))
                                    except:
                                        s(no_audio.format(dw,"",??k))
                                else:   
                                    try:
                                        s(normal.format(dw,au,komut,??k))
                                    except:
                                        s(normal.format(dw,au,"",??k))
                    else:
                        dw = ''.join(random.choices(string.ascii_letters+string.digits, k = uz))    
                        au = ''.join(random.choices(string.ascii_letters+string.digits, k = uz))
                        ??k=title+"_"
                        if  komut=="":
                            dw="Successful"
                            s("curl {}/DASH_{}.mp4 -o files/{}.mp4".format(link,i,??k))
                            
                        else:
                            ??k=??k+"_"+number
                            s("curl {}/DASH_{}.mp4 -o files/{}.mp4".format(link,i,dw))
                            if "-vf" in komut:
                                try:
                                    s(speed_wa.format(dw,komut,??k))
                                except:
                                    s(no_audio.format(dw,"",??k))    
                            try:
                                s(no_audio.format(dw,komut,??k))
                            except:
                                s(no_audio.format(dw,"",??k))
                    break
                else:
                    print("olmad??")
                    continue
            if dw==None:
                return render_template("hata.html",id=link)#Returns error
            else:
                return render_template("download.html",l="{}.mp4".format(??k))
@site.route("/d/<link>/<komut>/<quality>/<title>/<id>/",methods=["GET","POST"])
def indirti(link,komut,quality,title,id):
    #Clean the title
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
    title=title.replace("??","u")
    title=title.replace("??","o")
    title=title.replace("??","g")
    title=title.replace("??","c")
    title=deEmojify(title)
    title=secure_filename(title)
    id=id.replace("|","")
    id=id.replace("&","")
    id=id.replace(";","")
    id=id.replace(":","")
    id=id.replace("#","")
    id=id.replace("/","")
    id=id.replace("<","")
    id=id.replace(">","")
    id=id.replace("?","")
    id=id.replace("??","u")
    id=id.replace("??","o")
    id=id.replace("??","g")
    id=id.replace("??","c")
    try:
        link=bytes(link,"utf-8")
        link=link[2:]
        link=fernet.decrypt(link).decode()
    except:
        #Useless
        link=link.decode("utf-8")
        if temizmi(link)==False:
            link="Nice try buddy."
    test=[]
    uz = 10
    has_audio=True
    ex=False
    if komut=="None":
        komut=""
    else:
        komut=bytes(komut,"utf-8")
        komut=komut[2:]
        komut=fernet.decrypt(komut).decode()
    if quality!="None":
        quality=bytes(quality,"utf-8")
        quality=quality[2:]
        quality=fernet.decrypt(quality).decode()
        if "a" in quality:
            has_audio=False
            quality=quality[-1]
            test.append(quality)
    if komut!="":
        number = int(''.join(i for i in komut if i.isdigit()))
        number=str(number)
    else:
        number=""
    if quality=="None" and has_audio==True and komut=="" and isfile("files/{}_None_{}.mp4".format(title,id))==True:
        print("Returning the same file...")
        try:
            return render_template("download.html",l="{}_None_{}.mp4".format(title,id))
        except:
            pass
    elif isfile("files/{}_{}_{}.mp4".format(title,number,id))==True and number!="" :
        print("Returning the same file...")
        try:
            return render_template("download.html",l="{}_{}_{}.mp4".format(title,number,id))
        except:
            pass        
    else:  
        normal="ffmpeg -i files/{}.mp4 -i files/{}.mp4 {} -c copy 'files/{}.mp4'"
        no_audio="ffmpeg -i files/{}.mp4 {} -c copy 'files/{}.mp4'"
        speed="ffmpeg -i files/{}.mp4 -i files/{}.mp4 {} 'files/{}.mp4'"
        speed_wa="ffmpeg -i files/{}.mp4 {} 'files/{}.mp4'"
        if link.startswith("watch/")==True:
            url="https://www.redgifs.com/{}".format(link)
            fname=link.split("/",1)[1]
            if komut=="":
                if isfile("files/{}.mp4".format(fname))==True:
                    print("Sending the same RedGIF.")
                    return render_template("download.html",l="{}.mp4".format(fname))   
                else:
                    download.url_file(redgifs_url=url, filename="files/{}.mp4".format(fname))
                    return render_template("download.html",l="{}.mp4".format(fname))
            else:
                if isfile("files/{}_{}.mp4".format(fname,number))==True:
                    print("Sending the same RedGIF.")
                    return render_template("download.html",l="{}_{}.mp4".format(fname,number))   
                else:
                    download.url_file(redgifs_url=url, filename="files/{}_{}.mp4".format(fname,number))
                    return render_template("download.html",l="{}_{}.mp4".format(fname,number))
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
            status=os.popen("curl -I {}/DASH_audio.mp4".format(link)).read()
            print(status)
            if status.startswith("HTTP/2 403")==False and status.startswith("HTTP/1.1 403")==False and status.startswith("HTTP/1 403")==False and status.startswith("HTTP/0.9 403")==False:
                has_audio=True
            else:
                has_audio=False
            for i in test:
                status=os.popen("curl -I {}/DASH_{}.mp4".format(link,i)).read()
                print(status)
                if status.startswith("HTTP/2 403")==False and status.startswith("HTTP/1.1 403")==False and status.startswith("HTTP/1 403")==False and status.startswith("HTTP/0.9 403")==False:
                    if has_audio==True:
                        print("{}/DASH_{}.mp4".format(link,i))
                        dw = ''.join(random.choices(string.ascii_letters+string.digits, k = uz))    
                        au = ''.join(random.choices(string.ascii_letters+string.digits, k = uz))
                        ??k=title+"_"
                        if komut=="":
                            ??k=??k+"None_{}".format(id)
                        else:
                            ??k =??k+number+"_"+str(id)
                        if has_audio==True:
                            s("curl {}/DASH_{}.mp4 -o files/{}.mp4".format(link,i,dw))
                            try:
                                s("curl {}/DASH_audio.mp4 -o files/{}.mp4".format(link,au))
                            except:
                                ex=True
                            if "-vf" in komut:
                                if ex==True:
                                    try:
                                        s(speed_wa.format(dw,komut,??k))
                                    except:
                                        s(no_audio.format(dw,"",??k))
                                else:
                                    try:
                                        s(speed.format(dw,au,komut,??k))
                                    except:
                                        s(normal.format(dw,au,"",??k))
                            else:
                                if ex==True:
                                    try:
                                        s(no_audio.format(dw,komut,??k))
                                    except:
                                        s(no_audio.format(dw,"",??k))
                                else:   
                                    try:
                                        s(normal.format(dw,au,komut,??k))
                                    except:
                                        s(normal.format(dw,au,"",??k))
                    else:
                        dw = ''.join(random.choices(string.ascii_letters+string.digits, k = uz))    
                        au = ''.join(random.choices(string.ascii_letters+string.digits, k = uz))
                        ??k=title+"_"+"None_"+id
                        if  komut=="":
                            dw="Successful"
                            s("curl {}/DASH_{}.mp4 -o files/{}.mp4".format(link,i,??k))
                            
                        else:
                            s("curl {}/DASH_{}.mp4 -o files/{}.mp4".format(link,i,dw))
                            ??k=title+"_"+number
                            if "-vf" in komut:
                                try:
                                    s(speed_wa.format(dw,komut,??k))
                                except:
                                    s(no_audio.format(dw,"",??k))    
                            try:
                                s(no_audio.format(dw,komut,??k))
                            except:
                                s(no_audio.format(dw,"",??k))
                    break
                else:
                    print("olmad??")
                    continue
            if dw==None:
                return render_template("hata.html",id=link)#Returns error
            else:
                return render_template("download.html",l="{}.mp4".format(??k))

@site.route("/z/<file>",methods=["GET","POST"])
def last(file):
    path="files/{}".format(file)
    return send_file(path, as_attachment=True)
@site.route("/ads.txt",methods=['GET', 'POST'])
def ads():
    return send_file("ads.txt",as_attachment=False)
@site.route("/db",methods=['GET', 'POST'])
def db():
    return send_file("instance/database.db",as_attachment=False)
@site.route("/robots.txt",methods=['GET', 'POST'])
def robots():
    return send_file("robots.txt",as_attachment=False)
@site.route("/sitemap.xml",methods=['GET', 'POST'])
def sitemap():
    return send_file("sitemap.xml",as_attachment=False)
@site.route("/privacy",methods=["POST","GET"])
def privacy():
    return render_template("privacy.html")
@site.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404
@site.errorhandler(500)
def page_not_found(e):
    return render_template('hata.html'), 500#Returns error page.
if __name__=="__main__":
    site.run()