import cv2
import pytesseract
import os
from tkinter import *
import tkinter as tk
import imutils
from PIL import Image, ImageTk
from datetime import date

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
#to use pytesseract it is needed to give exect path.
path = r'Receipt\Filtered receipts'

def get_name_price(item):
    img = cv2.imread(item)
    text = pytesseract.image_to_string(img)
    text_lines = text.splitlines()
    name = text_lines[0]

    sub = 0
    subDone = False
    tax = 0
    taxDone = False
    total = 0
    totalDone = False
    max_val = 0
    day = date.today()
    for line in text_lines[::-1]:
        if '$' in line:
            curr = 0
            try:
                curr = float(line.split('$')[1])
            except:
                curr = 0
            max_val = max(max_val, curr)

        if ("SUBTOTAL" in line.upper() or "SUB TOTAL" in line.upper()) and not subDone and totalDone:
            try:
                sub = float(line.split('$')[1])
            except:
                sub = 0
            subDone = True
        if "TAX" in line.upper():
            try:
                tax = float(line.split('$')[1])
                taxDone = True
            except:
                tax = 0
                taxDone = False
        if ("TOT" in line.upper() or "TOTA" in line.upper() or "TOTAL" in line.upper()) and not totalDone and not subDone:
            try:
                total = float(line.split('$')[1])
            except:
                total = 0
            totalDone = True

    if total != tax + sub or max_val != total:
        if tax <= 0.2 * sub and taxDone and sub > 0:
            total = sub + tax
        else:
            total = max_val

    return (name, total)

def conf_popup(name, total, img_path, theDate):
    name_final = name
    total_final = total
    date_use = theDate
    def focus1(event):
        comp_field.focus_set()
    def focus2(event):
        price_field.focus_set()
    def save_value():
        nonlocal name_final
        nonlocal total_final
        nonlocal date_use
        name_final = comp_field.get()
        total_final = price_field.get()
        date_use = date_field.get()
        root.destroy()

    root = Tk()
    root.configure(background='light blue')
    root.title("Confirm info")
    root.geometry("350x600")

    heading = Label(root, text="", bg="light blue")
    comp = Label(root, text="Company", bg="light blue")
    price = Label(root, text="Price", bg="light blue")
    date_lab = Label(root, text="Date", bg="light blue")

    #img = ImageTk.PhotoImage(Image.open(img_path))
    #panel = tk.Label(root, image = img)
    #panel.pack(side = "bottom", fill = "both", expand = "yes")

    heading.grid(row=0, column=1)
    comp.grid(row=1, column=0)
    price.grid(row=2, column=0)
    date_lab.grid(row=3, column=0)

    load = Image.open(img_path)
    render = ImageTk.PhotoImage(load)
    img = Label(image=render)
    img.image = render
    img.place(x=0, y=120)

    comp_field = Entry(root)
    comp_field.delete(0, tk.END)
    comp_field.insert(0, name)
    price_field = Entry(root)
    price_field.delete(0, tk.END)
    price_field.insert(0, total)
    date_field = Entry(root)
    date_field.delete(0, tk.END)
    date_field.insert(0, date_use)


    comp_field.bind("<Return>", focus1)
    price_field.bind("<Return>", focus2)
    comp_field.grid(row=1, column=1, ipadx="70")
    price_field.grid(row=2, column=1, ipadx="70")
    date_field.grid(row=3, column=1, ipadx="70")

    submit = Button(root, text="Save receipt", fg="Black", bg="light green", command=save_value)
    submit.grid(row=4, column=1)

    root.mainloop()

    return (name_final, total_final, date_use)

def unique_name(path, counter):
    if os.path.exists(path + '.jpg'):
        path = path + "_" + str(counter)
        if os.path.exists(path + '.jpg'):
            return unique_name(path, counter + 1)
        else:
            return path
    else:
        return path


def save_receipts():
    photos = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    for item in photos:
        theDate = item.split('_')[0]
        (name, price) = get_name_price(path + "\\" + item)
        (name, price, theDate) = conf_popup(name, str(price), path + "\\" + item, theDate)
        path_photo = r''+ path + "\\" + name
        check_comp = os.path.isdir(path_photo)
        image = cv2.imread(path + "\\" + item)
        if check_comp:
            unique_path = unique_name(path_photo + "\\" + theDate + "_" + price, 0)
            cv2.imwrite(unique_path + '.jpg', image)
            os.remove(r'' + path + "\\" + item)
        else:
            os.mkdir(path_photo)
            cv2.imwrite(path_photo + "\\" + theDate + "_" + price + '.jpg', image)
            os.remove(r'' + path + "\\" + item)

save_receipts()
