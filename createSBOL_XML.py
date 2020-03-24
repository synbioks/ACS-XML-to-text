
# coding: utf-8

# # Extract data and create json of formatted data
# Runs over existing XML files, extracts data, formats into new xml structure, and writes out the new version.

# In[20]:

import pathlib
from lxml import etree
import random
import requests
import json
import time
from bs4 import BeautifulSoup


# In[21]:

xmlfiles = list(pathlib.Path('data_folders/').glob('**/*.xml'))


# In[22]:

originalfiles = [f for f in xmlfiles if not f.stem.endswith('-RDF')]


# In[23]:

rando = random.choice(originalfiles)


# In[24]:

rando


# In[25]:

def create_new_xml(json_record):
    xmlout = """<?xml version="1.0" encoding="UTF-8"?>
<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:prov="http://www.w3.org/ns/prov#" xmlns:sbol="http://sbols.org/v2#" xmlns:xsd="http://www.w3.org/2001/XMLSchema#dateTime/" xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:obo="http://purl.obolibrary.org/obo/">"""
    xmlout += '\n    <sbol:Attachment rdf:about="https://dummy.org/' + json_record['sbol:displayId'] + '/1">'
    xmlout += '\n        <sbol:persistentIdentity rdf:resource="https://dummy.org/'+ json_record['sbol:displayId'] + '"/>'
    xmlout += '\n        <sbol:version>1</sbol:version>'
    xmlout += '\n        <sbol:source rdf:resource="'+ json_record['doi_formatted'] + '"/>'
    xmlout += '\n        <sbol:format rdf:resource="http://identifiers.org/edam/format_3508"/>'
    xmlout += '\n        <obo:OBI_0001617>' + json_record['pmid'] + '</obo:OBI_0001617>'
    xmlout += '\n        <dcterms:type rdf:resource="http://purl.org/dc/dcmitype/Text"/>'
    xmlout += '\n        <dc:type>' + json_record['article_type'] +'</dc:type>'
    xmlout += '\n        <dcterms:isPartOf>' + json_record['jounal_title'] +'</dcterms:isPartOf>'
    xmlout += '\n        <dc:publisher>' + json_record['jounal_publisher'] + '</dc:publisher>'
    xmlout += '\n        <dcterms:isPartOf rdf:resource="http://pubs.acs.org/journal/asbcd6" />'
    xmlout += '\n        <dcterms:title>' + json_record['article-title'] + '</dcterms:title>'
    for each in json_record['authors']:
        xmlout += '\n        <dc:creator>' + each + '</dc:creator>'
    try:
        xmlout += '\n        <dcterms:created>Missing</dcterms:created>'
    except:
        xmlout += '\n        <dcterms:created>' + json_record['created_date'] + '</dcterms:created>'
    xmlout += '\n        <dcterms:dateSubmitted>' + json_record['submitted_date'] + '</dcterms:dateSubmitted>'
    xmlout += '\n        <dcterms:dateCopyrighted>' + json_record['copyrightyear'] + '</dcterms:dateCopyrighted>'
    xmlout += '\n        <dcterms:dateAccepted>' + json_record['accepteddate'] + '</dcterms:dateAccepted>'
    xmlout += '\n        <dc:rights>' + json_record['copyrightstatement'] + '</dc:rights>'
    xmlout += '\n        <dcterms:rightsHolder>' + json_record['rightsholder'] + '</dcterms:rightsHolder>'
    xmlout += '\n        <dcterms:abstract>' + json_record['abstract'] + '</dcterms:abstract>'
    xmlout += '\n        <dcterms:description>' + json_record['abstract'] + '</dcterms:description>'
    for each in json_record['keywords']:
        xmlout += '\n        <dc:subject>' + each + '</dc:subject>'
    for each in json_record['refs']:
        xmlout += '\n        <dcterms:references>' + each + '</dcterms:references> '
    xmlout += '    </sbol:Attachment>'
    xmlout += '</rdf:RDF>'
    soup = BeautifulSoup(xmlout, 'lxml')
    tree = etree.fromstring(soup.prettify().encode('utf-8'))
    root = tree.xpath('//body/*')[0]
    return etree.tostring(root, pretty_print=True)


# In[26]:


def get_pmid(doi):
    """Function to retrieve UID crosswalk from pubmed.
       Pass it a doi as a string, starting with the 10..., and it will download the json results."""
#     url = "https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?ids=" + doi + "&format=json"
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=" + doi + "&format=json"
    print(url)
    r = requests.get(url)
    results = json.loads(r.text)
    r.close()
    time.sleep(2)
    count = results['esearchresult']['count']
    if count == "0":
        return "ZERO ERROR"
    elif count == "1":
        ids = results['esearchresult']['idlist']
        if len(ids) != 1:
            return "NUMBER OF IDS ERROR"
        else:
            return ids[0]
    else:
        print(results)
        return "MORE THAN 1 RESULT ERROR"
    
def assemble_date(node):
    "takes in a node and extracts values and assembles iso date"
    day = node.xpath('./day/text()')
    assert len(day) == 1
    month = node.xpath('./month/text()')
    assert len(month) == 1
    year = node.xpath('./year/text()')
    assert len(month) == 1
    daytext = day[0].strip()
    monthtext = month[0].strip()
    yeartext = year[0].strip()
    date = '-'.join([yeartext, monthtext, daytext])
    return date

def create_journal(node):
    result = ""
    names = node.xpath('.//name')
    formattednames = []
    for n in names:
        sur = "".join(n.xpath('./surname//text()'))
        gn = "".join(n.xpath('./given-names//text()'))
        formattednames.append(sur + ", " + gn)
    result += ", ".join(formattednames)
    
#     title = " ".join("".join(node.xpath('.//article-title//text()')))
    result += " " + " ".join(("".join(node.xpath('.//article-title//text()'))).split())
    result += " " + " ".join(("".join(node.xpath('.//source//text()'))).split())
    result += " " + " ".join(("".join(node.xpath('.//year//text()'))).split())  + "."
    try:
        result += " " + node.xpath('.//volume//text()')[0]
        try:
            result += ":" + node.xpath('.//fpage//text()')[0] + "-" + node.xpath('.//lpage//text()')[0] + "."
        except:
            result += "."
    except:
        pass
    
    return result

def create_book(node):
    return " ".join(("".join(node.xpath('.//text()'))).split())
#     result = ""
#     names = node.xpath('.//name')
#     formattednames = []
#     for n in names:
#         sur = "".join(n.xpath('./surname//text()'))
#         gn = "".join(n.xpath('./given-names//text()'))
#         formattednames.append(sur + ", " + gn[0].upper() + ".")
#     result += ", ".join(formattednames)
    
    

def assemble_citation(node):
    "accept a single ref element and assemble a single string citation from it."
    reftype = node.xpath('./*/@publication-type')
    if len(reftype) == 0:
        return "ERROR"
    elif reftype[0] == 'journal':
        return create_journal(node)
    elif reftype[0] == 'book':
        return create_book(node)
    elif reftype[0] == 'weblink':
        return create_book(node)
    else:
        return create_book(node)


def process_record(path):
    print(path)
    data = {'sbol:displayId': "", 'doi': ""}
    xml = path.read_text().encode('utf-8')
    root = etree.fromstring(xml)
    ns = root.nsmap

    # get 'sbol:displayId' from article id
    article_id = root.xpath('//article/@id', namespaces = ns)
    assert len(article_id) == 1
    data['sbol:displayId'] = article_id[0]
    
    # get doi
    doi = root.xpath('//article-id[@pub-id-type = "doi"]/text()')
    assert len(doi) == 1
    data['doi_formatted'] = "https://pubs.acs.org/doi/" + doi[0]
    data['doi'] = doi[0]
    data['pmid'] = get_pmid(data['doi'])
    
    # get article type
    article_type = root.xpath('//article/@article-type')
    if len(article_type) == 1:
        data['article_type'] = article_type[0]
    else:
        data['article_type'] = "Research Article"
        
    # get journal title
    jtitle = root.xpath('//journal-title-group/journal-title//text()')
    if len(jtitle) == 1:
        data['jounal_title'] = jtitle[0]
    else:
        print("warning missing title")
        data['jounal_title'] = "ACS Synthetic Biology"
        
    # get journal publisher
    jpublisher = root.xpath('//publisher/publisher-name//text()')
    if len(jpublisher) == 1:
        data['jounal_publisher'] = jpublisher[0]
    else:
        print("warning missing publisher")
        data['jounal_publisher'] = "American Chemical Society"
        
    # get article title
    
    atitle = root.xpath('//title-group/article-title//text()')
    data['article-title'] = " ".join(" ".join(atitle).split())
    
    # get authors
    authors = root.xpath('//contrib-group/contrib[@contrib-type = "author"]')
    authornames = []
    for a in authors:
        surname = " ".join(a.xpath('./name/surname/text()')).replace('\n', ' ')
        givennames = " ".join(a.xpath('./name/given-names/text()')).replace('\n', ' ')
        name = givennames + " " + surname
        authornames.append(name)
    data['authors'] = authornames
    
    # get created date
    
    creatednode = root.xpath('//pub-date[@pub-type="epub"]')
    
    assert len(creatednode) <= 1
    if len(creatednode) == 1:
        data['created_date'] = assemble_date(creatednode[0])
    else:
        data['created_node'] = "Missing"

    # get date submitted
    
    submittednode = root.xpath('//history/date[@date-type = "received"]')
    assert len(submittednode) == 1
    data['submitted_date'] = assemble_date(submittednode[0])
    
    # get copyright date
    
    copyrightdatenode = root.xpath('//permissions/copyright-year/text()')
    assert len(copyrightdatenode) == 1
    data['copyrightyear'] = copyrightdatenode[0]
    
    # get accepted date
    
    accepteddatenode = root.xpath('//history/date[@date-type ="just-accepted"]')
    if len(accepteddatenode) == 1:
        data['accepteddate'] = assemble_date(accepteddatenode[0])
    else:
        data['accepteddate'] = "Missing"
    
    # get copyright statement
    
    copyrightstatement = root.xpath('//permissions/copyright-statement/text()')
    if len(copyrightstatement) == 1:
        data['copyrightstatement'] = copyrightstatement[0]
    else:
        data['copyrightstatement'] = "Missing"
    
    # get rights holder
    
    rightsholder = root.xpath('//permissions/copyright-holder/text()')
    assert len(rightsholder) == 1
    data['rightsholder'] = rightsholder[0]
    
    # get abstract
    
    abstract = root.xpath('//abstract[not(@*)]//text()')
    spotlight = root.xpath('//abstract[@abstract-type = "spotlight-teaser"]//text()')
    if len(abstract) > 0:
        data['abstract'] = "".join(abstract).strip().replace('\n', ' ')
    elif len(spotlight) > 0:
        data['abstract'] = "".join(spotlight).strip().replace('\n', ' ')
    elif len(root.xpath('//abstract')) == 0:
        data['abstract'] = "Missing"
    else:
        assert False
    
    data['description'] = data['abstract']
    
    # get keywords
    
    kwds = root.xpath('//kwd-group/kwd')
    keywords = []
    for k in kwds:
        k = "".join(k.xpath('.//text()'))
        keywords.append(k)
    data['keywords'] = keywords
    
    # assemble citations
    
    refs = root.xpath('//ref-list/ref')
    formattedrefs = []
    for r in refs:
        formattedrefs.append(assemble_citation(r))
    
    data['refs'] = formattedrefs
    
    return data


# In[ ]:




# In[19]:

data = []

for f in originalfiles:
    xmlfname = f.parent / pathlib.Path(str(f.stem) + '-RDF.xml')
    j = process_record(f)
    xml = create_new_xml(j)
    xmlfname.write_text(xml.decode('utf-8'))
#     data.append(process_record(f))


# In[20]:

with open('inital_data_extraction.json', 'w') as fout:
    json.dump(data, fout, indent = 4)


# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:
