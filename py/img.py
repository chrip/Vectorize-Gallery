from mod_python import apache
import subprocess

tmp_dir = '/home/ubuntu1/Vectorize-Gallery/tmp/'

def index(req, img = None):
  return 'index'

def img(req, **params):
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

  cat_output = subprocess.Popen(['cat', tmp_dir + params.get('session_id') + '.bmp'], stdout=subprocess.PIPE)
  mkbitmap_output = subprocess.Popen(mkbitmap_commands, stdin=cat_output.stdout, stdout=subprocess.PIPE)
  potrace_output = subprocess.Popen(potrace_commands, stdin=mkbitmap_output.stdout, stdout=subprocess.PIPE)
  cat_output.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
  mkbitmap_output.stdout.close()  # Allow p2 to receive a SIGPIPE if p3 exits.
  svg_image = potrace_output.communicate()[0]

  req.content_type = 'image/svg+xml'
  req.write(svg_image)
  return #params.get('session_id'), 'mkbitmap', '--filter', highpass_filter, '--scale', scale_factor, scale_method, '--threshold', threshold, invert, 'potrace', '--turnpolicy', turnpolicy, '--turdsize', turdsize, '--svg', '--alphamax', alphamax, '--color', foreground_color, opaque_background, '--fillcolor', background_color

