import tkinter as tk
from tkinter import *
from tkinter.ttk import *
import tkinter.font as font
from tkinter import messagebox
import math

import os
import sys
import csv

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


with open(resource_path('FullEmployeeList.csv'), mode="r", encoding="utf-8", newline='') as f:
    reader = csv.reader(f)
    next(reader)
    dpt = dict(reader)  


newDict = {}

def export(eN, tH):
    # print("this is the export function")
    if eN not in dpt: 
        print("Employee name is not found in the database")
    else:
        newDict[eN] =  tH
        print(newDict)

    return None


def createCSV(d):
    nn = numDays_entry.get()
    # print("this is the createCSV function")
    b = f'Total hours worked in {nn} days'
    headers = ['Employee Name', b]
    x = [{'Employee Name':key, b:value} for key, value in newDict.items()]  # Make a list of dictionaries
    with open('Time-Sheet.csv', 'w' , encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = headers)
        writer.writeheader()
        writer.writerows(x)
    return None

def generateData(): 
    roundedTotalHours = None
    dailyHours = None
    numberofDays = None
    employeeName = None
    e = empName_entry.get()
    n =  numDays_entry.get()

    if len(e) == 0 or len(n) == 0:
        messagebox.showwarning("Warning!", "Employee name or Number of working days is not filled!")
    else:
        employeeName = empName_entry.get()
        numberofDays = int(float(numDays_entry.get()))

        if employeeName in dpt:
            employeeRate = float(dpt[employeeName])
            dailyHours = employeeRate * 8
            totalHours = dailyHours * numberofDays
            roundedTotalHours = round(totalHours, 2)
            
            print(employeeName, "worked a total of", roundedTotalHours, "hours in",numberofDays, "days")
            print(employeeName, "worked for", dailyHours, "hours everyday in", numberofDays, "days")
            
        else:
            messagebox.showwarning("Warning!", "There is no such employee in the database!")
            print("There is no employee with the name", employeeName, "in the database!")

    export(employeeName, roundedTotalHours)

    r = f'{employeeName} worked a total of: {roundedTotalHours} hours in {numberofDays} days'
    output_result.config(text=r)

    return (roundedTotalHours, dailyHours)


window = tk.Tk()
window.title("Employee TimeSheet")

def on_closing():
    createCSV(newDict)
    # print("this is the on_closing function")
    window.destroy()

frame = tk.Frame(window)
frame.pack()

#user info frame ///////////////////////////////////////////////////////////
user_info_frame = tk.LabelFrame(frame, text="User Information")
user_info_frame.grid(row=0, column=0, padx=10, pady=20)

empty_top_padding = tk.Label(user_info_frame)
empty_top_padding.grid(row=0, column=0)

#employee name
empName = tk.Label(user_info_frame, text="Enter Employee Name:", font=("Helvetica", 12))
empName.grid(row=1, column=0)
empName_entry = tk.Entry(user_info_frame, width=18, font=("Helvetica", 18))
empName_entry.grid(row=2, column=0)

#number of days
numDays = tk.Label(user_info_frame, text="Enter Number of working days:", font=("Helvetica", 12))
numDays.grid(row=3, column=0)
numDays_entry = tk.Entry(user_info_frame, width=5, font=("Helvetica", 18))
numDays_entry.grid(row=4, column=0, pady=5)

empty_bottom_padding = tk.Label(user_info_frame)
empty_bottom_padding.grid(row=5, column=0)


for widget in user_info_frame.winfo_children():
    widget.grid_configure(padx=30, pady=8)

#button frame ////////////////////////////////////////////////////////////
button_frame = tk.LabelFrame(frame)
button_frame.grid(row=1, column=0, sticky="news", padx=20, pady=5)

f = tk.font.Font(size=14)
generate_text = tk.StringVar()
generate_btn = tk.Button(button_frame, textvariable=generate_text, font=("Helvetica Neue LT Com", 20), bg='#d5ae68', fg='black', height=3, width=45, command=generateData)
generate_text.set("Click to Generate working hours")
# generate_btn['font'] = f
generate_btn.grid(column=1, row=6, columnspan=2, rowspan=5)


# output frame //////////////////////////////////////////////////////////
output_frame = tk.LabelFrame(frame, text="Results")
output_frame.grid(row=2, column=0, padx=20, pady=20)

inner_frame = tk.Frame(output_frame, bg="white", padx=20, pady=20, width=150)
inner_frame.grid(row=0, column=0)

# output_result_var = StringVar()
output_result = tk.Label(inner_frame, background="white", fg="#05336e", text="You will see the results here... ", font=("Helvetica Oblique", 12))
# output_result = tk.Label(inner_frame, textvariable=output_result_var, background="white", text="You will see the results here... ")
output_result.grid(row=0, column=0)

for widget in output_frame.winfo_children():
    widget.grid_configure(padx=10, pady=10)

window.resizable(width=False, height=False)
window.protocol("WM_DELETE_WINDOW", on_closing)
window.mainloop()





