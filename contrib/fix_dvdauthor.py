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
    et.strip_attributes(s, 'present', 'id')

# fix buttons

for b in root.findall('.//buttons'):
    vod = b.getparent()
    for button in reversed(b.getchildren()):
        vod.addnext(button)
    vod.remove(b)

tree.write('/tmp/out.xml', pretty_print=True)
