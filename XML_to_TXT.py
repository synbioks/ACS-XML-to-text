import pathlib #using pathlib to navigate the directory structures
from lxml import etree #going to use lxml's etree methods to parse the XML and perform the XSL
from shutil import unpack_archive #using shutil's unpacker to unzip the XML files

# unpack all the archives

archives = pathlib.Path().glob('*.zip')

for a in archives:
    if not pathlib.Path(a.stem).is_dir(): # will not overwrite existing files
        unpack_archive(str(a))

folder = list(pathlib.Path().glob('**/*.xml')) #establish the paths to the files

#for f in folder[:10]: # limit to the first 10 for debugging
for f in folder:
    with open(f, 'rb') as fin:
        text = fin.read()
    tree = etree.fromstring(text)
    text = tree.xpath('//sec//text()') #locates each "section" node and dumps its text and the text of all of its child nodes into the text file

#     text = tree.xpath('//*[sec or ref-list]//text()')
#     use above if capturing the reference text is also desirable

#     text = tree.xpath('//*[sec or back]//text()')
#  use above if capturing all of the "back matter" text (references, acknowledgements, notes, etc.) is desirable

#     text = tree.xpath('//*[p or title]//text()')
#     use above if we only want to dump text from section title nodes and section paragraph (p) nodes


#note that the below pathlib works on Mac and Windows...not sure about Linux systems...may need adjusting for local runtime environment
    pathlib.Path(f.parent / (f.stem + '.txt')).write_text(" ".join(text), encoding = 'utf-8')
    print("finished", f.stem) #graceful completion report for debugging