"""

Module for making rig controls

"""

import maya.cmds as mc

class Control():
    """

    """
    def __init__(self, prefix = 'new', scale = 1.0, translateTo = '', rotateTo = '', parent = '', shape = 'circle', lockChannels = ['s', 'v']):

        """
        :param prefix: str, prefix to name new objects
        :param scale: float, scale value for size of control shapes
        :param translateTo: str, reference object for control position
        :param rotateTo: str, reference object for the control orientation
        :param parent: str, object to be parent of new control
        :param shape: str, shape of the new control
        :param lockChannels: list( str ), list of channels on the control to be locked and non-keyable
        :return none
        """

        ctrlObject = mc.circle(n = prefix + '_ctl', ch = False, normal = [1,0,0], radius = scale )[0]
        ctrlOffset = mc.group( n = prefix + 'offset_grp', em = 1 )
        mc.parent( ctrlObject, ctrlOffset )

        #color control

        ctrlShape = mc.listRelatives( ctrlObject, s = 1 )[0]
        mc.setAttr( ctrlShape + '.ove', 1 )

        if prefix.startswith( 'l_' ):
            mc.setAttr( ctrlShape + '.ovc', 6 )

        elif prefix.startswith( 'r_' ):
            mc.setAttr( ctrlShape + '.ovc', 13 )

        else:
            mc.setAttr( ctrlShape + '.ovc', 22 )

        # translate control

        if mc.objExists ( translateTo ):
            mc.delete( mc.pointConstraint( translateTo, ctrlOffset ) )

        #rotate control

        if mc.objExists( rotateTo ):
            mc.delete( mc.orientConstraint( rotateTo, ctrlOffset ))

        #parent control

        if mc.objExists( parent ):
            mc.parent( ctrlOffset, parent )

        #lock control channels

        singleAttributeLockList = []

        for lockChannel in lockChannels:
            if lockChannel in ['x', 'y', 'z']:
                for axis in ['x', 'y', 'z']:
                    at = lockChannel + axis
                    singleAttributeLockList.append( at )
                else:
                    singleAttributeLockList.append( lockChannel )

        for at in singleAttributeLockList:
            mc.setAttr( ctrlObject + '.' + at, l = 1, k = 0)

        #add public members

        self.C = ctrlObject
        self.Off = ctrlOffset