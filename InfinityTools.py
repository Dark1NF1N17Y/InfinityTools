import requests
import json
import time
import os
import datetime
import ffmpeg
import tkinter as tkgui
from pymongo import MongoClient
from tkinter import messagebox , PhotoImage
import sys
mongodb = MongoClient("mongodb+srv://Infinity:Unknown0660@infinity.7rzkmhw.mongodb.net/")
database = mongodb["InfinityApps"]
CurrentVersion = "stableWindows(11.0.310324)"
PreRelease = 0
    
###########WorldTime###########
def WorldTime():
    mainmenu.destroy()
    def process():
        city = cityinput.get()
        if city == "Palestine" or city == "palestine" or city == "PALESTINE": city = "Gaza"
        api_url = 'https://api.api-ninjas.com/v1/worldtime?city={}'.format(city)
        response = requests.get(api_url, headers={'X-Api-Key': 'yjH2pODlmO1ZiEryEqgrLQ==CVmm2HS8sNrF6KNv'})
        if response.status_code == requests.codes.ok:
            data = json.loads(response.text)
            hour = data["hour"]
            minute = data["minute"]
            second = data["second"]
            zonetime = data["timezone"]
            devicetime = datetime.datetime.now()
            if zonetime == "Asia/Jerusalem":
                zonetime = "Asia/Gaza"
                city = "Palestine"
            if int(hour)-int(devicetime.hour) < 0:
                message = (f"\n-------------------------------------------------------\n")
                message += (f"\nTime In {city} : {hour}:{minute}:{second} | Device Time : {devicetime.hour}:{devicetime.minute}:{devicetime.second}\n")
                message += (f"\nThe Time In {city} Is Past Of The Device By {int(devicetime.hour)-int(hour)} Hours\n")
                message += (f"\n{city} TimeZone : {zonetime}\n")
                message += (f"\n-------------------------------------------------------\n")
            elif int(hour)-int(devicetime.hour) == 0:
                message = (f"\n-------------------------------------------------------\n")
                message += (f"\nTime In {city} : {hour}:{minute}:{second} | Device Time : {devicetime.hour}:{devicetime.minute}:{devicetime.second}\n")
                message += (f"\nThere Is 0 Hours Difference Between The Device And {city}\n")
                message += (f"\n{city} TimeZone : {zonetime}\n")
                message += (f"\n-------------------------------------------------------\n")
            else:
                message = (f"\n-------------------------------------------------------\n")
                message += (f"\nTime In {city} : {hour}:{minute}:{second} | Device Time : {devicetime.hour}:{devicetime.minute}:{devicetime.second}\n") 
                message += (f"\nThe Time In {city} Is Ahead Of The Device By {int(hour)-int(devicetime.hour)} Hours\n")
                message += (f"\n{city} TimeZone : {zonetime}\n")
                message += (f"\n-------------------------------------------------------\n")
            messagebox.showinfo("- Time Information -" , message)
        else:
            data = json.loads(response.text)
            error = data["error"]
            message = (f"\n-------------------------------\n")
            message += (f"Error : {error}")
            message += (f"\n-------------------------------\n")
            messagebox.showinfo("- Time Information -" , message)

    gui = tkgui.Tk()
    gui.title("- Timezone Lookup -")

    label = tkgui.Label(gui , text = "- Enter City To Lookup -" , pady = 10)
    label.pack()

    cityinput = tkgui.Entry(gui)
    cityinput.pack()

    buttonframe = tkgui.Frame(gui)
    buttonframe.pack()

    search = tkgui.Button(buttonframe , text = "Search" , command = process , width = 10 , height = 1)
    search.pack(side = tkgui.LEFT , padx = 5 , pady = 10)

    frame = tkgui.Frame(gui , width = 400 , bg = "lightgray")
    frame.pack()


    gui.mainloop()           
###########WorldTime###########
    
###########VideoCompressor###########
def VideoCompressor():
    mainmenu.destroy()
    def checkinputs():
        filename = filenameentry.get()
        outputname = outputnameentry.get()
        if filename != outputname:
            if filename.endswith(".mp4"):
                filename = (filename)
            else:
                filename = (filename + ".mp4")

            if outputname.endswith(".mp4"):
                outputname = (outputname)
            else:
                outputname = (outputname + ".mp4")
            if os.path.isfile(filename):
                videoprocess()
            else:
                message = (f"\n-------------------------------------------------------\n")
                message += (f"\nVideo Not Found With Me In The Folder!\n")
                message += (f"\n-------------------------------------------------------\n")
                messagebox.showinfo("- Video Compressor -" , message)
        else:
            message = (f"\n-------------------------------------------------------\n")
            message += (f"\nPlease Change The Output Name!\n")
            message += (f"\n-------------------------------------------------------\n")
            messagebox.showinfo("- Video Compressor -" , message)
    def videoprocess():
        filename = filenameentry.get()
        outputname = outputnameentry.get()
        if filename.endswith(".mp4"):
            filename = (filename)
        else:
            filename = (filename + ".mp4")

        if outputname.endswith(".mp4"):
            outputname = (outputname)
        else:
            outputname = (outputname + ".mp4")
        def compress_video(video_full_path, output_file_name, target_size):  
            message = (f"\n-------------------------------------------------------\n")
            message += (f"\nSee The Process In The Terminal\n")
            message += (f"\nWhen We Finish You Will See Another Message!\n")
            message += (f"\n-------------------------------------------------------\n")
            messagebox.showinfo("- Video Compressor -" , message)
            min_audio_bitrate = 32000
            max_audio_bitrate = 256000
            probe = ffmpeg.probe(video_full_path)
            duration = float(probe['format']['duration'])
            audio_bitrate = float(next((s for s in probe['streams'] if s['codec_type'] == 'audio'), None)['bit_rate'])
            target_total_bitrate = (target_size * 1024 * 8) / (1.073741824 * duration)

            if 10 * audio_bitrate > target_total_bitrate:
                audio_bitrate = target_total_bitrate / 10
                if audio_bitrate < min_audio_bitrate < target_total_bitrate:
                    audio_bitrate = min_audio_bitrate
                elif audio_bitrate > max_audio_bitrate:
                    audio_bitrate = max_audio_bitrate
            video_bitrate = target_total_bitrate - audio_bitrate

            i = ffmpeg.input(video_full_path)
            ffmpeg.output(i, os.devnull,
                  **{'c:v': 'libx264', 'b:v': video_bitrate, 'pass': 1, 'f': 'mp4'}
                  ).overwrite_output().run()
            ffmpeg.output(i, output_file_name,
                  **{'c:v': 'libx264', 'b:v': video_bitrate, 'pass': 2, 'c:a': 'aac', 'b:a': audio_bitrate}
                  ).overwrite_output().run() 
            message = (f"\n-------------------------------------------------------\n")
            message += (f"\nCompressing Completed!\n")
            message += (f"\n-------------------------------------------------------\n")
            messagebox.showinfo("- Video Compressor -" , message)
        compress_video(filename , outputname , 50 * 1000)

    VideoCompressor = tkgui.Tk()
    VideoCompressor.title("- Video Compressor -")

    label = tkgui.Label(VideoCompressor , text = "- Enter File Name -" , pady = 10)
    label.pack()

    filenameentry = tkgui.Entry(VideoCompressor)
    filenameentry.pack()

    label2 = tkgui.Label(VideoCompressor , text = "- Enter Output Name ( Not Used ) -" , pady = 10)
    label2.pack()

    outputnameentry = tkgui.Entry(VideoCompressor)
    outputnameentry.pack()

    buttonframe = tkgui.Frame(VideoCompressor)
    buttonframe.pack()

    process = tkgui.Button(buttonframe , text = "Start" , command = checkinputs , width = 10 , height = 1)
    process.pack(side = tkgui.LEFT , padx = 5 , pady = 10)

    frame = tkgui.Frame(VideoCompressor , width = 400 , bg = "lightgray")
    frame.pack()


    VideoCompressor.mainloop()
###########VideoCompressor###########
    
###########IPLocator###########
def ipinfo():
    mainmenu.destroy()
    def ipsearch():
        ip_address = ipaddress.get()
        url = f"http://ip-api.com/json/{ip_address}?fields=status,message,continent,continentCode,country,countryCode,region,regionName,city,district,zip,lat,lon,timezone,offset,currency,isp,org,as,asname,reverse,mobile,proxy,hosting,query"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            message = (f"\n== IP Information ==\n")
            message += (f"\nIP Address: {data['query']}\n")
            message += (f"\nContinent: {data['continent']} ({data['continentCode']})\n")
            message += (f"\nCountry: {data['country']} ({data['countryCode']})\n")
            message += (f"\nRegion: {data['regionName']} ({data['region']})\n")
            message += (f"\nCity: {data['city']}\n")
            message += (f"\nZip Code: {data['zip']}\n")
            message += (f"\nLatitude: {data['lat']}\n")
            message += (f"\nLongitude: {data['lon']}\n")
            message += (f"\nTimezone: {data['timezone']}\n")
            message += (f"\nCurrency: {data['currency']}\n")
            message += (f"\nISP: {data['isp']}\n")
            message += (f"\nOrganization: {data['org']}\n")
            message += (f"\nAS Number: {data['as']}\n")
            message += (f"\nAS Name: {data['asname']}\n")
            message += (f"\nReverse DNS: {data['reverse']}\n")
            message += (f"\nMobile: {data['mobile']}\n")
            message += (f"\nProxy: {data['proxy']}\n")
            message += (f"\nHosting: {data['hosting']}\n")
            messagebox.showinfo("- IP Information -" , message)
        else:
            message = (f"\n== IP Information ==\n")
            message += (f"Failed To Retrieve IP Information\n")
            messagebox.showinfo("- IP Information -" , message)
    def selfsearch():
        url = f"https://api.seeip.org/jsonip?"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            url = f"http://ip-api.com/json/{data['ip']}?fields=status,message,continent,continentCode,country,countryCode,region,regionName,city,district,zip,lat,lon,timezone,offset,currency,isp,org,as,asname,reverse,mobile,proxy,hosting,query"
            response = requests.get(url)
            data = response.json()
            message = (f"\n== IP Information ==\n")
            message += (f"\nIP Address: {data['query']}\n")
            message += (f"\nContinent: {data['continent']} ({data['continentCode']})\n")
            message += (f"\nCountry: {data['country']} ({data['countryCode']})\n")
            message += (f"\nRegion: {data['regionName']} ({data['region']})\n")
            message += (f"\nCity: {data['city']}\n")
            message += (f"\nZip Code: {data['zip']}\n")
            message += (f"\nLatitude: {data['lat']}\n")
            message += (f"\nLongitude: {data['lon']}\n")
            message += (f"\nTimezone: {data['timezone']}\n")
            message += (f"\nCurrency: {data['currency']}\n")
            message += (f"\nISP: {data['isp']}\n")
            message += (f"\nOrganization: {data['org']}\n")
            message += (f"\nAS Number: {data['as']}\n")
            message += (f"\nAS Name: {data['asname']}\n")
            message += (f"\nReverse DNS: {data['reverse']}\n")
            message += (f"\nMobile: {data['mobile']}\n")
            message += (f"\nProxy: {data['proxy']}\n")
            message += (f"\nHosting: {data['hosting']}\n")
            messagebox.showinfo("- IP Information -" , message)
        else:
            message = (f"\n== IP Information ==\n")
            message += (f"Failed To Retrieve IP Information\n")
            messagebox.showinfo("- IP Information -" , message)
            
    ipinfo = tkgui.Tk()
    ipinfo.title("- IP Information -")

    label = tkgui.Label(ipinfo , text = "- Enter IP Address -" , pady = 10)
    label.pack()

    ipaddress = tkgui.Entry(ipinfo)
    ipaddress.pack()

    buttonframe = tkgui.Frame(ipinfo)
    buttonframe.pack()

    process = tkgui.Button(buttonframe , text = "Check" , command = ipsearch , width = 10 , height = 1)
    process.pack(side = tkgui.LEFT , padx = 5 , pady = 10)

    selfprocess = tkgui.Button(buttonframe , text = "Check Yourself" , command = selfsearch , width = 12 , height = 1)
    selfprocess.pack(side = tkgui.LEFT , padx = 5 , pady = 10)

    frame = tkgui.Frame(ipinfo , width = 400 , bg = "lightgray")
    frame.pack()


    ipinfo.mainloop()
###########IPLocator###########
    
###########Jokes###########
def jokessearch():
    api_url = f"https://api.api-ninjas.com/v1/dadjokes?limit=1"
    response = requests.get(api_url, headers={'X-Api-Key': 'yjH2pODlmO1ZiEryEqgrLQ==CVmm2HS8sNrF6KNv'})
    if response.status_code == requests.codes.ok:
        data = response.json()
        msg = data[0]['joke']
    else:
        msg = "Faild To Get The Joke!"
    message = (f"\n== Joke ==\n")
    message += (f"\n{msg}\n")
    message += (f"\n===========\n")
    messagebox.showinfo("- Jokes -" , message)
###########Jokes###########

###########NATIONALID###########
def nationalid():
    mainmenu.destroy()
    def process():
        national_id = national_input.get()
        if len(national_id) != 14:
            message = (f"\n-----------------------------------------\n")
            message += (f"\nInvalid National ID\n")
            message += (f"\n-----------------------------------------\n")
            messagebox.showinfo("- National ID Info -" , message)
            return

        birth_year = int(national_id[1:3])
        birth_month = int(national_id[3:5])
        birth_day = int(national_id[5:7])
        birth_city_code = int(national_id[7:9])
        gender_digit = int(national_id[12])

        if birth_year <= 3:
                birth_year += 2000
        elif 4 <= birth_year <= 21:
            birth_year += 2000
        elif 22 <= birth_year <= 99:
            birth_year += 1900

        gender = "Female" if gender_digit in [2, 4, 6, 8] else "Male"

        birth_cities = {
            1: "Cairo",
            2: "Alexandria",
            3: "Port_Said",
            4: "Suez",
            11: "Damietta",
            12: "Dakahlia",
            13: "Sharqia",
            14: "Qalyubia",
            15: "Kafr_El_Sheikh",
            16: "Gharbia",
            17: "Monufia",
            18: "Beheira",
            19: "Ismailia",
            21: "Giza",
            22: "Beni_Suef",
            23: "Faiyum",
            24: "Minya",
            25: "Assiut",
            26: "Sohag",
            27: "Qena",
            28: "Aswan",
            29: "Luxor",
            31: "Red Sea",
            32: "New_Valley",
            33: "Matrouh",
            34: "North_Sinai",
            35: "South_Sinai",
            88: "Non_Egyptian"
        }

        birth_city = birth_cities.get(birth_city_code, "Unknown")

        message = (f"\n-----------------------------------------\n")
        message += (f"\nBirth Data : {str(birth_day)}/{str(birth_month)}/{str(birth_year)}\n")
        message += (f"\nGender  : {str(gender)}\n")
        message += (f"\nBirth City  : {str(birth_city)}\n")
        message += (f"\n-----------------------------------------\n")
        messagebox.showinfo("- National ID Info -" , message)

        

    gui = tkgui.Tk()
    gui.title("- National ID Info -")

    label = tkgui.Label(gui , text = "- Enter The Egyptian National ID (14 digits) -" , pady = 10)
    label.pack()

    national_input = tkgui.Entry(gui)
    national_input.pack()

    buttonframe = tkgui.Frame(gui)
    buttonframe.pack()

    search = tkgui.Button(buttonframe , text = "Search" , command = process , width = 10 , height = 1)
    search.pack(side = tkgui.LEFT , padx = 5 , pady = 10)

    frame = tkgui.Frame(gui , width = 400 , bg = "lightgray")
    frame.pack()
    
    gui.mainloop()  
###########NATIONALID###########

###########INFO###########
def info():
        for version in database.AppVersion.find({},{ "_id": 0, "LatestWindows_Version": 1}):
            if(str(version.get("LatestWindows_Version")) != str(CurrentVersion) and PreRelease == 0):
                status = "Outdated"
            elif(str(version.get("LatestWindows_Version")) != str(CurrentVersion) and PreRelease == 1):
                status = "PreRelease"
            else:
                status = "Latest"
            message = (f"\n-------------------------------------------------------\n")
            message += (f"\nDeveloper Name : Fahdsameh\n")
            message += (f"\nApp Version ( {status} ) : {CurrentVersion}\n")
            message += (f"\nRelease Date : 12/2/2024\n")
            message += (f"\nDescription : All In One Tool\n")
            message += (f"\nGithub : https://github.com/Dark1NF1N17Y\n")
            message += (f"\nContact Us : fahdsameh2008@yahoo.com\n")
            message += (f"\n-------------------------------------------------------\n")
            messagebox.showinfo("- App Information -" , message)
###########INFO###########
    
###########MainMenu###########
mainmenu = tkgui.Tk()
for version in database.AppVersion.find({},{ "_id": 0, "LatestWindows_Version": 1}):
            if(str(version.get("LatestWindows_Version")) != str(CurrentVersion) and PreRelease == 0):
                message = (f"\n-------------------------------------------------------\n")
                message += (f"\nNew Update Available!\n")
                message += (f"\nGithub : https://github.com/Dark1NF1N17Y\n")
                message += (f"\nContact Us : fahdsameh2008@yahoo.com\n")
                message += (f"\n-------------------------------------------------------\n")
                messagebox.showinfo("- Update Reminder -" , message)
                mainmenu.title("- 1NF1N17Y Tools ( Outdated ) -")
            elif(str(version.get("LatestWin_Version")) != str(CurrentVersion) and PreRelease == 1):
                mainmenu.title("- 1NF1N17Y Tools ( PreRelease ) -")
            else:
                mainmenu.title("- 1NF1N17Y Tools ( Latest ) -")

label = tkgui.Label(mainmenu , text = "- All In One Tool -" , pady = 10)
label.pack()

buttonframe = tkgui.Frame(mainmenu)
buttonframe.pack()

WorldTime = tkgui.Button(buttonframe , text = "WorldTime" , command = WorldTime , width = 10 , height = 1)
WorldTime.pack(side = tkgui.LEFT , padx = 5 , pady = 10)

VideoCompressor = tkgui.Button(buttonframe , text = "VideoCompressor" , command = VideoCompressor , width = 15 , height = 1)
VideoCompressor.pack(side = tkgui.LEFT , padx = 5 , pady = 10)

ipinfo = tkgui.Button(buttonframe , text = "IP Info" , command = ipinfo , width = 10 , height = 1)
ipinfo.pack(side = tkgui.LEFT , padx = 5 , pady = 10)

buttonframe2 = tkgui.Frame(mainmenu)
buttonframe2.pack()

jokes = tkgui.Button(buttonframe2 , text = "Jokes" , command = jokessearch , width = 10 , height = 1)
jokes.pack(side = tkgui.LEFT , padx = 5 , pady = 10)

buttonframe3 = tkgui.Frame(mainmenu)
buttonframe3.pack()

info = tkgui.Button(buttonframe3 , text = "Info" , command = info , width = 10 , height = 1)
info.pack(side = tkgui.LEFT , padx = 5 , pady = 10)

nationalid = tkgui.Button(buttonframe2 , text = "National ID Info" , command = nationalid , width = 12 , height = 1)
nationalid.pack(side = tkgui.LEFT , padx = 5 , pady = 10)

appexit = tkgui.Button(buttonframe3 , text = "Exit" , command = mainmenu.destroy , width = 10 , height = 1)
appexit.pack(side = tkgui.LEFT , padx = 5 , pady = 10)

frame = tkgui.Frame(mainmenu , width = 400 , bg = "lightgray")
frame.pack()


mainmenu.mainloop()
###########MainMenu###########
