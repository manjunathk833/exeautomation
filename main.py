import time
import sys
import os
from selenium import webdriver
from tkinter import *

main_window = Tk()

def on_click():
    # print(testurl.get())
    main_window.quit()

#Labels
l = Label(main_window, text="Enter the url you want to test")
l.pack()

#Text Input
testurl = Entry(main_window, width=50, borderwidth=5 )
testurl.pack()

#Button
buttonclick = Button(main_window, height=1, width=10, text="Commit", command=lambda: on_click())
buttonclick.pack()

main_window.mainloop()

turl = testurl.get()

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)

driver = webdriver.Chrome(resource_path('./driver/chromedriver.exe'))

try:
    driver.get(turl)
    time.sleep(3.0)
finally:
    driver.quit()