#Author-
#Description-

import adsk.core, adsk.fusion, adsk.cam, traceback, math

A = 4
B = 4
a = 5
b = 4
wd = 0.3
th = 0.5
stp = 2

app = adsk.core.Application.get()
if app:
    ui = app.userInterface
    product = app.activeProduct
design = adsk.fusion.Design.cast(product)
rootComp = design.rootComponent
sketches = rootComp.sketches
xyPlane = rootComp.xYConstructionPlane

def run(context):
    ui = None
    toolBodies = adsk.core.ObjectCollection.create()
    try:
        s = stp * 2
        r1 = A - wd / 2
        r2 = B - wd / 2
        d = math.pi / 180
        ctr = 0
        for i in range(0, 720 + s, s):
            x1 = math.cos(i * a / 2 * d) * r1
            x2 = math.cos((i + s) * a / 2 * d) * r1
            y1 = math.sin(i * b / 2 * d) * r2
            y2 = math.sin((i + s) * b / 2 * d) * r2
            vx = y1 - y2
            vy = x2 - x1
            l = math.sqrt(vx * vx + vy * vy)
            vx = vx / l
            vy = vy / l
            x1s = x1 - vx * wd / 2
            x1e = x1 + vx * wd / 2
            y1s = y1 - vy * wd / 2
            y1e = y1 + vy * wd / 2
            if i != 0:
                sk1 = sk2
            sk2 = sketches.add(xyPlane)
            linel2 = sk2.sketchCurves.sketchLines
            linel2.addByTwoPoints(adsk.core.Point3D.create(x1s, y1s, 0), adsk.core.Point3D.create(x1e, y1e, 0))
            linel2.addByTwoPoints(adsk.core.Point3D.create(x1e, y1e, 0), adsk.core.Point3D.create(x1e, y1e, th))
            linel2.addByTwoPoints(adsk.core.Point3D.create(x1e, y1e, th), adsk.core.Point3D.create(x1s, y1s, th))
            linel2.addByTwoPoints(adsk.core.Point3D.create(x1s, y1s, th), adsk.core.Point3D.create(x1s, y1s, 0))
            if i != 0:
                prof1 = sk1.profiles.item(0)
                prof2 = sk2.profiles.item(0)
                loftFeats = rootComp.features.loftFeatures
                loftInput = loftFeats.createInput(adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
                loftSectionsObj = loftInput.loftSections
                loftSectionsObj.add(prof1)
                loftSectionsObj.add(prof2)
                loftInput.isSolid = True
                loft = loftFeats.add(loftInput)
            if ctr == 1:
                targetBody = loft.bodies.item(0)
            elif ctr > 1:
                toolBodies.add(loft.bodies.item(0))
            ctr += 1
        combFeats = rootComp.features.combineFeatures
        combInput = combFeats.createInput(targetBody, toolBodies)
        comb = combFeats.add(combInput)
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
