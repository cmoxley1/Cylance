import requests
import pandas as pd
import arrow
import warnings
import io
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import logging
warnings.filterwarnings('ignore', 'Unverified HTTPS request')
url = "https://protect.cylance.com/Reports/ThreatDataReportV1/memoryprotection/"
token = "Token"
fullurl = (url + token)
path = 'Filepath'
logfile = 'FilePath'
nv = arrow.now()
date = nv.shift(days=-1).format('M/D/YYYY')
date2 = nv.shift(days=-1).format('YYYYMD')
def email_send(email_data):
    from_addr = "EmailFrom"
    to_addr = "EmailTo"
    to_list = ["To_List"]
    msg = MIMEMultipart()
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Subject'] = "Cylance Exploit Attempts for %s" %(date)
    part2 = MIMEText(email_data, 'html')
    msg.attach(part2)
    server = smtplib.SMTP("smtpRelay", 25)
    server.sendmail(from_addr,to_list,msg.as_string())
    server.quit()

if __name__ == '__main__':

    logging.basicConfig(filename=logfile, level=logging.INFO, format='%(asctime)s %(levelname)-8s %(message)s')
    logging.info('Requesting MEM TDR')
    urlData = requests.get(fullurl).content
    rawData = pd.read_csv(io.StringIO(urlData.decode('utf-8')))
    logging.info('Creating dataframe')
    df2 = pd.DataFrame(rawData)
    logging.info('Dropping Serial Column')
    df3 = df2.drop(["Serial Number",], axis = 1)
    logging.info('Filtering Data by date')
    test3 = (df3[df3['ADDED'].str.contains(date)])
    logging.info('Selecting Column Headers')
    output = (test3[["Device Name","ADDED",'PROCESS NAME','ACTION','TYPE','USER NAME']])
    print(output)

    if output.empty:
        logging.info('No Memory Exploit for %s' % (date))

    else:
        logging.info('Creating CSV')
        output.to_csv(path + date2 + "mem.csv", index=False)
        logging.info('CSV Created')
        logging.info('Converting Data to HTML')
        email_data = output.to_html(index = False)
        logging.info('Preparing Email')
        email_send(email_data)
        logging.info('Email Sent')
