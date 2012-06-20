from PyQt4 import QtCore
from PyQt4 import QtGui
import sys
import urllib2
import datetime
import re


class GetImageThread(QtCore.QThread):
    def __init__(self, days_to_go_back, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.exiting = False
        self.days_to_go_back = days_to_go_back

    def run(self):
        page_url = self.get_page_url()
        page_html = self.get_page_html(page_url)
        image_url, image_title = self.parse_for_image_link_and_title(page_html)
        image_title = image_title[0]
        image = QtGui.QImage()
        if not image_url or not image_title:
            self.emit(QtCore.SIGNAL("finished(QString, QString, QImage)"),
                page_url,
                image_title,
                image
                )
        else:
            image_url = "http://apod.nasa.gov/apod/image/%s" % image_url[0]
            image_data = self.get_image_from_url(image_url)
            image.loadFromData(image_data)
            self.emit(QtCore.SIGNAL("finished(QString, QString, QImage)"),
                page_url,
                image_title,
                image
                )

    def start_thread(self):
        self.start()

    def get_page_url(self):
        todays_date = datetime.date.today()
        minus_days = datetime.timedelta(days=self.days_to_go_back)
        image_date = todays_date + minus_days
        page_url = "http://apod.nasa.gov/apod/ap%s.html" % image_date.strftime("%y%m%d")
        return page_url

    def get_page_html(self, page_url):
        open_url = urllib2.urlopen(page_url)
        html = open_url.read()
        return html

    def parse_for_image_link_and_title(self, html):
        image_url = re.findall('<a href="image/(.*?)"', html)
        image_name = re.findall("<title> APOD: (.*?)\n</title>", html)
        return image_url, image_name

    def get_image_from_url(self, image_url):
        image_data = urllib2.urlopen(image_url).read()
        return image_data

    def __del__(self):
        self.exiting = True
        self.wait()


class APODPhotoViewer(QtGui.QWidget):
    def __init__(self, win_parrent=None):
        super(APODPhotoViewer, self).__init__()

        self.days_to_go_back = 0
        self.too_far_forward = False

        self.GUI()
        self.next_button.clicked.connect(self.load_next_image)
        self.prev_button.clicked.connect(self.load_prev_image)
        self.get_image()

    def GUI(self):
        self.picture_title = QtGui.QLabel()
        self.picture_title.setStyleSheet("QLabel {font-size: 20px; font-weight: bold;}")
        self.picture_title.setFixedHeight(30)
        self.picture_title.setAlignment(QtCore.Qt.AlignCenter)
        self.display_picture_label = QtGui.QLabel()
        self.display_picture_label.setStyleSheet("QLabel {background-color : grey; font-size: 30px; font-weight: bold;}")
        self.display_picture_label.setAlignment(QtCore.Qt.AlignCenter)

        title_picture_grid = QtGui.QVBoxLayout()
        title_picture_grid.addWidget(self.picture_title)
        title_picture_grid.addWidget(self.display_picture_label)

        self.prev_button = QtGui.QPushButton("Previous")
        self.prev_button.setFixedSize(100, 50)
        self.next_button = QtGui.QPushButton("Next")
        self.next_button.setFixedSize(100, 50)

        bottom_container = QtGui.QGridLayout()
        bottom_container.addWidget(self.prev_button, 1, 0)
        bottom_container.addWidget(self.next_button, 1, 1)

        self.vbox = QtGui.QVBoxLayout()
        self.vbox.addLayout(title_picture_grid)
        self.vbox.addLayout(bottom_container)

        self.setLayout(self.vbox)

        self.setFixedSize(1200, 900)
        self.setWindowTitle('Astronomy Picture of the Day Photo Viewer')

    def get_image(self):
        self.next_button.setEnabled(False)
        self.prev_button.setEnabled(False)
        self.picture_title.setText("")
        self.get_image_thread = GetImageThread(self.days_to_go_back)
        self.set_loading_image_text()
        self.connect(self.get_image_thread, QtCore.SIGNAL('finished(QString, QString, QImage)'), self.set_image)
        self.get_image_thread.start_thread()

    def load_next_image(self):
        if self.days_to_go_back + 1 > 0:
            self.display_picture_label.setText("No picture here :(")
            self.too_far_forward = True
        else:
            self.days_to_go_back += 1
            self.get_image()

    def load_prev_image(self):
        if self.too_far_forward is True:
            self.days_to_go_back = 0
            self.too_far_forward = False
        else:
            self.days_to_go_back -= 1
            self.get_image()

    def set_loading_image_text(self):
        self.display_picture_label.setText("Loading...")

    def set_image(self, page_link, title, image):
        image_pixmap = QtGui.QPixmap(image).scaled(
                QtCore.QSize(self.display_picture_label.size()),
                QtCore.Qt.KeepAspectRatio,
                QtCore.Qt.FastTransformation
            )
        if image_pixmap.isNull():
            self.display_picture_label.setText(
                "<qt>Image not found. It might be a video, <a href='" + str(page_link) + "'>click here</a> to visit the page.</qt>"
            )
            self.picture_title.setText(title)
            self.connect(self.display_picture_label, QtCore.SIGNAL("linkActivated(QString)"), self.open_URL)
        else:
            self.display_picture_label.setPixmap(image_pixmap)
            self.picture_title.setText(title)

        self.next_button.setEnabled(True)
        self.prev_button.setEnabled(True)

    def open_URL(self, URL):
        QtGui.QDesktopServices().openUrl(QtCore.QUrl(URL))

if __name__ == '__main__':
    APODPhotoViewerMain = QtGui.QApplication(sys.argv)
    APODPhotoViewer = APODPhotoViewer()
    APODPhotoViewer.show()
    sys.exit(APODPhotoViewerMain.exec_())
