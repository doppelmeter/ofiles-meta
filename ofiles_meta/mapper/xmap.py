import xml.etree.ElementTree as ET


def analyze(ofilemeta):
    tree = ET.parse(ofilemeta.path)
    root = tree.getroot()

    for each in root:
        if each.tag == "{http://openorienteering.org/apps/mapper/xml/v2}notes":
            ofilemeta.note = each.text
        elif each.tag == "{http://openorienteering.org/apps/mapper/xml/v2}georeferencing":
            ofilemeta.scale = each.attrib["scale"]
        elif each.tag == "{http://openorienteering.org/apps/mapper/xml/v2}colors":
            for color in each:
                atr = color.attrib
                ofilemeta._add_color(
                    number=atr["priority"],
                    name=atr["name"],
                    cyan=atr["c"],
                    magenta=atr["m"],
                    yellow=atr["y"],
                    black=atr["k"],
                    opacity=atr["opacity"])
        elif each.tag == "{http://openorienteering.org/apps/mapper/xml/v2}barrier":
            for barrier in each:
                if barrier.tag == "{http://openorienteering.org/apps/mapper/xml/v2}symbols":
                    for symbol in barrier:
                        atr = symbol.attrib
                        ofilemeta._add_symbol(
                            number=atr["code"], name=atr["name"])
                        print(symbol.attrib)
                print(color.tag)
        print(each.tag)

    return (ofilemeta)


class x:
    def _add_color(self, *namd):
        pass

    pass


x.path = r"C:\Users\Marius\Google Drive\Computer\Python\ofiles_meta\ofiles_meta\mapper\forest_sample.xmap"

# analyze(x)
