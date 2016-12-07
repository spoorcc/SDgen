# ServiceDispatcher IDL

This (proof-of-concept) script generates header files based on OMG IDL language.

## Setup

    pip install idl_parser

## Usage

To demonstrate usage, a example interface was created in data folder.
When passed to SDgen as only argument a RGB_client.h file is generated.

    bin/SDgen.py data/RGB.idl


