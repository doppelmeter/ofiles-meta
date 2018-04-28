from xml.etree import ElementTree as ET


class Xmap:
    def analyze(ofilemeta):
        tree = ET.parse(ofilemeta.file_path)
        root = tree.getroot()

        for each in root:
            if each.tag == "{http://openorienteering.org/apps/mapper/xml/v2}notes":
                ofilemeta.meta_note = each.text
            elif each.tag == "{http://openorienteering.org/apps/mapper/xml/v2}georeferencing":
                ofilemeta.map_scale = each.attrib["scale"]
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

        return (ofilemeta)
