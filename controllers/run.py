import sys
import os
import threading
from subprocess import Popen, PIPE
import json

stdout_result = 1
stderr_result = 1


def path_to_dict(path):
    d = {'name': os.path.basename(path)}
    if os.path.isdir(path):
        d['type'] = "directory"
        d['children'] = [path_to_dict(os.path.join(path,x)) for x in os.listdir(path)]
    else:
        d['type'] = "file"
    return d

    return json.dumps(path_to_dict('.'))


def heimpt():
    command = ["python", "/home/www-data/web2py/applications/heimpt/static/tools/heimpt.py", "/home/www-data/web2py/applications/heimpt/static/tools/configurations/02_wintz.bits.json"]

    #process = Popen(command, stdout=PIPE)
    #(output, err) = process.communicate()
    #exit_code = process.wait()

    #return exec_command(command)
    return dict(files=path_to_dict("/home/www-data/web2py/applications/heimpt/static/tools/configurations"))




def list_files(startpath):
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print('{}{}'.format(subindent, f))

def stdout_thread(pipe):
    global stdout_result
    while True:
        out = pipe.stdout.read(1)
        stdout_result = pipe.poll()
        if out == '' and stdout_result is not None:
            break

        if out != '':
            sys.stdout.write(out)
            sys.stdout.flush()


def stderr_thread(pipe):
    global stderr_result
    while True:
        err = pipe.stderr.read(1)
        stderr_result = pipe.poll()
        if err == '' and stderr_result is not None:
            break

        if err != '':
            sys.stdout.write(err)
            sys.stdout.flush()


def exec_command(command, cwd=None):
    if cwd is not None:
        print '[' + ' '.join(command) + '] in ' + cwd
    else:
        print '[' + ' '.join(command) + ']'

    p = Popen(
        command, stdout=PIPE, stderr=PIPE, cwd=cwd
    )

    out_thread = threading.Thread(name='stdout_thread', target=stdout_thread, args=(p,))
    err_thread = threading.Thread(name='stderr_thread', target=stderr_thread, args=(p,))

    err_thread.start()
    out_thread.start()

    out_thread.join()
    err_thread.join()

    return stdout_result + stderr_result