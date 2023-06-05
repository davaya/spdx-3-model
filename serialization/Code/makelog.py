import jadn
import json
import os


def flatten(nested: dict, path: str = '', fdict: dict = None, sep: str = '.') -> dict:
    """
    Convert a nested dict to a flat dict with hierarchical keys
    """
    if fdict is None:
        fdict = {}
    flat = fdict.copy()
    if isinstance(nested, (dict, list)) and len(nested) == 0:
        flat[path] = None
    elif isinstance(nested, dict):
        for k, v in nested.items():
            k = k.split(':')[1] if ':' in k else k
            flat = flatten(v, sep.join((path, k)) if path else k, flat)
    elif isinstance(nested, list):
        for n, v in enumerate(nested):
            flat.update(flatten(v, sep.join([path, str(n)])))
    else:
        flat[path] = nested
    return flat


def unflatten(flat: dict, sep: str = '.') -> dict:
    nested = {}
    for k, v in flat.items():
        current = nested
        path = k.split(sep)

        for key in path[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
        current[path[-1]] = v if v is not None else {}
    return nested


def dlist(src: dict) -> dict:
    """
    Convert dicts with numeric keys to lists

    :param src: {'a': {'b': {'0':'red', '1':'blue'}, 'c': 'foo'}}
    :return: {'a': {'b': ['red', 'blue'], 'c': 'foo'}}
    """
    if isinstance(src, dict) and len(src) > 0:
        for k in src:
            src[k] = dlist(src[k])
        if set(src) == {str(k) for k in range(len(src))}:
            src = [src[str(k)] for k in range(len(src))]
    return src


print(f'JADN Version: {jadn.__version__}')
with open('spdx-v3.jidl') as fp:
    schema = jadn.load_any(fp)
print(f"JADN schema: {schema['info']['package']}")
codec = jadn.codec.Codec(schema, verbose_rec=True, verbose_str=True)
for e in os.scandir(os.path.join('..', 'json', 'examples')):
    fname, fext = os.path.splitext(e.name)
    if e.is_file() and fext == '.json':
        with open(e.path) as fp:
            element = json.load(fp)
        e = codec.decode('Element', element)
        element_f = flatten(element)
        element_u = dlist(unflatten(element_f))
        assert element_u == element
        with open(os.path.join('..', 'logical', 'examples', fname) + '.logval', 'w') as fp:
            for k, v in element_f.items():
                fp.write(f'{k:>35} = {repr(v) if v is not None else "nil"}\n')
