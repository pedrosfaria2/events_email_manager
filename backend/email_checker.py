import os
import win32com.client
import re
from bs4 import BeautifulSoup
from datetime import datetime
from .models import db, EmailLog
import pythoncom

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

log_file_path = os.path.join(BASE_DIR, "emails/log/email_log.txt")
attachment_dir = os.path.join(BASE_DIR, "emails/attachments")
email_dir = os.path.join(BASE_DIR, "emails/htmls")

sender_emails = ["liquidacao.certifica@b3.com.br", "tradingcertification@b3.com.br", "suporteanegociacao@b3.com.br", "tradingsupport@b3.com.br"]

os.makedirs(email_dir, exist_ok=True)
os.makedirs(attachment_dir, exist_ok=True)
os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

if not os.path.exists(log_file_path):
    with open(log_file_path, 'w') as f:
        pass

def save_email_content(message, email_id):
    body = message.HTMLBody
    body = re.sub(r'<!-- Conteúdo da Publicação -->(.*?)<hr>', '', body, flags=re.DOTALL)
    soup = BeautifulSoup(body, "html.parser")
    title = soup.find("span", style=lambda value: "font-size: 24px;" in value)
    subject = "No Subject Found"
    if title:
        match = re.search(r'\|(.*)', title.text)
        if match:
            subject = match.group(1).strip()
    content = str(soup).strip()
    content = '<p style="font-size: 17px; color: black;">Dear customer, please find below a recent notification from B3.<br> If you have any questions, please reach out to us at <a href="mailto:hft@novafutura.com.br" target="_blank" title="mailto:hft@novafutura.com.br" rel="noopener noreferrer nofollow">hft@novafutura.com.br</a> or +55 (11) 4871-1012/13/14/15.</p> ' + content
    content = re.sub(r'<!-- Rodapé da Publicação-->.*', '', content, flags=re.DOTALL)
    
    email_filename = f'{email_id}.html'
    email_path = os.path.join(email_dir, email_filename)
    with open(email_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    email_log = EmailLog(subject=subject, html_file=email_filename)
    db.session.add(email_log)
    db.session.commit()
    
    return subject, email_path, email_filename

def save_inline_images(message, email_id):
    inline_images = {}
    for i, attachment in enumerate(message.Attachments):
        try:
            cid = attachment.PropertyAccessor.GetProperty("http://schemas.microsoft.com/mapi/proptag/0x3712001F")
            filename = re.sub(r'[^a-zA-Z0-9]', '', f"cid{cid}") + ".png"
            file_path = os.path.join(attachment_dir, filename)
            attachment.SaveAsFile(file_path)
            inline_images[cid] = file_path
            print(f"Salvo: {file_path}")
        except Exception as e:
            print(f"Erro ao salvar o anexo: {e}")
    return inline_images

def update_html_with_images(html_content, inline_images):
    soup = BeautifulSoup(html_content, "html.parser")
    images = soup.find_all('img')

    for img in images:
        src = img.get('src')
        if (src and src.startswith('cid:')):
            cid = src[4:]
            if cid in inline_images:
                img['src'] = "cid:" + cid

    return str(soup)

def check_emails(app):
    with app.app_context():
        Outlook = win32com.client.Dispatch("Outlook.Application")
        namespace = Outlook.GetNamespace("MAPI")
        inbox = namespace.Folders['HFT'].Folders['Caixa de Entrada']
        messages = inbox.Items
        messages.Sort("[ReceivedTime]", True)

        for message in messages:
            if hasattr(message, 'SenderEmailAddress'):
                if message.SenderEmailAddress in sender_emails:
                    if message.Subject.startswith("[Listados - "):
                        if "REENVIO" not in message.body:
                            match = re.search(r'Ref:(.*)', message.Body)
                            if match:
                                unique_id = match.group(1).strip()
                                with open(log_file_path, 'r') as f:
                                    if unique_id in f.read():
                                        continue
                                try:
                                    subject, email_path, email_filename = save_email_content(message, unique_id)
                                    
                                    with open(email_path, 'r', encoding='utf-8') as f:
                                        html_content = f.read()
                                    
                                    inline_images = save_inline_images(message, unique_id)
                                    updated_html = update_html_with_images(html_content, inline_images)

                                    with open(email_path, 'w', encoding='utf-8') as f:
                                        f.write(updated_html)

                                    outlook = win32com.client.Dispatch("Outlook.Application")
                                    new_message = outlook.CreateItem(0)
                                    new_message.Subject = "[B3] " + subject
                                    new_message.HTMLBody = updated_html
                                    new_message.SentOnBehalfOfName = "hft@novafutura.com.br"
                                    new_message.To = "pedro.faria@novafutura.com.br"
                                    
                                    for cid, img_path in inline_images.items():
                                        attachment = new_message.Attachments.Add(img_path)
                                        attachment.PropertyAccessor.SetProperty("http://schemas.microsoft.com/mapi/proptag/0x3712001F", cid)
                                    
                                    new_message.Send()

                                    email_log = EmailLog(subject=subject, date_sent=datetime.now(), html_file=email_filename)
                                    db.session.add(email_log)
                                    db.session.commit()
                                    
                                    with open(log_file_path, 'a') as f:
                                        f.write(f'{unique_id} {datetime.now()}\n')
                                except Exception as e:
                                    print(f"Erro ao processar o e-mail: {e}")

def send_saved_email(email_id):
    pythoncom.CoInitialize()
    email_log = EmailLog.query.get(email_id)
    if not email_log:
        raise ValueError('Email not found')

    email_path = os.path.join(BASE_DIR, 'emails/htmls', email_log.html_file)
    with open(email_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    try:
        outlook = win32com.client.Dispatch("Outlook.Application")
        new_message = outlook.CreateItem(0)
        new_message.Subject = "[B3] " + email_log.subject
        new_message.HTMLBody = html_content
        new_message.To = "pedro.faria@novafutura.com.br"

        attachment_dir = os.path.join(BASE_DIR, 'emails/attachments')

        # Adicionar imagens inline
        soup = BeautifulSoup(html_content, "html.parser")
        images = soup.find_all('img')
        for img in images:
            src = img.get('src')
            if src and src.startswith('/static/attachments/'):
                cid = src.split('/')[-1].split('.')[0][3:]  # remover 'cid'
                img_path = os.path.join(attachment_dir, f"cid{cid}.png")
                attachment = new_message.Attachments.Add(img_path)
                attachment.PropertyAccessor.SetProperty("http://schemas.microsoft.com/mapi/proptag/0x3712001F", cid)

        new_message.Display(True)
        #new_message.Send()
    except Exception as e:
        print(f'Failed to send email: {str(e)}')
        raise