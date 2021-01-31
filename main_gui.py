import threading
import os
import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog
import time

from image_loader import ImageLoader
from safe_counter import SafeCounter
from image_compressor import ImageCompressor
from MainWindow import Ui_MainWindow
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5 import QtGui



class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    _signal = pyqtSignal(int)

    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.lineEditSource.textChanged.connect( self.insert_in_list )
        self.pushButtonCompress.clicked.connect( self.compress )
        self.pushButtonDestination.clicked.connect( self.destination_directory )
        self.pushButtonSource.clicked.connect( self.source_directory )
        
    def source_directory(self): 
        dir_path = QFileDialog.getExistingDirectory(self,
                                                    "Choose Directory")
        print(dir_path)
        self.lineEditSource.setText( dir_path )

    def destination_directory(self): 
        dir_path = QFileDialog.getExistingDirectory(self,
                                                    "Choose Directory")
        print(dir_path)
        self.lineEditDestination.setText( dir_path )

    def insert_in_list(self, text):
        try:
            source_path = self.lineEditSource.text()
            print(source_path)
            image_loader = ImageLoader(source_path)
            self.images = image_loader.get_images()
            self.filenames = [image.split('\\')[-1] for image in self.images]
            self.listWidgetFiles.clear()
            self.listWidgetFiles.addItems( self.filenames )
            
        except:
            print('Invalid directory')

    def compress(self):
        number_of_threads = self.spinBoxThreads.value()
        self.quality = self.spinBoxQuality.value()
        source_path = self.lineEditSource.text()
        destination_path = self.lineEditDestination.text()
        
        # Set default/output directory
        os.chdir(destination_path)

        number_of_images = len(self.images)
        self.safe_counter = SafeCounter( number_of_images )

        self._signal.connect(self.update_progressbar)

        if (number_of_threads > number_of_images):
            number_of_threads = number_of_images
        
        main_thread = threading.Thread( target=self.main_routine, args=(number_of_threads, ) ).start()
            

    def update_progressbar(self, msg):
        progress = int(int(msg)/len(self.images)*100)
        self.progressBar.setProperty("value", progress )
        print(msg, progress)
        if (progress==100):
            self.pushButtonCompress.setEnabled(True)
        else:
            self.pushButtonCompress.setEnabled(False)
            self.listWidgetFiles.item(int(msg)).setBackground(QtGui.QColor('sea green'))
            
        
    def main_routine(self, number_of_threads):    
        threads = []
        for _ in range(number_of_threads):
            threads.append( threading.Thread( target=self.thread_routine ) )

        for thread in threads:
            thread.start() 
        
        for thread in threads:
            thread.join()

        self._signal.emit( len(self.images) )
    
    def thread_routine(self):
        file_n = self.safe_counter.get()
        while (file_n != -1):
            ImageCompressor(self.images[file_n], quality=self.quality)
            print(len(self.images), file_n)
            self._signal.emit( file_n )
            file_n = self.safe_counter.get()
            
            
        print(file_n)
        #self._signal.emit( 100 )

       
app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec()