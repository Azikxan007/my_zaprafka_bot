import os
import sqlite3


class DataBasa:
    def __init__(self, db_name='main.db'):
        # 1. Class joylashgan faylning papkasini aniqlaymiz
        base_dir = os.path.dirname(os.path.abspath(__file__))

        # 2. db_name ni o'sha papka manzili bilan birlashtiramiz
        self.db_path = os.path.join(base_dir, db_name)

        # Endi self.db_name o'rniga self.db_path dan foydalanamiz
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def execute_query(self, query, params=()):
        with sqlite3.connect(self.db_path) as conn:
            return conn.execute(query, params)
    def manager(self, sql, *args, commit: bool = False, fetchall: bool = False, fetchone: bool = False, many: bool = False, lastrowid: bool = False):
        with sqlite3.connect(self.db_path) as db:
            cursor = db.cursor()
            cursor.execute(sql, args)
            result = None
            if commit:
                db.commit()
            if fetchall:
                result = cursor.fetchall()
            if fetchone:
                result = cursor.fetchone()
            if lastrowid:
                result = cursor.lastrowid
        return result


#------------------------- Mashina nomer ------------------------------------------
    def create_table_avto_tigach(self):
        sql = """CREATE TABLE IF NOT EXISTS avto_tigach(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Auto_num VARCHAR(30),
            rusum VARCHAR(30))"""
        self.manager(sql, commit=True)

    def insert_into_avto_tigach(self, Auto_num, rusum):
        sql = """INSERT INTO avto_tigach (Auto_num, rusum) VALUES (?, ?)"""
        self.manager(sql, Auto_num, rusum , commit=True)

    def delete_avto_tigach(self, Auto_num):
        sql = """DELETE FROM avto_tigach WHERE Auto_num = ?"""
        self.manager(sql, Auto_num, commit=True)


    def select_avto_tigach(self):
        sql = """SELECT Auto_num, rusum FROM avto_tigach
              order by auto_num
              """
        return self.manager(sql, fetchall=True)

# ------------------------- Viloyatlar ------------------------------------------
    def create_table_county(self):
        sql = """CREATE TABLE IF NOT EXISTS viloyatlar(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            viloyat_nomi VARCHAR(50),
            intermediate_distance INTEGER default 50)
        """
        self.manager(sql, commit=True)


    def insert_into_distance(self, intermediate_distance):
        sql = """UPDATE viloyatlar SET intermediate_distance = ? WHERE viloyatlar_id = (?)"""
        self.manager(sql, intermediate_distance, commit=True)

    def insert_into_county(self, viloyat_nomi):
        sql = """INSERT INTO viloyatlar (viloyat_nomi) VALUES (?)"""
        self.manager(sql, viloyat_nomi, commit=True)

    def delete_county(self, viloyat_nomi):
        sql = """DELETE FROM viloyatlar WHERE viloyat_nomi = ?"""
        self.manager(sql, viloyat_nomi, commit=True)


    def select_county(self):
        sql = """SELECT viloyat_nomi FROM viloyatlar
                order by viloyat_nomi
            """
        return self.manager(sql, fetchall=True)

# ------------------------- Mashina haydovchisi ------------------------------------------
    def create_table_driver(self):
        sql = """CREATE TABLE IF NOT EXISTS driver(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            driver_id_number INTEGER,
            driver_name VARCHAR(50),
            telegram_user_id INTEGER DEFAULT 7859350476)"""
        self.manager(sql, commit=True)

    def update_table_driver(self, telegram_user_id, driver_id_number):
        sql = """UPDATE driver SET user_id = ? WHERE driver_id_number = ?"""
        self.manager(sql, telegram_user_id, driver_id_number, commit=True)

    def delete_table_driver(self, driver_id_number):
        sql = """DELETE FROM driver WHERE driver_id_number = ?"""
        self.manager(sql, driver_id_number, commit=True)

    def insert_into_driver(self, driver_id_number, driver_name):
        sql = """INSERT INTO driver (driver_id_number, driver_name) VALUES (?, ?)"""
        self.manager(sql, driver_id_number, driver_name, commit=True)

    def select_driver(self):
        sql = """SELECT driver_id_number, driver_name FROM driver
              order by driver_name"""
        return self.manager(sql, fetchall=True)

    def select_driver_user_id(self, driver_id_number):
        sql = """SELECT user_id FROM driver WHERE driver_id_number = ? LIMIT 1"""
        return self.manager(sql, driver_id_number, fetchone=True)

    def select_driver_name(self, driver_id_number):
        sql = """SELECT driver_name FROM driver WHERE driver_id_number = ? LIMIT 1"""
        return self.manager(sql, driver_id_number, fetchone=True)

    def select_all_driver_id(self):
        sql = """SELECT driver_id_number FROM driver"""
        res = self.manager(sql, fetchall=True)
        return res

# ------------------------- Yoqilgi astatka ------------------------------------------
    def create_table_fuel_info(self):
        sql = """CREATE TABLE IF NOT EXISTS fuel_info(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            out_or_in integer,
            user_id_sender INTEGER,
            data TEXT,
            machine_number TEXT  references machine(machine_number) ON DELETE set null,
            county_name TEXT  references county(county_name) ON DELETE set null,
            driver_name TEXT  references driver(driver_name) ON DELETE set null,
            fuel_liters INTEGER,
            walking_distance INTEGER,
            created_at TEXT,
            user_id_receiver INTEGER,
            is_active INTEGER,
            description text DEFAULT  NULL,
            receiver_at TEXT)
        """
        self.manager(sql, commit=True)

    def fuel_output_row_id(self):
        sql = "INSERT INTO fuel_info DEFAULT VALUES"

        fuel_info_id = self.manager(sql, commit=True, lastrowid=True)
        return fuel_info_id


    def delete_table_fuel_output(self):
        sql = """DROP TABLE IF EXISTS fuel_info"""
        self.manager(sql, commit=True)

    def delete_table_fuel_info(self):
        sql = """DELETE FROM fuel_info"""
        self.manager(sql, commit=True)

    def update_table_fuel_output(self, out_or_in, user_id_sender, data, machine_number, county_name, driver_name, fuel_liters, walking_distance, created_at, row_id):
        sql = """UPDATE fuel_info SET out_or_in = ?, user_id_sender = ?, data = ?, machine_number = ?, county_name = ?, driver_name = ?, fuel_liters = ?, walking_distance = ?, created_at = ? WHERE id = ?"""
        self.manager(sql, out_or_in , user_id_sender, data, machine_number, county_name, driver_name, fuel_liters, walking_distance, created_at, row_id, commit=True)

    def nsert_into_fuel_output(self, user_id_sender, data, machine_number):
        sql = """INSERT INTO fuel_info (user_id_sender, data, machine_number) VALUES (?, ?, ?)"""
        self.manager(sql, user_id_sender, data, machine_number, commit=True)

    def update_table_fuel_output_driver(self, user_id_receiver, is_active, description, receiver_at, row_id):
        sql = """UPDATE fuel_info SET user_id_receiver = ?, is_active = ?, description = ?, receiver_at = ? WHERE id = ?"""
        self.manager(sql, user_id_receiver, is_active, description, receiver_at, row_id, commit=True)

    def select_fuel_output_all_data(self, data):
        sql = """Select * FROM fuel_info WHERE data = (?)"""
        return self.manager(sql, data, fetchall=True)

    def select_fuel_output_machine_distance(self, machine_number):
        sql = """SELECT walking_distance FROM fuel_info WHERE machine_number = (?)
            order by walking_distance desc
            limit 1"""
        return self.manager(sql, machine_number, fetchone=True)

    # ------------------------- adminlar royxati ------------------------------------------
    def admins(self):
        sql = """CREATE TABLE IF NOT EXISTS admins (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    telegram_id INTEGER NOT NULL,
                    username TEXT NOT NULL
                 )"""
        self.manager(sql, commit=True)

    def insert_admin(self, telegram_id, username):
        sql = """INSERT INTO admins (telegram_id, username) VALUES (?, ?)"""
        self.manager(sql, telegram_id, username, commit=True)

    def delete_admin(self, telegram_id):
        sql = """DELETE FROM admins WHERE telegram_id = (?)"""
        self.manager(sql, telegram_id, commit=True)

    def select_all_admins(self):
        sql = """SELECT telegram_id, username FROM admins"""
        res = self.manager(sql, fetchall=True)
        admins = []
        for admin_id in res:
            admins.append(admin_id[0])
        return admins

    # ------------------------- menegerlar royxati ------------------------------------------
    def tgmenegers(self):
        sql = """CREATE TABLE IF NOT EXISTS menegers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    telegram_id INTEGER NOT NULL,
                    username TEXT NOT NULL
                 )"""
        self.manager(sql, commit=True)

    def insert_meneger(self, telegram_id, username):
        sql = """INSERT INTO menegers (telegram_id, username) VALUES (?, ?)"""
        self.manager(sql, telegram_id, username, commit=True)

    def delete_meneger(self, telegram_id):
        sql = """DELETE FROM menegers WHERE telegram_id = (?)"""
        self.manager(sql, telegram_id, commit=True)

    def select_all_menegers(self):
        sql = """SELECT telegram_id FROM menegers"""
        res = self.manager(sql, fetchall=True)
        managers = []
        for manager_id in res:
            managers.append(manager_id[0])
        return managers
