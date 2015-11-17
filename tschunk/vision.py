import zbar
from PIL import Image
from SimpleCV import Image as SimpleImage, Camera


class vision(object):

    cam = Camera(2)

    def get_commands_array (self):
        img = self.cam.getImage()
        img.save('image.jpg')

        # create a reader
        scanner = zbar.ImageScanner()

        # configure the reader
        scanner.parse_config('enable')

        # obtain image data
        pil = img.getPIL().convert('L')
        width, height = pil.size
        raw = pil.tostring()

        # wrap image data
        image = zbar.Image(width, height, 'Y800', raw)

        # scan the image for barcodes
        scanner.scan(image)

        # extract results
        for symbol in image:
            # do something useful with results
            print 'decoded', symbol.type, 'symbol', '"%s"' % symbol.data

        return [[6, 3, 1, 3], [0, 0, 0, 5], [0, 0, 0, 0], [0, 0, 0, 0]]
