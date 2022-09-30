
import requests
from time import sleep
import requests
from bs4 import BeautifulSoup
import threading
import re
import json
from datetime import datetime

paivat = ["Maanantai", "Tiistai", "Keskiviikko", "Torstai", "Perjantai", "Lauantai", "Sunnuntai"]


def auth():
    global session_items
    with open("wilmaScheduleConfig.json", "r") as file: config = json.loads(file.read())
    session = requests.Session()
    r = session.get("https://espoo.inschool.fi/index_json")

    sessionid = r.json()["SessionID"]
    payload = {
        "Login": config["settings"]["username"],
        "Password": config["settings"]["password"],
        "submit": "Kirjaudu sisään",
        "SESSIONID": sessionid,
        "format": "json"
    }
    r = session.post("https://espoo.inschool.fi/login", data=payload)

    session_items = session.cookies.get_dict()

day = datetime.today().weekday()

aineet = []
groupids = []
tomorrows_classes = []

dingdongit = {
    "huomisen_tunnit": [],
    "kokeet": [
        
    ],
    "laksyt": [
    ]
    
}


def get_schedule(param=None):
    global aikataulu
    HEADERS = {
    "Cookie": "Wilma2SID=" + session_items["Wilma2SID"] + ";",
    "format": "json"
    
}

    url = "https://espoo.inschool.fi/schedule"
    if param:
        url += f"?{param}"
    
    
    r = requests.get(url, headers=HEADERS)
    #print(r.text)
    
    soup = BeautifulSoup(r.text, 'html.parser')
    gay = str(soup.find_all("script")[-1])
    gay = gay.replace('<script type="text/javascript">', "").replace('      </script>', "").replace('        var weekdays = ["Maanantai","Tiistai","Keskiviikko","Torstai","Perjantai","Lauantai","Sunnuntai"];', "").replace(";", "").replace("var eventsJSON = ", "").replace(" ", "").replace("ViewOnly:true,DayCount:5,DayStarts:490,DayEnds:945,Events:", '"ViewOnly":"true","DayCount":5,"DayStarts":490,"DayEnds":945,"Events":').replace('ActiveTyyppi:"",ActiveId:"",DialogEnabled:0', '"ActiveTyyppi":"","ActiveId":"","DialogEnabled":0').replace("ä", "a").replace("ö", "o").replace("Ä", "A").replace("Ö", "O")
    
    gay = eval(gay)["Events"]
    print(gay)
    aikataulu = {
        "schedule": [
        ]
    }
    goober = {
        "goofy": [
            
        ]
        }
    for count, key in enumerate(gay):
        
        aine = key["LongText"]["0"].replace("lkaste:8", "")
        if not aine:
            aine = "Unknown. Mahdollisesti lv-tuokio?"
        alkaa = key["Start"]
        
        end = key["End"]
        paiva = key["ViikonPaiva"]
        try:
            if gay[count+1]["Start"] > end:
                valitunti = True
            else:
                valitunti = False
        except IndexError:
            valitunti = False
        
        def get_time(total_minutes):
            hours = total_minutes // 60

            # Get additional minutes with modulus
            minutes = total_minutes % 60
            if minutes < 10:
                minutes = f"0{minutes}"
                
                print(minutes)
            

            # Create time as a string
            return "{}:{}:00".format(hours, minutes)
        starttime = get_time(int(alkaa))
        endtime = get_time(int(end))
        thingimabobjson = {
            "tunninalku": starttime,
            "tunti": aine
            }
        if count == 0:
            last_day = paiva
        if last_day != paiva:
            thingimabobjson = {
                "tunninalku": get_time(int(gay[count-1]["End"])),
                "tunti": "Kotiin!"
            }
            
            
            goober["goofy"].append(thingimabobjson)
            
            aikataulu["schedule"].append(goober["goofy"])
            goober = {
                "goofy": [
                    
                ]
                }
            print(gay[count+1]["Start"] - end)
            if end < gay[count+1]["End"]:
                valitunti = True
            else:
                valitunti = False
            thingimabobjson = {
                "tunninalku": starttime,
                "tunti": aine
            }
            
            
            goober["goofy"].append(thingimabobjson)
            last_day = paiva
        
        else:
            goober["goofy"].append(thingimabobjson)
                
        if valitunti:
            thingimabobjson = {
                    "tunninalku": endtime,
                    "tunti": "Valitunti"
                }
                
                
            goober["goofy"].append(thingimabobjson)
        
        #print(goober)
            
        
            
            
        
            
        
        try:
            ope = key["OpeInfo"]["0"]["0"]["nimi"]
        except:
            pass
            ope = None
        

        
        last_day = paiva
        #print(type(ope))
        
        #print(aine, ope, paiva)
        
        if count >= len(gay) -1:
            
            thingimabobjson = {
                "tunninalku": get_time(int(gay[count]["End"])),
                "tunti": "Kotiin!"
            }
            
            
            goober["goofy"].append(thingimabobjson)
            aikataulu["schedule"].append(goober["goofy"])
    #print(aikataulu)
    with open("aikataulu.json", "w") as file: file.write(json.dumps(aikataulu, indent=4))


def schedule_dingong(param=None):
    global aineet, groupids, paivat, day, tomorrows_classes, dingdongit
    HEADERS = {
    "Cookie": "Wilma2SID=" + session_items["Wilma2SID"] + ";",
    "format": "json"
    
}

    url = "https://espoo.inschool.fi/schedule"
    if param:
        url += f"?{param}"
    
    
    r = requests.get(url, headers=HEADERS)
    #print(r.text)
    
    soup = BeautifulSoup(r.text, 'html.parser')
    gay = str(soup.find_all("script")[-1])
    gay = gay.replace('<script type="text/javascript">', "").replace('      </script>', "").replace('        var weekdays = ["Maanantai","Tiistai","Keskiviikko","Torstai","Perjantai","Lauantai","Sunnuntai"];', "").replace(";", "").replace("var eventsJSON = ", "").replace(" ", "").replace("ViewOnly:true,DayCount:5,DayStarts:490,DayEnds:945,Events:", '"ViewOnly":"true","DayCount":5,"DayStarts":490,"DayEnds":945,"Events":').replace('ActiveTyyppi:"",ActiveId:"",DialogEnabled:0', '"ActiveTyyppi":"","ActiveId":"","DialogEnabled":0').replace("ä", "a").replace("ö", "o").replace("Ä", "A").replace("Ö", "O")
    
    gay = eval(gay)["Events"]
    #with open("res.json", "w") as file: file.write(json.loads(gay))
    
    for count, key in enumerate(gay):
        
        
        alkaa = key["Start"]
        
        end = key["End"]
        paiva = key["ViikonPaiva"]
        aine = key["Text"]["0"]
        groupid = key["ArvKirjaNro"]["0"]
        if aine not in aineet:
            print(aine, groupid)
            aineet.append(aine) 
            groupids.append(groupid)
        
        if paiva == paivat[day] or paiva == paivat[day + 1]:
            tomorrows_classes.append(aine)
        
        print(tomorrows_classes)
        dingdongit["huomisen_tunnit"] = tomorrows_classes
        
def get_homework(param=None):
    global aineet, groupids, dingdongit
    HEADERS = {
    "Cookie": "Wilma2SID=" + session_items["Wilma2SID"] + ";",
    "format": "json"
    
}
    

    

    schedule_dingong()
    for aine_index, gid in enumerate(groupids):
        if aineet[aine_index] in tomorrows_classes:
            url = f"https://espoo.inschool.fi/groups/{gid}"
            if param:
                url += f"?{param}"
            
            
            r = requests.get(url, headers=HEADERS)
            #print(r.text)
            
            soup = BeautifulSoup(r.text, 'html.parser')
            gay = soup.find_all(["table"], {"class": ["table allow-printlink datatable gridtable"]})
            #print(gay[0])
            
            for c, g in enumerate(gay):
                ok = gay[c].find("tbody")
                ok = ok.find_all("tr")
                if c not in (1, 3):
                    for count, table in enumerate(ok):
                        ko_element = {
                                            "kokeen-aihe": "",
                                            "paivamaara": "",
                                            "lisatiedot": ""
                                        }
                        laksy_element = {
                                "aine": "",
                                "tehtavat": "",
                                "paivamaara": ""
                            }
                        for i, element in enumerate(table.find_all("td")):
                            if c == 0:
                                if i == 0: ko_element["paivamaara"] = element.text
                                elif i == 2: ko_element["lisatiedot"] = element.text.replace("ä", "a").replace("ö", "o").replace("Ä", "A").replace("Ö", "O")
                                elif i == 3:
                                    ko_element["kokeen-aihe"] = element.text.replace("ä", "a").replace("ö", "o").replace("Ä", "A").replace("Ö", "O")
                                    dingdongit["kokeet"].append(ko_element)
                            elif c == 2:
                                if i == 0: laksy_element["paivamaara"] = element.text
                                elif i == 1:
                                    laksy_element["tehtavat"] = element.text.replace("ä", "a").replace("ö", "o").replace("Ä", "A").replace("Ö", "O")
                                    laksy_element["aine"] = aineet[aine_index]
                                    dingdongit["laksyt"].append(laksy_element)
    with open("homework.json", "w") as file: file.write(json.dumps(dingdongit, indent=4))
        

auth()
get_homework()