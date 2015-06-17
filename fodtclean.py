#!/usr/bin/python3
import sys
import os
from os import path
from copy import deepcopy
import defusedxml.ElementTree as etree

def readxml(l_f):
    with open(l_f, mode='r', encoding='UTF-8') as f:
        return etree.fromstring(f.read())

def writexml(l_f, x_etree):
    with open(l_f, mode='wb') as f:
        s_xml=etree.tostring(x_etree)
        f.write(s_xml)
        f.flush()

NAMESPACES={}
for x in ['office', 'style', 'text', 'table', 'drawing', 'meta', 'datastyle', 'svg-compatible', 'chart', 'dr3d', 'form', 'script', 'config']:
    NAMESPACES[x] = '{'+ 'urn:oasis:names:tc:opendocument:xmlns:{}:1.0'.format(x) + '}'
def deautostyler(fodt_etree_in):
    fodt_etree = deepcopy(fodt_etree_in)    
    fodt_etree.find()
    return fodt_etree

def main(l_fodt, l_fodt_out=None):
    l_out=l_fodt_out if l_fodt_out else l_fodt
    fodt=_readxml(l_fodt)
    _writexml(l_out, deautostyler(fodt))
    
if __name__=='__main__':
    main(sys.argv[1])
