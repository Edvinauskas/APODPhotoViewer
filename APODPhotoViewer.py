from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
import urllib2, urllib
from time import strftime
import datetime
import re
import cStringIO
import Image

class GetImageThread(QThread):
    def __init__(self, days_to_go_back, parent=None):
        QThread.__init__(self, parent)
        self.exiting = False
        self.days_to_go_back = days_to_go_back

    def run(self):
        print "running..."
        page_url = self.get_page_url()
        page_html = self.get_page_html(page_url)
        image_url, image_name = self.parse_for_image_link_and_title(page_html)
        image_url = "http://apod.nasa.gov/apod/image/%s" % image_url[0]
        image = self.get_image_from_url(image_url)
        print type(image)
        image_title = QString(image_name[0])
        final_image = QImage(image)
        self.sleep(1)
        self.emit(SIGNAL("finished(QString, QImage)"),
            image_title,
            final_image
            )
        print "Done..."


    def start_thread(self):
        print "Starting thread..."
        self.start()

    def get_page_url(self):
        today_date = datetime.date.today()
        minus_days = datetime.timedelta(days=self.days_to_go_back)
        image_date = today_date + minus_days
        page_url = "http://apod.nasa.gov/apod/ap%s.html" % image_date.strftime("%y%m%d")
        # self.image_title_date = "%s" % image_date.strftime("%d/%m/%Y")
        print page_url, " page url"
        return page_url

    def get_page_html(self, page_url):
        print "Fetching html..."
        open_url = urllib2.urlopen(page_url)
        html = open_url.read()
        print "Got page html..."
        return html

    def parse_for_image_link_and_title(self, html):
        print "Parsing HTML..."
        image_url = re.findall('<a href="image/(.*?)">', html)
        image_name = re.findall('<center>\n<b>(.*?)</b> <br> \n<b> Image Credit', html)
        print "Done parsing HTML..."
        print image_url
        print image_name
        return image_url, image_name

    def get_image_from_url(self, image_url):
        print image_url
        import urllib, cStringIO
        img_file = cStringIO.StringIO(urllib.urlopen(image_url).read())
        image_file = Image.open(img_file)
        # image_file = urllib2.urlopen(image_url).read()
        # print type(image_file)
        return image_file

    def __del__(self):
        self.exiting = True
        self.wait()

class APODPhotoViewer(QWidget):
    def __init__(self, win_parrent = None):
        super(APODPhotoViewer, self).__init__()

        self.days_to_go_back = 0
        self.too_far_forward = False
        self.image_title_date = ""
        self.page_url = ""
        self.page_html = ""
        self.image_url = ""

        self.GUI()
        self.connect(self.next_button, SIGNAL('clicked()'), self.load_next_image)
        self.connect(self.prev_button, SIGNAL('clicked()'), self.load_prev_image)
        self.get_image()

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
        self.prev_button.setFixedSize(100, 50)
        self.next_button = QPushButton("Next")
        self.next_button.setFixedSize(100, 50)

        bottom_container = QGridLayout()
        bottom_container.addWidget(self.prev_button, 1, 0)
        bottom_container.addWidget(self.next_button, 1, 1)

        self.vbox = QVBoxLayout()
        self.vbox.addLayout(title_picture_grid)
        self.vbox.addLayout(bottom_container)

        self.setLayout(self.vbox)

    	self.setFixedSize(1100, 900)
        self.setWindowTitle('Astronomy Picture of the Day Photo Viewer')
        

    def get_image(self):
        self.get_image_thread = GetImageThread(self.days_to_go_back) 
        self.set_loading_image_text()
        self.connect(self.get_image_thread, SIGNAL('finished(QString, QImage)'), self.set_image)
        self.get_image_thread.start_thread()

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

    def set_loading_image_text(self):
        self.display_picture_label.setText("Loading...")

    def set_image(self, title, image):
        print type(image), " testing"
        self.display_picture_label.setText("Done...")
        self.picture_title.setText(title)
        self.main_picture_pixmap = QPixmap.fromImage(image).scaled(
            QSize(self.display_picture_label.size()), 
            Qt.KeepAspectRatio, 
            Qt.FastTransformation
        )
        self.display_picture_label.setPixmap(self.main_picture_pixmap)

if __name__ == '__main__':
    APODPhotoViewerMain = QApplication(sys.argv)
    APODPhotoViewer = APODPhotoViewer()
    APODPhotoViewer.show()
    sys.exit(APODPhotoViewerMain.exec_())