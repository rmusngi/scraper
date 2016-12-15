#scrapes urls from spreadsheets displays questions
import gspread
from oauth2client.service_account import ServiceAccountCredentials


from bs4 import BeautifulSoup
import requests
import pprint
import re
import smtplib

scope = ['https://spreadsheets.google.com/feeds']

credentials = ServiceAccountCredentials.from_json_keyfile_name('Test2-1c041060494e.json', scope)

gc = gspread.authorize(credentials)


#selects the spreadsheet
sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1u7BliswZlNN-Us2RmQPGkaM10uughup3hv9HUlimmD8/edit#gid=0')


worksheet = sh.worksheet('Keywords')
colvalue = "A"  
rownumber = 2

for rownumber in range (2,202):
    try:
        val = worksheet.acell(colvalue +str(rownumber)).value
        url = val    
        #scrape elements
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        #print titles only
        h1 = soup.find("h1", class_= "sg-text--headline")    
        updatecolvalue = "B"    
        worksheet.update_acell(updatecolvalue +str(rownumber), h1.get_text())
    except AttributeError:
        worksheet.update_acell(updatecolvalue +str(rownumber), "ERROR IN SCRAPING QUESTION")
        
print('DONE')

 
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login("pythonrudolph@gmail.com", "rudolph102292")
 
msg = "Hello Rudolph! Your script has successfully scraped new keywords.

Check the link here: https://goo.gl/H9R9XE"
server.sendmail("pythonrudolph@gmail.com", "rudolph.musngi@brainly.com", msg)
print("email sent")
server.quit()
