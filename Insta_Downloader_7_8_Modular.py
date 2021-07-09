#we will use the script to scrape an insta account and create a file to be used for image-based machine learning tasks

#instagram api
import instaloader

#directory handling
import os 
import shutil
from pathlib import Path
import pickle

#image handling
from PIL import Image
import numpy as np

#making GUIs
import tkinter as tk

#handling dates
from datetime import date

#for warnings
import warnings

#create the tkiner selector object
class TkinterSelector:
        
        #select the profile type
        def profile_selector(self):
            #create the root
            self.root = tk.Tk()
            self.root.geometry("400x300")
            self.root.title('Enter the Profile Type')
            self.label_profile_type = tk.Label(self.root, text='Choose "Public" or "Private"')
            self.entry_profile_type = tk.Entry(self.root)
            self.label_profile_type.pack()
            self.entry_profile_type.pack()
            
            #grab entries
            def enter_profile_info():
                self.profile_type = self.entry_profile_type.get()
                self.root.destroy()
            
            #helper function to pass benefit function
            def get_profile_info():
                self.store = True
                enter_profile_info()
            
            #make buttons
            self.get_profile_button = tk.Button(self.root, text='Submit', command = get_profile_info)
            self.get_profile_button.pack()
            
            #close the GUI
            self.root.mainloop()
            
            #get range of time
            return self.profile_type

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
            if self.profile_type == 'Private':
                self.label_password = tk.Label(self.root, text='Enter Password')
                self.entry_password = tk.Entry(self.root, show ='*')
                self.label_password.pack()
                self.entry_password.pack()
            self.label_photo = tk.Label(self.root, text='Enter "All", "Most Recent", or the N-th most recent photos')
            self.entry_photo = tk.Entry(self.root)
            self.label_photo.pack()
            self.entry_photo.pack()
                        
            #grab entries
            def enter_photo_info():
                self.username = self.entry_username.get()
                if self.profile_type == 'Private':
                    self.password = self.entry_password.get()
                else:
                    self.password = None
                self.photo = self.entry_photo.get()
                self.root.destroy()
            
            #helper function to pass benefit function
            def get_photo_info():
                self.store = True
                enter_photo_info()
            
            #make buttons
            self.get_photo_button = tk.Button(self.root, text='Submit', command = get_photo_info)
            self.get_photo_button.pack()
            
            #close the GUI
            self.root.mainloop()
            
            #get range of time
            return self.username, self.password, self.photo

#instadownloader class
class InstaDownloader:
    
    #initialize with the login credentials
    def __init__(self, username, password, photo_range, profile_type):
        
        self.username = username
        self.password = password
        self.photo_range = photo_range
        self.profile_type = profile_type
        self.today = date.today().strftime("%m_%d_%y")
        
    #start a session
    def start_session(self):
        #Get instance
        self.loader = instaloader.Instaloader()
        
        # Optionally, login or load session
        if self.profile_type == 'Private':
            self.loader.login(self.username, self.password)
        
        #download the photos
        self.profile = instaloader.Profile.from_username(self.loader.context, self.username)
        
        return self.loader, self.profile
        
    #get the most recent image
    def get_most_recent_image(self):
        counter = 0
        self.images = []
        for post in self.profile.get_posts():
            if counter <1:
                self.loader.download_post(post, target=f'{self.profile.username}_{self.today}')
                counter +=1
        for file in os.listdir(Path(os.getcwd()+ f'\\{self.profile.username}_{self.today}\\')):
            if file.find('.jpg')!=-1:
                self.image = Image.open(os.path.join(Path(os.getcwd()+ f'\\{self.profile.username}_{self.today}\\', file)))
                self.images.append(self.image)
        return self.images

    #get any image
    def get_image(self):
        counter = 0
        self.images = []
        for post in self.profile.get_posts():
            if counter < self.photo_range:
                self.loader.download_post(post, target=self.profile.username)
                counter +=1
        for file in os.listdir(Path(os.getcwd()+ f'\\{self.profile.username}_{self.today}\\')):
            if file.find('.jpg')!=-1:
                self.image = Image.open(os.path.join(Path(os.getcwd()+ f'\\{self.profile.username}_{self.today}\\', file)))
                self.images.append(self.image)
        return self.images
    
    #get all images
    def get_all_images(self):
        self.images = []
        for post in self.profile.get_posts():
            self.loader.download_post(post, target=self.profile.username)
        for file in os.listdir(Path(os.getcwd()+ f'\\{self.profile.username}_{self.today}\\')):
            if file.find('.jpg')!=-1:
                self.image = Image.open(os.path.join(Path(os.getcwd()+ f'\\{self.profile.username}_{self.today}\\', file)))
                self.images.append(self.image)
        return self.images
    
    #empty the directory of the newly downloaded files
    def empty_directory(self):
        self.folder = Path(os.getcwd()+ f'\\{self.profile.username}_{self.today}\\')
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
                    
    #save pickle file
    def save_pickle_file(self):
        os.chdir(os.path.join(Path(os.getcwd()+ f'\\{self.profile.username}_{self.today}\\')))
        pickle.dump(self.images, open(f'{self.profile.username}_{self.today}_raw_images.pkl','wb'))
        self.array_images = [np.array(image) for image in self.images]
        pickle.dump(self.array_images, open(f'{self.profile.username}_{self.today}_array_images.pkl','wb'))
                
if __name__ == '__main__':
    
    #filter warnings
    warnings.filterwarnings("ignore")
    
    #get the credentials
    selector = TkinterSelector()
    profile_type = selector.profile_selector()
    username, password, photo_range = selector.photo_entry()
    
    #convert the photo range to integer if downloading range of photos
    try:
        photo_range = int(photo_range)
    except Exception as e:
        print(e)

    #get credentials
    instadownloader = InstaDownloader(username, password, photo_range, profile_type)
    
    #start the session
    loader, profile = instadownloader.start_session()
    
    #download the images
    try:
        if photo_range  == 'All':
            images = instadownloader.get_all_images()
        elif photo_range == 'Most Recent':
            images = instadownloader.get_most_recent_image()
        elif type(photo_range) == int:
            images = images = instadownloader.get_image()
    except Exception as e:
        print(e)
    
    #empty the directory
    instadownloader.empty_directory()
    
    #save pickle file
    instadownloader.save_pickle_file()
