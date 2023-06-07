import fire
import json
import jadn
import os
import shutil
from jsonschema import validate, Draft202012Validator
from jsonschema.exceptions import ValidationError
from io import TextIOWrapper
from typing import TextIO
from urllib.request import urlopen, Request
from urllib.parse import urlparse

DATA_DIR = os.path.join('..', 'json', 'examples')
DATA_REPO = 'https://api.github.com/repos/oasis-open/openc2-jadn-software/contents/Test'
DATA = DATA_DIR

AUTH = {'Authorization': f'token {os.environ["GitHubToken"] if DATA == DATA_REPO else "None"}'}
VALIDATE_JADN = True


class WebDirEntry:
    """
    Fake os.DirEntry type for GitHub filesystem
    """
    def __init__(self, name, path, url):
        self.name = name
        self.path = path
        self.url = url


def list_dir(dirpath: str) -> dict:
    """
    Return a dict listing the files and directories in a directory on local filesystem or GitHub repo.

    :param dirpath: str - a filesystem path or GitHub API URL
    :return: dict {files: [DirEntry*], dirs: [DirEntry*]}
    Local Filesystem: Each list item is an os.DirEntry structure containing name and path attributes
    GitHub Filesystem: Each list item has name, path, and url (download URL) attributes
    """

    files, dirs = [], []
    u = urlparse(dirpath)
    if all([u.scheme, u.netloc]):
        with urlopen(Request(dirpath, headers=AUTH)) as d:
            for dl in json.loads(d.read().decode()):
                url = 'url' if dl['type'] == 'dir' else 'download_url'
                entry = WebDirEntry(dl['name'], dl[url], dl['url'])
                (dirs if dl['type'] == 'dir' else files).append(entry)
    else:
        with os.scandir(dirpath) as dlist:
            for entry in dlist:
                (dirs if os.path.isdir(entry) else files).append(entry)
    return {'files': files, 'dirs': dirs}


def open_file(fileentry: os.DirEntry) -> TextIO:
    u = urlparse(fileentry.path)
    if all([u.scheme, u.netloc]):
        return TextIOWrapper(urlopen(Request(fileentry.path, headers=AUTH)), encoding='utf8')
    return open(fileentry.path, 'r', encoding='utf8')


def validate(dpath, codec, json_schema):  # Validate serialized Element examples
    print(f'\n{dpath}:')
    dl = list_dir(dpath)
    print(dl)

    try:
        if VALIDATE_JADN:
            codec.decode('Element', json.load(open_file(dpath)))
        else:
            validate(json.load(open_file(dpath)), json_schema,
                     format_checker=Draft202012Validator.FORMAT_CHECKER)
    except ValidationError as e:    # JSON Schema validation error
        print(f' Fail: {e.message}')
    except ValueError as e:         # JADN validation error
        print(f' Fail: {e}')
    except json.decoder.JSONDecodeError as e:
        print(f' Bad JSON: {e.msg} "{e.doc}"')


def main(data: str = DATA) -> None:
    print(f'Installed JADN version: {jadn.__version__}\n')
    codec = json_schema = None
    try:
        if VALIDATE_JADN:
            with open_file('spdx-v3.jidl') as fp:
                codec = jadn.codec.Codec(jadn.load_any(fp), verbose_rec=True, verbose_str=True)
        else:
            with open_file('spdx-v3.json') as fp:
                json_schema = json.load(fp)
    except ValueError as e:
        print(e)

    for f in list_dir(data):
        validate(f, codec=codec, json_schema=json_schema)


if __name__ == '__main__':
    fire.Fire(main)
