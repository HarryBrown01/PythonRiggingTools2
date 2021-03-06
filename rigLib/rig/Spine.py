import maya.cmds as mc

from ..base import module
from ..base import control

def build( spineJoints, rootJnt, spineCurve, bodyLocator, chestLocator, pelvisLocator, prefix = 'spine', rigScale = 1.0, baseRig = None ):

    # make rig module

    rigmodule = module.Module( prefix = prefix, baseObj = baseRig )

    # make spine curve clusters

    spineCurveCVs = mc.ls( spineCurve + '.cv[*]', fl = 1 )
    numSpineCVs = len( spineCurveCVs )
    spineCurveClusters = []

    for i in range( numSpineCVs ):

        cls = mc.cluster( spineCurveCVs[i], n = prefix + 'Cluster%d' % ( i + 1 ) )[1]
        spineCurveClusters.append( cls )

    mc.hide( spineCurveClusters )

    # make controls

    bodyCtrl = control.Control( prefix = prefix + 'Body', translateTo = bodyLocator, scale = rigScale * 4,
                               parent = rigmodule.controlsGrp )

    chestCtrl = control.Control( prefix = prefix + 'Chest', translateTo = chestLocator, scale = rigScale * 6,
                               parent = bodyCtrl.C )

    pelvisCtrl = control.Control( prefix = prefix + 'Pelvis', translateTo = pelvisLocator, scale = rigScale * 6,
                               parent = bodyCtrl.C )

    middleCtrl = control.Control( prefix = prefix + 'Middle', translateTo = spineCurveClusters[2], scale = rigScale * 6,
                               parent = bodyCtrl.C )

    # attach controls

    mc.parentConstraint( chestCtrl.C, pelvisCtrl.C, middleCtrl.C, sr = ['x', 'y', 'z'], mo = 1 )

    # attach clusters

    mc.parent( spineCurveClusters[3:], chestCtrl.C )
    mc.parent( spineCurveClusters[2], middleCtrl.C )
    mc.parent( spineCurveClusters[:2], pelvisCtrl.C )

    # make IK handle

    spineIk = mc.ikHandle( n = prefix + '_ikh', sol = 'ikSplineSolver', sj = spineJoints[0], ee = spineJoints[-2], c = spineCurve, ccv = 0, parentCurve = 0 )[0]
    mc.hide( spineIk )
    mc.parent( spineIk, rigmodule.partsNoTransGrp )

    # setup IK twist

    mc.setAttr( spineIk + '.dTwistControlEnable', 1 )
    mc.setAttr( spineIk + '.dWorldUpType', 4 )
    mc.connectAttr( chestCtrl.C + '.worldMatrix[0]', spineIk + '.dWorldUpMatrixEnd' )
    mc.connectAttr( pelvisCtrl.C + '.worldMatrix[0]', spineIk + '.dWorldUpMatrix' )

    # attach root joint

    mc.parentConstraint( pelvisCtrl.C, rootJnt, mo = 1 )

    return  { 'module':rigmodule }
