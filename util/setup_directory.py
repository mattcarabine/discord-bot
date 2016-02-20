import errno
import os
DIRECTORY = os.environ.get('DATA_PATH')


def setup_dir(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

if __name__ == '__main__':
    setup_dir(DIRECTORY)
