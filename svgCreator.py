def render_svg(name, size, color_background, color_line, coordinates):

    #save some infos
    

    #start writing file
    image = open(name + '.svg', 'w')
    writePreamble(image, size, color_background)
    coordsOld = coordinates.pop(0)
    for coords in coordinates:
        x1 = str(coordsOld[0])
        y1 = str(coordsOld[1])
        x2 = str(coords[0])
        y2 = str(coords[1])
        image.write('<line x1="' + x1 + '" y1="' + y1 + '" x2="' + x2 + '" y2="' + y2 + '" ')
        image.write('style="stroke:rgba' + str(color_line) + ';stroke-width:2" />\n')
        coordsOld = coords
    writePostamble(image)



def writePreamble(image, size, color_background):
    width = str(size[0])
    height = str(size[1])
    image.write('<?xml version="1.0" standalone="no"?>\n')
    image.write('<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" ')
    image.write('"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">\n')
    image.write('<svg width="' +  width + '" height="' + height + '" ')
    image.write('version="1.1" xmlns="http://www.w3.org/2000/svg">\n')
    image.write('<rect width="' + width + '" height="' + height + '" ')
    image.write('style="fill:rgb' + str(color_background) +'" />')



def writePostamble(image):
    image.write('</svg>')
