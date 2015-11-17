import zbar
from PIL import Image
from SimpleCV import Image as SimpleImage, Camera
import ImageEnhance


# Command Values
# 1 ... Left
# 3 ... Straight
# 4 ... Non Operation
# 5 ... Drop
# 6 ... Start


class vision(object):

    cam = Camera(2)

    def get_commands_array(self):
        #return [[3, 1, 3, 5], [4, 0, 0, 1], [4, 1, 3, 1], [0, 0, 0, 0]]

        img = self.cam.getImage()
        img.save('image.jpg')
        pil = img.getPIL().convert('L')

        # enhance contrast
        contrast = ImageEnhance.Contrast(pil)
        pil = contrast.enhance(2);

        width, height = pil.size

        scanner = zbar.ImageScanner()
        scanner.parse_config('enable')

        image_count = 0
        commands_array = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        x = 0
        for left_pos in range(0, width, (width / 4)):
            y = 0
            for top_pos in range(0, height, (height / 4)):
                image_count += 1
                crop_box = (left_pos, top_pos, left_pos + (width / 4), top_pos + (height / 4))
                crop_image = pil.crop(crop_box)
                crop_image.save('image' + `image_count` + '.jpg')

                raw = crop_image.tobytes()
                # todo: what is Y800?
                image = zbar.Image((width / 4), (height / 4), 'Y800', raw)
                scanner.scan(image)

                for symbol in image:
                    commands_array[x][y] = int(symbol.data)
                    break
                y += 1
            x += 1

        print commands_array
        return commands_array
