from image_loader import ImageLoader

source_path = r'H:\etc\PythonTest'
destination_path = r'H:\etc\PythonTestD'

#os.chdir(destination_path)

image_loader = ImageLoader(source_path)
print( image_loader.get_images()[0] )