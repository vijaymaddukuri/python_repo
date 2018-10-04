from xml.etree.ElementTree import Element, SubElement, ElementTree



root_tag = Element('directories')
dir_tag=SubElement(root_tag, 'directory')
dir_tag.set('name', r'c:\users\madduv\Desktop')

file_tag=SubElement(dir_tag, 'file')
file_tag.attrib=dict(size='308160', mtime= 'Sun Dec 11 11:11:11: 2017')
file_tag.text= 'instance.xls'
doc_tree = ElementTree(root_tag)
doc_tree.write('tmp.xml')

