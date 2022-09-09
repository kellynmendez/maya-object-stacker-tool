#!/usr/bin/env python
#SETMODE 777

#----------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------ HEADER --#

"""
:author:
    kpm200000

:synopsis:
    This module stacks three random shapes in Maya on top of each other.

:description:
    This module creates a stack of objects from the list of objects given. The base object
    is the first object in the list, and it provides the center point to stack the other
    objects on top of, but does not move. The rest of the objects in the list are stacked
    in the order that they are given, with the last object in the list being the top.
    All the objects are centered around the base's top center point.

:applications:
    Maya

:see_also:
    n/a
"""

#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- IMPORTS --#

# Default Python Imports
import maya.cmds as cmds

# Imports That You Wrote

#----------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------- FUNCTIONS --#

def stack_objs(obj_trans_list=None):
    """
    This function stacks the given objects on top of one another, all centered
    around the top center point of the base object. The objects are stacked in the order
    they are passed, the first object being the base and the last object being the top.

    :param obj_trans_list: The translational nodes of the objects to stack
    :type: list

    :return: Indicates if the objects were stacked successfully.
    :type: bool
    """
    # Check to see if the correct arguments were passed
    if not verify_args(obj_trans_list):
        cmds.warning("You need to provide a list that contains the translational"
                     " nodes of objects.")
        return None

    # Getting the first base object of the list
    base_obj = obj_trans_list[0]
    # For every object in the list, stack it on object listed before it
    for top_obj in obj_trans_list:
        # Skip the first object since it is the first base object
        if top_obj is obj_trans_list[0]:
            continue
        # Get the top center of the base object
        bases_top_center = get_center_point(base_obj, True, False)
        # Get the bottom center of the top object
        tops_bottom_center = get_center_point(top_obj, False, True)
        # Move the top object so that it is resting on the base object
        create_stack(top_obj, tops_bottom_center, bases_top_center)
        # Changing next base object to current top object
        base_obj = top_obj
    return True

def create_stack(obj_trans=None, bottom_center_point=None, point_to_place=None):
    """
    This function moves the object given so that its bottom center point is sitting at
    the point in space given to place the object.

    :param obj_trans: The translational node of the object.
    :type: str

    :param bottom_center_point: The current point of the object's bottom center, given in
    form (x, y, z).
    :type: list

    :param point_to_place: The point in space at which to place the object, given in
    form (x, y, z).
    :type: list
    """
    # Finding the amount to move the object in each axis relative to its current location
    x_move_amt = point_to_place[0] - bottom_center_point[0]
    y_move_amt = point_to_place[1] - bottom_center_point[1]
    z_move_amt = point_to_place[2] - bottom_center_point[2]
    # Moving the object
    cmds.move(x_move_amt, y_move_amt, z_move_amt, obj_trans, relative=True)


def get_center_point(obj_trans=None, top_center_flag=None, bottom_center_flag=None):
    """
    This function uses the bounding box of an object to return a list with either the top
    center coordinates (x, y, z) or the bottom center coordinates (x, y, z) of an object,
    depending on the flags passed.

    :param obj_trans: The translational node of the object.
    :type: str

    :param top_center_flag: True if returning the top center coordinates.
    :type: bool

    :param bottom_center_flag: True if returning the bottom center coordinates.
    :type: bool

    :return: Either the top center coordinates (x, y, z) or the bottom center coordinates
    (x, y, z) depending on the flags passed.
    :type: list
    """
    # Get the bounding box of the object passed in; note that bounding box is returned as
    #   a list with argument order [xmin, ymin, zmin, xmax, ymax, zmax]
    bounding_box = cmds.xform(obj_trans, query=True, boundingBox=True)
    # Calculate the X and Z center coordinates
    center_point = [0, 0, 0]
    center_point[0] = (bounding_box[0] + bounding_box[3]) / 2
    center_point[2] = (bounding_box[2] + bounding_box[5]) / 2
    # Set Y coordinate based on flags
    if top_center_flag:
        # Y coordinate is ymax, because we are looking for the top center point
        center_point[1] = bounding_box[4]
    if bottom_center_flag:
        # Y coordinate is ymin, because we are looking for the bottom center point
        center_point[1] = bounding_box[1]
    return center_point

def offset_objs_in_x(stationary_obj=None, move_obj =None, offset=0):
    """
    This function takes two transform nodes, where one will be moved to be a given offset
    away from the other along the x-axis by using the bounding box information of the
    nodes. The offset is the distance between the edges of the two bounding boxes.

    :param stationary_obj: The translational node of the object that will not be moved.
    :type: str

    :param move_obj: The translational node of the object that will be moved.
    :type: str

    :param offset: The distance/separation between the two translational nodes.
    :type: float
    """
    # Get the bounding box of both objects passed in; note that bounding box is returned
    #   as a list with argument order [xmin, ymin, zmin, xmax, ymax, zmax]
    bound_box_stat = cmds.xform(stationary_obj, query=True, boundingBox=True)
    bound_box_move = cmds.xform(move_obj, query=True, boundingBox=True)
    # Moving the object so the two objects are right next to each other
    #    (stationary's xmax - move's xmin) then adding the offset
    cmds.move(bound_box_stat[3] - bound_box_move[0] + offset, 0, 0, move_obj,
              relative=True)

def verify_args(obj_trans_list=None):
    """
    This function checks that the argument passed into the stack_objs function is a
    non-empty list

    :param obj_trans_list: The translational nodes of the objects to stack
    :type: list

    :return: Indicates if the arguments were passed in.
    :type: bool
    """
    # Checking that the argument exists and is not empty
    if not list:
        return None
    # Checking that what was passed is a list
    if type(obj_trans_list) is not list:
        return None
    # Return true if argument is a non-empty list
    return True



#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- CLASSES --#

