import sqlite3


class DataBasa:
    def __init__(self, db_name = 'main.db'):
        self.db_name = db_name


    def manager(self, sql, *args, commit: bool = False, fetchall: bool = False, fetchone: bool = False, many: bool = False, lastrowid: bool = False):
        with sqlite3.connect(self.db_name) as db:
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


    def select_avto_tigach(self):
        sql = """SELECT Auto_num, rusum FROM avto_tigach
              order by auto_num
              """
        return self.manager(sql, fetchall=True)

# ------------------------- Viloyatlar ------------------------------------------
    def create_table_county(self):
        sql = """CREATE TABLE IF NOT EXISTS viloyatlar(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            viloyat_nomi VARCHAR(50))
        """
        self.manager(sql, commit=True)
    # def alter_table_county(self):
    #     sql = """ALTER TABLE viloyatlar ADD COLUMN intermediate_distance INTEGER default 50"""
    #     self.manager(sql, commit=True)

    def insert_into_distance(self, intermediate_distance):
        sql = """UPDATE viloyatlar SET intermediate_distance = ? WHERE viloyatlar_id = (?)"""
        self.manager(sql, intermediate_distance, commit=True)

    def insert_into_county(self, viloyat_nomi):
        sql = """INSERT INTO viloyatlar (viloyat_nomi) VALUES (?)"""
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
            driver_id_number INTEGER NOT NULL,
            driver_name VARCHAR(50) NOT NULL)"""
        self.manager(sql, commit=True)

    # def alter_table_driver(self):
    #     sql = """ALTER TABLE driver ADD COLUMN user_id INTEGER default 7859350476"""
    #     self.manager(sql, commit=True)
    #
    def update_table_driver(self, user_id, driver_id_number):
        sql = """UPDATE driver SET user_id = ? WHERE driver_id_number = ?"""
        self.manager(sql, user_id, driver_id_number, commit=True)

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

# ------------------------- Yoqilgi astatka ------------------------------------------
    def create_table_fuel_output(self):
        sql = """CREATE TABLE IF NOT EXISTS fuel_output(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id_sender INTEGER,
            data TEXT,
            machine_number TEXT  references machine(machine_number),
            county_name TEXT  references county(county_name),
            driver_name TEXT  references driver(driver_name),
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
        sql = "INSERT INTO fuel_output DEFAULT VALUES"

        fuel_output_id = self.manager(sql, commit=True, lastrowid=True)
        return fuel_output_id


    def delete_table_fuel_output(self):
        sql = """DROP TABLE IF EXISTS fuel_output"""
        self.manager(sql, commit=True)

    def update_table_fuel_output(self, user_id_sender, data, machine_number, county_name, driver_name, fuel_liters, walking_distance, created_at, row_id):
        sql = """UPDATE fuel_output SET user_id_sender = ?, data = ?, machine_number = ?, county_name = ?, driver_name = ?, fuel_liters = ?, walking_distance = ?, created_at = ? WHERE id = ?"""
        self.manager(sql, user_id_sender, data, machine_number, county_name, driver_name, fuel_liters, walking_distance, created_at, row_id, commit=True)

    def nsert_into_fuel_output(self, user_id_sender, data, machine_number):
        sql = """INSERT INTO fuel_output (user_id_sender, data, machine_number) VALUES (?, ?, ?)"""
        self.manager(sql, user_id_sender, data, machine_number, commit=True)

    def update_table_fuel_output_driver(self, user_id_receiver, is_active, description, receiver_at, row_id):
        sql = """UPDATE fuel_output SET user_id_receiver = ?, is_active = ?, description = ?, receiver_at = ? WHERE id = ?"""
        self.manager(sql, user_id_receiver, is_active, description, receiver_at, row_id, commit=True)

    def select_fuel_output_all_data(self, data):
        sql = """Select * FROM fuel_output WHERE data = (?)"""
        return self.manager(sql, data, fetchall=True)

    def select_fuel_output_machine_distance(self, machine_number):
        sql = """SELECT walking_distance FROM fuel_output WHERE machine_number = (?)
            order by walking_distance desc
            limit 1"""
        return self.manager(sql, machine_number, fetchone=True)