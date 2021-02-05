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

"""
    Obtengo el modulo que fueron invocados
"""
module = GetParams("module")


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


if module == "read":
    path = GetParams("path")
    result = GetParams("var_")
    mails = []
    try:
        for mail_ in mailbox.mbox(path):
            data = dict()
            data["from"] = mail_["From"]
            data["subject"] = mail_["Subject"]
            data["date"] = mail_["Date"]
            data["to"] = mail_["To"]
            data["cc"] = mail_["Cc"] if mail_["Cc"] is not None else ""
            body = get_body(mail_)
            data["body"] = body
            mails.append(data)
        SetVar(result, mails)
    except Exception as e:
        PrintException()
        raise e
