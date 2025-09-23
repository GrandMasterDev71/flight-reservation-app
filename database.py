import sqlite3
from sqlite3 import Error

def create_connection():
    """ إنشاء اتصال بقاعدة بيانات SQLite """
    conn = None
    try:
        conn = sqlite3.connect('flights.db')
        return conn
    except Error as e:
        print(e)
    return conn

def create_table(conn):
    """ إنشاء جدول الحجوزات """
    try:
        sql_create_reservations_table = """ CREATE TABLE IF NOT EXISTS reservations (
                                            id integer PRIMARY KEY AUTOINCREMENT,
                                            name text NOT NULL,
                                            flight_number text NOT NULL,
                                            departure text NOT NULL,
                                            destination text NOT NULL,
                                            date text NOT NULL,
                                            seat_number text NOT NULL
                                        ); """
        cursor = conn.cursor()
        cursor.execute(sql_create_reservations_table)
    except Error as e:
        print(e)

def create_reservation(conn, reservation):
    """ إضافة حجز جديد """
    sql = ''' INSERT INTO reservations(name, flight_number, departure, destination, date, seat_number)
              VALUES(?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, reservation)
    conn.commit()
    return cur.lastrowid

def update_reservation(conn, reservation):
    """ تحديث حجز موجود """
    sql = ''' UPDATE reservations
              SET name = ? ,
                  flight_number = ? ,
                  departure = ? ,
                  destination = ? ,
                  date = ? ,
                  seat_number = ?
              WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, reservation)
    conn.commit()

def delete_reservation(conn, id):
    """ حذف حجز بالمعرف """
    sql = 'DELETE FROM reservations WHERE id=?'
    cur = conn.cursor()
    cur.execute(sql, (id,))
    conn.commit()

def select_all_reservations(conn):
    """ الاستعلام عن جميع الحجوزات """
    cur = conn.cursor()
    cur.execute("SELECT * FROM reservations")
    rows = cur.fetchall()
    return rows

def select_reservation_by_id(conn, id):
    """ الاستعلام عن حجز بالمعرف """
    cur = conn.cursor()
    cur.execute("SELECT * FROM reservations WHERE id=?", (id,))
    rows = cur.fetchall()
    return rows[0] if rows else None