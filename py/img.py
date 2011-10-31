from mod_python import apache
from mod_python import Session
from mod_python import util
import subprocess
import gzip
import cStringIO
import string


def compressBuf(buf):
  zbuf = cStringIO.StringIO()
  zfile = gzip.GzipFile(mode = 'wb',  fileobj = zbuf)
  zfile.write(buf)
  zfile.close()  
  return zbuf.getvalue()

def testAcceptsGzip(req):
  if req.headers_in.has_key('accept-encoding'):
    encodings = req.headers_in['accept-encoding']
    req.headers_out['Content-Encoding'] = 'gzip'
    return (string.find(encodings, "gzip") != -1)
  else:
    return 0

def vectorGraphic(req, **params):
#  import rpdb2; rpdb2.start_embedded_debugger('password')
  
  #### mkbitmap
  # filter n: highpass filter
  # scale n: scale the image with factor n
  # linear: scale linear (fast) - cubic: scale cubic best results (slow) [linear,cubic]
  # threshold [0 .. 1]: the threshold grey value for bilevel conversion
  # invert: invert the image [yes,no]

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
  # turnpolicy [black, white, right, left, minority, majority, or random]
  # turdsize n: suppress speckles of up to this many pixels
  # alphamax n: how smooth the result is [-1 .. 1.334] default 1
  # color #rrggbb: foreground color
  # opaque background [yes,no]
  # fillcolor #rrggbb: background color

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

  if testAcceptsGzip(req):
    zbuf = compressBuf(svg_image)    
    req.headers_out['Content-Length'] = '%d' % (len(zbuf))
    req.write(zbuf)
  else:
    req.write(svg_image)
  return

