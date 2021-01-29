from PIL import Image

class ImageCompressor:
    def __init__(self, image_source, quality):
        self.image_source = image_source
        self.quality = quality
        self.open_image()
        self.compress()

    def open_image(self):
        self.image = Image.open(self.image_source)

    def compress(self):
        print(self.image_source.split('\\')[-1])
        self.image.save("Compressed_and_resized_with_function_"
                            +self.image_source.split('\\')[-1], 
                            optimize=True, quality=self.quality)