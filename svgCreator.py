def render_svg(fileName, size, color_background, color_line, coordinates, scalingFactor = 1.):

    # Output some infos
    print ('\nCreating SVG-image...')
    
    # Write file
    image = open(fileName + '.svg', 'w')
    writePreamble(image, size, color_background, scalingFactor)
    image.write('<polygon points="')
    for coords in coordinates:
        # No need to be perfect, integers are alright
        x = str(int(coords[0] * scalingFactor))
        y = str(int(coords[1] * scalingFactor))
        image.write(x + ',' + y + ' ')
        coordsOld = coords
    image.write('" style="stroke:rgba' + str(color_line) + ';stroke-width:1" />')
    writePostamble(image)

    # Output stuff
    print (fileName + '.svg successfully created!')



def writePreamble(image, size, color_background, scalingFactor):
    width = str(size[0] * scalingFactor)
    height = str(size[1] * scalingFactor)
    image.write('<?xml version="1.0" standalone="no"?>\n')
    image.write('<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" ')
    image.write('"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">\n')
    image.write('<svg width="' +  width + '" height="' + height + '" ')
    image.write('version="1.1" xmlns="http://www.w3.org/2000/svg">\n')
    image.write('<rect width="' + width + '" height="' + height + '" ')
    image.write('style="fill:rgb' + str(color_background) +'" />\n')



def writePostamble(image):
    image.write('</svg>')
