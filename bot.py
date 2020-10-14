import imaplib
import email
import base64
import vk_api
import random
import requests
import telebot
import os


bot = telebot.TeleBot('TgToken')
vk = vk_api.VkApi(token="VkToken")
ids=[тут id диалогов]
idst=[тут id диалогов]

def lastemail():
    mail= imaplib.IMAP4_SSL('imap сервер')
    mail.login('логин', 'пароль')
    mail.list()
    mail.select() # connect to inbox.
    typ, data = mail.search(None, 'All')
    num= data[0].split()
    if 1:
        typ, data = mail.fetch(num[-1], '(RFC822)')
        msg = email.message_from_bytes(data[0][1])
        fr=list(msg['From'].split("?= "))[1]
        for part in msg.walk():
            if part.get_content_type() == 'text/plain':
                s = str(part.get_payload())
                try:
                    qwety = base64.b64decode(s)
                except:
                    qwety=s.encode()
                try:
                    ere = base64.b64decode(str(msg['Subject'])[9:])
                except:
                    ere=str(msg['Subject']).encode()

        ans="From: "+fr+"\n"+str(ere.decode(errors='ignore'))+"\n"+str(qwety.decode(errors='ignore'))
        return (ans, mail)


def docinemail(mail):
    typ, data = mail.search(None, 'All')
    num= data[0].split()
    typ, data = mail.fetch(num[-1], '(RFC822)')
    msg = email.message_from_bytes(data[0][1])
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            filename = part.get_filename()
            if filename:
                # Нам плохого не надо, в письме может быть всякое барахло
                if 1:
                    fname=part.get_filename()
                    fname=base64.b64decode(fname[10:-2]).decode(errors='ignore')
                    if fname == "":
                        fname="doc.pdf"
                    if fname[-3:]==".pd":
                        fname+="f"
                    if fname[-3:]==".pn":#Да, это костыль, но что вы мне сделаете, я в другом городе
                        fname+="g"
                    if fname[-3:]==".jp":
                        fname+="g"
                    if fname[-4:]==".gpe":
                        fname+="g"
                    with open("doc."+list(fname.split("."))[1], 'wb') as new_file:
                        new_file.write(part.get_payload(decode=True))
                    return("doc."+list(fname.split("."))[1])
                if 0:
                    with open("doc.pdf", 'wb') as new_file:
                        new_file.write(part.get_payload(decode=True))
                    return("doc.pdf")


def uploaddoc(fln):
    a = vk.method("docs.getUploadServer")
    b = requests.post(a['upload_url'], files={'doc': open(fln, 'rb')}).json()
    c = vk.method('docs.getMessagesUploadServer', {'doc': b['doc'], 'server': b['server'], 'hash': b['hash']})[0]
    d  = "doc{}_{}".format(c["owner_id"], c["id"])
    return(d)

def check(ans,emails):
    for i in range(len(emails)):
        if ans ==emails[i]:
            return(0)
    return(1)

while 1:
    try:
        f = open('emails.TXT', 'r')
        emails = list(map(str, f.read().split("~~~")))https://github.com/shameful-coyot-number-1-in-Russia/EmailsToVkandTg
        f.close()
        ans,mail=lastemail()
        try:
            ans=str(ans.split("\r")[0]+ans.split("\r")[1])
        except:
            ans=ans
        if check(ans,emails):
            emails.append(ans)
            f = open('emails.TXT', 'a')
            f.write(ans + "~~~")
            f.close()

            fln=docinemail(mail)

            for i in range(len(idst)):
                try:
                    with open(fln, 'rb') as f1:
                        bot.send_document(idst[i], f1,caption=ans)
                except:
                    bot.send_message(idst[i],text=ans)

            for i in range(len(ids)):
                vk.method("messages.send", {"peer_id": ids[i], "message": ans, 'attachment': uploaddoc(fln),"random_id": random.randint(1, 2147483647)})

            os.remove(fln)
    except:
        print("Произошла ошибка")
    mail.close()
    mail.logout()


