import os
from PIL import Image

from flask import url_for, current_app

def add_profile_pic(pic_upload,username):

    filename = pic_upload.filename
    ext_type = filename.split('.')[-1]
    #splits the filename at . and makes 2 strings, so we grab last string
    storage_filename = str(username) + '.' +ext_type
    
    filepath = os.path.join(current_app.root_path, 'static\profile_pics', storage_filename)
    #takes rootpath of our current application (myproject), and look for static\profile_pics

    output_size = (200, 200)

    pic = Image.open(pic_upload)
    pic.thumbnail(output_size)
    #this method allows us to squeeze it into a certain size 
    pic.save(filepath)

    return storage_filename
