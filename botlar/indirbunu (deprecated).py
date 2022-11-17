import praw
from time import sleep
bekleme=1
reddit = praw.Reddit(
client_id="7WRxoX58DSJCVTXabUF-JA",
client_secret="R_66NGKodNzlXgIrYp3YboSt9-6bRg",
user_agent="<console:LOL:1.0>",
username="indirbunu",
password="Ahmetse12",
ratelimit_seconds=1200,
)
import requests as r
from bs4 import BeautifulSoup as bs
from urllib.parse import quote_plus
from random import sample
#sxtng=["sik","gay","yarrak","yarrağ","çük","yala","am","evet","sexting"]
#niye=["neden","niye","niçin","ne için","ne sebeple"]
#niye_c=["botla sexting mi yapılır olum","sonum indirbeni gibi olacak yoksa","maalesef malum cevabı veremicem,yapımcım tembellik yaptı","işte","çünkü Hz.R.T.E(s.a.v) hala cumhurbaşkanı","yapımcım istemiyor","sane ne","canım istemiyor"]
#rast=["çaydanlığın altı","bota bağış yapın olum","kerbala ne oldu la","ne mütlü türk'üm diyene","yaşasın ırmıkız,çine ırkımız","alakasız bilgi:adnan menderes,kırşehirde bir muhalefet lideri kazandığı için kırşehiri ilçe yapmıştır ve kırşehirin eski bazı ilçelerinden nevşehiri kurmuştur.aynı şeyi malatyayada malatyanın ilçeleriyle adıyaman ilini kurmuştur","nerden arazi alabilirim","büyük memeleri severim","merhaba ben yapımcı son 15 dakikamı botun vereceği cevapları yazmakları geçirdim bıktım bune olum sadece indirme botu anlayın işte niye konuşuyounuz botla mk "]
cevap_ls=[]
kal_ls=[]
ban_ls=[]
yorum_ls=[]
kayıt_kişi=[]
kayıt_post=[]
kayıt_sub=[]
dön_ls=[]
k_defter=reddit.submission("x1krdg")
a_defter=reddit.submission("x1kv05")
d=False
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
                if l in kal_ls:
                    pass
                else:
                    if l.author=="None":
                        nu=cevap_ls.index(l)
                        kişi=kayıt_kişi[nu]
                        post=kayıt_post[nu]
                        sub=kayıt_post[nu]
                        k_defter.reply("u/{} | {} | {}".format(kişi,post,sub))
                        kal_ls.append(l)
                continue
            else:
                ls.append(l)
        if len(ls)==0:
            print("Bot çağrılmamış")
            sleep(bekleme)
        else:
            for x in ls:
                x.reply("Sadly u/indirbunu is no more for the better.Use u/_saveit instead"+"\n\n"+"Also u/_saveit has very useful commands,[here](https://www.reddit.com/user/_saveit/comments/yhco0q/commands_of_u_saveit/) is how to use it.")
                try:
                    x.author.message(subject="u/indirbunu is deprecated", message="Sadly u/indirbunu is no more for the better.Use u/_saveit instead"+"\n\n"+"Also u/_saveit has very useful commands,[here](https://www.reddit.com/user/_saveit/comments/yhco0q/commands_of_u_saveit/) is how to use it.")
                except:
                    print("Mesaj dönülemedi")
                kayıt_kişi.append(x.author)
                kayıt_post.append(post.title)
                kayıt_sub.append(x.subreddit)
                print("Link dönüldü!")
                cevap_ls.append(x)
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


    except Exception as e:
        print("Hata döndü!:{}".format(e))
        sleep(bekleme)
    if len(cevap_ls) > 100:
        for z in range(21):
            cevap_ls.pop(z)
    if len(yorum_ls) > 100:
        for z in range(21):
            yorum_ls.pop(z)
    if len(ban_ls) > 100:
        for z in range(21):
            ban_ls.pop(z)
    if len(kal_ls) > 100:
        for z in range(21):
            kal_ls.pop(z)
    if len(dön_ls) > 100:
        for z in range(21):
            dön_ls.pop(z)
    if len(kayıt_kişi) > 100:
        for z in range(21):
            kayıt_kişi.pop(z)
    if len(kayıt_post) > 100:
        for z in range(21):
            kayıt_post.pop(z)
    if len(kayıt_sub) > 100:
        for z in range(21):
            kayıt_sub.pop(z)

