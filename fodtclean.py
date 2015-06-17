#!/usr/bin/python3
import sys
import os
from os import path
from copy import deepcopy
import defusedxml.ElementTree as etree
import re

def readxml(l_f):
    with open(l_f, mode='r', encoding='UTF-8') as f:
        return etree.fromstring(f.read())

def writexml(l_f, x_etree):
    with open(l_f, mode='wb') as f:
        s_xml=etree.tostring(x_etree)
        f.write(s_xml)
        f.flush()
        
_NAMESPACES={}
for x in ['office', 'style', 'text', 'table', 'drawing', 'meta', 'datastyle', 'svg-compatible', 'chart', 'dr3d', 'form', 'script', 'config']:
    _NAMESPACES[x] = '{'+ 'urn:oasis:names:tc:opendocument:xmlns:{}:1.0'.format(x) + '}'

class ODTree:
    NAMESPACES=_NAMESPACES
    
    @staticmethod
    def find(el, namespace, key):
        return el.find(ODTree.NAMESPACES[namespace]+key)

    # returns key and value of first attribute with the passed
    # key-end, regardless of namespace
    
    @staticmethod
    def item_match(el, key):
        pattern = re.compile('^.*\}'+key+'$')
        for curkey in el.keys():
            if re.match(pattern, curkey):
                return {'key': curkey, 'value': el.get(curkey)}
        return None    
    
    @staticmethod
    def get(el, namespace, key):
        return el.get(ODTree.NAMESPACES[namespace]+key)

def deautostyler(fodt_etree_in):
    fodt_etree = deepcopy(fodt_etree_in)    
    el_autostyles=ODTree.find(fodt_etree, 'office', 'automatic-styles')
    set_autostyles=set()
    for x in el_autostyles.getchildren():
        set_autostyles.add(ODTree.get(x, 'style', 'name'))
    it_body=ODTree.find(fodt_etree, 'office', 'body').iter()
    for x in it_body:
        style=ODTree.item_match(x, 'style-name')
        if style['value'] in set_autostyles:
            del x.attrib(style['key'])
    return fodt_etree

def main(l_fodt, l_fodt_out=None):
    l_out=l_fodt_out if l_fodt_out else l_fodt
    fodt=_readxml(l_fodt)
    fodt=deautostyler(fodt)
    _writexml(l_out, fodt)
    
if __name__=='__main__':
    main(sys.argv[1])
