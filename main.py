import tkinter as tk
from tkinter import ttk
import database as db
import home
import booking
import reservations
import edit_reservation

class FlightReservationApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # إعداد النافذة الرئيسية
        self.title("Flight Reservation App")
        self.geometry("800x600")
        self.resizable(False, False)
        
        # إنشاء اتصال بقاعدة البيانات
        self.conn = db.create_connection()
        if self.conn is not None:
            db.create_table(self.conn)
        else:
            print("Error! cannot create the database connection.")
        
        # إنشاء إطار للصفحات
        self.container = ttk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        # قاموس لتخزين الصفحات
        self.frames = {}
        
        # إنشاء الصفحات
        for F in (home.HomePage, booking.BookingPage, reservations.ReservationsPage, edit_reservation.EditReservationPage):
            frame = F(self.container, self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        # عرض الصفحة الرئيسية
        self.show_frame("HomePage")
    
    def show_frame(self, page_name):
        """عرض الصفحة المحددة"""
        frame = self.frames[page_name]
        frame.tkraise()
    
    def get_conn(self):
        """الحصول على اتصال قاعدة البيانات"""
        return self.conn

if __name__ == "__main__":
    app = FlightReservationApp()
    app.mainloop()