#!/usr/bin/env python
#SETMODE 777

#----------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------ HEADER --#

"""
:author:
    kpm200000

:synopsis:
    This module contains the Autovivification class and reads the contents of
    an XML file.

:description:
    This module contains the Autovivification class, which allows easier/more
    comprehensive access to a dictionary's contents than a normal dictionary. It also
    contains the function to read the contents of an XML file and format them into an
    Autovivification dictionary.

:applications:
    Maya

:see_also:
    n/a
"""

#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- IMPORTS --#

# Default Python Imports
import maya.cmds as cmds
import xml.etree.ElementTree as et

# Imports That You Wrote

#----------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------- FUNCTIONS --#

def read_stack_xml(file_path=None):
    """
    This function reads the contents of a given XML file into a dictionary.

    :param file_path: The location of the XML file on disk.
    :type: str

    :return: The success of the operation
    :type: Autovivificiation dictionary
    """
    # Check the argument
    if not file_path:
        cmds.warning("You must provide a location to write the file.")
        return None

    # Read the XML data from the document
    xml_fh = et.parse(file_path)
    root = xml_fh.getroot()

    # Create the auto dictionary
    contents = Autovivification()
    # Put in the values for every stack listed in the file
    for stack in root:
        for obj in root[0]:
            contents[stack.tag][obj.tag]['tx'] = obj[0].attrib['value']
            contents[stack.tag][obj.tag]['ty'] = obj[1].attrib['value']
            contents[stack.tag][obj.tag]['tz'] = obj[2].attrib['value']
    # Return the auto dictionary
    return contents

#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- CLASSES --#

class Autovivification(dict):
    """
    This is a Python implementation of Perl's Autovivification feature.
    """
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value