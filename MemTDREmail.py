import requests
import pandas as pd
import arrow
import warnings
import io
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
warnings.filterwarnings('ignore', 'Unverified HTTPS request')
nv = arrow.now()
date = nv.shift(days=-1).format('M/D/YYYY')
date2 = nv.shift(days=-1).format('YYYYMD')
url = "https://protect.cylance.com/Reports/ThreatDataReportV1/memoryprotection/"
token = "YourToken"
fullurl = (url + token)
path = 'File_Path'

def email_send(email_data):
    from_addr = "From email"
    to_addr = "To email address"
    to_list = [List of addresses to send email to ]
    msg = MIMEMultipart()
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Subject'] = "Cylance Exploit Attempts for %s" %(date)
    part2 = MIMEText(email_data, 'html')
    msg.attach(part2)
    server = smtplib.SMTP("SmtpRelayAaddress", 25)
    server.sendmail(from_addr,to_list,msg.as_string())
    server.quit()

urlData = requests.get(fullurl).content
rawData = pd.read_csv(io.StringIO(urlData.decode('utf-8')))
df2 = pd.DataFrame(rawData)
df3 = df2.drop(["Serial Number",], axis = 1)
test3 = (df3[df3['ADDED'].str.contains(date)])
output = (test3[["Device Name","ADDED",'PROCESS NAME','ACTION','TYPE','USER NAME']])
output.to_csv(path+date2+"mem.csv", index = False)
email_data = output.to_html(index = False)
email_send(email_data)
