import requests
import sys
import subprocess
import os

# change these values to the date and time you want to book
username = ""  # username login for recreation.utoronto.ca
password = ""  # password logic for recreation.utoronto.ca
month = '8'    # month of the year, for example august is 8
day   = '06'   # date of the month, for example 4th is 04 and 21 is 21
time  = '[6]'  # time of the day, for example 6pm is '[6] '
am    = '[PM]' # [PM] or [AM]

with requests.Session() as s:
  recreations_page = s.get("https://recreation.utoronto.ca/")
  verification_token = recreations_page.text.split('<input name="__RequestVerificationToken" type="hidden" value="')[1].split('"')[0]
  login = s.post("https://recreation.utoronto.ca/account/signin", data={"Username": username, "Password": password, "__RequestVerificationToken": verification_token, "Redirect": None})

token = login.headers['Set-Cookie'].split(';')[0].split('.AspNet.ApplicationCookie=')[1] 
cwd = os.getcwd()
os.chdir(cwd + "/cogs/CourtBookingFiles/")
command = "python BookCourt.py " +  month + ' ' +  day + ' ' + time + ' ' + am + " 1 " + token
subprocess.run(command, shell=True) 