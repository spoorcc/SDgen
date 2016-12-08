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

def process_idl_file(idl_str, outdir):
  _parser = idl_parser.IDLParser()
  global_module = _parser.load(idl_str)

  for module in global_module.modules:

     generate_c_module(module, outdir)

def generate_c_module(module, outdir):

    for interface in module.interfaces:
        generate_c_interface(module.name, interface, outdir)


def generate_c_interface(module_name, interface, outdir):

    filename = os.path.join(outdir, "%s_%s.h" % (module_name, interface.name))

    with open(filename, 'w') as header_file:
        logging.info('Creating %s' % header_file.name)
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

    parser = argparse.ArgumentParser(description='Generate Service Dispatcher headers')
    parser.add_argument('files', metavar='<idl-file>', type=str, nargs='+',
                         help='IDL file to convert')
    parser.add_argument('-o','--outdir',
                    default='.',
                    help='Output directory for generated files (default: current dir)')

    args = parser.parse_args()

    mkdir_p(args.outdir)

    for path in args.files:
        with open(path,'r') as idl_file:
            logger.info('Converting %s' % idl_file.name)
            process_idl_file(idl_file.read(), args.outdir)
