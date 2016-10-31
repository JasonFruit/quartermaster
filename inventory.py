import os
from sqlite3 import connect
import codecs
import math
from datetime import datetime, timedelta
from dateutil.parser import parse

class Report(object):
    def __init__(self, filename):

        with codecs.open(filename, "r", "utf-8") as f:
            lines = f.readlines()

        i = 0
        header_lines = []
        
        while lines[i].startswith("--"):
            header_lines.append(lines[i].strip(" -"))
            i += 1

        self.title = header_lines[0].strip()

        self.description = "\n".join(header_lines[1:]).strip(" \n")

        self.sql = "\n".join(map(lambda s: s.strip(" \n"),
                                 lines[i:]))
            

class Measurement(object):
    """Represents a numeric measurement with a unit"""
    def __init__(self, number, unit):
        self.number = number
        self.unit = unit
    def __repr__(self):
        return self.to_string()
    def to_string(self):
        # pluralize unit if needed
        if self.number == 1:
            return "%s %s" % (self.number, self.unit)
        else:
            if self.unit == "each":
                return "%s %s" % (self.number, self.unit)
            else:
                return "%s %ss" % (self.number, self.unit)

    def __lt__(self, other):
        if self.unit == other.unit:
            return self.number < other.number
        else:
            return self.unit < other.unit
    def __gt__(self, other):
        if self.unit == other.unit:
            return self.number > other.number
        else:
            return self.unit > other.unit
    def __eq__(self, other):
        if self.unit == other.unit:
            return ((self.number == other.number) and
                    (self.unit == other.unit))
        return False
    def __le__(self, other):
        if self.unit == other.unit:
            return self.number <= other.number
        else:
            return self.unit <= other.unit
    def __ge__(self, other):
        if self.unit == other.unit:
            return self.number >= other.number
        else:
            return self.unit >= other.unit
    def __ne__(self, other):
        return not self.__eq__(other)

# SQL to add a new inventory item    
add_inventory_sql = """insert into item (
    condition_id,
    item,
    weight,
    weight_unit_id,
    life,
    life_unit_id,
    record_type_id,
    purchase_date,
    expiration_date)
values (?, ?, ?, ?, ?, ?, ?, ?, ?);"""

# SQL to update an existing item
save_inventory_sql = """update item set
condition_id = ?,
item = ?,
weight = ?,
weight_unit_id = ?,
life = ?,
life_unit_id = ?,
purchase_date = ?,
expiration_date = ?
where id = ?"""

delete_sql = "delete from item where id = ?"

# SQL to return all inventory of a specific record type
inventory_sql = """
select i.id as id,
c.description as condition,
item as description,
weight,
wu.unit as weight_unit,
life,
lu.unit as life_unit,
rt.description as record_type,
purchase_date
from item i
inner join condition c
on i.condition_id = c.id
inner join unit wu
on i.weight_unit_id = wu.id
inner join unit lu
on i.life_unit_id = lu.id
inner join recordtype rt
on i.record_type_id = rt.id
where i.record_type_id = ?
order by purchase_date desc"""

class InventoryItem(object):
    """Represents an item of inventory (or a goal, or a ration recommendation)"""
    def __init__(self,
                 id,
                 condition,
                 description,
                 amount,
                 life,
                 purchase_date):

        self.id = id

        self.condition = condition
        self.description = description
        self.amount = amount
        self.life = life

        # make sure the purchase date is an actual datetime
        if type(purchase_date) == str:
            self.purchase_date = parse(purchase_date)
        else:
            self.purchase_date = purchase_date

    def clone(self, as_type="inventory"):
        """Copy this item to a new one with no ID as a specified type.  TODO:
        as_type is ignored.  Fix it."""
        
        item = InventoryItem(None,
                             self.condition,
                             self.description,
                             self.amount,
                             self.life,
                             datetime.today())
        
        return item
    
    @property
    def expiration_date(self):
        """Return the expiration date calculated from the purchase date and
        the item's life"""

        # can't if we don't know when it was bought
        if not self.purchase_date:
            return None

        if self.life.unit == "year":
            return datetime(self.purchase_date.year + self.life.number,
                            self.purchase_date.month,
                            self.purchase_date.day)
        elif self.life.unit == "month":
            years = math.floor(self.life.number / 12) + self.purchase_date.year
            months = self.life.number % 12 + self.purchase_date.month

            while months > 12:
                years += 1
                months -= 12

            return datetime(years,
                            months,
                            self.purchase_date.day)

        elif self.life.unit == "day":
            return self.purchase_date + timedelta(self.life.number)
    def to_string(self):
        return "%s (%s), %s" % (self.description,
                                self.condition,
                                self.amount.to_string())

        
class InventoryDB(object):
    """Manages storage of inventory, goal, and recommendation records"""
    def __init__(self, path):

        # read the SQL to create a database
        with open("sql/create-db.sql", "r") as f:
            self.create_sql = f.read()

        # read the SQL to add goals
        with codecs.open("sql/goal.sql") as f:
            self.goal_sql = f.read()

        # if the database specified exists, connect
        if os.path.exists(path):            
            self.conn = connect(path)
            self.cur = self.conn.cursor()
        else: # otherwise, create it
            self.conn = connect(path)
            self.cur = self.conn.cursor()
            self.cur.executescript(self.create_sql)
            self.conn.commit()

        # cache some invariable data
        self.record_types = {}
        self.cur.execute("select id, description from recordtype")
        for row in self.cur.fetchall():
            self.record_types[row[1]] = row[0]

        self.conditions = {}
        self.cur.execute("select id, description from condition")
        for row in self.cur.fetchall():
            self.conditions[row[1]] = row[0]

        self.amounts = {}
        self.cur.execute("select id, unit from unit where dimension = 'amount'")
        for row in self.cur.fetchall():
            self.amounts[row[1]] = row[0]

        self.durations = {}
        self.cur.execute("select id, unit from unit where dimension = 'time'")
        for row in self.cur.fetchall():
            self.durations[row[1]] = row[0]

    def set_goals(self, mult):
        """Set goals by multiplying the recommendation for an adult male by
        <mult>"""

        # remove any existing goals
        self.cur.execute("delete from item where record_type_id = ?",
                         (self.record_types["goal"],))

        # create new ones
        self.cur.execute(self.goal_sql, (mult,))
        self.conn.commit()

    def save_inventory(self, item):
        """Save an altered inventory item to the database"""

        # get the IDs for units from cached data
        amount, amount_id = item.amount.number, self.amounts[item.amount.unit]
        life, life_id = item.life.number, self.durations[item.life.unit]
        condition_id = self.conditions[item.condition]
        
        self.cur.execute(save_inventory_sql,
                         (condition_id,
                          item.description,
                          amount,
                          amount_id,
                          life,
                          life_id,
                          item.purchase_date,
                          item.expiration_date,
                          item.id))
        self.conn.commit()

    def add_inventory(self, item, record_type="inventory"):
        """Save a new inventory item to the database"""

        # get the IDs for units from cached data
        amount, amount_id = item.amount.number, self.amounts[item.amount.unit]
        life, life_id = item.life.number, self.durations[item.life.unit]
        rec_type_id = self.record_types[record_type]
        condition_id = self.conditions[item.condition]
        
        self.cur.execute(add_inventory_sql,
                         (condition_id,
                          item.description,
                          amount,
                          amount_id,
                          life,
                          life_id,
                          rec_type_id,
                          item.purchase_date,
                          item.expiration_date))
        self.conn.commit()

        # update the item's ID with the new row ID
        item.id = self.cur.lastrowid

    def all_inventory(self, record_type=None):
        """Return all items of the specified type (or "inventory" if not
        specified)"""

        if not record_type:
            record_type = "inventory"

        record_type_id = self.record_types[record_type]
            
        self.cur.execute(inventory_sql, (record_type_id,))
        
        output = []

        # just too involved to do as a list comprehension because
        # Python lambdas blow chunks
        for row in self.cur.fetchall():
            (id,
             condition,
             description,
             amount,
             amount_unit,
             life,
             life_unit,
             record_type,
             purchase_date) = row

            amount = Measurement(amount, amount_unit)
            life = Measurement(life, life_unit)
            
            output.append(InventoryItem(id, condition, description, amount, life, purchase_date))
        
        return output

    def delete_item(self, item):
        self.cur.execute(delete_sql, (item.id,))
        self.conn.commit()
