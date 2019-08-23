#!/usr/bin/python

from __future__ import print_function
import fontforge

def drawRectangleGlyph(aGlyph, aWidth, aAscent, aDescent):
    p = aGlyph.glyphPen()
    p.moveTo(0, -aDescent)
    p.lineTo(0, aAscent)
    p.lineTo(aWidth, aAscent)
    p.lineTo(aWidth, -aDescent)
    p.closePath();
    aGlyph.width = aWidth

def createStretchyRadical(aFont, em):
    radicalCodePoint = 0x221a
    g = aFont.createChar(radicalCodePoint)
    drawRectangleGlyph(g, em, em, em)
    aFont.math.MinConnectorOverlap = em
    aFont[radicalCodePoint].verticalVariants = "radical"
    aFont[radicalCodePoint].verticalComponents = \
        (("radical", False, 0, em, 2 * em), \
         ("radical", True, em, em, 2 * em))

def createSpace(aFont, em):
    # Create a space character. Also force the creation of some MATH subtables
    # so that OTS will not reject the MATH table.
    g = aFont.createChar(ord(" "), "space")
    g.width = em
    g.italicCorrection = 0
    g.topaccent = 0
    g.mathKern.bottomLeft = tuple([(0,0)])
    g.mathKern.bottomRight = tuple([(0,0)])
    g.mathKern.topLeft = tuple([(0,0)])
    g.mathKern.topRight = tuple([(0,0)])
    aFont[ord(" ")].horizontalVariants = "space"
    aFont[ord(" ")].verticalVariants = "space"
    f.addLookup("gsub", "gsub_single", (), (("ssty", (("math", ("dflt")), ("latn", ("dflt")),)),))
    f.addLookupSubtable("gsub", "gsub_n")
    f["space"].addPosSub("gsub_n", "space")

em = 1000
name="ink-ascent-descent-test"
print("Generating %s..." % name, end="")
f = fontforge.font()
f.fontname = name
f.familyname = name
f.fullname = name
f.encoding = "UnicodeFull"

f.em = em
f.ascent = f.descent = em / 2
f.hhea_ascent = f.os2_typoascent = f.hhea_descent = f.os2_typodescent = em / 2
f.os2_winascent = f.os2_windescent = em
f.hhea_ascent_add = f.hhea_descent_add = f.hhea_linegap = 0
f.os2_typoascent_add = f.os2_typodescent_add = f.os2_typolinegap = 0
f.os2_winascent_add = f.os2_windescent_add = f.vhea_linegap = 0
f.os2_use_typo_metrics = True

createSpace(f, em)
g = f.createChar(ord('A'))
drawRectangleGlyph(g, em, em, 0)
g = f.createChar(ord('B'))
drawRectangleGlyph(g, em, 0, em)
g = f.createChar(ord('C'))
drawRectangleGlyph(g, em, em/2, em/2)
createStretchyRadical(f, em)

f.math.AxisHeight = 0
f.math.FractionDenominatorDisplayStyleGapMin = em
f.math.FractionDenominatorDisplayStyleShiftDown = 2 * em
f.math.FractionDenominatorGapMin = em
f.math.FractionDenominatorShiftDown = 2 * em
f.math.FractionNumeratorDisplayStyleGapMin = em 
f.math.FractionNumeratorDisplayStyleShiftUp = 2 * em
f.math.FractionNumeratorGapMin = em
f.math.FractionNumeratorShiftUp = 2 * em
f.math.FractionRuleThickness = em
f.math.RadicalDisplayStyleVerticalGap = em
f.math.RadicalExtraAscender = 2 * em
f.math.RadicalRuleThickness = em
f.math.RadicalVerticalGap = em

f.generate("%s.otf" % name)
f.generate("%s.woff" % name)
if f.validate() == 0:
    print(" done.")
else:
    print(" validation error!")
    exit(1)
