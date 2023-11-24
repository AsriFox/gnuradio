# Copyright 2016 Free Software Foundation, Inc.
# This file is part of GNU Radio
#
# SPDX-License-Identifier: GPL-2.0-or-later
#

from ruamel.yaml import YAML
from .yaml_grc import typ, init_typ, ListFlowing, OrderedDictFlowing
from ruamel.yaml.scalarstring import LiteralScalarString as MultiLineString

from collections import OrderedDict
from ruamel.yaml.comments import CommentedMap, CommentedSeq

__all__ = ['dump', 'safe_load',
           'ListFlowing', 'OrderedDictFlowing', 'MultiLineString']


class GRCYAML(YAML):
    def __init__(self, output=None):
        YAML.__init__(self, output=output)
        self.typ = [typ]
        init_typ(self)


def dump(data, stream, default_flow_style=False, indent=2):
    if isinstance(data, dict) or isinstance(data, OrderedDict):
        data = CommentedMap(data)
    elif not isinstance(data, CommentedMap):
        raise TypeError(f'Expected mapping, found {type(data)}')
    
    # Add line breaks between top-level keys
    keys = list(data.keys())
    for i in range(1, len(keys)):
        t = type(data[keys[i - 1]])
        if ((t in [list, CommentedSeq] and t is not ListFlowing)
            or (t in [dict, OrderedDict, CommentedMap]
                and t is not OrderedDictFlowing)):
            data.yaml_set_comment_before_after_key(keys[i], before='\n\n')

    with GRCYAML(output=stream) as yaml:
        yaml.default_flow_style = default_flow_style
        yaml.indent = indent
        return yaml.dump(data)


def safe_load(stream):
    with GRCYAML() as yaml:
        return yaml.load(stream)
