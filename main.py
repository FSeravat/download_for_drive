from modules import Drive
import zipfile
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
folders = data["folders"]

for d in drivers:
    drive = Drive.DriveService(d["id"])
    for file in foldersName:
        for folder in folders:
            if not os.path.exists(folder):
                print(folder+" não existe no computador")
                continue
            version = folder.split("\\")
            version = list(filter(lambda x:x.__contains__("Navisworks Manage"),version))[0][-4:]
            fileName = file+"_"+version+".zip"
            fileList = drive.view_all_files(d["folderId"])
            fileId = list(filter(lambda x:x["name"]==fileName, fileList))[0]
            zFile = drive.download_file(fileId["id"])
            with open(os.path.join(folder, fileName),"wb") as f:
                f.write(zFile)
                f.close()
            with zipfile.ZipFile(os.path.join(folder, fileName), mode="r") as archive:
                archive.extractall(folder)
                archive.close()
                folderLocal = os.remove(os.path.join(folder, fileName))
