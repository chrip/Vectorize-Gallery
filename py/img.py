from mod_python import apache
import subprocess

tmp_dir = '/home/ubuntu1/Vectorize-Gallery/tmp/'

def index(req, img = None):
  return "index"

def img(req, session_id = None, image_id = None):

  cat_output = subprocess.Popen(["cat", tmp_dir + session_id + ".bmp"], stdout=subprocess.PIPE)
  mkbitmap_output = subprocess.Popen(["mkbitmap", "--filter", "4", "--scale", "1", "--threshold", "0.35"], stdin=cat_output.stdout, stdout=subprocess.PIPE)
  potrace_output = subprocess.Popen(["potrace", "--turdsize", "1", "--svg", "--alphamax", "1"], stdin=mkbitmap_output.stdout, stdout=subprocess.PIPE)
  cat_output.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
  mkbitmap_output.stdout.close()  # Allow p2 to receive a SIGPIPE if p3 exits.
  svg_image = potrace_output.communicate()[0]

  req.content_type = "image/svg+xml"
  req.write(svg_image)
  return

