from mod_python import apache
from mod_python import Session
from mod_python import util
import Image
import subprocess
import urllib
import os
import StringIO


max_image_size = 400

def result(req, img = None):
  session = Session.Session(req)  
  try:
    image = Image.open(img.file)
    image_type = image.format
  except:
    util.redirect(req, '/error_page.html')
  if image_type != 'JPEG' and image_type != 'PNG' and image_type != 'BMP':
    util.redirect(req, '/error_page.html')
  else:    
    image.thumbnail((max_image_size,max_image_size))
    raw_image = StringIO.StringIO()
    image.save(raw_image, 'BMP')
    session['raw_image'] = raw_image
    session.save()
    all_pathes = _generate_svg_pathes()
    return _get_html_page(all_pathes, image.size)


def _generate_svg_pathes():  
  # mkbitmap
  #0 filter n: highpass filter
  #1 scale n: scale the image with factor n
  #2 linear: scale linear (fast) --cubic: scale cubic best results (slow) [l,c]
  #3 threshold [0 .. 1]: the threshold grey value for bilevel conversion
  #4 invert: invert the image [yes,no]

  # potrace
  #5 turnpolicy [black, white, right, left, minority, majority, or random]
  #6 turdsize n: suppress speckles of up to this many pixels
  #7 alphamax n: how smooth the result is [-1 .. 1.334] default 1
  #8 color #rrggbb: foreground color
  #9 opaque background [yes,no]
  #10 fillcolor #rrggbb: background color

  all_pathes = []
  all_thresholds = range(42,60,2)
  for t in all_thresholds:
    all_pathes.append('/py/img/vectorGraphic?highpass_filter=4&scale_factor=2&scale_method=cubic&threshold=0.{0:d}&invert=no&turnpolicy=black&turdsize=5&alphamax=1&foreground_color=000000&opaque_background=no&background_color=FFFFFF'.format(t))
  return all_pathes

def _get_img_tag(src, size):
  return '<img src="{0:s}" width="{1[0]:d}" height="{1[1]:d}" />'.format(src, size)

def _get_html_page(all_pathes, size):
  html = '<!doctype html><html><head><meta charset=utf-8><title>Vectorize</title></head><body>'
  for img in all_pathes:
    html += _get_img_tag(img, size)
  html += '</body></html>'
  return html

