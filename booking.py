import tkinter as tk
from tkinter import ttk, messagebox
import database as db

class BookingPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        # عنوان الصفحة
        label = ttk.Label(self, text="Book a Flight", font=("Arial", 20))
        label.pack(pady=10, padx=10)
        
        # إطار النموذج
        form_frame = ttk.Frame(self)
        form_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        # حقول الإدخال
        # الاسم
        ttk.Label(form_frame, text="Passenger Name:").grid(row=0, column=0, sticky=tk.W, pady=5, padx=5)
        self.name_entry = ttk.Entry(form_frame)
        self.name_entry.grid(row=0, column=1, sticky=tk.EW, pady=5, padx=5)
        
        # رقم الرحلة
        ttk.Label(form_frame, text="Flight Number:").grid(row=1, column=0, sticky=tk.W, pady=5, padx=5)
        self.flight_number_entry = ttk.Entry(form_frame)
        self.flight_number_entry.grid(row=1, column=1, sticky=tk.EW, pady=5, padx=5)
        
        # المغادرة
        ttk.Label(form_frame, text="Departure:").grid(row=2, column=0, sticky=tk.W, pady=5, padx=5)
        self.departure_entry = ttk.Entry(form_frame)
        self.departure_entry.grid(row=2, column=1, sticky=tk.EW, pady=5, padx=5)
        
        # الوجهة
        ttk.Label(form_frame, text="Destination:").grid(row=3, column=0, sticky=tk.W, pady=5, padx=5)
        self.destination_entry = ttk.Entry(form_frame)
        self.destination_entry.grid(row=3, column=1, sticky=tk.EW, pady=5, padx=5)
        
        # التاريخ
        ttk.Label(form_frame, text="Date (YYYY-MM-DD):").grid(row=4, column=0, sticky=tk.W, pady=5, padx=5)
        self.date_entry = ttk.Entry(form_frame)
        self.date_entry.grid(row=4, column=1, sticky=tk.EW, pady=5, padx=5)
        
        # رقم المقعد
        ttk.Label(form_frame, text="Seat Number:").grid(row=5, column=0, sticky=tk.W, pady=5, padx=5)
        self.seat_number_entry = ttk.Entry(form_frame)
        self.seat_number_entry.grid(row=5, column=1, sticky=tk.EW, pady=5, padx=5)
        
        # إطار الأزرار
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=10)
        
        # زر الإرسال
        submit_button = ttk.Button(
            button_frame, 
            text="Submit Booking", 
            command=self.submit_booking
        )
        submit_button.pack(side=tk.LEFT, padx=5)
        
        # زر العودة
        back_button = ttk.Button(
            button_frame, 
            text="Back to Home", 
            command=lambda: controller.show_frame("HomePage")
        )
        back_button.pack(side=tk.LEFT, padx=5)
        
        # تخزين مرجع وحدة التحكم
        self.controller = controller
        
        # تكوين الأعمدة للتوسعة
        form_frame.columnconfigure(1, weight=1)
    
    def submit_booking(self):
        """إرسال بيانات الحجز إلى قاعدة البيانات"""
        # الحصول على البيانات من حقول الإدخال
        name = self.name_entry.get()
        flight_number = self.flight_number_entry.get()
        departure = self.departure_entry.get()
        destination = self.destination_entry.get()
        date = self.date_entry.get()
        seat_number = self.seat_number_entry.get()
        
        # التحقق من أن جميع الحقول ممتلئة
        if not all([name, flight_number, departure, destination, date, seat_number]):
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        # إنشاء الحجز في قاعدة البيانات
        conn = self.controller.get_conn()
        reservation = (name, flight_number, departure, destination, date, seat_number)
        reservation_id = db.create_reservation(conn, reservation)
        
        if reservation_id:
            messagebox.showinfo("Success", f"Booking successful! Your reservation ID is: {reservation_id}")
            # مسح حقول الإدخال
            self.name_entry.delete(0, tk.END)
            self.flight_number_entry.delete(0, tk.END)
            self.departure_entry.delete(0, tk.END)
            self.destination_entry.delete(0, tk.END)
            self.date_entry.delete(0, tk.END)
            self.seat_number_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Failed to create reservation")