import os
from PIL import Image,ImageFilter
import subprocess


if __name__ == '__main__':
    out_folder = "./out"
    banner = "CAREBEARS"
    font_width = 26
    font_height = 26
    rows = 5
    characters_per_row = 12

    font = Image.open('fonts/carebear.jpg')
    banner_width = len(banner) * font_width
    #font.rotate(45).show()
    out_image = Image.new("RGB", (banner_width, font_height))

    letters={}
    character=' '
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

    #completed = subprocess.run(["jp2a", "--width=" + str(banner_width), "--colors", "24", "--fill",  banner_file], capture_output=True)
    completed = subprocess.run(["jp2a", "--width=" + str(banner_width), "--colors", "--color-depth=24","--fill", banner_file], capture_output=True)
    print(completed.stdout.decode("ascii"))

    print(completed.stderr.decode("ascii"))

    completed.check_returncode()

