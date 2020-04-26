import requests
import os
from tkinter import *

listDeviceInfo = []

def resource_path(relative_path):
     if hasattr(sys, '_MEIPASS'):
         return os.path.join(sys._MEIPASS, relative_path)
     return os.path.join(os.path.abspath("."), relative_path)

root = Tk()
root.title("Smart Home")
root.iconbitmap(resource_path("img/icon.ico"))
#root.iconbitmap("./logo.ico")
root.resizable(False, False)
root.config(bg="black")
root.geometry("350x350")

Label(root, text="Smart Home", bg="black", fg="white", font=("Vineta BT", 18)).place(x=175, y=15, anchor="center")

def limitSizeCode(*args):
    value = codeValue.get()
    if len(value) > 6: codeValue.set(value[:6])

def updateDeviceList():
    url = "https://us-central1-smart-house-dbd56.cloudfunctions.net/api/devices/{}".format(codeValue.get())
    r = requests.get(url)
    
    if r.status_code == 200:
        deviceListView.delete(0,'end')
        
        for x in r.json():
            listDeviceInfo.append(x)
            
            nameJson = x["name"]
            deviceName = nameJson["name"];
        
            if 'nicknames' in nameJson:
                deviceName = nameJson["nicknames"][0]
            
            elif 'defaultNames' in nameJson:
                deviceName = nameJson["defaultNames"][0]

            deviceListView.insert(END, deviceName)
            
            

def turnOn():
    deviceData = listDeviceInfo[deviceListView.curselection()[0]]
    sendDeviceCommand(deviceData["id"], "on", {'state': 'true'})

def turnOff():
    deviceData = listDeviceInfo[deviceListView.curselection()[0]]
    sendDeviceCommand(deviceData["id"], "on", {'state': 'false'})

def openDoor():
    deviceData = listDeviceInfo[deviceListView.curselection()[0]]
    sendDeviceCommand(deviceData["id"], "open", {'state': 'true'})
    
def sendDeviceCommand(devideId, param, payload):
    url = "https://us-central1-smart-house-dbd56.cloudfunctions.net/api/devices/{}/{}/{}".format(
        codeValue.get(),
        devideId,
        param
    )
    r = requests.get(url, payload)

def onselect(evt):
    deviceData = listDeviceInfo[deviceListView.curselection()[0]]

    onBtn.place_forget()
    offBtn.place_forget()
    openBtn.place_forget()

    traitsJson = deviceData["traits"]
    if 'action.devices.traits.OnOff' in traitsJson:
        onBtn.place(x=250, y=50, anchor="center")
        offBtn.place(x=300, y=50, anchor="center")

    elif 'action.devices.traits.OpenClose' in traitsJson:
        openBtn.place(x=280, y=50, anchor="center")

codeValue = StringVar()
codeValue.trace('w', limitSizeCode)

entry = Entry(root, bg="black", fg="white", insertbackground='white', textvariable=codeValue)
entry.place(x=80, y=50, anchor="center")

load = Button(root, text="Update", command=updateDeviceList)
load.place(x=190, y=50, anchor="center")

onBtn = Button(root, text="On", command=turnOn)
offBtn = Button(root, text="Off", command=turnOff)
openBtn = Button(root, text="Open", command=openDoor)

deviceListView = Listbox(root, bg="black", fg="white", width=57, height=17)
deviceListView.place(x=0, y=72)
deviceListView.bind('<<ListboxSelect>>', onselect)


#logo = PhotoImage(file="img.gif")
#Label(root, image=logo).place(x=175, y=150, anchor="center")

root.mainloop()
