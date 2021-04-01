'''
Banner endpoint handler (defined in swagger.yaml) 
'''

from app import metrics
import os
from PIL import Image,ImageFilter
import subprocess
from dataclasses import dataclass
import logging
from connexion.lifecycle import ConnexionResponse
from connexion import NoContent
from prometheus_client import Counter
from flask import make_response

def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1")

@dataclass
class Font:
    base_from_a: bool
    font_width: int
    font_height: int
    rows: int
    characters_per_row: int
    filename: str  

fonts = { 
    "carebear": Font(filename='fonts/carebear.jpg', base_from_a=False, font_width=26, font_height=26, characters_per_row=12, rows=5),
    "cuddly": Font(filename='fonts/cuddly.jpg', base_from_a=True, font_width=32, font_height=32, characters_per_row=10, rows=5),
    "knight4": Font(filename='fonts/knight4.jpg', base_from_a=False, font_width=32, font_height=25, characters_per_row=10, rows=7),
    "tcb": Font(filename='fonts/tcb.jpg', base_from_a=False, font_width=32, font_height=32, characters_per_row=10, rows=6)
}

SELECTED_FONTS = Counter('font', 'font', ['name'])

@metrics.summary('generate_by_status', 'generate Request latencies by status', labels={
    'code': lambda r: r.status_code
})
def generate(message: str, fontname: str, width: int) -> str:
    '''
    Render the banner message in a fontname with the given terminal width     
    '''

    logger = logging.getLogger()

    output = ""

    if len(message) > 0:    
        out_folder = "./out"
        banner = str.upper(message)

        if fontname not in fonts:
            SELECTED_FONTS.labels("error").inc()
            return "Unsupported font", 400

        selected_font = fonts[fontname]
        # increment font selection counter
        SELECTED_FONTS.labels(fontname).inc()

        font_width = selected_font.font_width
        font_height = selected_font.font_height
        rows = selected_font.rows
        characters_per_row = selected_font.characters_per_row
        font = Image.open(selected_font.filename)

        banner_width = len(banner) * font_width

        #font.rotate(45).show()
        out_image = Image.new("RGB", (banner_width, font_height))

        letters={}

        character=' '
        if selected_font.base_from_a:
            character='A'

        logger.info(f"Cut", extra={"selected_font": selected_font, "banner": message})

        for cursor_y in range(0, rows):
            for cursor_x in range(0, characters_per_row):
                coords = (cursor_x * font_width, cursor_y * font_height, (cursor_x * font_width) + font_width, (cursor_y * font_height) + font_height)
                #print(character + " " + str(coords))
                #letter = font.crop(corrds)
                #letters[character] = letter
                letters[character] = coords
                character = chr(ord(character) + 1) 

        cursor_x = 0
        for letter in banner:
            coords = letters[letter]
            letter_image = font.crop(coords)
            #print(letter + " " + str(coords))
            out_image.paste(letter_image, (cursor_x * font_width, 0)) 
            cursor_x += 1
        #out_image.show()

        if not os.path.exists(out_folder):
            os.makedirs(out_folder)

        banner_file = os.path.join(out_folder, 'banner.jpg')
        out_image.save(banner_file) 

        docker = False
        if 'DOCKER' in os.environ:
            docker = str2bool(os.environ['DOCKER'])
            logger.info(f"DOCKER found in environment {docker}", extra={"docker": docker})

        if width == 0:
            width = banner_width

        logger.info(f"Render", extra={"banner_file": banner_file, "banner": message, "width": width})
        if docker:
            completed = subprocess.run(["jp2a", "--width=" + str(width), "--colors", "--color-depth=24", "--fill", banner_file], capture_output=True)
        else:
            completed = subprocess.run(["jp2a", "--width=" + str(width), "--invert", banner_file], capture_output=True)

        if completed.returncode != 0:
            logger.error(f"Error running jp2a", extra={"stderr": completed.stderr})
            return "Failed to process", 503

        output = completed.stdout.decode("ascii")
        
    logger.info(f"Output", extra={"length": len(output)})

    # ensure that the response is not quoted
    response = make_response(output, 200)
    response.mimetype = "text/plain"
    return response    

@metrics.summary('supported_fonts_by_status', 'supported fonts Request latencies by status', labels={
    'code': lambda r: r.status_code
})
def supported_fonts() -> list:
    '''
    Return list of available fonts
    '''

    return(list(fonts.keys()))
