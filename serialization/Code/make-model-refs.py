import json
import os
import re
from io import TextIOWrapper
from typing import TextIO
from urllib.request import urlopen, Request
from urllib.parse import urlparse

SPDX_MODEL = 'https://api.github.com/repos/spdx/spdx-3-model/contents/model'

AUTH = {'Authorization': f'token {os.environ["GitHubToken"]}'}
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


def load_model_file(file):
    meta = {}
    state = ''
    with open_file(file) as fp:
        for line in fp.readlines():
            if m := re.match(r'^\s*##\s*(\w+)(.*)$', line):
                state = m.group(1).lower()
            if m := re.match(r'^\s*[-*]\s*(\w+):\s*(.*)\s*$', line):
                if state == 'metadata':
                    meta[m.group(1)] = m.group(2)
    return meta


if __name__ == '__main__':
    modelRefs = {}
    e1 = list_dir(SPDX_MODEL)
    assert len(e1['files']) == 0
    for d1 in e1['dirs']:
        print(f'{d1.name}')
        e2 = list_dir(d1.path)
        assert len(e2['files']) == 1
        prefix = load_model_file(e2['files'][0])['id']
        for d2 in e2['dirs']:
            print(f'. {d2.name}')
            e3 = list_dir(d2.path)
            assert len(e3['dirs']) == 0
            assert d2.name in {'Classes', 'Individuals', 'Properties', 'Vocabularies'}
            if d2.name in {'Classes', 'Vocabularies'}:
                for f3 in e3['files']:
                    f = load_model_file(f3)
                    print(f". . {f['name']}")
                    if f['name'] in modelRefs:
                        print(f"###### Duplicate: {f['name']}")
                    modelRefs[f['name']] = '/'.join((prefix, f['name']))
                    for k, v in f.items():
                        print(f'. . . {k}: {v}')

    print('\nModel References:')
    for k, v in modelRefs.items():
        print(f'{k:>40}: {v}')
    with open('modelRefs.json', 'w') as fp:
        json.dump(modelRefs, fp, indent=2)
