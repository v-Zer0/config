import functools, hashlib, json, re, requests, os
from collections import Counter, defaultdict
from datetime import datetime
from tabulate import tabulate

import openai
openai.organization = os.getenv("OPENAI_ORG")
openai.api_key = os.getenv("OPENAPI")

def get_time():
  now = datetime.now()
  return now.strftime("%B %d, %Y @ %H:%M")


def req(method, url, headers={}, json={}, token=None):
  if token:
    headers['Authorization'] = f'Bearer {token}'
  if method == 'get':
    r = requests.get(url, headers=headers)
  elif method == 'post':
    r = requests.post(url, json=json, headers=headers)
  return r


def write(file_name, obj):
  with open(file_name, "w") as outfile:
    outfile.write(json.dumps(obj, default=str, indent=2))


# recursive attribute getter: obj.nested.attribute
def get_attr(obj, attr):
  attrs = attr.split(".")
  for a in attrs:
    try:
      obj = obj[a]
    except (KeyError, TypeError):
      return None
  return obj


# Split string on -, _, or camelCase
def ss(input_string):
  pattern = r'[\s_-]|(?<!^)(?=[A-Z])'
  return re.split(pattern, input_string)


def get_keys(objs):
  keys = set()
  for obj in objs: keys.update(obj.keys())
  return list(keys)


def find_by_attr(objs, attr, val):
  ret = []
  for o in objs:
    if val == get_attr(o, attr):
      ret.append(o)
  return ret


# Group list of objects by attributes, will compute == of composite types
def gb_attrs(objs, attrs):
  groups = defaultdict(list)
  for obj in objs:
    key = hashlib.sha1(json.dumps({k:get_attr(obj, k) for k in attrs}).encode('utf-8')).hexdigest()
    groups[key].append(obj)
  return groups


def pp(obj):
  print(json.dumps(obj, indent=2, default=str))


def pp_tab(objs, group_by=[], keys=[]):
  if not keys:
    keys = get_keys(objs)

  rows = []
  if group_by:
    headers = [' '.join(ss(k)).title() for k in group_by] + ['Count']
    groups = gb_attrs(objs, group_by)
    for k in groups:
      grp = groups[k]
      rows.append([get_attr(grp[0], attr) for attr in group_by] + [len(grp)])
  else:
    headers = [' '.join(ss(k)).title() for k in keys]
    for o in objs:
      rows.append([o[k] if k in o else None for k in keys])

  # Lexicographic sort then by descending
  rows.sort(key=lambda x: x[0] if type(x) not in [list, dict, set] else 0)
  rows.sort(key=lambda x: x[len(headers)-1], reverse=True)
  print(tabulate(rows, headers=headers))
  print(f"\n{len(rows)} rows\n")

print(f"\n\n{get_time()}\n\nimported: functools, hashlib, json, re, requests, os")
