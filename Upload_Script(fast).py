import os
from zipfile import ZipFile
from os import walk
import sys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
from time import sleep
from datetime import datetime

my_mail = "opustempdan@gmail.com"
os.chdir("/home/daniel/Desktop/stations")
current_directory = os.getcwd()
print(current_directory)
zip_list = []
chunks=[]


def Upload(file):
        my_file = os.path.abspath(file)
        driver = webdriver.Chrome("/usr/local/bin/chromedriver")
        driver._is_remote = False

        driver.get("https://www.ngs.noaa.gov/OPUS/")
        assert "OPUS" in driver.title

        upload = driver.find_element_by_name("uploadfile")
        upload.send_keys(my_file)

        dropdown = driver.find_element_by_name("ant_type")
        select = Select(dropdown)
        select.select_by_value("TRM55970.00     NONE")
        height = driver.find_element_by_name("height")
        height.clear()
        height.send_keys("2.000")
        email = driver.find_element_by_name("email_address")
        email.send_keys(my_mail)

        driver.find_element_by_name("Static").click()

        try:
            if driver.find_element_by_name("cancelButton") == True:
                driver.quit()
                return True
        except TimeoutException:
            print("Page timed out!")
            driver.quit()
            return False 


startTime = datetime.now()

#add all .Z file to a list named zip_list
for f in os.listdir(current_directory): 
        if f.endswith('.Z'):
                zip_list.append(f)

#append chunks of 50 files onto a list called chunks
for item in range(0,len(zip_list),50):
        chunks.append(zip_list[item:item+50])

#give index to each chunk of 50 files and zip them with as *index*.zip
for index,chunk_1 in enumerate(chunks):
        with ZipFile(str(index) + '.zip', 'w') as myzip:
                for files in chunk_1:
                                myzip.write(files)
#remove all the .Z files                                
for file in os.listdir(current_directory):
        if file.endswith('.Z'):
                os.remove(file)
#Uploads each zip file 
for file in os.listdir(current_directory):
        if file.endswith('.zip'):
                Upload(file)


startTime = datetime.now()

print('Upload took',datetime.now() - startTime)
