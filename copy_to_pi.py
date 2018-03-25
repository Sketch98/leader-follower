import errno
import os
import shutil

src = '/home/nathan/leader-follower'
dst = '/home/nathan/pi/leader-follower'

try:
    if os.path.exists(dst):
        shutil.rmtree(dst)
    shutil.copytree(src, dst)
except OSError as exc:
    if exc.errno == errno.ENOTDIR:
        shutil.copy(src, dst)
    else:
        raise
