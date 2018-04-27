from struct import unpack_from


def analyze(ofilemeta):
    file = open(ofilemeta.file_path, "rb")

    header = file.read(65)
    file.close()

    struc_string ="<b8shx10i"
    unpacked = unpack_from(struc_string, header)

    ofilemeta.meta_version = unpacked[2]
    ofilemeta.raster_pixelsize = str(unpacked[3])+"x"+str(unpacked[4])
    ofilemeta.raster_coordinate_bottomleft = str(unpacked[5])+", "+str(unpacked[7])
    ofilemeta.raster_coordinate_topright = str(unpacked[6])+", "+str(unpacked[8])
    ofilemeta.raster_pixel_minvalue = unpacked[9]
    ofilemeta.raster_pixel_maxvalue = unpacked[10]
    ofilemeta.raster_pixel_pixelsize_in_x = unpacked[11]
    ofilemeta.raster_pixel_pixelsize_in_y = unpacked[12]

    return(ofilemeta)


class x:
    pass


x.path = r"C:\Users\Marius\Google Drive\Computer\Python\ofiles_meta\ofiles_meta\test\testfiles\OcadDem-File-Sample.ocdDem"
# analyze(x)
