#!/usr/bin/env python3

import sys, os
import datetime
import errno

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


from idl_parser import parser as idl_parser
import argparse

__author__ = 'Ben'

INDENT = ' '*4

header_file_template='''
/*
 * {filename}
 *
 *  Created on: {date}
 *      Author: {author}
 */

#ifndef {inc_guard}_H_
#define {inc_guard}_H_

#include "ServiceDispatcher.h"

{body}

#endif /* {inc_guard}_H_ */

'''

function_template='''
{indent}void S_{module}{interface}_{method}({arguments});'''

arg_template='''{type} {name}'''

def mkdir_p(path):
    ''' Make directory if it does not exist '''
    try:
        os.makedirs(path)
        logger.info('Created directory %s' % path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

def process_idl_file(idl_path, outdir):

  toplevel = open_and_parse_file(idl_path)

  for module in global_module.modules:
     generate_c_module(module, outdir)

def open_and_parse_file(file_path):

    with open(file_path,'r') as idl_file:
        logger.info('Parsing %s' % idl_file.name)
        _parser = idl_parser.IDLParser()
        global_module = _parser.load(idl_file.read())

    return global_module

def generate_c_module(module, outdir):

    for interface in module.interfaces:
        write_file( *generate_c_interface(module.name, interface, outdir))

def write_file(path, content):

    with open(filename, 'w') as outfile:
        outfile.write(content)

def generate_c_interface(module_name, interface, outdir=''):
    ''' Generate a C header file for an interface '''

    filename = os.path.join(outdir, "%s_%s.h" % (module_name, interface.name))

    logging.info('Creating %s' % filename)

    body = generate_c_methods(module_name, interface)
    inc_guard = (module_name+interface.name).upper()

    content = header_file_template.format(author=__author__,
                                          date=datetime.date.today().isoformat(),
                                          filename=filename,
                                          inc_guard=inc_guard,
                                          body=body)
    return (filename, content)

def generate_c_methods(module_name, interface):

    functions = []

    for method in interface.methods:

        arguments = [arg_template.format(type=generate_c_type(argument.type),
                                         name=argument.name,
                                         indent=INDENT) for argument in method.arguments]
        arguments = ',\n{indent}'.format(indent=3*INDENT).join(arguments) or 'void'

        functions += [function_template.format(arguments=arguments,
                                               indent=INDENT,
                                               module=module_name,
                                               interface=interface.name,
                                               method=method.name)]

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

    parser = argparse.ArgumentParser(description='Generate Service Dispatcher headers')
    parser.add_argument('files', metavar='<idl-file>', type=str, nargs='+',
                         help='IDL file to convert')
    parser.add_argument('-o','--outdir',
                    default='.',
                    help='Output directory for generated files (default: current dir)')

    args = parser.parse_args()

    mkdir_p(args.outdir)

    for path in args.files:
        process_idl_file(idl_file, args.outdir)
