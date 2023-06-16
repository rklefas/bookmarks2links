import bookmarks_parser
import configparser
import filedate
import glob
import os
from pathlib import Path
import time
import re

config = configparser.RawConfigParser()
config.optionxform = str


def clean_title(x):

    x = re.sub("[\W]", "_", x)
    x = re.sub("_+", " ", x).strip()
    x = x[0:100]
    
    return x
    

def convert_date(added):
    if added == None:
        added = time.time()

    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(added)))
   

def create_bookmark(bookmark, folder_name):
    
    try:
    
        if len(bookmark['title']) < 10:
            next_file_name = bookmark['title'] + ' ' + bookmark['url']
        else:
            next_file_name = bookmark['title']

        next_file_name = '{}/{}.url'.format(folder_name, clean_title(next_file_name))
        date = convert_date(bookmark['add_date'])

        print('+ Bookmark:   ', date, next_file_name)
        
        with open(next_file_name, 'w') as configfile:
            config['InternetShortcut'] = {'URL': bookmark['url'], 'DateModified': date}
            config.write(configfile)
        if os.path.isfile(next_file_name):
        
            # adjust timestamp on file
            filedate.File(next_file_name).set(
                created = date,
                modified = date
            )
            
    except Exception as e: 
        print('! Exception encountered', e)
        input('Press enter to continue processing... ')
            
    
        

def create_folders(child, folder_name, folder_date = None):

    # no way to set folder dates currently, use None date
    date = convert_date(None)
    bookmark_folder_path = Path(folder_name)

    if not bookmark_folder_path.exists():
        print('+ Folder:     ', date, folder_name)
        bookmark_folder_path.mkdir()
    else:
        print('  Folder:     ', date, folder_name)


    for bookmark in child:
        if bookmark.get('children'):
            next_folder_name = '{}/{}'.format(folder_name, clean_title(bookmark['title']))
            create_folders(bookmark['children'], next_folder_name, bookmark.get('last_modified'))
                
        elif bookmark['type'] == 'bookmark':
            create_bookmark(bookmark, folder_name)


if __name__ == '__main__':

    for file in glob.glob('./input/*.html'):
        bookmarks = bookmarks_parser.parse(file)
        create_folders(bookmarks, Path(file).stem)


    input('Press enter to exit... ')
