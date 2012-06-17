from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys

class APODPhotoViewer(QWidget):
    
    def __init__(self, win_parrent = None):
        super(APODPhotoViewer, self).__init__()
        
        self.GUI()
        
    def GUI(self):        
    	self.setFixedSize(900, 700)
        self.setWindowTitle('Astronomy Picture of the Day Photo Viewer')    
        self.show()

if __name__ == '__main__':
    APODPhotoViewerMain = QApplication(sys.argv)
    APODPhotoViewer = APODPhotoViewer()
    APODPhotoViewer.show()
    sys.exit(APODPhotoViewerMain.exec_())