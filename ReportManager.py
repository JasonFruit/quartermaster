from PySide.QtGui import *

class ReportDialog(QDialog):
    def __init__(self, reports, parent=None):
        QDialog.__init__(self, parent)
        self.setWindowTitle("Manage Reports")

        self.canceled = True
        self.reports = reports

        self.layout = QVBoxLayout(self)

        self.report_frame = QVBoxLayout()
        
        self.report_combo = QComboBox()
        self.report_combo.addItems([report.title
                                    for report in self.reports])
        self.report_frame.addWidget(self.report_combo)

        self.btn_hbx = QHBoxLayout()

        self.delete_btn = QPushButton("&Delete")
        self.delete_btn.clicked.connect(self.delete)
        
        self.rename_btn = QPushButton("&Rename")

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
            if report.title == self.report_combo.itemText(self.report_combo.currentIndex()):
                self.reports.remove(report)
                self.report_combo.clear()
                self.report_combo.addItems([report.title
                                            for report in self.reports])

    def rename(self, *args):
        for report in self.reports:
            if report.title == self.report_combo.itemText(self.report_combo.currentIndex()):
                id = QInputDialog(self)
                # id.setTextValue( TODO: finish this

    def commit(self, *args):
        self.canceled = False
        self.close()

    def cancel(self, *args):
        self.close()
        

if __name__ == "__main__":
    app = QApplication("Hi.")
    from inventory import Report
    rd = ReportDialog([Report("reports/nearing-expiration.rpt"),
                       Report("reports/unmet-goals.rpt")])
    rd.exec()
    print(rd.reports)
