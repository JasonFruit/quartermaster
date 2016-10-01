import os
from sqlite3 import connect
import codecs
import math
from datetime import datetime, timedelta
from dateutil.parser import parse

class Measurement(object):
    def __init__(self, number, unit):
        self.number = number
        self.unit = unit
    def __repr__(self):
        if self.number == 1:
            return "%s %s" % (self.number, self.unit)
        else:
            return "%s %ss" % (self.number, self.unit)
    def to_string(self):
        return repr(self)
    def __lt__(self, other):
        return self.number < other.number
    def __gt__(self, other):
        return self.number > other.number
    def __eq__(self, other):
        return ((self.number == other.number) and
                (self.unit == other.unit))
    def __le__(self, other):
        return self.number <= other.number
    def __ge__(self, other):
        return self.number >= other.number
    def __ne__(self, other):
        return not self.__eq__(other)
    
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

save_inventory_sql = """update item set
condition_id = ?,
item = ?,
weight = ?,
weight_unit_id = ?,
life = ?,
life_unit_id = ?,
record_type_id = ?,
purchase_date = ?,
expiration_date = ?
where id = ?"""

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
        if type(purchase_date) == str:
            self.purchase_date = parse(purchase_date)
        else:
            self.purchase_date = purchase_date
    @property
    def expiration_date(self):
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

        
class InventoryDB(object):
    def __init__(self, path):

        with open("sql/create-db.sql", "r") as f:
            create_sql = f.read()

        if os.path.exists(path):            
            self.conn = connect(path)
            self.cur = self.conn.cursor()
        else:
            self.conn = connect(path)
            self.cur = self.conn.cursor()
            self.cur.executescript(create_sql)
            self.conn.commit()

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
        self.cur.execute("delete from item where record_type_id = ?",
                         (self.record_types["goal"],))
        with codecs.open("sql/goal.sql") as f:
            sql = f.read()
        self.cur.execute(sql, (mult,))
        self.conn.commit()

    def save_inventory(self, item):
        amount, amount_id = item.amount.number, self.amounts[item.amount.unit]
        life, life_id = item.life.number, self.durations[item.life.unit]
        rec_type_id = self.record_types["inventory"]
        condition_id = self.conditions[item.condition]
        self.cur.execute(save_inventory_sql,
                         (condition_id,
                          item.description,
                          amount,
                          amount_id,
                          life,
                          life_id,
                          rec_type_id,
                          item.purchase_date,
                          item.expiration_date,
                          item.id))
        self.conn.commit()

    def add_inventory(self, item):
        amount, amount_id = item.amount.number, self.amounts[item.amount.unit]
        life, life_id = item.life.number, self.durations[item.life.unit]
        rec_type_id = self.record_types["inventory"]
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
        item.id = self.cur.lastrowid

    def all_inventory(self, record_type=None):

        if not record_type:
            record_type = "inventory"

        record_type_id = self.record_types[record_type]
            
        self.cur.execute(inventory_sql, (record_type_id,))
        
        output = []
        
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

if __name__ == "__main__":
    import sys
    db = InventoryDB(sys.argv[1])
    db.set_goals(3.5)
