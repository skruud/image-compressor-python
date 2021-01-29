import threading
import os

import datetime

from image_loader import ImageLoader
from safe_counter import SafeCounter
from image_compressor import ImageCompressor

start_time = datetime.datetime.now()

number_of_threads = 8
source_path = r'H:\etc\PythonTest'
destination_path = r'H:\etc\PythonTestD'

# Set default/output directory
os.chdir(destination_path)

image_loader = ImageLoader(source_path)
images = image_loader.get_images()

number_of_images = len(images)
safe_counter = SafeCounter( number_of_images )

if (number_of_threads > number_of_images):
    number_of_threads = number_of_images

def thread_routine():
    file_n = safe_counter.get()
    while (file_n != -1):
        ImageCompressor(images[file_n], quality=65)
        print(len(images), file_n)
        file_n = safe_counter.get()
    print(file_n)


threads = []
for _ in range(number_of_threads):
    threads.append(threading.Thread(target=thread_routine))

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()

end_time = datetime.datetime.now()

print( end_time - start_time)