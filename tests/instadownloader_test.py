# -*- coding: utf-8 -*-
"""
Created on Thu Jul 29 23:00:50 2021

@author: bam3k
"""

import instadownloader
import warnings

if __name__ == '__main__':
    
    #filter warnings
    warnings.filterwarnings("ignore")
    
    #get the credentials
    selector = instadownloader.TkinterSelector()
    profile_type = selector.profile_selector()
    username, password, photo_range = selector.photo_entry()
    
    #convert the photo range to integer if downloading range of photos
    try:
        photo_range = int(photo_range)
    except:
        print('Not an integer-based photo range')
        print('')
        
    #get credentials
    instadownloader = instadownloader.InstaDownloader(username, password, photo_range, profile_type)
    
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