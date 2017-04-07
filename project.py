import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import linear
import two_d

class MainWindow(QWidget):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        layout = QVBoxLayout()

        self.label = QLabel("Barcode Detection and Reading")
        self.label.setStyleSheet("color: #ffffff;"
                                 "font-size: 28px;"
                                 "margin-left: 100px;"
                                 "margin-top: 10px;"
                                 "margin-bottom:10px")
        layout.addWidget(self.label)

        self.btn = QPushButton("Select Barcode Image")
        self.btn.clicked.connect(self.getfile)
        self.btn.setStyleSheet("background-color: #c1b84d;"
                                "font-size: 28px;"
                                "border-style: outset;"
                                "border-width: 2px;"
                                "border-radius: 10px;"
                                "border-color: beige;"
                                "font: bold 14px;"
                                "min-width: 10em;"
                                "padding: 10px;"
                                "margin:0 auto;"
                                "color: #ffffff;"
                                "font-family: Palatino Linotype, Book Antiqua, Palatino, serif"

                              )

        layout.addWidget(self.btn)

        self.le = QLabel("    ")

        self.le.setStyleSheet("margin-left:50px;"
                              "margin-right:50px")

        layout.addWidget(self.le)

        HbtnLayout = QHBoxLayout()
        self.oneD = QPushButton("linear Barcode Extraction")
        self.twoD = QPushButton("2D Barcode Extraction")

        self.oneD.setStyleSheet("background-color: #ff1a1a; "
                                "font-size: 28px;"
                                "border-style: outset;"
                                "border-width: 2px;"
                                "border-radius: 10px;"
                                "border-color: beige;"
                                "font: bold 14px;"
                                "min-width: 10em;"
                                "padding: 10px;"
                                "margin:0 auto;"
                                "color: #fffafa;"
                                "font-family: Palatino Linotype, Book Antiqua, Palatino, serif"
                               )

        self.twoD.setStyleSheet("background-color: #ff1a1a; "
                                "border-style: outset;"
                                "font-size: 28px;"
                                "border-width: 2px;"
                                "border-radius: 10px;"
                                "border-color: beige;"
                                "font: bold 14px;"
                                "min-width: 10em;"
                                "padding: 10px;"
                                "margin:0 auto;"
                                "color: #fffafa;"
                                "font-family: Palatino Linotype, Book Antiqua, Palatino, serif"
                                )

        self.oneD.clicked.connect(self.oneDB)
        self.twoD.clicked.connect(self.twoDB)

        HbtnLayout.addWidget(self.oneD)
        HbtnLayout.addWidget(self.twoD)

        layout.stretch(1)
        layout.addLayout(HbtnLayout)

        self.result = QLabel("Result")

        self.result.setStyleSheet("font-size: 18px;"
                                  "font-family: Palatino Linotype, Book Antiqua, Palatino, serif;"
                                  "color: #a2b2c2;"
                                  )

        layout.addWidget(self.result)

        self.resultBox = QLineEdit(" ")
        #self.resultBox.setReadOnly(True)
        self.resultBox.setStyleSheet("background-color:white;"
                                     "font-size:15px;"
                                     "color:black;"

        )
        layout.addWidget(self.resultBox)

        self.setStyleSheet("background-color:#4e4d50")
        self.setLayout(layout)
        self.resize(300,300)
        self.setWindowIcon(QIcon('logo.png'))
        self.setWindowTitle("BDR")

    def getfile(self):
        self.FName = QFileDialog.getOpenFileName(self, 'Open file',
                                            'c:\\', "Image files (*.jpg *.gif)")

        PixMap = QPixmap(self.FName)
        PixMap = PixMap.scaled(720, 405, Qt.KeepAspectRatio)
        self.le.setPixmap(PixMap)

    def oneDB(self):

        self.barcode = linear.linear(self.FName)
        print(self.barcode)
        self.resultBox.setText(self.barcode)

    def twoDB(self):

        self.barcode = two_d.two_d(self.FName)
        print(self.barcode)
        self.resultBox.setText(self.barcode)

def main():
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()