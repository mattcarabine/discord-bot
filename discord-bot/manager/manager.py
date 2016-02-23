import json
import os

from util.setup_directory import setup_dir


class FileNotFoundError(IOError):
    """
    Custom error used to for fallback logic in the calling code
    """
    def __init__(self, *args, **kwargs):
        super(IOError, self).__init__(*args, **kwargs)


class Manager(object):

    def set(self, key, value):
        raise NotImplementedError

    def get(self, key):
        raise NotImplementedError


class FileManager(Manager):

    def __init__(self):
        self.data_path = os.environ.get('DATA_PATH')
        setup_dir(self.data_path)

    def set(self, key, value):
        key = '{}.json'.format(key)
        file_path = os.path.join(self.data_path, key)
        with open(file_path, 'w') as f:
            f.write(json.dumps(value))

    def get(self, key):
        key = '{}.json'.format(key)
        file_path = os.path.join(self.data_path, key)
        try:
            with open(file_path, 'r') as f:
                value = json.loads(f.read())
        except IOError:
            raise FileNotFoundError()

        return value


class CouchbaseManager(Manager):

    def __init__(self, bucket):
        from couchbase.bucket import Bucket
        self.bucket = Bucket('couchbase://{}/{}'.format(
            os.environ.get('CB_HOST'), bucket))
        self.bucket.timeout = 30

    def set(self, key, value):
        self.bucket.upsert(key, value)

    def get(self, key):
        from couchbase.exceptions import NotFoundError
        try:
            return self.bucket.get(key).value
        except NotFoundError:
            raise FileNotFoundError()
