import os
import re

re_prefix = re.compile(r'^\w+_')
for filename in os.listdir('.'):
    match = re_prefix.match(filename)
    if match:
        new_name = filename.replace(match.group(0), '')
        os.rename(filename, new_name)
