#!/usr/bin/python3
import sys
import os
from os import path
from copy import deepcopy
import defusedxml.ElementTree as Detree
# we need to use xml.etree as well because while
# defusedxml's () fn is really just a callthrough
# to xml's tostring, defusedxml doesn't also
# have a facade for its register_namespace fn.
# required for correct serialization
import xml.etree.ElementTree as Xetree
import re

VERBOSE=True

def debug(msg):
    if VERBOSE:
        print(msg)

def readxml(l_f):
    with open(l_f, mode='r', encoding='UTF-8') as f:
        return Detree.fromstring(f.read())

def xml_to_str(o_etree):
    return '<?xml version="1.0" encoding="UTF-8"?>\n'.encode('utf-8')+\
        Xetree.tostring(o_etree)
    
def write_utf8(l_f, data):
    with open(l_f, mode='wb') as f:
        f.write(data)
        f.flush()
        
_NAMESPACES={}
for x in ['office', 'style', 'text', 'table', 'drawing', 'meta', 'datastyle', 'svg-compatible', 'chart', 'dr3d', 'form', 'script', 'config']:
    uri='urn:oasis:names:tc:opendocument:xmlns:{}:1.0'.format(x)
    _NAMESPACES[x] = '{'+uri+'}'
    Xetree.register_namespace(x, uri)
    
class ODTree:
    NAMESPACES=_NAMESPACES

    # the below three methods basically reproduce relatively
    # new (3.2+) search-by-namespace fn-ality also w/o facade
    # in defusedxml elements
    
    @staticmethod
    def find(el, namespace, key):
        return el.find(ODTree.NAMESPACES[namespace]+key)

    # returns key and value of first attribute with the passed
    # key-end, regardless of namespace

    @staticmethod
    def namespace_match(text, key):
        pattern=re.compile('^.*\}'+key+'$')
        return re.match(pattern, text)
    
    @staticmethod
    def item_match(el, key):
        for curkey in el.keys():
            print("curkey:"+curkey)
            if ODTree.namespace_match(curkey, key):
                print("match")
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
        el_autostyles.remove(x)
    it_body=ODTree.find(fodt_etree, 'office', 'body').iter()
    for x in it_body:
        style=ODTree.item_match(x, 'style-name')
        if style and style['value'] in set_autostyles:
            del x.attrib[style['key']]
    return fodt_etree

def first_deletion_pass(fodt_etree_in):
    # mark redundant open tags (tags with contents,
    #  where the tag's existence doesnt have any effect
    #  on the contents, document, etc.) for deletion
    # remove closed tags.
    
    fodt_etree = deepcopy(fodt_etree_in)    
    it_body=ODTree.find(fodt_etree, 'office', 'body').iter()
    for x in it_body:
        if x.tag == ODTree.NAMESPACES['text']+'span' and not \
           ODTree.item_match(x, 'style-name'):
            x.tag='DELETEME'    
    return fodt_etree

def second_deletion_pass(fodt_str_in):
    fodt_str=fodt_str_in
    fodt_str=re.sub('</?DELETEME[^<>]*>'.encode('utf-8'),b'', fodt_str)
    return fodt_str

def main(l_fodt, l_fodt_out=None):
    l_out=l_fodt_out if l_fodt_out else l_fodt
    fodt=readxml(l_fodt)
    fodt=deautostyler(fodt)
    fodt=first_deletion_pass(fodt)
    fodt_str=xml_to_str(fodt)
    fodt_str=second_deletion_pass(fodt_str)
    write_utf8(l_out, fodt_str)
    
if __name__=='__main__':
    main(sys.argv[1])
