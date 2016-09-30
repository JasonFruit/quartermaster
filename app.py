import sys
 
from PySide.QtCore import *
from PySide.QtGui import *

from inventory import Measurement, InventoryDB

qt_app = QApplication(sys.argv)

class InventoryListModel(QAbstractTableModel):
    def __init__(self, parent, items, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        self.item_attribs = ['id', 'condition', 'description', 'amount',
                             'life', 'purchase_date']
        self.items = items
    def rowCount(self, parent):
        return len(self.items)
    def columnCount(self, parent):
        return len(self.item_attribs)
    def data(self, index, role):
        if not index.isValid():
            return None
        elif role != Qt.DisplayRole:
            return None
        
        val = getattr(self.items[index.row()],
                      self.item_attribs[index.column()])
        
        try:
            val = val.to_string() # if it has a to_string() method,
                                  # convert it to a string
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
        self.items = sorted(self.items,
                            key=lambda s: getattr(s, self.item_attribs[col]))
        if order == Qt.DescendingOrder:
            self.items.reverse()
            
        self.emit(SIGNAL("layoutChanged()"))

class InventoryItemDialog(QDialog):
    def __init__(self, parent, item=None):
        QDialog.__init__(self, parent)
        self.setMinimumWidth(400)
        self.setWindowTitle("Add/Edit Inventory Item")
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

        self.setLayout(self.layout)
        
        
class Quartermaster(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle("Quartermaster: Survival Inventory Management")
        self.setMinimumWidth(400)

        self.db = InventoryDB("inventory.db")
        self.conditions = [str(key)
                           for key in self.db.conditions.keys()]
        self.amounts = [str(key)
                        for key in self.db.amounts.keys()]
        self.durations = [str(key)
                          for key in self.db.durations.keys()]
        
        self.addControls()
        self.showMaximized()

    def showAddEdit(self, selected, deselected):
        row = selected.indexes()[0].row()
        frm = InventoryItemDialog(self, self.inventory_model.items[row])
        frm.exec()
        
    def addControls(self):
        self.layout = QVBoxLayout(self)

        self.inventory_table = QTableView()
        self.inventory_model = InventoryListModel(self.inventory_table,
                                                  self.db.all_inventory())
        self.inventory_table.setModel(self.inventory_model)
        self.inventory_table.setColumnHidden(0, True)
        self.inventory_table.resizeColumnsToContents()
        self.inventory_table.setSortingEnabled(True)

        sm = self.inventory_table.selectionModel()
        sm.selectionChanged.connect(self.showAddEdit)
        
        self.layout.addWidget(self.inventory_table)

        self.setLayout(self.layout)

    def run(self):
        self.show()
        qt_app.exec_()

app = Quartermaster()
app.run()
