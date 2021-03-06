"""
joint utils @ utils
"""

import maya.cmds as mc

def listHierarchy( topJoint, withEndJoints = True ):

    """
    List joint hierarchy starting with top joint

    :param topJoint: str, joint to get the listed with its joint hierarchy
    :param withEndJoints: bool, list hierarchy including end joints
    :return: list( str ), listed joints starting with top joint
    """

    listedJoints = mc.listRelatives( topJoint, type = 'joint', ad = True )
    listedJoints.append( topJoint )
    listedJoints.reverse()

    completeJoints = listedJoints[:]

    if not withEndJoints:
        completeJoints = [ j for j in listedJoints if mc.listRelatives( j, c = 1, type = 'joint' ) ]

    return completeJoints