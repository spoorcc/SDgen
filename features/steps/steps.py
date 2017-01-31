from behave import *
from SDgen import *
from idl_parser import parser as idl_parser

@given(u'an interface description file')
def step_impl(context):
    context.idl_file = 'data/RGB.idl'

@when(u'a c header file is generated for the interface')
def step_impl(context):

    toplevel = SDgen.open_and_parse_file(context.idl_file)
    context.toplevel_module = toplevel

    assert len(toplevel.modules) > 0
    for module in toplevel.modules:

        assert len(module.interfaces) > 0
        for interface in module.interfaces:
            (filename, body) = SDgen.generate_c_interface(module.name, interface)
            context.generated_c_headers = {filename: body}

    assert len(context.generated_c_headers) > 0

@then(u'the C header has include guards consisting of name of the IDL interface')
def step_impl(context):

    assert len(context.toplevel_module.modules) > 0
    for module in context.toplevel_module.modules:
        assert len(module.interfaces) > 0
        for interface in module.interfaces:
            assert len(context.generated_c_headers) > 0
            for filename, body in context.generated_c_headers.items():

                if module.name in filename and interface.name in filename:
                    define = '{0}{1}_H_'.format(module.name.upper(),
                                                interface.name.upper())
                    assert '#ifndef {0}'.format(define) in body
                    assert '#define {0}'.format(define) in body
                    assert '#endif /* {0} */'.format(define) in body


@then(u'the C header includes {header_file}')
def step_impl(context, header_file):

    assert len(context.toplevel_module.modules) > 0

    for module in context.toplevel_module.modules:

        assert len(module.interfaces) > 0
        for interface in module.interfaces:
            assert len(context.generated_c_headers) > 0
            for filename, body in context.generated_c_headers.items():

                assert '#include "{header_file}"'.format(**locals()) in body

