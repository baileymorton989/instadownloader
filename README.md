# instadownloader

`instadownloader` is a Python library built on top of [instaloader](https://instaloader.github.io/) for scraping and storing Instagram photos to generate training datasets. It is currently designed so that a user can download "All Photos", the "Most Recent" Photo, or the Nth-Most Recent Photos, for both public and private users. For private users, the login credentials must be provided.

The script will save .jpg files for the photos downloaded, a pickle file with the raw .jpg files and a pickle file with the photos converted to numpy arrays. These photos will be stored in a folder with the following format : {username}_{today's date}, where today's date is in the format "MM_DD_YY".

To read more about the documentation, visit the [src](https://github.com/baileymorton989/instadownloader/tree/main/src) folder.

## Installation

Installation is made simple by using [pip](https://pip.pypa.io/en/stable/)

```bash
pip install instadownloader
```

## Usage

Here is a simple example. A tkinter GUI will be used and all the user will need to do is choose whether the profile is public or private, provide the account name, a password if the account is private, as well the photo range that they desire.

Example : 

```python
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
```
These examples and other can be found in the [examples](https://github.com/baileymorton989/instadownloader/tree/main/examples) folder.

## Contributing
We are open to pull requests and look forward to expanding this library further to tackle more complex games. Please open an issue to discuss any changes or improvements.
To install `instadownloader`, along with the tools you need to develop and run tests, run the following in your virtualenv:

```bash
$pip install -e .[dev]
```

## License

[MIT](https://choosealicense.com/licenses/mit/)
