import threading
import os
import sys
from PyQt5 import QtWidgets, uic
import datetime

from image_loader import ImageLoader
from safe_counter import SafeCounter
from image_compressor import ImageCompressor
from MainWindow import Ui_MainWindow

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.lineEditSource.textEdited.connect( self.insert_in_list )
        self.pushButtonCompress.clicked.connect( self.compress )

    def insert_in_list(self):
        image_loader = ImageLoader(source_path)
        self.images = image_loader.get_images()

        self.listWidgetFiles.addItems( self.images )

    def compress(self):
        number_of_threads = self.spinBoxThreads.value()
        self.quality = self.spinBoxQuality.value()
        source_path = self.lineEditSource.text()
        destination_path = self.lineEditDestination.text()
        print(source_path)
        # Set default/output directory
        os.chdir(destination_path)

        
        

        number_of_images = len(self.images)
        self.safe_counter = SafeCounter( number_of_images )

        if (number_of_threads > number_of_images):
            number_of_threads = number_of_images
        
        threads = []
        for _ in range(number_of_threads):
            threads.append( threading.Thread( target=self.thread_routine ) )

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()
        
        self.progressBar.setProperty("value", 100)
    
    def thread_routine(self):
        file_n = self.safe_counter.get()
        while (file_n != -1):
            ImageCompressor(self.images[file_n], quality=self.quality)
            print(len(self.images), file_n)
            file_n = self.safe_counter.get()
            self.progressBar.setProperty("value", file_n/len(self.images)*100)
        print(file_n)
        


app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec()


start_time = datetime.datetime.now()








end_time = datetime.datetime.now()

print( end_time - start_time)