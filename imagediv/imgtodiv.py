#!/usr/bin/env python

import random
import imageio
import pathlib

PRJ_WORKDIR = pathlib.Path(__file__).parent.resolve()
PRJ_ROOT = PRJ_WORKDIR.parent
PRJ_NAME = PRJ_ROOT.name
IMG_EXAMPLE = PRJ_ROOT / 'example.png'


class Converter:
    """ Converts a source image to a html file containing colored divs, each one
    corresponding to a pixel of the original image.
    Source images can be .png or .jpg, oder formats may work but are
    untested.
    Since this is crazy inefficient, output files and browser load get 
    huge pretty quickly.
    The example source image is a gameboy color screenshot in original 
    resolution: 160x144. This still works reasonably well.
    """
    def __init__(self, img_source):
        self.pixelarray = imageio.imread(img_source)
        self.img_height = len(self.pixelarray)
        self.img_width = len(self.pixelarray[0])
        with open(PRJ_WORKDIR / 'frame.html', 'r') as f:
            self.html = f.read()
        html, css = self.make_html()
        with open(PRJ_WORKDIR / 'output' / 'index.html', 'w') as f:
            f.write(html)
        with open(PRJ_WORKDIR / 'output' / 'style.css', 'w') as f:
            f.write(css)
        
    def make_html(self):
        divs = []
        css = ['div {\n width:1px; height:1px; float: left }\n']
        colors = {}
        k = 1
        for i in range(self.img_height):
            hexvalue_prev = ''
            n = 1
            for j in range(self.img_width):
                # Get the rgb value for current pixel and convert to hex
                r, g, b, _ = self.pixelarray[i][j]
                hexvalue = f'#{r:02x}{g:02x}{b:02x}'
                # Only create div when horizontal color changes.
                if (hexvalue_prev == hexvalue) and (j + 1 < self.img_width):
                    n += 1
                    continue
                else:
                    # See if this color is already indexed
                    try:
                        css_id = colors[hexvalue_prev]
                    except KeyError:
                        css_id = k 
                        colors[hexvalue_prev] = css_id
                        css.append(f'#n{css_id} {{\n background: {hexvalue_prev} }}\n')
                    # Create the div with id
                    divs.append(' ' * 8 + f'<div id=n{css_id} style="width:{n}px"></div>')
                    k += 1
                    n = 1
                    hexvalue_prev = hexvalue
            divs.append('<div style="float:none"></div>')
        return self.html.replace('{}', '\n'.join(divs)), ''.join(css)
        

if __name__ == '__main__':
    c = Converter(IMG_EXAMPLE)

