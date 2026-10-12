"""Canonical JSON and immutable records."""
import hashlib
import json
import math
import re

from .errors import IntentlineError
from .paths import read_file, text


def sha(data):
    return hashlib.sha256(data).hexdigest()


def canonical(value):
    return (json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False, allow_nan=False) + '\n').encode('utf-8')


def parse(data):
    def pairs(items):
        obj = {}
        for key, value in items:
            if key in obj:
                raise IntentlineError(f'Duplicate JSON key: {key}')
            obj[key] = value
        return obj
    def invalid(value):
        raise IntentlineError(f'Non-finite JSON number: {value}')
    def finite(value):
        parsed = float(value)
        if not math.isfinite(parsed):
            raise IntentlineError('Non-finite JSON number')
        return parsed
    try:
        return json.loads(text(data), object_pairs_hook=pairs, parse_constant=invalid, parse_float=finite)
    except (ValueError, RecursionError) as exc:
        raise IntentlineError('Malformed JSON') from exc


def load(path):
    return parse(read_file(path)[0])


def fields(obj, required, optional=()):
    if not isinstance(obj, dict) or set(obj) - set(required) - set(optional) or set(required) - set(obj):
        raise IntentlineError(f'Expected fields {sorted(required)}; optional {sorted(optional)}')


def string(value):
    if not isinstance(value, str) or not value.strip() or any(ord(c) < 32 and c not in '\n\r\t' for c in value):
        raise IntentlineError('Expected nonempty text without control characters')
    try:
        value.encode('utf-8')
    except UnicodeEncodeError as exc:
        raise IntentlineError('Malformed Unicode text') from exc


def digest(value):
    if not isinstance(value, str) or not re.fullmatch('[0-9a-f]{64}', value):
        raise IntentlineError('Malformed SHA-256 digest')


def integer(value, minimum=1):
    if type(value) is not int or value < minimum:
        raise IntentlineError('Expected positive integer')


def immutable(directory, name, value):
    data = canonical(value)
    try:
        prior, _ = directory.read(name)
    except FileNotFoundError:
        directory.write(name, data)
    else:
        if prior != data:
            raise IntentlineError('Conflicting immutable record', 3)
    return sha(data)
