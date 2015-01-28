#!/usr/bin/python

from xml.dom.minidom import parse
import sys
import os

STARTUP_DIR=sys.path[0]

def insert_empty_el(doc, el, tag_name, attr_dict):
  newline = doc.createTextNode('\n            ')
  el.insertBefore(newline, el.lastChild)
  ent_attr = doc.createElement(tag_name)
  for k in attr_dict:
    ent_attr.setAttribute(k, attr_dict[k])
  el.insertBefore(ent_attr, el.lastChild)

# return attrs as list of tuples sorted 
# starting with name followed by the rest in alphabetical
def get_sorted_attrs(el):
  attrs = []
  attrs.append((u'name', el.getAttribute('name')))

  other_attrs = []
  for i in range(el.attributes.length):
    attr_name = el.attributes.item(i).name
    if attr_name != 'name':
      other_attrs.append((attr_name, el.attributes.item(i).value))

  other_attrs.sort()
  attrs += other_attrs
  return attrs

def write_ent_attr(out, el):
  attrs = get_sorted_attrs(el)
  out.write(u"<attr %s/>" % u" ".join(['%s="%s"' % a for a in attrs]))

def write_ent_attrs(out, el):
  out.write('<attrs>')
  attrs_children = el.childNodes
  for ac in attrs_children:
    if ac.nodeType == ac.ELEMENT_NODE:
      write_ent_attr(out, ac)
    else:
      ac.writexml(out)
  out.write('</attrs>')

def write_entry(out, el):
  attrs = get_sorted_attrs(entry)
  out.write(u"      <entry %s>" % u" ".join(['%s="%s"' % a for a in attrs]))
  children = entry.childNodes
  for c in children:
    if c.nodeType == c.ELEMENT_NODE and c.tagName == 'attrs':
      write_ent_attrs(out, c)
    else:
      c.writexml(out)
  out.write(u"</entry>")

if __name__ == '__main__':
  doc = parse(os.path.join(STARTUP_DIR, '../share/tmpl.xml'))

  entry = doc.documentElement
  #entry.writexml(sys.stdout)

  #for c in children:
  #  print c.nodeType

  entry.setAttribute(u'name', u'CMS_T2_US_UCSD_gw7')
  entry.setAttribute(u'comment', u'Added 2013-03-13 --Alex')
  entry.setAttribute(u'gatekeeper', u'osg-gw-7.t2.ucsd.edu:2119/jobmanager-condor')
  entry.setAttribute(u'gridtype', u'gt5')
  entry.setAttribute(u'rsl', u'(queue=default)(jobtype=single)')
  entry.setAttribute(u'work_dir', u'Condor')

  attrs_el = entry.getElementsByTagName('attrs')[0]

  insert_empty_el(doc, attrs_el, u'attr', {u'name':u"GLIDEIN_Max_Walltime",
    u'const':u"True",
    u'glidein_publish':u"False",
    u'job_publish':u"False",
    u'parameter':u"True",
    u'publish':u"True",
    u'type':u"int",
    u'value':u"171000"})

  insert_empty_el(doc, attrs_el, u'attr', {u'name':u"GLIDEIN_ResourceName",
    u'const':u"True",
    u'glidein_publish':u"True",
    u'job_publish':u"True",
    u'parameter':u"True",
    u'publish':u"True",
    u'type':u"string",
    u'value':u"UCSDT2"})

  insert_empty_el(doc, attrs_el, u'attr', {u'name':u"GLIDEIN_Supported_VOs",
    u'const':u"True",
    u'glidein_publish':u"False",
    u'job_publish':u"False",
    u'parameter':u"True",
    u'publish':u"True",
    u'type':u"string",
    u'value':u"CMS,HCC,NEBioGrid,SBGrid,GLUEX,UCSDRok,NWICG,HCCLONG,CMST2UCSD,EngageVO,NEES,OSGVO,CIGI,glowVO,OSGEDU,Fermilab"})

  infosys_el = entry.getElementsByTagName('infosys_refs')[0]

  insert_empty_el(doc, infosys_el, u'infosys_ref',
    {u'ref':u"GlueCEUniqueID=osg-gw-7.t2.ucsd.edu:2119/jobmanager-condor-default,Mds-Vo-name=UCSDT2,Mds-Vo-name=local,o=grid",
      u'server':u'is.grid.iu.edu',
      u'type':u"BDII"})

  write_entry(sys.stdout, entry)
  print
  doc.unlink()
