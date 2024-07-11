import tkinter as tk
import os
import csv

from tkinter import ttk, messagebox
from PIL import ImageTk, Image

from datetime import datetime
import pytz

def on_focus_loss(event, List, Country, Timezones, Default):
    try:
        List = pytz.country_timezones[CountryISO2[Country.get()]]
        Timezones['menu'].delete(0, 'end')

        for opt in List:
            Timezones['menu'].add_command(label= opt, command= tk._setit(Default, opt))

    except:
        messagebox.showerror(title= "Error!", message= "Invalid country name.")

def maintain_focus():
    root.lift()
    root.after(1000, maintain_focus)

def resource_path(relative_path):
    try:
        base_path = os.sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def convert_timezone(TimezoneH, TimezoneW, DateH, DateW, fmt):
    date = datetime.strptime(DateH.get(), fmt)
    tzH = pytz.timezone(TimezoneH.get())
    tzW = pytz.timezone(TimezoneW.get())

    date = date.replace(tzinfo= tzH)

    converted_date = date.astimezone(tzW)
    DateW.delete(0, tk.END)
    DateW.insert(0, converted_date.strftime(fmt))

root = tk.Tk()
root.title("Juan/Ruan")
root.geometry("400x100")
root.minsize(400, 100)
root.attributes("-topmost", True)
root.eval('tk::PlaceWindow . center')

root.geometry("+872+550")

icon = ImageTk.PhotoImage(Image.open(resource_path("./juan.png")))
root.iconphoto(False, icon)


CountryISO2 = {}
with open(resource_path("./wikipedia-iso-country-codes.csv")) as document:
        file= csv.DictReader(document, delimiter= ',')
        for line in file:
            CountryISO2[line["English short name lower case"]] = line["Alpha-2 code"]


fmt = "%Y-%m-%d %H:%M:%S" 

HereContainer = tk.Frame(root)
HereContainer.pack(expand= 'yes', fill= 'both')

WhereContainer = tk.Frame(root)
WhereContainer.pack(expand= 'yes', fill= 'both')

OperationsContainer = tk.Frame(root)
OperationsContainer.pack(expand= 'yes', fill= 'both')

CountryHere = ttk.Entry(HereContainer, width=1)
CountryHere.insert(tk.END, "Brazil")

listHere = pytz.country_timezones[CountryISO2[CountryHere.get()]]
timeDefaultHere = tk.StringVar()
timeDefaultHere.set("America/Sao_Paulo")
TimezonesHere = tk.OptionMenu(HereContainer, timeDefaultHere, *listHere)
TimezonesHere.configure(width=1, anchor= 'w')

DateHere = ttk.Entry(HereContainer)
DateHere.insert(tk.END, datetime.now().replace(tzinfo= None).strftime(fmt))

CountryWhere = ttk.Entry(WhereContainer, width=1)
CountryWhere.insert(tk.END, "France")

listWhere = pytz.country_timezones[CountryISO2[CountryWhere.get()]]
timeDefaultWhere = tk.StringVar()
timeDefaultWhere.set("Europe/Paris")
TimezonesWhere = tk.OptionMenu(WhereContainer, timeDefaultWhere, *listWhere)
TimezonesWhere.configure(width=1, anchor= 'w')

DateWhere = ttk.Entry(WhereContainer)

ConvertButton = ttk.Button(OperationsContainer, text= "Convert", command= lambda: convert_timezone(timeDefaultHere, timeDefaultWhere, DateHere, DateWhere, fmt))

CountryHere.pack(ipadx= 40, ipady= 0, side= "left", expand= "no")
TimezonesHere.pack(ipadx= 50, ipady= 0, side= "left", expand= "no")
DateHere.pack(ipadx= 50, ipady= 0, side= "left")

CountryWhere.pack(ipadx= 40, ipady= 0, side= "left", expand= "no")
TimezonesWhere.pack(ipadx= 50, ipady= 0, side= "left", expand= "no")
DateWhere.pack(ipadx= 50, ipady= 0, side= "left")

ConvertButton.pack(ipadx= 20, ipady= 0, side= "right", expand= "no")

CountryHere.bind('<FocusOut>', lambda event: on_focus_loss(event, listHere, CountryHere, TimezonesHere, timeDefaultHere))
CountryHere.bind('<Return>', lambda event: on_focus_loss(event, listHere, CountryHere, TimezonesHere, timeDefaultHere))

CountryWhere.bind('<FocusOut>', lambda event: on_focus_loss(event, listWhere, CountryWhere, TimezonesWhere, timeDefaultWhere))
CountryWhere.bind('<Return>', lambda event: on_focus_loss(event, listWhere, CountryWhere, TimezonesWhere, timeDefaultWhere))

root.mainloop()