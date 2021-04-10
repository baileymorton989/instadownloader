#import the libraries
from insta-nft import InstaNFT, input_credentials

if __name__ == '__main__':
    
    #get arguments from the command line
    username, password, photo_range = input_credentials()
    
    #get credentials
    instanft = InstaNFT(username, password, photo_range)
    
    #get the image
    images = instanft.get_image()
    
    #empty the directory
    instanft.empty_directory()
