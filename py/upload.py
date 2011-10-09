from mod_python import apache
from mod_python import Session
from mod_python import util
import Image
import subprocess
import urllib
import os

absolut_path = '/home/ubuntu1/Vectorize-Gallery/'
relativ_upload_path = 'tmp/'

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
    image_path_prefix = session.id()    
    os.chdir(absolut_path + relativ_upload_path)
    image.save('{0:s}.bmp'.format(image_path_prefix), 'BMP')
    all_pathes = _generate_svgs(image_path_prefix)
    return _get_html_page(all_pathes, image.size)


def _generate_svgs(image_path_prefix):  
  all_pathes = []

  #bmp_path = '{0:s}.bmp'.format(image_path_prefix)
  #all_pathes.append(bmp_path)

  all_pathes.append(_potrace('mkbitmap --filter 4 --scale 2 --threshold 0.35 | potrace --turdsize 5 --svg --alphamax 1', image_path_prefix))
  all_pathes.append(_potrace('mkbitmap --filter 4 --scale 2 --threshold 0.40 | potrace --turdsize 5 --svg --alphamax 1', image_path_prefix))
  all_pathes.append(_potrace('mkbitmap --filter 4 --scale 2 --threshold 0.45 | potrace --turdsize 5 --svg --alphamax 1', image_path_prefix))
  all_pathes.append(_potrace('mkbitmap --filter 4 --scale 2 --threshold 0.47 | potrace --turdsize 5 --svg --alphamax 1', image_path_prefix))
  all_pathes.append(_potrace('mkbitmap --filter 4 --scale 2 --threshold 0.50 | potrace --turdsize 5 --svg --alphamax 1', image_path_prefix))

  all_pathes.append(_potrace('mkbitmap --filter 4 --scale 2 --threshold 0.52 | potrace --turdsize 5 --svg --alphamax 1', image_path_prefix))
  all_pathes.append(_potrace('mkbitmap --filter 4 --scale 2 --threshold 0.55 | potrace --turdsize 5 --svg --alphamax 1', image_path_prefix))
  all_pathes.append(_potrace('mkbitmap --filter 4 --scale 2 --threshold 0.60 | potrace --turdsize 5 --svg --alphamax 1', image_path_prefix))
  all_pathes.append(_potrace('mkbitmap --filter 6 --scale 2 --threshold 0.50 | potrace --turdsize 5 --svg --alphamax 1', image_path_prefix))
  all_pathes.append(_potrace('mkbitmap --filter 8 --scale 2 --threshold 0.50 | potrace --turdsize 5 --svg --alphamax 1', image_path_prefix))
  return all_pathes

def _get_img_tag(src, size):
  return '<img src="/{0:s}{1:s}" width="{2[0]:d}" height="{2[1]:d}" />'.format(relativ_upload_path, src, size)

def _potrace(cmd, image_path_prefix):
  # mkbitmap
  # --filter n: highpass filter
  # --scale n: scale the image with factor n
  # --linear: scale linear (fast)
  # --cubic: scale cubic best results (slow)
  # --threshold [0 .. 1]: the threshold grey value for bilevel conversion
  # --invert: invert the image

  # potrace
  # --svg: output format svg
  # --turnpolicy [black, white, right, left, minority, majority, or random]
  # --turdsize n: suppress speckles of up to this many pixels
  # --alphamax n: how smooth the result is [-1 .. 1.334] default 1
  # --scale n: scale image
  # --color #rrggbb: foreground color
  # --opaque --fillcolor #rrggbb: background color

  suffix = cmd.replace(' ','').replace('--','-').replace('|','').replace('.','')
  web_image_path = '{0:s}-{1:s}.svg'.format(image_path_prefix, suffix)
  subprocess.call('cat {0:s}.bmp | {1:s} > {2:s}'.format(image_path_prefix, cmd, web_image_path), shell=True)
  return web_image_path

def _get_html_page(all_pathes, size):
  html = '<!doctype html><html><head><meta charset=utf-8><title>Vectorize</title></head><body>'
  for img in all_pathes:
    html += _get_img_tag(img, size)
  html += '</body></html>'
  return html

