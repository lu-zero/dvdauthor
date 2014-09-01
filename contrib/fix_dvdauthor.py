#!/usr/bin/python2.7
from lxml import etree as et

"""
Patch the dvdunauthor output to work with dvdauthor
"""

parser = et.XMLParser(remove_blank_text=True)

tree = et.parse('dvdauthor.xml', parser)
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

tree.write('/tmp/out.xml', pretty_print=True)
