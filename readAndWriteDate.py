
# coding: utf-8

# # Load data and create text files
# 
# This notebook will load the zip file paths from `data_zips` and unzip them into the `data_folders` folder.  Each zip file makes one folder with a single xml file.
# 
# It then grabs all the `.xml` file paths and feeds them into the lxml parser.  From each file, the text is extracted from the xml and written into a `.txt` file.  The xpath term `//text()` is used, which recursively grabs text from all nodes.
# 
# Due to the nature of xml and `//text()`, there will be a bunch of extra tabs and newlines created. This shouldn't be a problem if you are just going after a bag of words model for processing.  Some additional cleaning can be done, but it gets very complicated very quickly.  

# In[2]:

import pathlib
from lxml import etree
from shutil import unpack_archive


# In[12]:

# unpack all the archives

archives = pathlib.Path().glob('data_zips/*.zip')

for a in archives:
    if not pathlib.Path(a.stem).is_dir(): # will not overwrite existing files
        unpack_archive(str(a), str(a.parent / a.stem))


# In[16]:

folder = list(pathlib.Path().glob('data_folders/**/*.xml'))

for f in folder: # limit to the first 10
    with open(f, 'rb') as fin:
        text = fin.read()
    tree = etree.fromstring(text)
    text = tree.xpath('//text()')

#     text = tree.xpath('//*[p or title or table-wrap]//text()')
    pathlib.Path(f.parent / (f.stem + '.txt')).write_text(" ".join(text), encoding = 'utf-8')
    print("finished", f.stem)

        


# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:

