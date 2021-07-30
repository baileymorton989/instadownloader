from setuptools import setup

with open('READMe.md', 'r') as fh:
    long_description = fh.read()

if __name__ == '__main__':
    setup(
        name = 'instadownloader',
        version = '0.0.1',
        description ='A photo-scraping and photo-storage tool used for generating training sets',
        long_description = long_description,
        long_description_content_type = 'text_markdown',
        author = 'Bailey Morton',
        author_email = 'baileymorton989@gmail.com',
        url = 'https://github.com/baileymorton989/instadownloader',
        license = 'MIT License',
        install_requires = ['instaloader >=4.7.1',
                            'numpy >=1.19.5'],
        py_modules = ['instadownloader'],
        package_dir = {'': 'src'},
        classifiers =[
             'Programming Language :: Python :: 3',
             'Programming Language :: Python :: 3.6',
             'Programming Language :: Python :: 3.7',
             'Programming Language :: Python :: 3.8',
             'Programming Language :: Python :: 3.9',
             'License :: OSI Approved :: MIT License',
             'Operating System :: OS Independent',
        ],
        extras_require = {
            'dev': [
                'pytest>3.7',
                ],
            },

    )