--
-- ���� ������������ � ������� SQLiteStudio v3.4.15 � �� ��� 8 18:15:07 2025
--
-- �������������� ��������� ������: System
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- �������: alembic_version
CREATE TABLE IF NOT EXISTS alembic_version (
	version_num VARCHAR(32) NOT NULL, 
	CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);

-- �������: categories
CREATE TABLE IF NOT EXISTS categories (
	id INTEGER NOT NULL, 
	name VARCHAR NOT NULL, 
	PRIMARY KEY (id)
);
INSERT INTO categories (id, name) VALUES (1, 'Base ');
INSERT INTO categories (id, name) VALUES (2, 'Whales_club');
INSERT INTO categories (id, name) VALUES (3, '��������� by ���');

-- �������: items
CREATE TABLE IF NOT EXISTS items (
	id INTEGER NOT NULL, 
	name VARCHAR NOT NULL, 
	description VARCHAR NOT NULL, 
	price FLOAT NOT NULL, 
	type VARCHAR(10) NOT NULL, 
	duration VARCHAR(12) NOT NULL, 
	category_id BIGINT NOT NULL, 
	PRIMARY KEY (id)
);
INSERT INTO items (id, name, description, price, type, duration, category_id) VALUES (1, '���� �����', '�������� Private �� 3 ������', 39.0, 'Base', 'one_month', 1);
INSERT INTO items (id, name, description, price, type, duration, category_id) VALUES (2, '���� 6 �������', '�������� Private �� 6 ������', 99.0, 'Base', 'six_months', 1);
INSERT INTO items (id, name, description, price, type, duration, category_id) VALUES (3, '���� ��� ����', '�������� Private �� 1 ���', 169.0, 'Base', 'one_year', 1);
INSERT INTO items (id, name, description, price, type, duration, category_id) VALUES (4, '���� ��������', '���������� Private ��������', 999.0, 'Base', 'forever', 1);
INSERT INTO items (id, name, description, price, type, duration, category_id) VALUES (5, 'Trial 1 �����', '������� ���Whales_club�����', 119.33, 'Whales_club', 'one_month', 2);
INSERT INTO items (id, name, description, price, type, duration, category_id) VALUES (6, 'Trial 3 ������', '������� �������� �� 3 ������', 150.0, 'Whales_club', 'three_months', 2);
INSERT INTO items (id, name, description, price, type, duration, category_id) VALUES (7, 'Trial 6 �������', '������� �������� �� 6 �������', 300.0, 'Whales_club', 'six_months', 2);
INSERT INTO items (id, name, description, price, type, duration, category_id) VALUES (8, 'Biohacking 6 �������', '�������� �� Biohacking �� 6 ������', 290.0, 'biohacking', 'six_months', 3);
INSERT INTO items (id, name, description, price, type, duration, category_id) VALUES (9, 'Biohacking 1 ���', '�������� �� Biohacking �� 1 ���', 490.0, 'biohacking', 'one_year', 3);
INSERT INTO items (id, name, description, price, type, duration, category_id) VALUES (10, 'Biohacking 3 ������', '�������� �� Biohacking �� 3 ������', 190.0, 'biohacking', 'three_months', 3);

-- �������: user_subscriptions
CREATE TABLE IF NOT EXISTS user_subscriptions (
	id INTEGER NOT NULL, 
	user_id INTEGER NOT NULL, 
	item_id INTEGER NOT NULL, 
	start_date VARCHAR NOT NULL, 
	end_date VARCHAR NOT NULL, 
	status VARCHAR NOT NULL, transaction_hash VARCHAR(255) NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES users (id), 
	FOREIGN KEY(item_id) REFERENCES items (id)
);

-- �������: users
CREATE TABLE IF NOT EXISTS users (
	id INTEGER NOT NULL, 
	tg_id BIGINT NOT NULL, 
	username VARCHAR, 
	PRIMARY KEY (id), 
	UNIQUE (tg_id)
);
INSERT INTO users (id, tg_id, username) VALUES (1, 7727794334, NULL);
INSERT INTO users (id, tg_id, username) VALUES (3, 1107486256, NULL);
INSERT INTO users (id, tg_id, username) VALUES (4, 2070761513, NULL);

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
