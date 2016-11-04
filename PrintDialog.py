from PySide.QtGui import *

class PrintDialog(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)

        self.setWindowTitle("Print document to...")

        self.printers = QPrinterInfo().availablePrinters()

        self.orientations = [s
                             for s in dir(QPrinter.Orientation)
                             if s != s.lower() and not s.startswith("_")]
        self.addControls()

        self.setDefaults()

    def addControls(self):
        self.layout = QVBoxLayout()

        self.printer_combo = QComboBox()
        self.printer_combo.currentIndexChanged.connect(self.printerSelected)
        self.printer_combo.addItems([p.printerName()
                                     for p in self.printers])
        self.layout.addWidget(self.printer_combo)

        self.page_size_combo = QComboBox()
        self.page_size_combo.setEnabled(False)
        self.page_size_combo.currentIndexChanged.connect(self.pageSizeChanged)
        self.printerSelected(self.printer_combo.currentIndex())
        self.layout.addWidget(self.page_size_combo)
        
        self.orientation_combo = QComboBox()
        self.orientation_combo.addItems(self.orientations)
        self.orientation_combo.currentIndexChanged.connect(self.orientationChanged)
        self.layout.addWidget(self.orientation_combo)

        self.btn_box = QHBoxLayout()

        self.print_btn = QPushButton("&Print")
        self.print_btn.clicked.connect(self.commit)
        self.btn_box.addWidget(self.print_btn)

        self.cancel_btn = QPushButton("&Cancel")
        self.cancel_btn.clicked.connect(self.close)
        self.btn_box.addWidget(self.cancel_btn)

        self.layout.addLayout(self.btn_box)

        self.setLayout(self.layout)

    def setDefaults(self):
        p = self.printer

        print(self.pageSizes.index(p.pageSize().name.decode("utf-8")))
        self.page_size_combo.setCurrentIndex(
            self.pageSizes.index(p.pageSize().name.decode("utf-8")))

        if self.printer.orientation() == QPrinter.Orientation.Landscape:
            self.orientation_combo.setCurrentIndex(self.orientations.index("Landscape"))
        else:
            self.orientation_combo.setCurrentIndex(self.orientations.index("Portrait"))    

    def printerSelected(self, new_index):
        try:
            self.page_size_combo.clear()
            self.page_size_combo.setEnabled(True)
            self.currentPrinterInfo = self.printers[new_index]
            self.printer = QPrinter(self.currentPrinterInfo)
            self.pageSizes = (
                [s.name.decode("utf-8")
                 for s in self.currentPrinterInfo.supportedPaperSizes()
                 if s.name.decode("utf-8") not in ["NPageSize", "NPaperSize"]])
            self.page_size_combo.addItems(self.pageSizes)
            self.setDefaults()
        except AttributeError:
            pass

    def pageSizeChanged(self, new_index):
        pass

    def orientationChanged(self, new_index):
        pass

    def commit(self, *args):
        page_size_index = self.page_size_combo.currentIndex()
        new_size = self.pageSizes[page_size_index]
        for size in self.currentPrinterInfo.supportedPaperSizes():
            if size.name.decode("utf-8") == new_size:
                self.printer.setPageSize(size)

        orientation_index = self.orientation_combo.currentIndex()
        sel = self.orientation_combo.itemText(orientation_index)
        if sel == "Portrait":
            self.printer.setOrientation(QPrinter.Orientation.Portrait)
        elif sel == "Landscape":
            self.printer.setOrientation(QPrinter.Orientation.Landscape)
        else:
            raise NotImplementedError("Orientation %s not implemented." % sel)
        
        self.accept()

if __name__ == "__main__":
    app = QApplication([])
    pd = PrintDialog()
    if pd.exec_() == QDialog.Accepted:
        p = pd.printer
        print(p.printerName(),
              p.pageSize(),
              p.orientation())
