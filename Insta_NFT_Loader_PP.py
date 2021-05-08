# -*- coding: utf-8 -*-
"""
Created on Sun Apr  4 23:33:24 2021

@author: bam3k
"""

#we will use the script to scrape an insta account, turn them into NFTs, and then upload them for purchase

#libraries
import instaloader
import os 
import shutil
from pathlib import Path
from PIL import Image
import tkinter as tk
from tkinter import filedialog
import urllib
import base64

#parse the arguments
def input_credentials():
    username = input('Enter Username: ')
    password = input('Enter Password: ')
    photo_range = int(input('Enter the Index of the Photos: '))
    return username, password, photo_range

#create the tkiner selector object
class TkinterSelector:
        
        #select the benefit and dates
        def photo_entry(self):            
            #create the root
            self.root = tk.Tk()
            self.root.geometry("400x300")
            self.root.title('Enter the Credenentials and Select Photos')
            self.label_username = tk.Label(self.root, text='Enter Username')
            self.entry_username= tk.Entry(self.root)
            self.label_username.pack()
            self.entry_username.pack()
            self.label_password = tk.Label(self.root, text='Enter Password')
            self.entry_password = tk.Entry(self.root)
            self.label_photo = tk.Label(self.root, text='Enter "All", "Most Recent", or the N-th most recent photos')
            self.entry_photo = tk.Entry(self.root)
            self.label_password.pack()
            self.entry_password.pack()
            self.label_photo.pack()
            self.entry_photo.pack()
            
            #grab entries
            def enter_info():
                self.username = self.entry_username.get()
                self.password = self.entry_password.get()
                self.photo = self.entry_photo.get()
                self.root.destroy()
            
            #helper function to pass benefit function
            def get_info():
                self.store = True
                enter_info()
            
            #make buttons
            self.get_photo_button = tk.Button(self.root, text='Submit', command = get_info)
            self.get_photo_button.pack()
            
            #close the GUI
            self.root.mainloop()
            
            #get range of time
            return self.username, self.password, self.photo

#InstaNFT class
class InstaNFT:
    
    #initialize with the login credentials
    def __init__(self, username, password, photo_range):
        
        self.username = username
        self.password = password
        self.photo_range = photo_range
         
    #get the most recent image
    def get_most_recent_image(self):

        #Get instance
        self.loader = instaloader.Instaloader()
        
        # Optionally, login or load session
        self.loader.login(self.username, self.password)
        
        #download the photos
        self.profile = instaloader.Profile.from_username(self.loader.context, self.username)
        counter = 0
        for post in self.profile.get_posts():
            if counter <1:
                self.loader.download_post(post, target=self.profile.username)
                counter +=1
        for file in os.listdir(Path(os.getcwd()+ f'\\{self.profile.username}\\')):
            if file.find('.jpg')!=-1:
                self.image = Image.open(os.path.join(Path(os.getcwd()+ f'\\{self.profile.username}\\', file)))
        return self.image

    #get any image
    def get_image(self):

        #Get instance
        self.loader = instaloader.Instaloader()
        
        # Optionally, login or load session
        self.loader.login(self.username, self.password)
        
        #download the photos
        self.profile = instaloader.Profile.from_username(self.loader.context, self.username)
        counter = 0
        self.images = []
        for post in self.profile.get_posts():
            if counter < self.photo_range:
                self.loader.download_post(post, target=self.profile.username)
                counter +=1
        for file in os.listdir(Path(os.getcwd()+ f'\\{self.profile.username}\\')):
            if file.find('.jpg')!=-1:
                self.image = Image.open(os.path.join(Path(os.getcwd()+ f'\\{self.profile.username}\\', file)))
                self.images.append(self.image)
        return self.images
    
    #get all images
    def get_all_images(self):

        #Get instance
        self.loader = instaloader.Instaloader()
        
        # Optionally, login or load session
        self.loader.login(self.username, self.password)     
        
        #download the photos
        self.profile = instaloader.Profile.from_username(self.loader.context, self.username)
        self.images = []
        for post in self.profile.get_posts():
            self.loader.download_post(post, target=self.profile.username)
        for file in os.listdir(Path(os.getcwd()+ f'\\{self.profile.username}\\')):
            if file.find('.jpg')!=-1:
                self.image = Image.open(os.path.join(Path(os.getcwd()+ f'\\{self.profile.username}\\', file)))
                self.images.append(self.image)
        return self.images
    
    #empty the directory of the newly downloaded files
    def empty_directory(self):
        self.folder = Path(os.getcwd()+ f'\\{self.profile.username}\\')
        for filename in os.listdir(self.folder):
            self.file_path = os.path.join(self.folder, filename)
            if self.file_path.find('.jpg') == -1:
                try:
                    if os.path.isfile(self.file_path) or os.path.islink(self.file_path):
                        os.unlink(self.file_path)
                    elif os.path.isdir(self.file_path):
                        shutil.rmtree(self.file_path)
                except Exception as e:
                    print('Failed to delete %s. Reason: %s' % (self.file_path, e))
                    
    #connect to your digital wallet
    def connect_to_digital_wallet(self):
        pass
        
if __name__ == '__main__':
    
    #get the credentials
    selector = TkinterSelector()
    username, password, photo_range = selector.photo_entry()
    
    #convert the photo range to integer if downloading range of photos
    try:
        photo_range = int(photo_range)
    except:
        print('Not an integer')

    #get credentials
    instanft = InstaNFT(username, password, photo_range)
    
    #download the images
    try:
        if photo_range  == 'All':
            images = instanft.get_all_images()
        elif photo_range == 'Most Recent':
            images = instanft.get_most_recent_image()
        elif type(photo_range) == int:
            images = images = instanft.get_image()
    except Exception as e:
        print(e)
    
    #empty the directory
    instanft.empty_directory()