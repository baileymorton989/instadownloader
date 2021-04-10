#we will use the script to scrape an insta account, turn them into NFTs, and then upload them for purchase

#libraries
import instaloader
import os 
import shutil
from pathlib import Path
from PIL import Image
import argparse
import numpy as np

#parse the arguments
def input_credentials():
    username = input('Enter Username: ')
    password = input('Enter Password: ')
    photo_range = int(input('Enter the Index of the Photos: '))
    return username, password, photo_range

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
        self.image  = Image.open(os.path.join(Path(os.getcwd()+ f'\\{self.profile.username}\\',os.listdir(os.getcwd())[0])))
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
