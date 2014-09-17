#!/usr/bin/python2.7
from lxml import etree as et
import sys

"""
Patch the dvdunauthor output to work with dvdauthor
"""

parser = et.XMLParser(remove_blank_text=True)

input_file = 'dvdauthor.xml'
output_file = 'dvdauthor.xml.fixed'

try:
    input_file = sys.argv[1]
    output_file = sys.argv[2]
except:
    pass

print("Converting %s to %s" % (input_file, output_file))

tree = et.parse(input_file, parser)
root = tree.getroot()

# drop titlemap

for t in root.findall('.//titlemap'):
    t.getparent().remove(t)

# drop audio

for a in root.findall('.//audio'):
    a.getparent().remove(a)

# drop subpicture attributes

for s in root.findall('.//subpicture'):
    present = s.get('present')
    et.strip_attributes(s, 'present')
    et.strip_attributes(s, 'id')
    if present != None and present == 'no':
        s.getparent().remove(s)

for s in root.findall('.//pgc'):
    et.strip_attributes(s, 'next')
    et.strip_attributes(s, 'prev')
# fix buttons

for b in root.findall('.//buttons'):
    vod = b.getparent()
    for button in reversed(b.getchildren()):
        vod.addnext(button)
    vod.remove(b)

tree.write(output_file, pretty_print=True)
