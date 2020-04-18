import os
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from inventory import Report

class ReportManagerDialog(QDialog):
    def __init__(self, reports, parent=None):
        QDialog.__init__(self, parent)
        self.setWindowTitle("Manage Reports")
        self.setMinimumWidth(600)

        self.canceled = True
        self.reports = reports

        self.layout = QVBoxLayout(self)

        self.report_frame = QVBoxLayout()
        
        self.report_combo = QComboBox()
        self.report_combo.addItems([report.title
                                    for report in self.reports])
        self.report_frame.addWidget(self.report_combo)

        self.btn_hbx = QHBoxLayout()

        self.import_btn = QPushButton("&Import")
        self.import_btn.clicked.connect(self.import_)

        
        self.delete_btn = QPushButton("&Delete")
        self.delete_btn.clicked.connect(self.delete)
        
        self.rename_btn = QPushButton("&Rename")
        self.rename_btn.clicked.connect(self.rename)
        
        self.btn_hbx.addWidget(self.import_btn)
        self.btn_hbx.addWidget(self.delete_btn)
        self.btn_hbx.addWidget(self.rename_btn)

        self.report_frame.addLayout(self.btn_hbx)

        self.layout.addLayout(self.report_frame)

        self.ok_cancel_hbx = QHBoxLayout()

        self.ok_btn = QPushButton("&OK")
        self.ok_btn.clicked.connect(self.commit)
        
        self.cancel_btn = QPushButton("&Cancel")
        self.cancel_btn.clicked.connect(self.cancel)

        self.ok_cancel_hbx.addSpacing(10)
        self.ok_cancel_hbx.addWidget(self.ok_btn)
        self.ok_cancel_hbx.addWidget(self.cancel_btn)
        self.ok_cancel_hbx.addSpacing(10)
        
        self.layout.addLayout(self.ok_cancel_hbx)

    def delete(self, *args):
        for report in self.reports:
            if report.title == self.report_combo.itemText(
                    self.report_combo.currentIndex()):
                self.reports.remove(report)
                self.report_combo.clear()
                self.report_combo.addItems([report.title
                                            for report
                                            in self.reports])

    def rename(self, *args):
        for report in self.reports:
            if report.title == self.report_combo.itemText(
                    self.report_combo.currentIndex()):
                id = QInputDialog(self)
                id.setLabelText("New title:")
                id.setTextValue(report.title)

                id.exec_()

                report.title = id.textValue()

                self.report_combo.setItemText(
                    self.report_combo.currentIndex(),
                    report.title)
                break

    def import_(self, *args):
        fd = QFileDialog(self, "Import report file")
        fd.setNameFilter("Report specifications (*.rpt)")
        fd.setDefaultSuffix("rpt") # force new files to have .qm
                                   # extension
        fd.exec()
        fn = fd.selectedFiles()[0]
        
        # if a filename was chosen
        if fn and os.path.isfile(fn):
            rpt = Report(fn)
            self.reports.append(rpt)
            self.report_combo.addItem(rpt.title)

    def commit(self, *args):
        self.canceled = False
        self.close()

    def cancel(self, *args):
        self.close()
