from . import four_point_transform
from skimage.filters import threshold_local
import cv2
import imutils
import os
from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk

oldPhotosPath = r'Receipt/Unfiltered receipts'
newPhotosPath = r'Receipt/Filtered receipts'
class ScanReceipts(object):
    def __init__(self):
        self.photos = [f for f in os.listdir(oldPhotosPath) if os.path.isfile(os.path.join(oldPhotosPath, f))]
        self.photos_left = []

    def get_photos(self):
        return (self.photos)

    def del_photo(self, name):
        os.remove(r''+ oldPhotosPath + "\\" + name)
        self.photos.remove(name)

    def add_photos_left(self, name):
        self.photos_left.append(name)

    def save_photo(self, path, photo):
        cv2.imwrite(path , imutils.resize(photo, height=650))

    def no_scan(self, img_path):
        save = False

        def save_value():
            nonlocal save
            save = True
            root.destroy()
        def destroy():
            root.destroy()

        root = Tk()
        root.configure(background='light blue')
        root.title("Error occured")
        root.geometry("500x600")

        heading = Label(root, text="Photo did not get scanned. Do you want to save it with scanned photos?", bg="light blue")

        heading.grid(row=0, column=0)

        load = Image.open(img_path)
        load = load.resize((500,500))
        render = ImageTk.PhotoImage(load)
        img = Label(image=render)
        img.image = render
        #image = imutils.resize(image, height=500)
        img.place(x=0, y=60)

        yes = Button(root, text="Yes", fg="Black", bg="light green", command=save_value)
        yes.place(x = 400, y = 20)
        no = Button(root, text="No", fg="Black", bg="red", command=destroy)
        no.place(x = 440, y = 20)

        root.mainloop()
        return save

    def create_photos(self):
        tempPhotos = self.photos[:]
        for item in tempPhotos:
            oldpath = r'' + oldPhotosPath + "\\" + item

            image = cv2.imread(oldpath)
            ratio = image.shape[0] / 500.0
            orig = image.copy()
            image = imutils.resize(image, height=500)

            # convert photos to gray and find edges
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (5, 5), 0)
            edged = cv2.Canny(gray, 75, 200)

            # find the contours in the edged image, keeping only the
            # largest ones, and initialize the screen contour
            cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)
            cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]

            # loop over the contours
            for c in cnts:
                peri = cv2.arcLength(c, True)
                approx = cv2.approxPolyDP(c, 0.02 * peri, True)

                if len(approx) == 4:
                    screenCnt = approx
                    break

            newPath = r'' + newPhotosPath + '\\' + item + '.jpg'
            if len(approx) != 4:
                self.add_photos_left(item)
                save_photo = self.no_scan(oldpath)
                if save_photo:
                    self.save_photo(newPath, image)
                    self.del_photo(item)
                else:
                    self.del_photo(item)
                    continue
            else:
                cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 2)

                warped = four_point_transform.four_point_transform(orig, screenCnt.reshape(4, 2) * ratio)
                warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
                T = threshold_local(warped, 11, offset=10, method="gaussian")
                warped = (warped > T).astype("uint8") * 255

                self.save_photo(newPath, warped)
                self.del_photo(item)
