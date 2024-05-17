import win32com.client
from datetime import date, timedelta
from dateutil.parser import parse
import sys
import os

# Adicione o caminho do backend ao sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend import create_app, db
from backend.add_event_to_db import add_events_to_db

# Crie a aplicação Flask
app = create_app() 

Outlook = win32com.client.Dispatch("Outlook.Application")
ns = Outlook.GetNamespace("MAPI")

calendar_name = "B3 events"
calendar = None
calendars_folder = ns.GetDefaultFolder(9)
for folder in calendars_folder.Folders:
    if folder.Name == calendar_name:
        calendar = folder
        break

if not calendar:
    print(f"Calendário '{calendar_name}' não encontrado.")
    sys.exit(1)

appts = calendar.Items
appts.Sort("[Start]")
appts.IncludeRecurrences = True

end = date.today() + timedelta(days=500)
end = end.strftime('%m/%d/%Y')
begin = date.today().strftime('%m/%d/%Y')
appts = appts.Restrict("[Start] >= '" + begin + "' AND [END] <= '" + end + "'")

excluded_subjects = ('<first excluded subject>', '<second excluded subject>', '<third excluded subject>', '<etc … >')

events = []
for a in appts:
    subject = str(a.Subject)
    if subject in excluded_subjects:
        continue
    
    title = subject
    description = str(a.Body)
    date = parse(str(a.Start)).date().strftime("%Y-%m-%d")
    start_time = "08:00"
    end_time = "19:00"
    
    event = {
        "title": title,
        "description": description,
        "date": date,
        "start_time": start_time,
        "end_time": end_time,
        "tags": "automatic exercise, futures"
    }
    events.append(event)

with app.app_context():
    add_events_to_db(events)
