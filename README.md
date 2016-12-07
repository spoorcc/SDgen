# ServiceDispatcher IDL

This (proof-of-concept) script generates header files based on OMG IDL language.

## Setup

    pip install idl_parser

## Usage

To demonstrate usage, a example interface was created in data folder.
When passed to SDgen as only argument a RGB_client.h file is generated.

    bin/SDgen.py data/RGB.idl

## Background info

* [Intro to OMG IDL](https://mhanckow.students.wmi.amu.edu.pl/corba/IDL.html)
* [idl_parser on pip](https://pypi.python.org/pypi/idl_parser/)
* [ServiceDispatcher](https://github.com/Tom360V/ServiceDispatcher)

