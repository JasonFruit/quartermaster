BEGIN TRANSACTION;

CREATE TABLE unit (
    id integer not null primary key,
    unit text,
    dimension text,
    multiplier integer null,
    ref_id integer null,
    foreign key (ref_id) references unit(id)
);

INSERT INTO "unit" VALUES(1,'each','amount',NULL,NULL);
INSERT INTO "unit" VALUES(2,'fl. oz.','amount',NULL,NULL);
INSERT INTO "unit" VALUES(3,'gallon','amount',128,2);
INSERT INTO "unit" VALUES(4,'ounce','amount',NULL,NULL);
INSERT INTO "unit" VALUES(5,'pound','amount',16,4);
INSERT INTO "unit" VALUES(6,'day','time',NULL,NULL);
INSERT INTO "unit" VALUES(7,'month','time',30,6);
INSERT INTO "unit" VALUES(8,'year','time',365,6);

CREATE TABLE condition (
    id integer not null primary key,
    description text
);

INSERT INTO "condition" VALUES(1,'');
INSERT INTO "condition" VALUES(2,'Canned');
INSERT INTO "condition" VALUES(3,'Dry');
INSERT INTO "condition" VALUES(4,'Frozen');

CREATE TABLE recordtype (
    id integer not null primary key,
    description text
);

INSERT INTO "recordtype" VALUES(1,'recommendation');
INSERT INTO "recordtype" VALUES(2,'goal');
INSERT INTO "recordtype" VALUES(3,'inventory');

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
    expiration_date datetime null,
    foreign key (condition_id) references condition(id),
    foreign key (weight_unit_id) references unit(id),
    foreign key (life_unit_id) references unit(id),
    foreign key (record_type_id) references recordtype(id)
);

INSERT INTO "item" VALUES(1,1,'Cereal',5,5,3,8,1,NULL,NULL);
INSERT INTO "item" VALUES(2,1,'Cornmeal',10,5,30,8,1,NULL,NULL);
INSERT INTO "item" VALUES(3,1,'Flour',75,5,8,8,1,NULL,NULL);
INSERT INTO "item" VALUES(4,1,'Mixes',10,5,2,8,1,NULL,NULL);
INSERT INTO "item" VALUES(5,1,'Oats',20,5,30,8,1,NULL,NULL);
INSERT INTO "item" VALUES(6,3,'Pasta',40,5,30,8,1,NULL,NULL);
INSERT INTO "item" VALUES(7,1,'Rice',40,5,30,8,1,NULL,NULL);
INSERT INTO "item" VALUES(8,1,'Wheat',100,5,30,8,1,NULL,NULL);
INSERT INTO "item" VALUES(9,2,'Black beans',5,5,2,8,1,NULL,NULL);
INSERT INTO "item" VALUES(10,3,'Black beans',5,5,30,8,1,NULL,NULL);
INSERT INTO "item" VALUES(11,2,'Chili beans',5,5,2,8,1,NULL,NULL);
INSERT INTO "item" VALUES(12,2,'Kidney beans',5,5,2,8,1,NULL,NULL);
INSERT INTO "item" VALUES(13,3,'Kidney beans',5,5,30,8,1,NULL,NULL);
INSERT INTO "item" VALUES(14,3,'Lentils',5,5,30,8,1,NULL,NULL);
INSERT INTO "item" VALUES(15,2,'Pinto beans',7,5,2,8,1,NULL,NULL);
INSERT INTO "item" VALUES(16,3,'Pinto beans',7,5,30,8,1,NULL,NULL);
INSERT INTO "item" VALUES(17,2,'Pork and beans',5,5,2,8,1,NULL,NULL);
INSERT INTO "item" VALUES(18,2,'Refried beans',10,5,2,8,1,NULL,NULL);
INSERT INTO "item" VALUES(19,2,'Evaporated milk',2,5,2,8,1,NULL,NULL);
INSERT INTO "item" VALUES(20,3,'Powdered milk',12,5,20,8,1,NULL,NULL);
INSERT INTO "item" VALUES(21,2,'Sweetened condensed milk',1,5,2,8,1,NULL,NULL);
INSERT INTO "item" VALUES(22,3,'Powdered cheese',1,5,2,8,1,NULL,NULL);
INSERT INTO "item" VALUES(23,1,'Brown sugar',6,5,2,8,1,NULL,NULL);
INSERT INTO "item" VALUES(24,1,'Corn syrup',1,5,2,8,1,NULL,NULL);
INSERT INTO "item" VALUES(25,1,'Honey',3,5,30,8,1,NULL,NULL);
INSERT INTO "item" VALUES(26,1,'Jams/Jellies',3,5,2,8,1,NULL,NULL);
INSERT INTO "item" VALUES(27,3,'Jello',1,5,18,7,1,NULL,NULL);
INSERT INTO "item" VALUES(28,1,'Maple syrup',3,5,2,8,1,NULL,NULL);
INSERT INTO "item" VALUES(29,1,'Molasses',1,5,2,8,1,NULL,NULL);
INSERT INTO "item" VALUES(30,1,'Powdered sugar',6,5,2,8,1,NULL,NULL);
INSERT INTO "item" VALUES(31,1,'Powdered pudding',1,5,18,7,1,NULL,NULL);
INSERT INTO "item" VALUES(32,1,'White sugar',35,5,30,8,1,NULL,NULL);
INSERT INTO "item" VALUES(33,4,'Butter',2,5,1,8,1,NULL,NULL);
INSERT INTO "item" VALUES(34,1,'Vegetable oil',5,5,2,8,1,NULL,NULL);
INSERT INTO "item" VALUES(35,4,'Margarine',2,5,1,8,1,NULL,NULL);
INSERT INTO "item" VALUES(36,1,'Mayonnaise',4,5,1,8,1,NULL,NULL);
INSERT INTO "item" VALUES(37,1,'Olive oil',3,5,2,8,1,NULL,NULL);
INSERT INTO "item" VALUES(38,1,'Peanut butter',4,5,4,8,1,NULL,NULL);
INSERT INTO "item" VALUES(39,1,'Salad dressing',2,5,1,8,1,NULL,NULL);
INSERT INTO "item" VALUES(40,1,'Shortening',3,5,2,8,1,NULL,NULL);
INSERT INTO "item" VALUES(41,1,'Salt',8,5,30,8,1,NULL,NULL);
INSERT INTO "item" VALUES(42,2,'Chicken',2,5,2,8,1,NULL,NULL);
INSERT INTO "item" VALUES(43,2,'Tuna',5,5,2,8,1,NULL,NULL);
INSERT INTO "item" VALUES(44,2,'Turkey',1,5,2,8,1,NULL,NULL);
INSERT INTO "item" VALUES(45,2,'Meat soups',2,5,2,8,1,NULL,NULL);
INSERT INTO "item" VALUES(46,2,'Clams',1,5,2,8,1,NULL,NULL);
INSERT INTO "item" VALUES(47,2,'Spam',1,5,2,8,1,NULL,NULL);
INSERT INTO "item" VALUES(48,2,'Stew',2,5,2,8,1,NULL,NULL);
INSERT INTO "item" VALUES(49,2,'Sausage',1,5,2,8,1,NULL,NULL);
INSERT INTO "item" VALUES(50,3,'TVP',1,5,20,8,1,NULL,NULL);
INSERT INTO "item" VALUES(51,2,'Applesauce',9,5,2,8,1,NULL,NULL);
INSERT INTO "item" VALUES(52,3,'Fruit',4,5,2,8,1,NULL,NULL);
INSERT INTO "item" VALUES(53,2,'Fruit cocktail',3,5,2,8,1,NULL,NULL);
INSERT INTO "item" VALUES(54,2,'Oranges',9,5,2,8,1,NULL,NULL);
INSERT INTO "item" VALUES(55,2,'Peaches',6,5,2,8,1,NULL,NULL);
INSERT INTO "item" VALUES(56,2,'Pears',6,5,2,8,1,NULL,NULL);
INSERT INTO "item" VALUES(57,2,'Pineapple',6,5,2,8,1,NULL,NULL);
INSERT INTO "item" VALUES(58,2,'Beets',3,5,2,8,1,NULL,NULL);
INSERT INTO "item" VALUES(59,2,'Carrots',2,5,2,8,1,NULL,NULL);
INSERT INTO "item" VALUES(60,2,'Corn',6,5,2,8,1,NULL,NULL);
INSERT INTO "item" VALUES(61,2,'Green beans',6,5,2,8,1,NULL,NULL);
INSERT INTO "item" VALUES(62,2,'Green chilies',1,5,2,8,1,NULL,NULL);
INSERT INTO "item" VALUES(63,3,'Instant potatoes',8,5,30,8,1,NULL,NULL);
INSERT INTO "item" VALUES(64,2,'Mixed vegetables',2,5,2,8,1,NULL,NULL);
INSERT INTO "item" VALUES(65,2,'Mushrooms',1,5,1,8,1,NULL,NULL);
INSERT INTO "item" VALUES(66,3,'Onions',5,5,18,7,1,NULL,NULL);
INSERT INTO "item" VALUES(67,2,'Peas',2,5,2,8,1,NULL,NULL);
INSERT INTO "item" VALUES(68,2,'Pickles',2,5,2,8,1,NULL,NULL);
INSERT INTO "item" VALUES(69,2,'Pumpkin',3,5,2,8,1,NULL,NULL);
INSERT INTO "item" VALUES(70,2,'Salsa',2,5,2,8,1,NULL,NULL);
INSERT INTO "item" VALUES(71,2,'Spaghetti sauce',8,5,2,8,1,NULL,NULL);
INSERT INTO "item" VALUES(72,2,'Tomato paste',1,5,2,8,1,NULL,NULL);
INSERT INTO "item" VALUES(73,2,'Tomato sauce',1,5,2,8,1,NULL,NULL);
INSERT INTO "item" VALUES(74,2,'Tomato soup',2,5,2,8,1,NULL,NULL);
INSERT INTO "item" VALUES(75,2,'Tomatoes',7,5,2,8,1,NULL,NULL);
INSERT INTO "item" VALUES(76,2,'Yams',1,5,2,8,1,NULL,NULL);
INSERT INTO "item" VALUES(77,1,'Baking powder',3,5,3,8,1,NULL,NULL);
INSERT INTO "item" VALUES(78,1,'Baking soda',2,5,3,8,1,NULL,NULL);
INSERT INTO "item" VALUES(79,1,'Cocoa powder',2,5,3,8,1,NULL,NULL);
INSERT INTO "item" VALUES(80,1,'Vanilla extract',1,5,3,8,1,NULL,NULL);
INSERT INTO "item" VALUES(81,1,'Vinegar',3,4,2,8,1,NULL,NULL);
INSERT INTO "item" VALUES(82,4,'Yeast',2,5,1,8,1,NULL,NULL);
INSERT INTO "item" VALUES(83,3,'Coffee',8,5,1,8,1,NULL,NULL);
INSERT INTO "item" VALUES(84,3,'Baking mixes',10,1,1,8,1,NULL,NULL);
INSERT INTO "item" VALUES(85,3,'Crackers',3,5,1,8,1,NULL,NULL);
INSERT INTO "item" VALUES(86,3,'Spices',12,1,3,8,1,NULL,NULL);
INSERT INTO "item" VALUES(87,1,'Chocolate',3,5,18,7,1,NULL,NULL);
INSERT INTO "item" VALUES(88,1,'BBQ sauce',1,5,2,8,1,NULL,NULL);
INSERT INTO "item" VALUES(89,1,'Ketchup',1,5,2,8,1,NULL,NULL);
INSERT INTO "item" VALUES(90,1,'Mustard',1,5,2,8,1,NULL,NULL);
COMMIT;
