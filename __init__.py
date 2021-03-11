# coding: utf-8
"""
Base para desarrollo de modulos externos.
Para obtener el modulo/Funcion que se esta llamando:
     GetParams("module")

Para obtener las variables enviadas desde formulario/comando Rocketbot:
    var = GetParams(variable)
    Las "variable" se define en forms del archivo package.json

Para modificar la variable de Rocketbot:
    SetVar(Variable_Rocketbot, "dato")

Para obtener una variable de Rocketbot:
    var = GetVar(Variable_Rocketbot)

Para obtener la Opcion seleccionada:
    opcion = GetParams("option")


Para instalar librerias se debe ingresar por terminal a la carpeta "libs"
    
    pip install <package> -t .

"""
base_path = tmp_global_obj["basepath"]
cur_path = base_path + 'modules' + os.sep + 'mbox' + os.sep + 'libs' + os.sep
sys.path.append(cur_path)
import mailbox
import quopri
from bs4 import BeautifulSoup

"""
    Obtengo el modulo que fueron invocados
"""
module = GetParams("module")
global attached_folder


def get_body(mail):
    import quopri
    global get_body
    body = ""
    if mail.is_multipart():
        for part in mail.get_payload():
            body = str(get_body(part))
            try:
                body = quopri.decodestring(body).decode('utf-8')
            except:
                pass
        return body
    body = quopri.decodestring(mail.get_payload()).decode('utf-8')
    return mail.get_payload()


def extractattachements(message):
    if message.get_content_maintype() == 'multipart':
        att = []
        for part in message.walk():
            if part.get_content_maintype() == 'multipart': continue
            if part.get('Content-Disposition') is None: continue
            if part.get('Content-Disposition').startswith("inline"): continue
            extension = part.get_content_type().split("/")[-1]
            from random import randrange
            subject = message["subject"].replace("?", "").replace("=", "")
            file_name = subject + str(int(randrange(999999)))
            path_files = attached_folder + os.sep + str(file_name)
            fb = open(path_files + "." + extension, 'wb')
            fb.write(part.get_payload(decode=True))
            fb.close()
            att.append(str(file_name) + "." + extension)

        return att


def getbodyfromemail(msg, count=0):
    global extractattachements
    global getbodyfromemail
    global BeautifulSoup
    global attachment_files_mod_mbox
    types_file = ["image/png", 'application/pdf']
    body = ""
    count += 1
    if msg.is_multipart():
        attachment_files_mod_mbox = attachment_files_mod_mbox + extractattachements(msg)
        print(attachment_files_mod_mbox, count)
        for part in msg.get_payload():
            if part.get_content_type() not in types_file:
                body += getbodyfromemail(part, count)
    else:
        try:
            html_body = msg.get_payload(decode=True).decode('utf-8')
        except UnicodeDecodeError:
            html_body = msg.get_payload(decode=True).decode('latin-1')
        try:
            soup = BeautifulSoup(html_body, 'html.parser')
            text = soup.body.get_text(strip=True)
        except Exception as e:
            text = html_body
        body += text.replace("\xa0", "")
    return body


if module == "read":
    path = GetParams("path")
    result = GetParams("var_")
    attached_folder = GetParams("attached_folder")
    mails = []

    try:
        for mail_ in mailbox.mbox(path):
            attachment_files_mod_mbox = []
            data = dict()
            data["from"] = mail_["From"]
            data["subject"] = mail_["Subject"]
            data["date"] = mail_["Date"]
            data["to"] = mail_["To"]
            data["cc"] = mail_["Cc"] if mail_["Cc"] is not None else ""
            body = getbodyfromemail(mail_)
            data["attachments"] = attachment_files_mod_mbox
            # soup = BeautifulSoup(body, 'html.parser')
            # text = soup.find_all(text=True)
            # text = soup.body.get_text()
            data["body"] = body
            mails.append(data)
        SetVar(result, mails)
    except Exception as e:
        PrintException()
        raise e
