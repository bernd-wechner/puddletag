import csv, os
from PyQt4.QtGui import QFileDialog, QApplication
from PyQt4.QtCore import SIGNAL
import sys
sys.path.insert(1,'/home/keith/Documents/python/puddletag')
from puddlestuff.findfunc import tagtofilename
from puddlestuff.audioinfo.util import lnglength
import puddlestuff.audioinfo as audioinfo

from os.path import abspath, dirname, normcase, normpath, splitdrive, realpath
from os.path import join as path_join, commonprefix
import os

def commonpath(a, b):
    """Returns the longest common to 'paths' path.

    Unlike the strange commonprefix:
    - this returns valid path
    - accepts only two arguments
    """
    a = normpath(normcase(a))
    b = normpath(normcase(b))

    if a == b:
        return a

    while len(a) > 0:
        if a == b:
            return a

        if len(a) > len(b):
            a = dirname(a)
        else:
            b = dirname(b)

    return None


def relpath(target, base_path=os.curdir):
    """\
    Return a relative path to the target from either the current directory
    or an optional base directory.

    Base can be a directory specified either as absolute or relative
    to current directory."""
    #http://code.activestate.com/recipes/302594/

    base_path = normcase(abspath(normpath(base_path)))
    target = normcase(abspath(normpath(target)))

    if base_path == target:
        return '.'

    # On the windows platform the target may be on a different drive.
    if splitdrive(base_path)[0] != splitdrive(target)[0]:
        return None

    common_path_len = len(commonpath(base_path, target))

    # If there's no common prefix decrease common_path_len should be less by 1
    base_drv, base_dir = splitdrive(base_path)
    if common_path_len == len(base_drv) + 1:
        common_path_len -= 1

    # if base_path is root directory - no directories up
    if base_dir == os.sep:
        dirs_up = 0
    else:
        dirs_up = base_path[common_path_len:].count(os.sep)

    ret = os.sep.join([os.pardir] * dirs_up)
    if len(target) > common_path_len:
        ret = path_join(ret, target[common_path_len + 1:])

    return ret

def readm3u(path):
    #From http://forums.fedoraforum.org/showthread.php?p=1224109
    fileHandle = open (path, 'r')
    reader = csv.reader(open(path, "r"))
    olddir = os.path.realpath(os.curdir)
    os.chdir(os.path.dirname(path))

    # List of mp3files
    mp3Files = []

    for row in reader:
        if len(row)<1:
            # Skip blanks
            continue
        elif row[0].startswith("#"):
            # Ignore comments
            continue
        else:
            # store rule
            mp3Files.append(unicode(normpath(realpath(row[0])), 'utf8'))

    fileHandle.close()
    os.chdir(olddir)
    return mp3Files

def exportm3u(tags, tofile, format = None, reldir = False):
    header = [u'#EXTM3U']

    if reldir:
        reldir = os.path.dirname(os.path.realpath(tofile))
        filenames = [relpath(f.filepath, reldir) for f in tags]
    else:
        filenames = [f.filepath for f in tags]

    if format is None:
        text = u'\n'.join(header + filenames)
    else:
        text = header
        extinfo = (u'#EXTINF: %s, %s' % (unicode(lnglength(f.length)),
                                tagtofilename(format, f, True)) for f in tags)
        [text.extend([z,y]) for z,y in zip(extinfo, filenames)]
        text = u'\n'.join(text)

    playlist = open(tofile, 'w')
    playlist.write(text.encode('utf8'))
    playlist.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    filedlg = QFileDialog()
    filedlg.setFileMode(filedlg.DirectoryOnly)
    filename = unicode(filedlg.getExistingDirectory(None,
        'Open Folder'))
    tags = []
    for z in os.listdir(filename):
        try:
            tag = audioinfo.Tag(os.path.join(filename,z))
            if tag:
                tags.append(tag)
        except Exception, e:
            print unicode(e)
    folder = unicode(filedlg.getSaveFileName(None,
            'Save File'))
    exportm3u(tags, folder)