from os import PathLike


def getOpener(fontPath:PathLike):
    openerKey = sniffFontType(fontPath)
    assert openerKey is not None
    numFontsFunc, openerFunc = fontOpeners[openerKey]
    return numFontsFunc, openerFunc


def sniffFontType(fontPath:PathLike):
    if not isinstance(fontPath, PathLike):
        raise TypeError("fontPath must be a Path(-like) object")
    assert fontPath.is_file()
    openerKey = fontPath.suffix.lower().lstrip(".")
    if openerKey not in fontOpeners:
        return None
    return openerKey


async def openOTF(fontPath:PathLike, fontNumber:int, fontData=None):
    from .baseFont import OTFFont
    if fontData is not None:
        font = OTFFont(fontData, fontNumber)
    else:
        font = OTFFont.fromPath(fontPath, fontNumber)
        fontData = font.fontData
    return (font, fontData)


def numFontsOTF(fontPath:PathLike):
    return 1


def numFontsTTC(fontPath:PathLike):
    from fontTools.ttLib.sfnt import readTTCHeader
    with open(fontPath, "rb") as f:
        header = readTTCHeader(f)
    return header.numFonts


fontOpeners = {
    "ttf":   (numFontsOTF, openOTF),
    "otf":   (numFontsOTF, openOTF),
    "woff":  (numFontsOTF, openOTF),
    "woff2": (numFontsOTF, openOTF),
    "ttc":   (numFontsTTC, openOTF),
    "otc":   (numFontsTTC, openOTF),
}
