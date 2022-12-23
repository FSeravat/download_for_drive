from modules import Drive
from modules import EmailSender
import json
import os
import logging
import datetime

date = datetime.datetime.now()
date = date.strftime("%Y_%m_%d_%H_%M")

try:
    logging.basicConfig(filename='log\\'+date+'.log', filemode="w" ,level=logging.DEBUG)
except FileNotFoundError:
    os.mkdir(os.getcwd()+"\\log")
    logging.basicConfig(filename='log\\'+date+'.log', filemode="w" ,level=logging.DEBUG)

try:
    data = json.load(open("settings.json", encoding='utf-8'))
except FileNotFoundError:
    logging.exception("settings.json não encontrado")
    os.system("pause")
    exit(0)
    


foldersName = data["files_name"]
drivers = data["drivers"]

for d in drivers:
    drive = Drive.DriveService(d["id"])
    for file in foldersName:
        fileList = drive.view_all_files(d["folderId"])
        fileId = list(filter(lambda x:x["name"]==file+"_2020.zip", fileList))[0]
        print(fileId["id"])
        print(fileId["mimeType"])


