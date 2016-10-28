import os
import sys
from datetime import datetime, timedelta
import math

# TODO: pare this down to what we actually need
from PySide.QtCore import *
from PySide.QtGui import *

from inventory import Measurement, InventoryDB, InventoryItem

# set up the QT application properties
qt_app = QApplication(sys.argv)
qt_app.setOrganizationName("Jason R. Fruit")
qt_app.setApplicationName("Quartermaster")

# use a human-readable settings filetype
QSettings.setDefaultFormat(QSettings.IniFormat)


class InventoryListModel(QAbstractTableModel):
    """A model to feed a table widget of inventory items"""
    def __init__(self, parent, items, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        
        # edit this if column definitions are changed
        self.item_attribs = ['id', 'condition', 'description', 'amount',
                             'life', 'purchase_date', 'expiration_date']
        
        self.base_items = items # always contains all items
        self.items = items # sometimes reduced by filtering
        
    def rowCount(self, parent):
        return len(self.items)
    def columnCount(self, parent):
        return len(self.item_attribs)
    def data(self, index, role):

        # get the attribute name for the column number
        attrib = self.item_attribs[index.column()]

        # not sure why the index object would be invalid, but the
        # whole thing died when I took this out!
        if not index.isValid():
            return None
        elif role != Qt.DisplayRole: # for example, tooltips and the like
            return None

        # get the attribute value from the row's item
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
                pass # it's already good
            
        return val

    def set_filter(self, filter):

        # let the control know it's about to see some changes around here
        self.emit(SIGNAL("layoutAboutToBeChanged()"))
        
        def item_contains(item, words):
            """returns True if the item contains all the words in the condition or
            description (case-insensitive)"""
            retval = True

            for word in words:
                if ((not word in item.condition.lower()) and
                    (not word in item.description.lower())):
                    retval = False

            return retval
        
        if filter.strip() == "": # don't loop if there's no filter
            self.items = self.base_items
        else:
            words = filter.lower().split(" ")

            # apply the filter
            self.items = [item
                          for item in self.base_items
                          if item_contains(item, words)]
            
        self.emit(SIGNAL("layoutChanged()")) # tell the control to refresh
        
    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            # make the attribute into nice column header text
            return self.item_attribs[col].replace("_", " ").title()

        # there are other header types, but we don't need to mess
        return None
    
    def sort(self, col, order):
        
        self.emit(SIGNAL("layoutAboutToBeChanged()"))

        # get the attribute name to sort by
        attrib = self.item_attribs[col]

        # do the sort, and reverse if needed
        self.items = sorted(self.items,
                            key=lambda s: getattr(s, attrib))
        if order == Qt.DescendingOrder:
            self.items.reverse()
            
        self.emit(SIGNAL("layoutChanged()"))

class MultSpinner(QHBoxLayout):
    """A HBox with a label and a numeric spinner control whose value is multiplied by <multiplier>"""
    def __init__(self, label, multiplier):
        QHBoxLayout.__init__(self)
        self.multiplier = multiplier
        self.addWidget(QLabel(label))
        self.spinner = QSpinBox()
        self.addWidget(self.spinner)
    def value(self):
        return self.spinner.value() * self.multiplier


class RationMultiplierDialog(QDialog):
    """A dialog for determining the multiplier for the base ration based
    on family size and ages"""
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)

        self.setWindowTitle("Family Size")

        # it's considered canceled until okayed
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
        """Runs when OK is clicked"""
        self.canceled = False
        self.value = sum([self.adult_males.value(),
                          self.adult_females.value(),
                          self.child_1_3.value(),
                          self.child_4_6.value(),
                          self.child_7_9.value()])
        self.close()

class InventoryItemDialog(QDialog):
    """A dialog to add and edit inventory items"""
    def __init__(self, parent, goals, amounts, item=None):
        QDialog.__init__(self, parent)

        if item:
            self.setWindowTitle("Edit Inventory Item")
        else:
            self.setWindowTitle("Add Inventory Item")

        self.item = item

        self.setMinimumWidth(400)

        self.goals = goals
        self.amounts = amounts

        self.addControls()
        
        if self.item:
            self._syncControlsToItem()
        else:
            self._initControls()

        self.canceled = True

    def format_goal(self, goal):
        if goal.condition == "":
            return goal.description
        else:
            return "%s (%s)" % (goal.description, goal.condition)

    def addControls(self):

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        self.goal_hbox = QHBoxLayout()
        self.goal_label = QLabel("Goal to fill:")
        self.goal_combo = QComboBox()

            
        self.goal_combo.addItems([self.format_goal(goal)
                                  for goal in self.goals])

        self.goal_hbox.addWidget(self.goal_label)
        self.goal_hbox.addWidget(self.goal_combo)

        self.layout.addLayout(self.goal_hbox)
        
        # amount (number and unit)
        self.amount_hbox = QHBoxLayout(self)
        self.amount_hbox.addWidget(QLabel("Amount:"))
        self.amount_text = QLineEdit()
        self.amount_hbox.addWidget(self.amount_text)
        self.amount_combo = QComboBox(self)
        self.amount_combo.addItems(self.parent().amounts)
        self.amount_hbox.addWidget(self.amount_combo)
        self.layout.addLayout(self.amount_hbox)

        # date purchased
        self.purch_hbox = QHBoxLayout(self)
        self.purch_hbox.addWidget(QLabel("Purchased:"))
        self.purch_datepicker = QDateTimeEdit()
        self.purch_datepicker.setCalendarPopup(True)
        self.purch_datepicker.setDisplayFormat("MMMM d, yyyy")
        self.purch_hbox.addWidget(self.purch_datepicker)
        self.layout.addLayout(self.purch_hbox, False)

        # buttons to confirm or cancel
        self.button_hbox = QHBoxLayout(self)
        self.ok_btn = QPushButton("&OK")
        self.ok_btn.clicked.connect(self._ok)
        self.cancel_btn = QPushButton("&Cancel")
        self.cancel_btn.clicked.connect(self._cancel)
        self.button_hbox.addWidget(self.ok_btn)
        self.button_hbox.addWidget(self.cancel_btn)
        self.layout.addLayout(self.button_hbox)

    def _syncControlsToItem(self, *args):
        for i in range(self.goal_combo.count()):
            if self.format_goal(self.item) == self.goal_combo.itemText(i):
                self.goal_combo.setCurrentIndex(i)

        self.amount_text.setText(str(self.item.amount.number))
        self.amount_combo.setCurrentIndex(self.amounts.index(self.item.amount.unit))
        if self.item.purchase_date:
            self.purch_datepicker.setDate(QDate(
                self.item.purchase_date.year,
                self.item.purchase_date.month,
                self.item.purchase_date.day))
        else:
            today = datetime.today()
            self.purch_datepicker.setDate(QDate(today.year,
                                                today.month,
                                                today.day))

    def _initControls(self):
        self.amount_text.setText("0")
        self.amount_combo.setCurrentIndex(self.amounts.index("pound"))
        today = datetime.today()
        self.purch_datepicker.setDate(QDate(today.year,
                                            today.month,
                                            today.day))

    def _syncItemToControls(self, *args):
        goal = self.goals[self.goal_combo.currentIndex()]
        
        if not self.item:
            self.item = goal.clone()
        else:
            self.item.condition = goal.condition
            self.item.description = goal.description

        self.item.amount = Measurement(
            int(self.amount_text.text()),
            self.amount_combo.itemText(self.amount_combo.currentIndex()))

        self.item.life = goal.life

        qd = self.purch_datepicker.date()
        
        self.item.purchase_date = datetime(qd.year(),
                                           qd.month(),
                                           qd.day())

    def _ok(self, *args):
        self.canceled = False
        self._syncItemToControls()
        self.close()
        
    def _cancel(self, *args):
        self.close()
        
class GoalDialog(QDialog):
    """A dialog to add or edit inventory items"""
    def __init__(self, parent, conditions, amounts, durations, item=None):
        QDialog.__init__(self, parent)

        self.item = item
        
        self.setMinimumWidth(400)
        self.setWindowTitle("Add/Edit Inventory Item")

        # avoid duplicating "enumerations" needed to specify an item
        self.conditions = conditions
        self.amounts = amounts
        self.durations = durations

        self.addControls()

        # if there's an item, sync the controls to it
        if self.item:
            self._syncControlsToItem()
        else: # otherwise, use sensible initial values
            self._initControls()

    def _syncControlsToItem(self):
        """Make the controls match the current item"""
        self.cond_combo.setCurrentIndex(self.conditions.index(self.item.condition))
        self.dsc_text.setText(self.item.description)
        self.amount_text.setText(str(self.item.amount.number))
        self.amount_combo.setCurrentIndex(self.amounts.index(self.item.amount.unit))
        self.life_text.setText(str(self.item.life.number))
        self.life_combo.setCurrentIndex(self.durations.index(self.item.life.unit))

    def _syncItemToControls(self):
        """Update or create the item to match the user input"""

        # if there's an item, update it
        if self.item: 
            self.item.condition = self.cond_combo.currentText()
            self.item.description = self.dsc_text.text()
            self.item.amount = Measurement(int(self.amount_text.text()),
                                           self.amounts[self.amount_combo.currentIndex()])
            self.item.life = Measurement(int(self.life_text.text()),
                                         self.durations[self.life_combo.currentIndex()])
            self.item.purchase_date = None
        else: # otherwise, create a new one
            self.item = InventoryItem(
                None, # no ID until it's saved
                self.cond_combo.currentText(),
                self.dsc_text.text(),
                Measurement(int(self.amount_text.text()),
                            self.amounts[self.amount_combo.currentIndex()]),
                Measurement(int(self.life_text.text()),
                            self.durations[self.life_combo.currentIndex()]),
                None)

    def commit(self, *args, **kwargs):
        """Run when OK is clicked"""
        
        self._syncItemToControls()

        # if there's an ID, save over it
        if self.item.id:
            self.parent().db.save_inventory(self.item)
        else: # otherwise add a new item
            self.parent().db.add_inventory(self.item)
            
        self.close()
        
    def _initControls(self):
        """Initialize the controls to sensible initial values"""
        self.cond_combo.setCurrentIndex(0)
        
        self.amount_text.setText("40") # a standard plastic bucket
                                       # holds about 40 pounds of
                                       # grain
        self.amount_combo.setCurrentIndex(self.amounts.index("pound"))
        
        self.life_text.setText("2") # 2 years is standard for canned
                                    # goods
    
        self.life_combo.setCurrentIndex(self.durations.index("year"))
        
    def addControls(self):
        """Set up the controls for the form"""
        
        self.layout = QVBoxLayout(self)

        self.cond_hbox = QHBoxLayout(self)

        # combo box for condition (e.g. dry, canned, etc.)
        self.cond_hbox.addWidget(QLabel("Condition:"))
        self.cond_combo = QComboBox(self)
        self.cond_combo.addItems(self.parent().conditions)
        self.cond_hbox.addWidget(self.cond_combo)
        self.layout.addLayout(self.cond_hbox, False)

        # description of the item
        self.dsc_hbox = QHBoxLayout(self)
        self.dsc_hbox.addWidget(QLabel("Description:"))
        self.dsc_text = QLineEdit()
        self.dsc_hbox.addWidget(self.dsc_text)
        self.layout.addLayout(self.dsc_hbox, False)

        # amount (number and unit)
        self.amount_hbox = QHBoxLayout(self)
        self.amount_hbox.addWidget(QLabel("Amount:"))
        self.amount_text = QLineEdit()
        self.amount_hbox.addWidget(self.amount_text)
        self.amount_combo = QComboBox(self)
        self.amount_combo.addItems(self.parent().amounts)
        self.amount_hbox.addWidget(self.amount_combo)
        self.layout.addLayout(self.amount_hbox)

        # life (number and duration unit)
        self.life_hbox = QHBoxLayout(self)
        self.life_hbox.addWidget(QLabel("Life:"))
        self.life_text = QLineEdit()
        self.life_hbox.addWidget(self.life_text)
        self.life_combo = QComboBox(self)
        self.life_combo.addItems(self.parent().durations)
        self.life_hbox.addWidget(self.life_combo)
        self.layout.addLayout(self.life_hbox)

        # buttons for OK and Cancel
        self.btn_hbox = QHBoxLayout(self)
        self.ok_btn = QPushButton("&OK")
        self.ok_btn.clicked.connect(self.commit)
        self.cancel_btn = QPushButton("&Cancel")
        self.cancel_btn.clicked.connect(self.close)
        self.btn_hbox.addWidget(self.ok_btn)
        self.btn_hbox.addWidget(self.cancel_btn)
        self.layout.addLayout(self.btn_hbox)
        
        
class Quartermaster(QMainWindow):
    """The main window of the application"""
    def __init__(self):
        QMainWindow.__init__(self)

        # if a file is loaded, its name will be stored here
        self.filename = ""

        # .ini file for settings
        self.settings = QSettings()
        
        self.setWindowTitle("Quartermaster")

        # any narrower than this won't really work
        self.setMinimumWidth(400)

        self.addControls()

        # read the last file opened from the settings file
        last_file = self.settings.value("last file")

        # if there was a last file, re-open it
        if last_file:
            self.loadFile(last_file)

        # TODO: restore saved window state
        self.showMaximized()

    def selectedRow(self):
        """Return the index of the selected row"""
        
        sm = self.inventory_table.selectionModel()
        selected = sm.selection()
        return selected.indexes()[0].row() # our selection mode only
    # allows single row
    # selections, so this is
    # safe

    def goalDialog(self, item):
        """Build a new dialog to edit the specified inventory item"""
        return GoalDialog(self,
                          self.conditions,
                          self.amounts,
                          self.durations,
                          item)
    
    def showClone(self, *args):
        """Clone an item and show a dialog to edit the clone"""
        
        row = self.selectedRow()
        
        # clone the selected item as a new inventory item
        item = self.inventory_model.items[row].clone("inventory")

        frm = InventoryItemDialog(self,
                                  self.allGoals(),
                                  self.amounts,
                                  item)
        frm.exec()

        if not frm.canceled:
            self.items.append(frm.item)
            self.set_model()
            self.db.add_inventory(frm.item)

    def deleteItem(self, *args):
        row = self.selectedRow()
        item = self.inventory_model.items[row]
        
        conf_dlg = QMessageBox()
        conf_dlg.setWindowTitle("Confirm item deletion")
        conf_dlg.setText("Really delete %s?" % item.to_string())
        
        conf_dlg.setIcon(QMessageBox.Question)
        conf_dlg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        
        conf_dlg.setDefaultButton(QMessageBox.Save)

        ret = conf_dlg.exec_()
        
        if ret == QMessageBox.Ok:
            self.db.delete_item(item)
            self.set_model()
        elif ret == QMessageBox.Cancel:
            pass

    def allGoals(self):
        goals = self.db.all_inventory("goal")
        goals.sort(key=lambda g: "%s (%s)" % (g.description, g.condition))
        return goals
    
    def showEdit(self, *args):
        """Show a dialog to edit the selected item"""

        view = self.view_combo.itemText(self.view_combo.currentIndex())
        item = self.inventory_model.items[self.selectedRow()]
        
        if view.lower() == "goal":
            gd = self.goalDialog(item)
            gd.exec()
            self.db.save_inventory(item)
            
        else:
            frm = InventoryItemDialog(self,
                                      self.allGoals(),
                                      self.amounts,
                                      item)
            frm.exec()

            if not frm.canceled:
                self.db.save_inventory(frm.item)

    def showAdd(self, *args, **kwargs):
        """Show a dialog to add a new inventory item"""

        view = self.view_combo.itemText(self.view_combo.currentIndex())

        if view.lower() == "goal":
            frm = self.goalDialog(None)
            frm.setWindowTitle("Add new goal")
            frm.exec()
            if frm.item:
                self.db.add_inventory(frm.item, "goal")
        else:
            frm = InventoryItemDialog(self, self.allGoals(), self.amounts)

            frm.exec()

            if not frm.canceled:
                self.items.append(frm.item)
                self.set_model()
                self.db.add_inventory(frm.item)

    def loadFile(self, filename):
        """Load the specified inventory file"""
        
        self.filename = filename
        
        self.setWindowTitle("Quartermaster (%s)" % os.path.basename(self.filename))
        self.db = InventoryDB(self.filename)

        # cache some immutable information from the database
        self.conditions = [str(key)
                           for key in self.db.conditions.keys()]
        self.amounts = [str(key)
                        for key in self.db.amounts.keys()]
        self.durations = [str(key)
                          for key in self.db.durations.keys()]
        self.record_types = [str(key)
                             for key in self.db.record_types.keys()]
        
        self.showItems()

    def showItems(self):
        """Show the items on the form"""

        self.clone_btn.setEnabled(self.view_combo.currentText().lower() == "goal")
        
        self.items = self.db.all_inventory(self.view_combo.currentText().lower())
        self.set_model()

    def view_combo_changed(self, *args):
        """Runs when the user changes the current view"""
        self.showItems()
        
    def browseOpenFile(self, *args, **kwargs):
        """Show a file dialog to open a .qm file"""

        # open a file dialog at the last-used path
        fn, _ = QFileDialog.getOpenFileName(self,
                                            'Open file',
                                            self.settings.value("save directory"),
                                            "*.qm")

        # if a file was chosen, open it
        if fn:
            # save the last file opened and its directory
            self.settings.setValue("last file", fn)
            self.settings.setValue("save directory", os.path.dirname(fn))
            
            self.loadFile(fn)

    def browseCreateFile(self, *args, **kwargs):
        """Show a file dialog to create a new .qm file"""
        
        fn, _ = QFileDialog.getSaveFileName(self,
                                            'New file',
                                            self.settings.value("save directory"),
                                            "*.qm")
        # if a filename was chosen
        if fn:
            # save the last file opened and its directory
            self.settings.setValue("last file", fn)
            self.settings.setValue("save directory", os.path.dirname(fn))
            
            self.loadFile(fn)

    def getRationNumber(self):
        """Show a dialog to determine base ration multiplier and return it"""
        dlg = RationMultiplierDialog(self)
        dlg.exec()
        return dlg.value

    def setGoals(self):
        """Add database records for inventory goals"""
        
        multiplier = self.getRationNumber()
        
        if multiplier:
            self.db.set_goals(multiplier)
            self.set_model()
        else: # if the dialog was canceled, let the user know no goals
            # were set
            mb = QMessageBox()
            mb.setText("Goals not set.")
            mb.exec_()

    def set_model(self):
        """Having loaded a file, show the items in the tableview"""
        
        self.filter_entry.setText("")

        # build and use  a new list model
        self.inventory_model = InventoryListModel(self.inventory_table,
                                                  self.items)
        self.inventory_table.setModel(self.inventory_model)

        # hide the ID column
        self.inventory_table.setColumnHidden(0, True)

        # make everything at least visible
        self.inventory_table.resizeColumnsToContents()

    def filterItems(self):
        """Apply the filter to the table model"""
        
        filter_text = self.filter_entry.text()
        
        if self.inventory_model:
            self.inventory_model.set_filter(filter_text)

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

        self.control_hbx = QHBoxLayout(self.main_widget)

        # a combo box of available views
        self.view_combo = QComboBox()
        self.view_combo.setMinimumWidth(200)
        self.view_combo.addItems(["Inventory", "Goal"])
        self.view_combo.currentIndexChanged.connect(self.showItems)
        self.control_hbx.addWidget(self.view_combo)

        # a way to enter filters
        self.filter_entry = QLineEdit()
        self.filter_entry.setPlaceholderText("Filter text. . . ")
        self.filter_entry.textChanged.connect(self.filterItems)
        self.control_hbx.addWidget(self.filter_entry)

        # filter clearing button
        self.clear_btn = QPushButton("C&lear")
        self.clear_btn.clicked.connect(lambda *args: self.filter_entry.setText(""))
        self.control_hbx.addWidget(self.clear_btn)

        self.layout.addLayout(self.control_hbx)

        # the table showing inventory items or goals
        self.inventory_table = QTableView()
        self.inventory_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.inventory_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.inventory_table.setSortingEnabled(True)

        self.inventory_table.doubleClicked.connect(self.showEdit)

        self.layout.addWidget(self.inventory_table)

        # buttons for various actions
        self.btn_hbx = QHBoxLayout(self)

        self.add_btn = QPushButton("&Add")
        self.add_btn.clicked.connect(self.showAdd)

        self.edit_btn = QPushButton("&Edit")
        self.edit_btn.clicked.connect(self.showEdit)

        self.clone_btn = QPushButton("Fulfill &goal")
        self.clone_btn.clicked.connect(self.showClone)
        
        self.delete_btn = QPushButton("&Delete")
        self.delete_btn.clicked.connect(self.deleteItem)
        
        self.btn_hbx.addWidget(self.add_btn)
        self.btn_hbx.addWidget(self.edit_btn)
        self.btn_hbx.addWidget(self.clone_btn)
        self.btn_hbx.addWidget(self.delete_btn)

        self.layout.addLayout(self.btn_hbx)

    def run(self):
        self.show()
        qt_app.exec_()

app = Quartermaster()

app.run()
