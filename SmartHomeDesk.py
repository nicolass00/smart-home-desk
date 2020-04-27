import requests
import os
import sqlite3
import keyboard
import json

from tkinter import messagebox
from tkinter import simpledialog
from win10toast import ToastNotifier
from tkinter import *

listDeviceInfo = []

conn = sqlite3.connect('smart-home.db')
c = conn.cursor()
toaster = ToastNotifier()

lastSelec = -1

try :
     # Create table
     c.execute('''CREATE TABLE keywords (deviceId text unique, firstCommand text, secondCommand text)''')
except :
     pass

try :
     # Create table
     c.execute('''CREATE TABLE user (code text unique)''')
except :
     pass

try :
     # Create table
     c.execute('''CREATE TABLE devices (id TEXT PRIMARY KEY, device json)''')
except :
     pass


def resource_path(relative_path):
     if hasattr(sys, '_MEIPASS'):
         return os.path.join(sys._MEIPASS, "img/" + relative_path)
     return os.path.join(os.path.abspath("."), relative_path)

root = Tk()
root.title("Smart Home")
root.iconbitmap(resource_path("icon.ico"))
root.resizable(False, False)
root.config(bg="black")
root.geometry("350x350")

Label(root, text="Smart Home", bg="black", fg="white", font=("Vineta BT", 18)).place(x=175, y=15, anchor="center")

def limitSizeCode(*args):
    value = codeValue.get()
    if len(value) > 6: codeValue.set(value[:6])

def updateDeviceList():
     value = codeValue.get()
     if len(value) == 6:
          c.execute('DELETE FROM user;',);
          c.execute('DELETE FROM devices;',);
          
          c.execute("INSERT INTO user VALUES ('{}')".format(value))
     
          url = "https://us-central1-smart-house-dbd56.cloudfunctions.net/api/devices/{}".format(value)
          r = requests.get(url)
     
          if r.status_code == 200:
               updateList(r.json())
               conn.commit()
               
          elif r.status_code == 401:
               toaster.show_toast("Invalid access token",
                         "Please update the access token and try it again!",
                         icon_path=resource_path("icon.ico"),
                         duration=5,
                         threaded=True)

"""def updateDeviceList():
     value = codeValue.get()
     if len(value) == 6:
          c.execute('DELETE FROM user;',);
          c.execute('DELETE FROM devices;',);
          
          c.execute("INSERT INTO user VALUES ('{}')".format(value))

          devicesJson = json.loads('[{"attributes":{"queryOnlyOpenClose":true},"deviceInfo":{"hwVersion":"0.1","manufacturer":"Tech MNF","model":"SM-D01","swVersion":"0.1"},"id":"door","name":{"defaultNames":["Door"],"name":"SMD010","nicknames":["Puerta casa"]},"traits":["action.devices.traits.OpenClose"],"type":"action.devices.types.DOOR"},{"deviceInfo":{"hwVersion":"0.1","manufacturer":"Tech MNF","model":"SM-D01","swVersion":"0.1"},"id":"door002","name":{"defaultNames":["Door"],"name":"SMD010","nicknames":["Puerta Principal"]},"traits":["action.devices.traits.OpenClose"],"type":"action.devices.types.DOOR"},{"attributes":{"commandOnlyOnOff":true},"deviceInfo":{"hwVersion":"1.0","manufacturer":"Tech MNF","model":"SM-L01","swVersion":"1.0"},"id":"light","name":{"defaultNames":["Bulb"],"name":"SM-Light","nicknames":["Luz pieza"]},"traits":["action.devices.traits.OnOff"],"type":"action.devices.types.LIGHT"},{"attributes":{"commandOnlyOnOff":true},"deviceInfo":{"hwVersion":"0.1","manufacturer":"Tech MNF","model":"SM-L01","swVersion":"0.1"},"id":"light002","name":{"defaultNames":["Bulb"],"name":"SM-Light","nicknames":["Luz bajo mesada"]},"traits":["action.devices.traits.OnOff"],"type":"action.devices.types.LIGHT"},{"attributes":{"commandOnlyOnOff":true},"deviceInfo":{"hwVersion":"0.1","manufacturer":"Tech MNF","model":"SM-L01","swVersion":"0.1"},"id":"light003","name":{"defaultNames":["Bulb"],"name":"SM-Light","nicknames":["Luz comedor"]},"traits":["action.devices.traits.OnOff"],"type":"action.devices.types.LIGHT"},{"attributes":{"commandOnlyOnOff":true},"deviceInfo":{"hwVersion":"0.1","manufacturer":"Tech MNF","model":"SM-L01","swVersion":"0.1"},"id":"light004","name":{"defaultNames":["Bulb"],"name":"SM-Light","nicknames":["Luz cocina"]},"traits":["action.devices.traits.OnOff"],"type":"action.devices.types.LIGHT"},{"attributes":{"commandOnlyOnOff":true},"deviceInfo":{"hwVersion":"1.0","manufacturer":"Tech MNF","model":"SM-L01","swVersion":"1.0"},"id":"light006","name":{"defaultNames":["Bulb"],"name":"SM-Light","nicknames":["Luz computadora","Luz de la computadora"]},"traits":["action.devices.traits.OnOff"],"type":"action.devices.types.LIGHT"},{"attributes":{"commandOnlyOnOff":true},"deviceInfo":{"hwVersion":"0.1","manufacturer":"Tech MNF","model":"SM-O001","swVersion":"0.1"},"id":"outlet","name":{"defaultNames":["Outlet"],"name":"SMOutlet","nicknames":["Computadora"]},"traits":["action.devices.traits.OnOff"],"type":"action.devices.types.OUTLET"},{"attributes":{"commandOnlyOnOff":true},"deviceInfo":{"hwVersion":"1.0","manufacturer":"Tech MNF","model":"SM-O01","swVersion":"1.0"},"id":"outlet001","name":{"defaultNames":["Outlet"],"name":"SM-Outlet","nicknames":["Tele"]},"traits":["action.devices.traits.OnOff"],"type":"action.devices.types.OUTLET"}]');
          updateList(devicesJson)
          conn.commit()"""
            
            

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
     
     if r.status_code == 200:
          toaster.show_toast("Request Success",
                    "The request was made successful!",
                    icon_path=resource_path("icon.ico"),
                    duration=5,
                    threaded=True)
     elif r.status_code == 401:
          toaster.show_toast("Invalid access token",
                    "Please update the access token and try it again!",
                    icon_path=resource_path("icon.ico"),
                    duration=5,
                    threaded=True)
          
     elif r.status_code == 403:
          toaster.show_toast("User device error",
                    "This device can't be controlled by you!",
                    icon_path=resource_path("icon.ico"),
                    duration=5,
                    threaded=True)
   

def updateList(jsonObject):
     global listDeviceInfo
     
     deviceListView.delete(0,'end')
     for x in jsonObject:
          listDeviceInfo.append(x)
          nameJson = x["name"]
          deviceName = nameJson["name"]

          if 'nicknames' in nameJson:
               deviceName = nameJson["nicknames"][0]
          elif 'defaultNames' in nameJson:
               deviceName = nameJson["defaultNames"][0]

          deviceListView.insert(END, deviceName)

          attributes = ""
          if 'attributes' in x:
               attributes = json.dumps(x["attributes"])
               
          c.execute("INSERT INTO devices VALUES ('{}','{}')".format(
               x["id"],
               json.dumps(x)
          ))

def onselect(evt):
     global lastSelec
     
     if len(listDeviceInfo) > deviceListView.curselection()[0]:
          
          deviceData = listDeviceInfo[deviceListView.curselection()[0]]
          traitsJson = deviceData["traits"]
          
          if lastSelec == deviceListView.curselection()[0]:
               text = "Write on and off commands splitted by ';'"
               if 'action.devices.traits.OpenClose' in traitsJson:
                    text = "Write open command"

               settedCommand = ""
                    
               c.execute('SELECT * FROM keywords WHERE deviceId=?', (deviceData["id"],))
               rows = c.fetchall()
                    
               if len(rows) > 0:
                    commands = list(rows[0])
                    settedCommand = commands[1] + ";" + commands[2]
                    
               keyboard_shortcuts = simpledialog.askstring(title="Input keyboard shortcuts",
                                                           initialvalue = settedCommand,
                                                           prompt=text)
               if keyboard_shortcuts:
                    commandList = keyboard_shortcuts.split(";")

                    if len(commandList) > 0:
                         if 'action.devices.traits.OpenClose' in traitsJson and len(commandList) > 1:
                              messagebox.showerror("Error", "For door you cannot choose more than one command")
                              
                         elif 'action.devices.traits.OnOff' in traitsJson and len(commandList) > 2:
                              messagebox.showerror("Error", "For on/off you cannot choose more than two command")
                              
                         else :
                              try :
                                   sqliteSentence = "INSERT INTO keywords VALUES ('{}', '{}', '{}')".format(
                                             deviceData["id"],
                                             commandList[0],
                                             ""
                                   )
                                   if len(commandList) == 2:
                                        sqliteSentence = "INSERT INTO keywords VALUES ('{}', '{}', '{}')".format(
                                             deviceData["id"],
                                             commandList[0],
                                             commandList[1]
                                        )
                                   c.execute(sqliteSentence)
                                             
                              except :
                                   sqliteSentence = "UPDATE keywords SET firstCommand = '{}', secondCommand = '{}' WHERE deviceId = '{}'".format(
                                        commandList[0],
                                        "",
                                        deviceData["id"]
                                   )
                                   if len(commandList) == 2:
                                        sqliteSentence = "UPDATE keywords SET firstCommand='{}', secondCommand='{}' WHERE deviceId='{}'".format(
                                             commandList[0],
                                             commandList[1],
                                             deviceData["id"]
                                        )
                                   c.execute(sqliteSentence)

                              conn.commit()
                              addKeyboardListener(commandList, deviceData["id"])

                    else :
                         messagebox.showerror("Error", "You must write one command")
                         
               else :
                    messagebox.showerror("Error", "You must select at least of one command splitted by ';'")
               lastSelec = -1
               
          else :
               lastSelec = deviceListView.curselection()[0]
          

          onBtn.place_forget()
          offBtn.place_forget()
          openBtn.place_forget()

          if 'action.devices.traits.OnOff' in traitsJson:
               onBtn.place(x=250, y=50, anchor="center")
               offBtn.place(x=300, y=50, anchor="center")

          elif 'action.devices.traits.OpenClose' in traitsJson:
               openBtn.place(x=280, y=50, anchor="center")

def addKeyboardListener(commandList, deviceId):
     if len(commandList) == 1:
          keyboard.add_hotkey(commandList[0], sendDeviceCommand, args=(deviceId, 'open', {'state': 'true'}))
          
     elif len(commandList) == 2:
          keyboard.add_hotkey(commandList[0], sendDeviceCommand, args=(deviceId, 'on', {'state': 'true'}))
          keyboard.add_hotkey(commandList[1], sendDeviceCommand, args=(deviceId, 'on', {'state': 'false'}))

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

try :
     c.execute('SELECT code FROM user')
     codeValue.set(c.fetchone()[0])
except :
     pass

try :
     c.execute('SELECT device FROM devices')
     
     deviceList = list(c.fetchall())
     strDevice = "[" + str(deviceList)[3:len(str(deviceList))-4] + "]"
     strDevice = strDevice.replace("('", "")
     strDevice = strDevice.replace(",)", "")
     strDevice = strDevice.replace("'", "")

     jsonDevice = json.loads(strDevice)
     for x in jsonDevice:
          listDeviceInfo.append(x)
          nameJson = x["name"]
          deviceName = nameJson["name"]

          if 'nicknames' in nameJson:
               deviceName = nameJson["nicknames"][0]
          elif 'defaultNames' in nameJson:
               deviceName = nameJson["defaultNames"][0]
          deviceListView.insert(END, deviceName)
except :
     pass

try :
     c.execute('SELECT * FROM keywords')
     commandTuple = c.fetchall()
     for command in commandTuple:
          commandList = []
          commandList.append(command[1])
          commandList.append(command[2])

          deviceId = command[0]
          
          addKeyboardListener(commandList, deviceId)
except :
     pass

#keyboard.add_hotkey('ctrl+shift+a', sendDeviceCommand, args=("light006", 'on', {'state': 'true'}))
#keyboard.add_hotkey('ctrl+shift+b', sendDeviceCommand, args=("light006", 'on', {'state': 'false'}))

#logo = PhotoImage(file="img.gif")
#Label(root, image=logo).place(x=175, y=150, anchor="center")

root.mainloop()
conn.close()
