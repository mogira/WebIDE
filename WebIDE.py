from bottle import get, post, route, run, debug, template, request, static_file, error, redirect
import json, os, urllib

try:
    import editor
    PYTHONISTA = True
except ImportError:
    PYTHONISTA = False

ROOT = os.path.expanduser('~/Documents')

def make_file_tree(dir_path=ROOT):
    file_dict = {}
    def recur(path, list):
        for l in os.listdir(path):
            f = os.path.join(path, l)
            if l[0] == '.':
              continue
            elif os.path.isdir(f):
                list[l] = {}
                recur(f, list[l])
            elif l.split('.')[-1] in ['py', 'txt', 'pyui', 'json']:
                list[l] = urllib.pathname2url(f[len(ROOT):])
    recur(dir_path, file_dict)
    return file_dict

@get('/')
def edit():
    #file_list = {
    #    'filename1': 'path1',
    #    'filename2': 'path2',
    #    'dirname1': {
    #        'filename3': 'path3',
    #        'dirname2': {
    #            'filename4': 'path4',
    #            'filename5': 'path5'
    #        }
    #    }
    #}
    file_list = make_file_tree(ROOT)
    file = request.GET.get('file')
    if file:
        with open(os.path.join(ROOT, file), 'r') as in_file:
            code = in_file.read()
      	if file.split('.')[-1] in ['pyui', 'json']:
            code = json.dumps(json.loads(code), indent=4, separators=(',', ': '))
        output = template('main.tpl', files = file_list, save_as = file, code = code)
    else:
        output = template('main.tpl', files = file_list)
    return output

@post('/')
def submit():
    filename = os.path.join(ROOT, request.forms.get('filename'))
    with open(filename, 'w') as f:
        f.write(request.forms.get('code').replace('\r', ''))
    if PYTHONISTA:
        editor.reload_files()

@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='./static')

@error(403)
def mistake403(code):
    return 'There is a mistake in your url!'

@error(404)
def mistake404(code):
    return "This is not the page you're looking for *waves hand*"

debug(True)
run(reloader=not PYTHONISTA, host='0.0.0.0')
