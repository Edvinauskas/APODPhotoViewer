from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys

class APODPhotoViewer(QWidget):
    
    def __init__(self, win_parrent = None):
        super(APODPhotoViewer, self).__init__()
        
        self.GUI()
        
    def GUI(self):        
        self.picture_title = QLabel("Picture title")
        self.picture_title.setFixedHeight(10)
        self.picture_title.setAlignment(Qt.AlignCenter)
        self.picture = QLabel("(pic)")
        self.picture.setAlignment(Qt.AlignCenter)

        title_picture_grid = QVBoxLayout()
        title_picture_grid.addWidget(self.picture_title)
        title_picture_grid.addWidget(self.picture)

        self.prev_button = QPushButton("Prev")
        self.prev_button.setFixedSize(50, 100)
        self.slide_show = QLabel("Slide Show")
        self.slide_show.setAlignment(Qt.AlignCenter)
        self.next_button = QPushButton("Next")
        self.next_button.setFixedSize(50, 100)

        bottom_container = QGridLayout()
        bottom_container.addWidget(self.prev_button, 1, 0)
        bottom_container.addWidget(self.slide_show, 1, 1)
        bottom_container.addWidget(self.next_button, 1, 2)

        self.vbox = QVBoxLayout()
        self.vbox.addLayout(title_picture_grid)
        self.vbox.addLayout(bottom_container)

        self.setLayout(self.vbox)

    	self.setFixedSize(900, 700)
        self.setWindowTitle('Astronomy Picture of the Day Photo Viewer')    

if __name__ == '__main__':
    APODPhotoViewerMain = QApplication(sys.argv)
    APODPhotoViewer = APODPhotoViewer()
    APODPhotoViewer.show()
    sys.exit(APODPhotoViewerMain.exec_())