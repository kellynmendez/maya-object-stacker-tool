#!/usr/bin/env python
#SETMODE 777

#----------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------ HEADER --#

"""
:author:
    kpm200000

:synopsis:
    This module creates a GUI for the user to input what items to stack.

:description:
    This module creates a GUI that will allow the user to select objects, choose which
    items belong to which category (bottom, middle, or top of the stack), the number of
    stacks to make, maximum height of a stack, and distance between stacks. The GUI will
    duplicate the geometry specified in order to create the stack of objects, will use the
    stacker module in order to stack the objects, and will also warn users if any fields
    are missing information or given the wrong information.

:applications:
    Maya

:see_also:
    n/a
"""

#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- IMPORTS --#

# Default Python Imports
import random
from PySide2 import QtWidgets
import maya.cmds as cmds

# Imports That You Wrote

from td_maya_tools.guis.maya_gui_utils import get_maya_window
from td_maya_tools.stacker import stack_objs
from td_maya_tools.stacker import get_center_point
from td_maya_tools.stacker import offset_objs_in_x
from td_maya_tools.gen_utils import read_stack_xml

#----------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------- FUNCTIONS --#

#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- CLASSES --#

class BuilderGUI(QtWidgets.QDialog):
    """
    A GUI that will create a certain number of stacks of three objects as specified
    by the user.
    """
    def __init__(self):
        QtWidgets.QDialog.__init__(self, parent=get_maya_window())
        # The line edits for the top, middle, and base categories
        self.top_le = None
        self.middle_le = None
        self.base_le = None
        # Lists of the objects chosen by the user for each category
        self.base_objects = None
        self.middle_objects = None
        self.top_objects = None
        # The QSpinBoxes for stack count and max height
        self.stack_count_box = None
        self.max_height_box = None
        # The QDoubleSpinBox for the separation
        self.set_separation_box = None
        # The tree view
        self.tree_view = None

    def init_gui(self):
        """
        Creates and displays the GUI to the user.
        """
        # Make the main layout
        main_vb = QtWidgets.QVBoxLayout(self)

        # Create horizontal layout for QFormLayout and tree view
        qform_and_tree_view_hb = QtWidgets.QHBoxLayout()
        # Getting and adding QFormLayout to horizontal layout
        qform_layout = self.make_options_layout()
        qform_and_tree_view_hb.addLayout(qform_layout)
        # Creating tree view
        self.tree_view = QtWidgets.QTreeWidget()
        # Customizing tree view
        self.tree_view.setAlternatingRowColors(True)
        self.tree_view.setMinimumWidth(200)
        self.tree_view.setMinimumHeight(140)
        self.tree_view.setHeaderLabel('Object Stacks')
        # Connect click function to whenever something is selected in tree view
        self.tree_view.selectionModel().selectionChanged.connect(
            self.tree_item_clicked)

        # Adding tree view to layout
        qform_and_tree_view_hb.addWidget(self.tree_view)
        # Add the horizontal layout to the main layout
        main_vb.addLayout(qform_and_tree_view_hb)

        # Create horizontal layout for load xml, make stacks, and cancel buttons
        btns_hb = QtWidgets.QHBoxLayout()
        # Create Load XML button and customize it
        load_xml_btn = QtWidgets.QPushButton('Load XML')
        load_xml_btn.clicked.connect(self.apply_xml)
        load_xml_btn.setStyleSheet('background-color: OrangeRed')
        # Create Make Stacks button and customize it
        make_stacks_btn = QtWidgets.QPushButton('Make Stacks')
        make_stacks_btn.clicked.connect(self.make_stacks)
        make_stacks_btn.setStyleSheet('background-color: ForestGreen')
        # Create Cancel button and customize it
        cancel_btn = QtWidgets.QPushButton('Cancel')
        cancel_btn.clicked.connect(self.close)
        cancel_btn.setStyleSheet('background-color: LightCoral')
        # Add buttons to horizontal layout
        btns_hb.addWidget(load_xml_btn)
        btns_hb.addWidget(make_stacks_btn)
        btns_hb.addWidget(cancel_btn)
        # Add the horizontal layout to the main layout
        main_vb.addLayout(btns_hb)

        # Add title to window
        self.setWindowTitle('Builder')
        # Show the GUI to the user
        self.setGeometry(300, 300, 600, 350)
        self.show()

    def make_options_layout(self):
        """
        Uses a QFormLayout to place the following widgets: three buttons for setting
        selection of top, middle and bottom parts; three line edits that acknowledge
        that top, middle, and bottom parts have been set; three labels that indicated
        the stack count, maximum height, and separation values; two QSpinBox widgets
        for entering count and max height; QDoubleSpinBox for setting separation value

        :return: The QFormLayout that was made.
        :type: QFormLayout
        """
        # Creating the QFormLayout
        layout = QtWidgets.QFormLayout()

        # Create horizontal layout for the top category row
        top_hb = QtWidgets.QHBoxLayout()
        # Create the top line edit
        self.top_le = QtWidgets.QLineEdit()
        # Create the top button, connect it, and name it
        top_btn = QtWidgets.QPushButton('Set Top Parts')
        top_btn.clicked.connect(self.set_selection)
        top_btn.setObjectName('Top Button')
        # Add button and line edit to horizontal layout
        top_hb.addWidget(top_btn)
        top_hb.addWidget(self.top_le)
        # Adding to QFormLayout
        layout.addRow(top_hb)

        # Create horizontal layout for the middle category row
        middle_hb = QtWidgets.QHBoxLayout()
        # Create the middle line edit
        self.middle_le = QtWidgets.QLineEdit()
        # Create middle the button, connect it, and name it
        mid_btn = QtWidgets.QPushButton('Set Mid Parts')
        mid_btn.clicked.connect(self.set_selection)
        mid_btn.setObjectName('Middle Button')
        # Add button and line edit to horizontal layout
        middle_hb.addWidget(mid_btn)
        middle_hb.addWidget(self.middle_le)
        # Adding to QFormLayout
        layout.addRow(middle_hb)

        # Create horizontal layout for the base category row
        base_hb = QtWidgets.QHBoxLayout()
        # Create the base line edit
        self.base_le = QtWidgets.QLineEdit()
        # Create the base button, connect it, and name it
        base_btn = QtWidgets.QPushButton('Set Base Parts')
        base_btn.clicked.connect(self.set_selection)
        base_btn.setObjectName('Base Button')
        # Add button and line edit to horizontal layout
        base_hb.addWidget(base_btn)
        base_hb.addWidget(self.base_le)
        # Adding to QFormLayout
        layout.addRow(base_hb)

        # Create labels for stack count, max height, and separation values
        num_stacks_lbl = QtWidgets.QLabel('Set Stack Count')
        max_height_lbl = QtWidgets.QLabel('Set Max Height')
        separation_lbl = QtWidgets.QLabel('Set Separation')
        # Create a QSpinBox for stack count
        self.stack_count_box = QtWidgets.QSpinBox()
        # Setting default to 3 and minimum to 1
        self.stack_count_box.setValue(3)
        # Create a QSpinBox for max height
        self.max_height_box = QtWidgets.QSpinBox()
        # Setting default max height to 3, and setting range to be 1 to 6
        self.max_height_box.setValue(3)
        # Create QDoubleSpinBox for setting separation
        self.set_separation_box = QtWidgets.QDoubleSpinBox()
        # Making increment 0.1 and setting default value and minimum value to 0.1
        self.set_separation_box.setValue(0.1)
        self.set_separation_box.setSingleStep(0.1)
        # Add each to the QFormLayout
        layout.addRow(num_stacks_lbl, self.stack_count_box)
        layout.addRow(max_height_lbl, self.max_height_box)
        layout.addRow(separation_lbl, self.set_separation_box)

        # Return the layout
        return layout

    def set_selection(self):
        """
        This function gets the current selection and updates the appropriate line edit
        by displaying the number of objects, making it uneditable, and changing its color

        :return: Whether the function completed without error
        :type: bool
        """
        # Get the user's selection
        sel = cmds.ls(selection=True)
        # Check if the selection exists
        if not sel:
            # If selection does not exist, warn the user
            self.warn_user('Builder - Selection', 'You must have objects selected.')
            return None
        # Getting size of selection and formatting into string
        sel_size = len(sel)
        num_objects_str = f"{sel_size} objects"

        # Find which button called the function
        sender = self.sender()
        if sender:
            # If button called was the top category button
            if str(sender.objectName()) == 'Top Button':
                # Save objects and change the line edit text to string with object amount
                self.top_objects = sel
                self.top_le.setText(num_objects_str)
                # Making read only and changing color
                self.top_le.setReadOnly(True)
                self.top_le.setStyleSheet('background-color: OliveDrab')
            # If button called was the middle category button
            elif str(sender.objectName()) == 'Middle Button':
                # Save objects and change the line edit text to string with object amount
                self.middle_objects = sel
                self.middle_le.setText(num_objects_str)
                # Making read only and changing color
                self.middle_le.setReadOnly(True)
                self.middle_le.setStyleSheet('background-color: OliveDrab')
            # If button called was the base category button
            elif str(sender.objectName()) == 'Base Button':
                # Save objects and change the line edit text to string with object amount
                self.base_objects = sel
                self.base_le.setText(num_objects_str)
                # Making read only and changing color
                self.base_le.setReadOnly(True)
                self.base_le.setStyleSheet('background-color: OliveDrab')
        # Return true if there are no errors
        return True

    def make_stacks(self):
        """
        This function randomly chooses an object given from each of the base, middle,
        and top categories, duplicates the geometry, then creates the stack using the
        stacker module and groups the pieces of the stack.

        :return: Whether the function completed without error.
        :type: bool
        """
        # Verify the arguments entered are valid
        valid_args = self.verify_args()
        # If the arguments are not valid, immediately end function
        if not valid_args:
            return None

        # Creating list of stacks
        list_of_stacks = []
        # Create the stacks
        for num in range(self.stack_count_box.value()):
            # Randomly choose an option from each category
            base = random.choice(self.base_objects)
            top = random.choice(self.top_objects)
            # Duplicate the base object and save in list of objects to duplicate
            obj_to_stack = cmds.duplicate([base])

            # Find how many random middle objects to add
            num_middle_objs = random.randint(1, self.max_height_box.value())
            # Make all middle object duplicates
            for mid_num in range(num_middle_objs):
                # Get random middle object
                middle = random.choice(self.middle_objects)
                # Duplicate the middle
                mid_dup = cmds.duplicate([middle])
                # Append it to the list of objects to duplicate
                obj_to_stack.append(mid_dup[0])

            # Append top object to list of objects to duplicate
            obj_to_stack.append(cmds.duplicate([top])[0])

            # Use stacker module to stack the objects
            stack_objs(obj_to_stack)
            # Group the pieces of the stack together
            group = cmds.group(obj_to_stack, name="stack%03d" % (num + 1))
            # Adding to list of stacks
            list_of_stacks.append(group)
            # Get center point of group using stacker module
            curr_pos = get_center_point(group, bottom_center_flag=True)
            # Use center point to move the group to the origin
            cmds.move(-(curr_pos[0]), -(curr_pos[1]), -(curr_pos[2]), group,
                      relative=True)
            # Freeze transformations so translation values for the group are all zero
            cmds.makeIdentity(group, apply=True, translate=True)
            # Move pivot of group to origin
            cmds.xform(group, absolute=True, worldSpace=True, pivots=[0, 0, 0])
            # Adding the stack to the tree view
            self.add_stack_to_tree_view(obj_to_stack, "stack%03d" % (num + 1))

        # Adding offset between each stack using stacker module
        prev_stack = list_of_stacks[0]
        for stack in list_of_stacks:
            # Skipping first stack
            if stack is list_of_stacks[0]:
                continue
            # Offset the previous stack and the current stack
            offset_objs_in_x(prev_stack, stack, self.set_separation_box.value())
            # Updating previous stack
            prev_stack = stack

        # Return true if there are no errors
        return True

    def add_stack_to_tree_view(self, obj_to_stack=None, stack_name=None):
        """
        This function adds the stack given to the tree view, with the group name as the
        parent and the transform nodes nested under it

        :param obj_to_stack: The contents of the stack to add to the tree view.
        :type: list

        :param stack_name: The name of the stack's group.
        :type: str
        """
        # Adding group to tree view
        group_list = QtWidgets.QTreeWidgetItem(self.tree_view, [stack_name])
        # Add every object that is in the group to the group in tree view
        for obj in obj_to_stack:
            QtWidgets.QTreeWidgetItem(group_list, [obj])

    def apply_xml(self):
        """
        This function allows the user to select an XML file and apply the values of stacks
        in the file to the scene

        :return: Whether XML file values were successfully applied to the scene
        :type: bool
        """
        # Allowing user to select an XML file
        filename, file_filter = QtWidgets.QFileDialog.getOpenFileName(
            caption="Select File",
            dir="C:/Users/kpm200000/Code/class_13",
            filter="Files (*.xml)")
        # If user did not select an XML file, return none
        if not filename:
            self.warn_user('Builder - XML File', 'You must select a file.')
            return None

        # Get contents of file
        contents = read_stack_xml(filename)
        # If the file is empty, return none
        if not contents:
            return None
        # Applying attributes of each stack to objects in Maya
        for stack in contents:
            for obj in contents[stack]:
                cmds.xform(obj, translation=[float(contents[stack][obj]['tx']),
                                               float(contents[stack][obj]['ty']),
                                               float(contents[stack][obj]['tz'])])
        return True

    def verify_args(self):
        """
        This function checks that the GUI has all the information it needs and verifies
        that the user entered an integer for the number of stacks to make.

        :return: Whether all the fields have a value which is valid.
        :type: bool
        """
        # Check if top line edit is empty
        if not self.top_le.text():
            # Warn the user if empty
            self.warn_user('Builder - Selection', 'You must set a selection for the top'
                                                  ' parts.')
            return None
        # Check if middle line edit is empty
        elif not self.middle_le.text():
            # Warn the user if empty
            self.warn_user('Builder - Selection', 'You must set a selection for the '
                                                  ' middle parts.')
            return None
        # Check if base line edit is empty
        elif not self.base_le.text():
            # Warn the user if empty
            self.warn_user('Builder - Selection', 'You must set a selection for the base'
                                                  ' parts.')
            return None
        # Check if stack count is at least 1
        elif not self.stack_count_box.value() >= 1:
            # Warn the user if less than 1
            self.warn_user('Builder - Count', 'You must make at least one stack.')
            return None
        # Check if max height is not a value in range [1,6]
        elif not (1 <= self.max_height_box.value() <= 6):
            # Warn the user if out of range
            self.warn_user('Builder - Height', 'The height must be a value from 1 to 6.')
            return None
        # Check if distance is 0
        elif self.set_separation_box.value() == 0:
            # Warn the user that distance is 0
            self.warn_user('Builder - Distance', 'The distance must be greater than'
                                                 ' 0.00.')
            return None
        # Return true if there are no errors
        return True

    def tree_item_clicked(self):
        """
        This function selects the object that is selected in the tree view whenever
        a new selection in the tree view is made
        """
        # Getting the index of the selected item
        index = self.tree_view.currentIndex()
        # Getting the object that was selected
        obj = self.tree_view.model().data(index)
        # Removing all previous selections
        cmds.select(clear=True)
        # Selecting the object
        cmds.select([obj])

    @classmethod
    def warn_user(cls, title=None, msg=None):
        """
        This function displays a message box that locks the screen until the user
        acknowledges it.

        :param title: The title of the message box window.
        :type: str

        :param msg: The text to show in the message box window.
        :type: str
        """
        if msg and title:
            # Create a QMessageBox
            msg_box = QtWidgets.QMessageBox()
            # Set the title and the message of the window
            msg_box.setWindowTitle(title)
            msg_box.setText(msg)
            # Show the message
            msg_box.exec_()