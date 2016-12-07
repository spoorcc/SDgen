#!/usr/bin/env python3

import sys
import datetime

from idl_parser import parser

__author__ = 'Ben'

INDENT = ' '*4

header_file_template='''
/*
 * {filename}
 *
 *  Created on: {date}
 *      Author: {author}
 */
'''

header_inc_guard_open_template='''

#ifndef {interface}_H_
#define {interface}_H_

'''

header_inc_guard_close_template='''

#endif /* {interface}_H_ */

'''

function_template='''
{indent}void S_{module}{interface}_{method}('''

def main(idl_str):
  _parser = parser.IDLParser()
  global_module = _parser.load(idl_str)

  for module in global_module.modules:

     generate_c_module(module)

def generate_c_module(module):

    for interface in module.interfaces:
        generate_c_interface(module.name, interface)


def generate_c_interface(module_name, interface):

    filename = "%s_%s.h" % (module_name, interface.name)

    with open(filename, 'w') as header_file:
        header_file.write(header_file_template.format(author=__author__,
                                                      date=datetime.date.today().isoformat(),
                                                      filename=filename))

        inc_guard = (module_name+interface.name).upper()

        header_file.write(header_inc_guard_open_template.format(interface=inc_guard))
        header_file.write('\n#include "ServiceDispatcher.h"\n')
        header_file.write(generate_c_methods(module_name, interface))
        header_file.write(header_inc_guard_close_template.format(interface=inc_guard))

def generate_c_methods(module_name, interface):

    functions = []


    for method in interface.methods:

        functions += [function_template.format(indent=INDENT,
                                               module=module_name,
                                               interface=interface.name,
                                               method=method.name)]

        for argument in method.arguments:
            functions += ['%s%s %s,' % (INDENT*3, generate_c_type(argument.type),
                                           argument.name)]

        functions += [INDENT * 2 + ');']

    return '\n'.join(functions)

def generate_c_type(idl_type):

    if idl_type.is_primitive:
        if str(idl_type) == 'octet':
            return 'uint8_t'
        raise NotImplementedError('Fixme')
    elif idl_type.is_struct:
        raise NotImplementedError('Fixme')

    return str(idl_type).replace('::','_')


if __name__ == '__main__':

    with open(sys.argv[1],'r') as idl_file:
      main(idl_file.read())
