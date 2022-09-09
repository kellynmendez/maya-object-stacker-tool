#!/usr/bin/env python
#SETMODE 777

#----------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------ HEADER --#

"""
:author:
    kpm200000

:synopsis:
    This module contains the function to get a pointer back to the Maya window.

:description:
    This module is used to get a pointer back to the Maya window in order to initialize
    the GUI to show to the user.

:applications:
    Maya

:see_also:
    n/a
"""

#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- IMPORTS --#

# Default Python Imports
from PySide2 import QtWidgets
from maya import OpenMayaUI as omui
from shiboken2 import wrapInstance

# Imports That You Wrote

#----------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------- FUNCTIONS --#

def get_maya_window():
    """
    This gets a pointer to the Maya window.

    :return: A pointer to the Maya window.
    :type: pointer
    """
    maya_main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(maya_main_window_ptr), QtWidgets.QWidget)

#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- CLASSES --#

