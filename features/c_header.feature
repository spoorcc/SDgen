Feature: The generated C header file

Scenario: Include guards
    Given an interface description file
    When a c header file is generated for the interface
    Then the C header has include guards consisting of name of the IDL interface

Scenario: Include files are correct
    Given an interface description file
    When a c header file is generated for the interface
    Then the C header includes ServiceDispatcher.h

