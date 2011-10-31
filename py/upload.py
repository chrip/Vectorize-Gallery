from mod_python import apache
from mod_python import Session
import Image
import subprocess
import os
import StringIO


max_image_size = 400

def index(req, img = None):
  session = Session.Session(req)  
  try:
    image = Image.open(img.file)
    image_type = image.format
  except:
    return 'Error: Could not open file.'
  if image_type != 'JPEG' and image_type != 'PNG' and image_type != 'BMP':
    return 'Error: Wrong file format.'
  else:
    # prevent IOError: cannot write mode RGBA as BMP
    image.load()
    if len(image.split()) == 4:      
      r, g, b, a = image.split()
      image = Image.merge("RGB", (r, g, b))

    image.thumbnail((max_image_size,max_image_size))
    raw_image = StringIO.StringIO()
    image.save(raw_image, 'BMP')
    session['raw_image'] = raw_image
    session.save()    
    return "OK"



