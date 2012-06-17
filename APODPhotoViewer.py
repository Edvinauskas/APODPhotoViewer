from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
from time import strptime, strftime
import datetime

class APODPhotoViewer(QWidget):
    
    today_date = datetime.date.today()
    days_to_go_back = 0
    too_far_forward = False
    image_title_date = ""
    url = ""

    def __init__(self, win_parrent = None):
        super(APODPhotoViewer, self).__init__()
        self.GUI()
        self.connect(self.next_button, SIGNAL('clicked()'), self.load_next_image)
        self.connect(self.prev_button, SIGNAL('clicked()'), self.load_prev_image)
        
    def GUI(self):        
        self.picture_title = QLabel("Picture title")
        self.picture_title.setFixedHeight(10)
        self.picture_title.setAlignment(Qt.AlignCenter)
        self.display_picture_label = QLabel()
        self.display_picture_label.setStyleSheet("QLabel {background-color : grey;}")
        self.display_picture_label.setAlignment(Qt.AlignCenter)

        title_picture_grid = QVBoxLayout()
        title_picture_grid.addWidget(self.picture_title)
        title_picture_grid.addWidget(self.display_picture_label)

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

    	self.setFixedSize(1100, 900)
        self.setWindowTitle('Astronomy Picture of the Day Photo Viewer')
        self.on_startup_image()

    def on_startup_image(self):
        self.loading_image()
        self.set_url()


    def load_next_image(self):
        if self.days_to_go_back + 1 > 0:
            self.display_picture_label.setText("No picture here :(")
            self.too_far_forward = True
        else:
            self.days_to_go_back += 1

    def load_prev_image(self):
        if self.too_far_forward is True:
            self.days_to_go_back = 0
            self.too_far_forward = False
        else:
            self.days_to_go_back -= 1

    def set_url(self):
        minus_days = datetime.timedelta(days=self.days_to_go_back)
        image_date = self.today_date + minus_days
        self.url = "http://apod.nasa.gov/apod/ap%s.html" % image_date.strftime("%y%m%d")
        self.image_title_date = "%s" % image_date.strftime("%d/%m/%Y")
        print self.url, " page url"
        return self.url

    def loading_image(self):
        self.display_picture_label.setText("Loading...")

        # self.main_picture_pixmap = QPixmap('spinner.gif').scaled(
        #     QSize(self.display_picture_label.size()), 
        #     Qt.KeepAspectRatio, 
        #     Qt.FastTransformation
        # )
        # self.display_picture_label.setPixmap(self.main_picture_pixmap)

if __name__ == '__main__':
    APODPhotoViewerMain = QApplication(sys.argv)
    APODPhotoViewer = APODPhotoViewer()
    APODPhotoViewer.show()
    sys.exit(APODPhotoViewerMain.exec_())