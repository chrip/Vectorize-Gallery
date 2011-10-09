from mod_python import apache
from mod_python import Session
from mod_python import util
import Image
import subprocess

doctype = '<!doctype html>'
header = '<head><meta charset=utf-8><title>Vectorize</title></head>'
home_dir = '/home/ubuntu1/Vectorize-Gallery'

def result(req, img = None):
  session = Session.Session(req)
  session.save()
  try:
    image = Image.open(img.file)
    image_type = image.format
  except:
    util.redirect(req, '/error_page.html')
  if image_type != 'JPEG' and image_type != 'PNG' and image_type != 'BMP':
    util.redirect(req, '/error_page.html')
  else:    
    image.thumbnail((250,250))
    image.save(home_dir + '/tmp/' + session.id() + '.bmp', "BMP")
    (width, height) = image.size
    subprocess.call('cat ' + home_dir + '/tmp/' + session.id() + '.bmp | mkbitmap -f 4 -s 2 -t 0.45 | potrace -t 5 -s > ' + home_dir + '/tmp/' + session.id() + '.svg', shell=True)
    return "{0:s}<html>{1:s}<body><img src='/tmp/{2:s}.bmp' width='{3:s}' height='{4:s}' /><img src='/tmp/{2:s}.svg' width='{3:s}' height='{4:s}' /></body></html>".format(doctype, header, session.id(), str(width), str(height))
