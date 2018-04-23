import os
from ofiles_meta.ocad.ocd import analyze as analyze_ocd
from ofiles_meta.ocad.ocdDem import analyze as analyze_ocdDem
from ofiles_meta.mapper.xmap import analyze as analyze_xmap


class _StatVar:
    file_type_from_ocad = [".ocd", ".ocdDem"]
    file_type_from_mapper = [".omap", ".xmap"]


class OFileMeta:
    def __init__(self):
        """Defines the variables for all posible attributes"""
        # basic file information
        self.path = None
        self.filename = None
        self.file_extension = None  # .ocd, .xmap, ...
        self.file_group = None  # OCAD, Mapper, ...
        self.file_type = None  # Map, CourseSetting, ...

        # general file informations
        self.note = None  # for example the OCAD-Map-note
        self.version = None  # vor example by OCAD files OCAD12

        # map's meta informations
        self.scale = None
        self.crs_code = None
        self.crs_name = None
        self.colors = []  # list of color-objects
        self.backgroundmaps = []  #list of backgroundmap objects
        self.symbols = []  #list of symbol objects

        # course-setting informations
        self.courses = []  # list of course-objects

        # raster file
        self.pixelsize = None
        self.coordinate_bottomleft = None
        self.coordinate_topright = None
        self.pixel_minvalue = None
        self.pixel_maxvalue = None
        self.pixel_pixelsize_in_x = None
        self.pixel_pixelsize_in_y = None

    def _add_color(self,
                   *,
                   number=None,
                   name=None,
                   cyan=None,
                   yellow=None,
                   black=None,
                   magenta=None,
                   opacity=None):
        self.colors.append(
            Color(
                number=number,
                name=name,
                cyan=cyan,
                yellow=yellow,
                black=black,
                magenta=magenta,
                opacity=opacity))

    def _add_symbol(self, *, number=None, name=None):
        self.symbols.append(Symbol(number=number, name=name))

    def info(self):
        output = ""
        output += "Filename: " + self.filename + "\n"
        output += "=" * 20 + "\n"
        for key in self.__dict__.keys():
            if type(self.__dict__[key]) == list:
                lenght = len(self.__dict__[key])
                if lenght > 0:
                    output += "{:<30}{:<}\n".format(key,
                                                    str(self.__dict__[key][0]))
                    for i in range(1, lenght):
                        output += "{:<30}{:<}\n".format(
                            "", str(self.__dict__[key][i]))
                else:
                    output += "{:<30}{:<}\n".format(key, "None")
            else:
                output += "{:<30}{:<}\n".format(key, str(self.__dict__[key]))
        return (output)

    def __str__(self):
        return (self.info())


class Color:
    def __init__(self,
                 *,
                 number=None,
                 name=None,
                 cyan=None,
                 yellow=None,
                 black=None,
                 magenta=None,
                 opacity=None):
        self.number = number
        self.name = name
        self.cyan = cyan
        self.yellow = yellow
        self.black = black
        self.magenta = magenta
        self.opacity = opacity

    def __str__(self):
        string = "Number:{:>8} Name:{:30} c:{:<6} m:{:<6} y:{:<6} k:{:<6} Opacity:{:<6}".format(
            self.number, self.name, self.cyan, self.magenta, self.yellow,
            self.black, self.opacity)
        return (string)


class backgroundmap:
    pass


class Symbol:
    def __init__(self, *, number=None, name=None):
        self.number = number
        self.name = name

    def __str__(self):
        string = "Number:{:>8} Name:{:30}".format(self.number, self.name)
        return (string)


class course:
    pass


def get_meta(path):
    """main function for getting all metadata of an file"""
    ofilemeta = OFileMeta()

    ofilemeta.path = path
    ofilemeta.filename = os.path.basename(path)
    ofilemeta.file_extension = os.path.splitext(ofilemeta.filename)[1]

    # Check to which file-group the file-type belongs to
    if ofilemeta.file_extension in _StatVar.file_type_from_ocad:
        ofilemeta.file_group = "OCAD"

        if ofilemeta.file_extension == ".ocd":
            ofilemeta = analyze_ocd(ofilemeta)
        elif ofilemeta.file_extension == ".ocdDem":
            ofilemeta = analyze_ocdDem(ofilemeta)
    elif ofilemeta.file_extension in _StatVar.file_type_from_mapper:
        ofilemeta.file_group = "Mapper"
        if ofilemeta.file_extension == ".xmap":
            ofilemeta = analyze_xmap(ofilemeta)
    else:
        ofilemeta.file_group = "Not Supported"

    return (ofilemeta)
