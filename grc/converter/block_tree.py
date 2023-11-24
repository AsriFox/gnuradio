# Copyright 2016 Free Software Foundation, Inc.
# This file is part of GNU Radio
#
# SPDX-License-Identifier: GPL-2.0-or-later
#
"""
Converter for legacy block tree definitions in XML format
"""


from ..core.io import yaml
from . import xml


def from_xml(filename):
    """Load block tree description from xml file"""
    element, version_info = xml.load(filename, 'block_tree.dtd')

    try:
        data = convert_category_node(element)
    except NameError:
        raise ValueError('Conversion failed', filename)

    return data


def dump(data, stream):
    stream.write('# auto-generated by grc.converter\n\n')
    yaml.dump(data, stream)


def convert_category_node(node):
    """convert nested <cat> tags to nested lists dicts"""
    assert node.tag == 'cat'
    name, elements = '', []
    for child in node:
        if child.tag == 'name':
            name = child.text.strip()
        elif child.tag == 'block':
            elements.append(child.text.strip())
        elif child.tag == 'cat':
            elements.append(convert_category_node(child))
    return {name: elements}
