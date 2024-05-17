import win32com.client

def send_email(subject, message, recipient):
    outlook = win32com.client.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    mail.Subject = subject
    mail.SentOnBehalfOfName = "pedro.faria@novafutura.com.br"
    mail.HTMLBody = message
    mail.To = recipient
    mail.Send()
    print("Email sent successfully via Outlook")
