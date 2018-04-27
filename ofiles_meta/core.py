import os
import datetime
from ofiles_meta.ocad.ocd import analyze as analyze_ocd
from ofiles_meta.ocad.ocdDem import analyze as analyze_ocdDem
from ofiles_meta.mapper.xmap import analyze as analyze_xmap


class _StatVar:
    file_type_from_ocad = [".ocd", ".ocdDem"]
    file_type_from_mapper = [".omap", ".xmap"]


class OFileMeta:


    def __init__(self):
        """Define the variables for all posible attributes"""
        # basic file information
        self.file_path = None
        self.file_name = None
        self.file_extension = None  # .ocd, .xmap, ...
        self.file_size = None
        self.file_date_last_modification = None
        self.file_date_last_access = None
        self.file_date_created = None


        # general file informations
        self.meta_group = None  # OCAD, Mapper, ...
        self.meta_type = None  # map, cs, ...
        self.meta_note = None  # for example the OCAD-Map-note
        self.meta_version = None  # vor example by OCAD files OCAD12

        # map's meta informations
        self.map_scale = None
        self.map_crs_code = None
        self.map_crs_name = None
        self.map_colors = []  # list of color-objects
        self.map_backgroundmaps = []  # list of backgroundmap objects
        self.map_symbols = []  # list of symbol objects

        # course-setting informations
        self.cs_courses = []  # list of course-objects

        # raster file
        self.raster_pixelsize = None
        self.raster_coordinate_bottomleft = None
        self.raster_coordinate_topright = None
        self.raster_pixel_minvalue = None
        self.raster_pixel_maxvalue = None
        self.raster_pixel_pixelsize_in_x = None
        self.raster_pixel_pixelsize_in_y = None

    def _add_color(self,
                   *,
                   number=None,
                   name=None,
                   cyan=None,
                   yellow=None,
                   black=None,
                   magenta=None,
                   opacity=None):
        self.map_colors.append(
            Color(
                number=number,
                name=name,
                cyan=cyan,
                yellow=yellow,
                black=black,
                magenta=magenta,
                opacity=opacity))

    def _add_symbol(self, *, number=None, name=None):
        self.map_symbols.append(Symbol(number=number, name=name))

    def info(self):
        """Return alle ofiles_meta attributes nicely formated as string."""
        output = ""
        output += "Filename: " + self.file_name + "\n"
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

def analyze_file(ofile_meta):
    """"add general file-information to a file-meta class

    :argument
    ofile_meta
    :return
    ofile_meta

    """
    if hasattr(ofile_meta, "file_path"):
        path = ofile_meta.file_path
    else:
        path = ofile_meta
    ofile_meta.file_name = os.path.basename(path)
    ofile_meta.file_extension = os.path.splitext(ofile_meta.file_name)[1]
    fileinfo = os.stat(path)
    ofile_meta.file_size = fileinfo.st_size
    ofile_meta.file_date_last_modification = datetime.datetime.fromtimestamp(fileinfo.st_mtime)
    ofile_meta.file_date_last_access = datetime.datetime.fromtimestamp(fileinfo.st_atime)
    ofile_meta.file_date_created = datetime.datetime.fromtimestamp(fileinfo.st_ctime)
    return ofile_meta



def get_meta(path):
    """Main function for getting all metadata of an file.

    arg:
    path: path to a file
    """
    ofilemeta = OFileMeta()

    ofilemeta.file_path = path

    ofilemeta = analyze_file(ofilemeta)

    # Check to which file-group the file-type belongs to
    if ofilemeta.file_extension in _StatVar.file_type_from_ocad:
        ofilemeta.meta_group = "OCAD"

        if ofilemeta.file_extension == ".ocd":
            ofilemeta = analyze_ocd(ofilemeta)
        elif ofilemeta.file_extension == ".ocdDem":
            ofilemeta = analyze_ocdDem(ofilemeta)
    elif ofilemeta.file_extension in _StatVar.file_type_from_mapper:
        ofilemeta.meta_group = "Mapper"
        if ofilemeta.file_extension == ".xmap":
            ofilemeta = analyze_xmap(ofilemeta)
    else:
        ofilemeta.meta_group = "Not Supported"

    return (ofilemeta)
