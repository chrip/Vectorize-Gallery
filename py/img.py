from mod_python import apache
from mod_python import Session
from mod_python import util
import subprocess

def index(req, img = None):
  return 'index'

def vectorGraphic(req, **params):
#  import rpdb2; rpdb2.start_embedded_debugger('password')
  
  #### mkbitmap
  mkbitmap_commands = ['mkbitmap']

  mkbitmap_commands.append('--filter')
  mkbitmap_commands.append(params.get('highpass_filter', '4'))

  mkbitmap_commands.append('--scale')
  mkbitmap_commands.append(params.get('scale_factor', '1'))

  mkbitmap_commands.append('--' + params.get('scale_method', 'linear'))

  mkbitmap_commands.append('--threshold')
  mkbitmap_commands.append(params.get('threshold', '0.5'))

  if params.get('invert', 'no') == 'yes':
    mkbitmap_commands.append('--invert')
  
  ### potrace
  potrace_commands = ['potrace', '--svg']

  potrace_commands.append('--turnpolicy')
  potrace_commands.append(params.get('turnpolicy', 'minority'))

  potrace_commands.append('--turdsize')
  potrace_commands.append(params.get('turdsize', '5'))

  potrace_commands.append('--alphamax')
  potrace_commands.append(params.get('alphamax', '1'))

  potrace_commands.append('--color')
  potrace_commands.append('#' + params.get('foreground_color', '000000'))

  if params.get('opaque_background', 'no') == 'yes':
    potrace_commands.append('--opaque')
    potrace_commands.append('--fillcolor')
    potrace_commands.append('#' + params.get('background_color', 'FFFFFF'))

  session = Session.Session(req)
  if session.is_new():
    util.redirect(req, '/error_page.html')

  mkbitmap = subprocess.Popen(mkbitmap_commands, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
  bitmap_image = mkbitmap.communicate(input=session.get('raw_image').getvalue())[0]
  potrace = subprocess.Popen(potrace_commands, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
  svg_image = potrace.communicate(input=bitmap_image)[0]
  
  req.content_type = 'image/svg+xml'
  req.write(svg_image)
  return

