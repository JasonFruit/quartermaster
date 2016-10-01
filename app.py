import sys
from datetime import datetime, timedelta
import math

from PySide.QtCore import *
from PySide.QtGui import *

from inventory import Measurement, InventoryDB, InventoryItem

qt_app = QApplication(sys.argv)

time_deltas = {"year": timedelta(365),
               "month": timedelta(30),
               "day": timedelta(1)}

class InventoryListModel(QAbstractTableModel):
    def __init__(self, parent, items, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        self.item_attribs = ['id', 'condition', 'description', 'amount',
                             'life', 'purchase_date', 'expiration_date']
        self.items = items
    def rowCount(self, parent):
        return len(self.items)
    def columnCount(self, parent):
        return len(self.item_attribs)
    def data(self, index, role):

        attrib = self.item_attribs[index.column()]


        if not index.isValid():
            return None
        elif role != Qt.DisplayRole:
            return None

        val = getattr(self.items[index.row()],
                      attrib)
        
        try:
            val = val.to_string() # if it has a to_string() method,
                                  # convert it to a string
        except:
            try:
                # if it's a date, format it nicely
                val = val.strftime("%B %d, %Y")
            except:
                pass
        
        return val
    
    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.item_attribs[col].replace("_", " ").title()
        elif orientation == Qt.Vertical and role == Qt.DisplayRole:
            return "»"
        return None
    
    def sort(self, col, order):
        self.emit(SIGNAL("layoutAboutToBeChanged()"))

        attrib = self.item_attribs[col]

        self.items = sorted(self.items,
                            key=lambda s: getattr(s, attrib))
        if order == Qt.DescendingOrder:
            self.items.reverse()
            
        self.emit(SIGNAL("layoutChanged()"))

class MultSpinner(QHBoxLayout):
    def __init__(self, label, multiplier):
        QHBoxLayout.__init__(self)
        self.multiplier = multiplier
        self.addWidget(QLabel(label))
        self.spinner = QSpinBox()
        self.addWidget(self.spinner)
    def value(self):
        return self.spinner.value() * self.multiplier
        
class RationMultiplierDialog(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.canceled = True
        self.value = None

        self.layout = QVBoxLayout(self)

        self.adult_males = MultSpinner("Adult males:", 1.0)
        self.layout.addLayout(self.adult_males)
        self.adult_females = MultSpinner("Adult females:", 0.75)
        self.layout.addLayout(self.adult_females)
        self.child_1_3 = MultSpinner("Children ages 1-3", 0.3)
        self.layout.addLayout(self.child_1_3)
        self.child_4_6 = MultSpinner("Children ages 4-6", 0.5)
        self.layout.addLayout(self.child_4_6)
        self.child_7_9 = MultSpinner("Children ages 7-9", 0.75)
        self.layout.addLayout(self.child_7_9)

        self.btn_hbox = QHBoxLayout()
        self.ok_btn = QPushButton("&OK")
        self.ok_btn.clicked.connect(self.commit)
        self.cancel_btn = QPushButton("&Cancel")
        self.cancel_btn.clicked.connect(self.close)
        self.btn_hbox.addWidget(self.ok_btn)
        self.btn_hbox.addWidget(self.cancel_btn)
        self.layout.addLayout(self.btn_hbox)


    def commit(self, *args):
        self.canceled = False
        self.value = sum([self.adult_males.value(),
                          self.adult_females.value(),
                          self.child_1_3.value(),
                          self.child_4_6.value(),
                          self.child_7_9.value()])
        self.close()

class InventoryItemDialog(QDialog):
    def __init__(self, parent, item=None):
        QDialog.__init__(self, parent)

        self.item = item
        
        self.setMinimumWidth(400)
        self.setWindowTitle("Add/Edit Inventory Item")

        self.conditions = self.parent().conditions
        self.amounts = self.parent().amounts
        self.durations = self.parent().durations

        self.addControls()
        if self.item:
            self._syncControlsToItem()
        else:
            self._initControls()

    def _syncControlsToItem(self):
        self.cond_combo.setCurrentIndex(self.conditions.index(self.item.condition))
        self.dsc_text.setText(self.item.description)
        self.amount_text.setText(str(self.item.amount.number))
        self.amount_combo.setCurrentIndex(self.amounts.index(self.item.amount.unit))
        self.life_text.setText(str(self.item.life.number))
        self.life_combo.setCurrentIndex(self.durations.index(self.item.life.unit))
        if self.item.purchase_date:
            self.purch_datepicker.setDate(QDate(self.item.purchase_date.year,
                                                self.item.purchase_date.month,
                                                self.item.purchase_date.day))

    def _syncItemToControls(self):
        if self.item:
            self.item.condition = self.cond_combo.currentText()
            self.item.description = self.dsc_text.text()
            self.item.amount = Measurement(int(self.amount_text.text()),
                                           self.amounts[self.amount_combo.currentIndex()])
            self.item.life = Measurement(int(self.life_text.text()),
                                         self.durations[self.life_combo.currentIndex()])
            date = self.purch_datepicker.date()
            self.item.purchase_date = datetime(date.year(),
                                               date.month(),
                                               date.day())
        else:
            date = self.purch_datepicker.date()
            self.item = InventoryItem(
                None,
                self.cond_combo.currentText(),
                self.dsc_text.text(),
                Measurement(int(self.amount_text.text()),
                            self.amounts[self.amount_combo.currentIndex()]),
                Measurement(int(self.life_text.text()),
                            self.durations[self.life_combo.currentIndex()]),
                datetime(date.year(),
                         date.month(),
                         date.day()))

    def commit(self, *args, **kwargs):
        self._syncItemToControls()

        if self.item.id:
            self.parent().db.save_inventory(self.item)
        else:
            self.parent().db.add_inventory(self.item)
        self.close()
        
    def _initControls(self):
        self.cond_combo.setCurrentIndex(0)
        self.amount_text.setText("0")
        self.amount_combo.setCurrentIndex(0)
        self.life_text.setText("2")
        self.life_combo.setCurrentIndex(0)
        self.purch_datepicker.setDate(QDate(datetime.now().year,
                                            datetime.now().month,
                                            datetime.now().day))

    def addControls(self):
        
        self.layout = QVBoxLayout(self)

        self.cond_hbox = QHBoxLayout(self)
        self.cond_hbox.addWidget(QLabel("Condition:"))
        self.cond_combo = QComboBox(self)
        self.cond_combo.addItems(self.parent().conditions)
        self.cond_hbox.addWidget(self.cond_combo)
        self.layout.addLayout(self.cond_hbox, False)

        self.dsc_hbox = QHBoxLayout(self)
        self.dsc_hbox.addWidget(QLabel("Description:"))
        self.dsc_text = QLineEdit()
        self.dsc_hbox.addWidget(self.dsc_text)
        self.layout.addLayout(self.dsc_hbox, False)
        
        self.amount_hbox = QHBoxLayout(self)
        self.amount_hbox.addWidget(QLabel("Amount:"))
        self.amount_text = QLineEdit()
        self.amount_hbox.addWidget(self.amount_text)
        self.amount_combo = QComboBox(self)
        self.amount_combo.addItems(self.parent().amounts)
        self.amount_hbox.addWidget(self.amount_combo)
        self.layout.addLayout(self.amount_hbox)

        self.life_hbox = QHBoxLayout(self)
        self.life_hbox.addWidget(QLabel("Life:"))
        self.life_text = QLineEdit()
        self.life_hbox.addWidget(self.life_text)
        self.life_combo = QComboBox(self)
        self.life_combo.addItems(self.parent().durations)
        self.life_hbox.addWidget(self.life_combo)
        self.layout.addLayout(self.life_hbox)

        self.purch_hbox = QHBoxLayout(self)
        self.purch_hbox.addWidget(QLabel("Purchased:"))
        self.purch_datepicker = QDateTimeEdit()
        self.purch_datepicker.setCalendarPopup(True)
        self.purch_datepicker.setDisplayFormat("MMMM d, yyyy")
        self.purch_hbox.addWidget(self.purch_datepicker)
        self.layout.addLayout(self.purch_hbox, False)

        self.btn_hbox = QHBoxLayout(self)
        self.ok_btn = QPushButton("&OK")
        self.ok_btn.clicked.connect(self.commit)
        self.cancel_btn = QPushButton("&Cancel")
        self.cancel_btn.clicked.connect(self.close)
        self.btn_hbox.addWidget(self.ok_btn)
        self.btn_hbox.addWidget(self.cancel_btn)
        self.layout.addLayout(self.btn_hbox)
        
        self.setLayout(self.layout)
        
        
class Quartermaster(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.filename = ""
        self.setWindowTitle("Quartermaster")
        self.setMinimumWidth(400)
        self.addControls()
        self.showMaximized()
        self.lastRow = None

    def showEdit(self, selected, deselected):
        row = selected.indexes()[0].row()
        if row != self.lastRow:
            self.lastRow = row
            frm = InventoryItemDialog(self, self.inventory_model.items[row])
            frm.exec()

    def showAdd(self, *args, **kwargs):
        frm = InventoryItemDialog(self, None)
        frm.exec()
        if frm.item:
            self.items.append(frm.item)
            self.set_model()

    def loadFile(self, filename):
        self.filename = filename
        self.setWindowTitle("Quartermaster (%s)" % self.filename)
        self.db = InventoryDB(self.filename)
        
        self.conditions = [str(key)
                           for key in self.db.conditions.keys()]
        self.amounts = [str(key)
                        for key in self.db.amounts.keys()]
        self.durations = [str(key)
                          for key in self.db.durations.keys()]
        print(self.durations)
        
        self.record_types = [str(key)
                             for key in self.db.record_types.keys()]
        self.showItems()

    def showItems(self, *args):
        self.items = self.db.all_inventory(self.view_combo.currentText().lower())
        self.set_model()

    def browseOpenFile(self, *args, **kwargs):
        fn, _ = QFileDialog.getOpenFileName(self, 'Open file', "", "*.qm")
        if fn:
            self.loadFile(fn)

    def browseCreateFile(self, *args, **kwargs):
        fn, _ = QFileDialog.getSaveFileName(self, 'New file', "", "*.qm")
        if fn:
            self.loadFile(fn)

    def getRationNumber(self):
        dlg = RationMultiplierDialog(self)
        dlg.exec()
        return dlg.value

    def setGoals(self):
        multiplier = self.getRationNumber()
        if multiplier:
            self.db.set_goals(multiplier)
        else:
            mb = QMessageBox()
            mb.setText("Goals not set.")
            mb.exec_()

    def set_model(self):
        self.inventory_model = InventoryListModel(self.inventory_table,
                                                  self.items)
        self.inventory_table.setModel(self.inventory_model)
        sm = self.inventory_table.selectionModel()
        sm.selectionChanged.connect(self.showEdit)
        self.inventory_table.setColumnHidden(0, True)
        self.inventory_table.resizeColumnsToContents()

    def setUpMenu(self):
        menu_bar = self.menuBar()
        
        self.file_menu = menu_bar.addMenu("&File")
        self.inventory_menu = menu_bar.addMenu("&Inventory")
        self.help_menu = menu_bar.addMenu("&Help")
        
        createAction = QAction(QIcon('create.png'), '&New', self)
        createAction.setShortcut('Ctrl+N')
        createAction.setStatusTip('New inventory file')
        createAction.triggered.connect(self.browseCreateFile)

        self.file_menu.addAction(createAction)
        
        openAction = QAction(QIcon('open.png'), '&Open', self)
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open an inventory file')
        openAction.triggered.connect(self.browseOpenFile)

        self.file_menu.addAction(openAction)

        exitAction = QAction(QIcon('exit.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)

        self.file_menu.addAction(exitAction)

        setGoalAction = QAction(QIcon('set-goals.png'), 'Set &goals', self)
        setGoalAction.setStatusTip('Set inventory goals')
        setGoalAction.triggered.connect(self.setGoals)

        self.inventory_menu.addAction(setGoalAction)
        
    def addControls(self):
        self.main_widget = QWidget()

        self.setUpMenu()
        
        self.setCentralWidget(self.main_widget)

        self.layout = QVBoxLayout(self.main_widget)

        self.view_combo = QComboBox()
        self.view_combo.addItems(["Inventory", "Goal"])
        self.view_combo.currentIndexChanged.connect(self.showItems)
        
        self.layout.addWidget(self.view_combo)

        self.inventory_table = QTableView()
        self.inventory_table.setSortingEnabled(True)

        self.layout.addWidget(self.inventory_table)

        self.btn_hbx = QHBoxLayout(self)

        self.add_btn = QPushButton("&Add")
        self.add_btn.clicked.connect(self.showAdd)
        self.delete_btn = QPushButton("&Delete")
        self.btn_hbx.addWidget(self.add_btn)
        self.btn_hbx.addWidget(self.delete_btn)

        self.layout.addLayout(self.btn_hbx)

    def run(self):
        self.show()
        qt_app.exec_()

app = Quartermaster()
app.run()
