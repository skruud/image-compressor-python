import os

class ImageLoader:
    def __init__(self, path):
        self.path = path
        self.load_images()

    def load_images(self):
        self.images = [self.path + '\\' + file for file in os.listdir(self.path) 
                        if file.endswith(('jpg', 'JPG', 'PNG', 'png' ))]

    def get_images(self):
        return self.images