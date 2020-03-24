
# coding: utf-8

# In[1]:

import json


# In[2]:

with open('inital_data_extraction.json', 'r') as fin:
    data = json.load(fin)


# In[4]:

data[0].keys()


# In[7]:

pmiderrors = [d['pmid'] for d in data if not d['pmid'].isdigit() ]


# In[9]:

set(pmiderrors)


# In[11]:

errors = []

for r in data:
    if r['pmid'] == 'ZERO ERROR':
        errors.append(r)


# In[13]:

with open('errorrecords.json', 'w') as fout:
    json.dump(errors, fout, indent = 4)


# In[ ]:

