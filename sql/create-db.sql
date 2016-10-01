BEGIN TRANSACTION;

CREATE TABLE unit (
    id integer not null primary key,
    unit text,
    dimension text,
    multiplier integer null,
    ref_id integer null,
    foreign key (ref_id) references unit(id)
);

INSERT INTO "unit" VALUES(1,'each', 'amount', null, null);
INSERT INTO "unit" VALUES(2,'fl. oz.', 'amount', null, null);
INSERT INTO "unit" VALUES(3,'gallon', 'amount', 128, 2);
INSERT INTO "unit" VALUES(4,'ounce.', 'amount', null, null);
INSERT INTO "unit" VALUES(5,'pound', 'amount', 16, 4);
INSERT INTO "unit" VALUES(6,'day', 'time', null, null);
INSERT INTO "unit" VALUES(7,'month', 'time', 30, 6);
INSERT INTO "unit" VALUES(8,'year', 'time', 365, 6);

CREATE TABLE condition (
    id integer not null primary key,
    description text
);

INSERT INTO "condition" VALUES(1,'');
INSERT INTO "condition" VALUES(2,'Canned');
INSERT INTO "condition" VALUES(3,'Dry');
INSERT INTO "condition" VALUES(4,'Frozen');

create table recordtype (
    id integer not null primary key,
    description text
);

insert into recordtype (id, description) values (1, 'recommendation');
insert into recordtype (id, description) values (2, 'goal');
insert into recordtype (id, description) values (3, 'inventory');

CREATE TABLE item (
    id integer not null primary key,
    condition_id integer,
    item text,
    weight integer,
    weight_unit_id integer,
    life integer,
    life_unit_id integer,
    record_type_id integer,
    purchase_date datetime null,
    foreign key (condition_id) references condition(id),
    foreign key (weight_unit_id) references unit(id),
    foreign key (life_unit_id) references unit(id),
    foreign key (record_type_id) references recordtype(id)
);


INSERT INTO "item" (condition_id, item, weight, weight_unit_id, life, life_unit_id, record_type_id) VALUES(1,'Cereal',5,3,3,5,1);
INSERT INTO "item" (condition_id, item, weight, weight_unit_id, life, life_unit_id, record_type_id) VALUES(1,'Cornmeal',10,3,30,5,1);
INSERT INTO "item" (condition_id, item, weight, weight_unit_id, life, life_unit_id, record_type_id) VALUES(1,'Flour',75,3,8,5,1);
INSERT INTO "item" (condition_id, item, weight, weight_unit_id, life, life_unit_id, record_type_id) VALUES(1,'Mixes',10,3,2,5,1);
INSERT INTO "item" (condition_id, item, weight, weight_unit_id, life, life_unit_id, record_type_id) VALUES(1,'Oats',20,3,30,5,1);
INSERT INTO "item" (condition_id, item, weight, weight_unit_id, life, life_unit_id, record_type_id) VALUES(3,'Pasta',40,3,30,5,1);
INSERT INTO "item" (condition_id, item, weight, weight_unit_id, life, life_unit_id, record_type_id) VALUES(1,'Rice',40,3,30,5,1);
INSERT INTO "item" (condition_id, item, weight, weight_unit_id, life, life_unit_id, record_type_id) VALUES(1,'Wheat',100,3,30,5,1);
INSERT INTO "item" (condition_id, item, weight, weight_unit_id, life, life_unit_id, record_type_id) VALUES(2,'Black beans',5,3,2,5,1);
INSERT INTO "item" (condition_id, item, weight, weight_unit_id, life, life_unit_id, record_type_id) VALUES(3,'Black beans',5,3,30,5,1);
INSERT INTO "item" (condition_id, item, weight, weight_unit_id, life, life_unit_id, record_type_id) VALUES(2,'Chili beans',5,3,2,5,1);
INSERT INTO "item" (condition_id, item, weight, weight_unit_id, life, life_unit_id, record_type_id) VALUES(2,'Kidney beans',5,3,2,5,1);
INSERT INTO "item" (condition_id, item, weight, weight_unit_id, life, life_unit_id, record_type_id) VALUES(3,'Kidney beans',5,3,30,5,1);
INSERT INTO "item" (condition_id, item, weight, weight_unit_id, life, life_unit_id, record_type_id) VALUES(3,'Lentils',5,3,30,5,1);
INSERT INTO "item" (condition_id, item, weight, weight_unit_id, life, life_unit_id, record_type_id) VALUES(2,'Pinto beans',7,3,2,5,1);
INSERT INTO "item" (condition_id, item, weight, weight_unit_id, life, life_unit_id, record_type_id) VALUES(3,'Pinto beans',7,3,30,5,1);
INSERT INTO "item" (condition_id, item, weight, weight_unit_id, life, life_unit_id, record_type_id) VALUES(2,'Pork and beans',5,3,2,5,1);
INSERT INTO "item" (condition_id, item, weight, weight_unit_id, life, life_unit_id, record_type_id) VALUES(2,'Refried beans',10,3,2,5,1);
INSERT INTO "item" (condition_id, item, weight, weight_unit_id, life, life_unit_id, record_type_id) VALUES(2,'Evaporated milk',2,3,2,5,1);
INSERT INTO "item" (condition_id, item, weight, weight_unit_id, life, life_unit_id, record_type_id) VALUES(3,'Powdered milk',12,3,20,5,1);
INSERT INTO "item" (condition_id, item, weight, weight_unit_id, life, life_unit_id, record_type_id) VALUES(2,'Sweetened condensed milk',1,3,2,5,1);
INSERT INTO "item" (condition_id, item, weight, weight_unit_id, life, life_unit_id, record_type_id) VALUES(3,'Powdered cheese',1,3,2,5,1);
INSERT INTO "item" (condition_id, item, weight, weight_unit_id, life, life_unit_id, record_type_id) VALUES(1,'Brown sugar',6,3,2,5,1);
INSERT INTO "item" (condition_id, item, weight, weight_unit_id, life, life_unit_id, record_type_id) VALUES(1,'Corn syrup',1,3,2,5,1);
INSERT INTO "item" (condition_id, item, weight, weight_unit_id, life, life_unit_id, record_type_id) VALUES(1,'Honey',3,3,30,5,1);
INSERT INTO "item" (condition_id, item, weight, weight_unit_id, life, life_unit_id, record_type_id) VALUES(1,'Jams/Jellies',3,3,2,5,1);
INSERT INTO "item" (condition_id, item, weight, weight_unit_id, life, life_unit_id, record_type_id) VALUES(3,'Jello',1,3,18,4,1);
INSERT INTO "item" (condition_id, item, weight, weight_unit_id, life, life_unit_id, record_type_id) VALUES(1,'Maple syrup',3,3,2,5,1);
INSERT INTO "item" (condition_id, item, weight, weight_unit_id, life, life_unit_id, record_type_id) VALUES(1,'Molasses',1,3,2,5,1);
INSERT INTO "item" (condition_id, item, weight, weight_unit_id, life, life_unit_id, record_type_id) VALUES(1,'Powdered sugar',6,3,2,5,1);
INSERT INTO "item" (condition_id, item, weight, weight_unit_id, life, life_unit_id, record_type_id) VALUES(1,'Powdered pudding',1,3,18,4,1);
INSERT INTO "item" (condition_id, item, weight, weight_unit_id, life, life_unit_id, record_type_id) VALUES(1,'White sugar',35,3,30,5,1);
INSERT INTO "item" (condition_id, item, weight, weight_unit_id, life, life_unit_id, record_type_id) VALUES(4,'Butter',2,3,1,5,1);
INSERT INTO "item" (condition_id, item, weight, weight_unit_id, life, life_unit_id, record_type_id) VALUES(1,'Vegetable oil',5,3,2,5,1);
INSERT INTO "item" (condition_id, item, weight, weight_unit_id, life, life_unit_id, record_type_id) VALUES(4,'Margarine',2,3,1,5,1);
INSERT INTO "item" (condition_id, item, weight, weight_unit_id, life, life_unit_id, record_type_id) VALUES(1,'Mayonnaise',4,3,1,5,1);
INSERT INTO "item" (condition_id, item, weight, weight_unit_id, life, life_unit_id, record_type_id) VALUES(1,'Olive oil',3,3,2,5,1);
INSERT INTO "item" (condition_id, item, weight, weight_unit_id, life, life_unit_id, record_type_id) VALUES(1,'Peanut butter',4,3,4,5,1);
INSERT INTO "item" (condition_id, item, weight, weight_unit_id, life, life_unit_id, record_type_id) VALUES(1,'Salad dressing',2,3,1,5,1);
INSERT INTO "item" (condition_id, item, weight, weight_unit_id, life, life_unit_id, record_type_id) VALUES(1,'Shortening',3,3,2,5,1);
INSERT INTO "item" (condition_id, item, weight, weight_unit_id, life, life_unit_id, record_type_id) VALUES(1,'Salt',8,3,30,5,1);
INSERT INTO "item" (condition_id, item, weight, weight_unit_id, life, life_unit_id, record_type_id) VALUES(2,'Chicken',2,3,2,5,1);
INSERT INTO "item" (condition_id, item, weight, weight_unit_id, life, life_unit_id, record_type_id) VALUES(2,'Tuna',5,3,2,5,1);
INSERT INTO "item" (condition_id, item, weight, weight_unit_id, life, life_unit_id, record_type_id) VALUES(2,'Turkey',1,3,2,5,1);
INSERT INTO "item" (condition_id, item, weight, weight_unit_id, life, life_unit_id, record_type_id) VALUES(2,'Meat soups',2,3,2,5,1);
INSERT INTO "item" (condition_id, item, weight, weight_unit_id, life, life_unit_id, record_type_id) VALUES(2,'Clams',1,3,2,5,1);
INSERT INTO "item" (condition_id, item, weight, weight_unit_id, life, life_unit_id, record_type_id) VALUES(2,'Spam',1,3,2,5,1);
INSERT INTO "item" (condition_id, item, weight, weight_unit_id, life, life_unit_id, record_type_id) VALUES(2,'Stew',2,3,2,5,1);
INSERT INTO "item" (condition_id, item, weight, weight_unit_id, life, life_unit_id, record_type_id) VALUES(2,'Sausage',1,3,2,5,1);
INSERT INTO "item" (condition_id, item, weight, weight_unit_id, life, life_unit_id, record_type_id) VALUES(3,'TVP',1,3,20,5,1);
INSERT INTO "item" (condition_id, item, weight, weight_unit_id, life, life_unit_id, record_type_id) VALUES(2,'Applesauce',9,3,2,5,1);
INSERT INTO "item" (condition_id, item, weight, weight_unit_id, life, life_unit_id, record_type_id) VALUES(3,'Fruit',4,3,2,5,1);
INSERT INTO "item" (condition_id, item, weight, weight_unit_id, life, life_unit_id, record_type_id) VALUES(2,'Fruit cocktail',3,3,2,5,1);
INSERT INTO "item" (condition_id, item, weight, weight_unit_id, life, life_unit_id, record_type_id) VALUES(2,'Oranges',9,3,2,5,1);
INSERT INTO "item" (condition_id, item, weight, weight_unit_id, life, life_unit_id, record_type_id) VALUES(2,'Peaches',6,3,2,5,1);
INSERT INTO "item" (condition_id, item, weight, weight_unit_id, life, life_unit_id, record_type_id) VALUES(2,'Pears',6,3,2,5,1);
INSERT INTO "item" (condition_id, item, weight, weight_unit_id, life, life_unit_id, record_type_id) VALUES(2,'Pineapple',6,3,2,5,1);
INSERT INTO "item" (condition_id, item, weight, weight_unit_id, life, life_unit_id, record_type_id) VALUES(2,'Beets',3,3,2,5,1);
INSERT INTO "item" (condition_id, item, weight, weight_unit_id, life, life_unit_id, record_type_id) VALUES(2,'Carrots',2,3,2,5,1);
INSERT INTO "item" (condition_id, item, weight, weight_unit_id, life, life_unit_id, record_type_id) VALUES(2,'Corn',6,3,2,5,1);
INSERT INTO "item" (condition_id, item, weight, weight_unit_id, life, life_unit_id, record_type_id) VALUES(2,'Green beans',6,3,2,5,1);
INSERT INTO "item" (condition_id, item, weight, weight_unit_id, life, life_unit_id, record_type_id) VALUES(2,'Green chilies',1,3,2,5,1);
INSERT INTO "item" (condition_id, item, weight, weight_unit_id, life, life_unit_id, record_type_id) VALUES(3,'Instant potatoes',8,3,30,5,1);
INSERT INTO "item" (condition_id, item, weight, weight_unit_id, life, life_unit_id, record_type_id) VALUES(2,'Mixed vegetables',2,3,2,5,1);
INSERT INTO "item" (condition_id, item, weight, weight_unit_id, life, life_unit_id, record_type_id) VALUES(2,'Mushrooms',1,3,1,5,1);
INSERT INTO "item" (condition_id, item, weight, weight_unit_id, life, life_unit_id, record_type_id) VALUES(3,'Onions',5,3,18,4,1);
INSERT INTO "item" (condition_id, item, weight, weight_unit_id, life, life_unit_id, record_type_id) VALUES(2,'Peas',2,3,2,5,1);
INSERT INTO "item" (condition_id, item, weight, weight_unit_id, life, life_unit_id, record_type_id) VALUES(2,'Pickles',2,3,2,5,1);
INSERT INTO "item" (condition_id, item, weight, weight_unit_id, life, life_unit_id, record_type_id) VALUES(2,'Pumpkin',3,3,2,5,1);
INSERT INTO "item" (condition_id, item, weight, weight_unit_id, life, life_unit_id, record_type_id) VALUES(2,'Salsa',2,3,2,5,1);
INSERT INTO "item" (condition_id, item, weight, weight_unit_id, life, life_unit_id, record_type_id) VALUES(2,'Spaghetti sauce',8,3,2,5,1);
INSERT INTO "item" (condition_id, item, weight, weight_unit_id, life, life_unit_id, record_type_id) VALUES(2,'Tomato paste',1,3,2,5,1);
INSERT INTO "item" (condition_id, item, weight, weight_unit_id, life, life_unit_id, record_type_id) VALUES(2,'Tomato sauce',1,3,2,5,1);
INSERT INTO "item" (condition_id, item, weight, weight_unit_id, life, life_unit_id, record_type_id) VALUES(2,'Tomato soup',2,3,2,5,1);
INSERT INTO "item" (condition_id, item, weight, weight_unit_id, life, life_unit_id, record_type_id) VALUES(2,'Tomatoes',7,3,2,5,1);
INSERT INTO "item" (condition_id, item, weight, weight_unit_id, life, life_unit_id, record_type_id) VALUES(2,'Yams',1,3,2,5,1);
INSERT INTO "item" (condition_id, item, weight, weight_unit_id, life, life_unit_id, record_type_id) VALUES(1,'Baking powder',3,3,3,5,1);
INSERT INTO "item" (condition_id, item, weight, weight_unit_id, life, life_unit_id, record_type_id) VALUES(1,'Baking soda',2,3,3,5,1);
INSERT INTO "item" (condition_id, item, weight, weight_unit_id, life, life_unit_id, record_type_id) VALUES(1,'Cocoa powder',2,3,3,5,1);
INSERT INTO "item" (condition_id, item, weight, weight_unit_id, life, life_unit_id, record_type_id) VALUES(1,'Vanilla extract',1,3,3,5,1);
INSERT INTO "item" (condition_id, item, weight, weight_unit_id, life, life_unit_id, record_type_id) VALUES(1,'Vinegar',3,2,2,5,1);
INSERT INTO "item" (condition_id, item, weight, weight_unit_id, life, life_unit_id, record_type_id) VALUES(4,'Yeast',2,3,1,5,1);
INSERT INTO "item" (condition_id, item, weight, weight_unit_id, life, life_unit_id, record_type_id) VALUES(3,'Coffee',8,3,1,5,1);
INSERT INTO "item" (condition_id, item, weight, weight_unit_id, life, life_unit_id, record_type_id) VALUES(3,'Baking mixes',10,1,1,5,1);
INSERT INTO "item" (condition_id, item, weight, weight_unit_id, life, life_unit_id, record_type_id) VALUES(3,'Crackers',3,3,1,5,1);
INSERT INTO "item" (condition_id, item, weight, weight_unit_id, life, life_unit_id, record_type_id) VALUES(3,'Spices',12,1,3,5,1);
INSERT INTO "item" (condition_id, item, weight, weight_unit_id, life, life_unit_id, record_type_id) VALUES(1,'Chocolate',3,3,18,4,1);
INSERT INTO "item" (condition_id, item, weight, weight_unit_id, life, life_unit_id, record_type_id) VALUES(1,'BBQ sauce',1,3,2,5,1);
INSERT INTO "item" (condition_id, item, weight, weight_unit_id, life, life_unit_id, record_type_id) VALUES(1,'Ketchup',1,3,2,5,1);
INSERT INTO "item" (condition_id, item, weight, weight_unit_id, life, life_unit_id, record_type_id) VALUES(1,'Mustard',1,3,2,5,1);

COMMIT;
