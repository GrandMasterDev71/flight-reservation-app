import tkinter as tk
from tkinter import ttk, messagebox
import database as db

class EditReservationPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        # عنوان الصفحة
        label = ttk.Label(self, text="Edit Reservation", font=("Arial", 20))
        label.pack(pady=10, padx=10)
        
        # إطار النموذج
        form_frame = ttk.Frame(self)
        form_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        # معرف الحجز (للقراءة فقط)
        ttk.Label(form_frame, text="Reservation ID:").grid(row=0, column=0, sticky=tk.W, pady=5, padx=5)
        self.id_label = ttk.Label(form_frame, text="")
        self.id_label.grid(row=0, column=1, sticky=tk.W, pady=5, padx=5)
        
        # حقول الإدخال
        # الاسم
        ttk.Label(form_frame, text="Passenger Name:").grid(row=1, column=0, sticky=tk.W, pady=5, padx=5)
        self.name_entry = ttk.Entry(form_frame)
        self.name_entry.grid(row=1, column=1, sticky=tk.EW, pady=5, padx=5)
        
        # رقم الرحلة
        ttk.Label(form_frame, text="Flight Number:").grid(row=2, column=0, sticky=tk.W, pady=5, padx=5)
        self.flight_number_entry = ttk.Entry(form_frame)
        self.flight_number_entry.grid(row=2, column=1, sticky=tk.EW, pady=5, padx=5)
        
        # المغادرة
        ttk.Label(form_frame, text="Departure:").grid(row=3, column=0, sticky=tk.W, pady=5, padx=5)
        self.departure_entry = ttk.Entry(form_frame)
        self.departure_entry.grid(row=3, column=1, sticky=tk.EW, pady=5, padx=5)
        
        # الوجهة
        ttk.Label(form_frame, text="Destination:").grid(row=4, column=0, sticky=tk.W, pady=5, padx=5)
        self.destination_entry = ttk.Entry(form_frame)
        self.destination_entry.grid(row=4, column=1, sticky=tk.EW, pady=5, padx=5)
        
        # التاريخ
        ttk.Label(form_frame, text="Date (YYYY-MM-DD):").grid(row=5, column=0, sticky=tk.W, pady=5, padx=5)
        self.date_entry = ttk.Entry(form_frame)
        self.date_entry.grid(row=5, column=1, sticky=tk.EW, pady=5, padx=5)
        
        # رقم المقعد
        ttk.Label(form_frame, text="Seat Number:").grid(row=6, column=0, sticky=tk.W, pady=5, padx=5)
        self.seat_number_entry = ttk.Entry(form_frame)
        self.seat_number_entry.grid(row=6, column=1, sticky=tk.EW, pady=5, padx=5)
        
        # إطار الأزرار
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=10)
        
        # زر التحديث
        update_button = ttk.Button(
            button_frame, 
            text="Update Reservation", 
            command=self.update_reservation
        )
        update_button.pack(side=tk.LEFT, padx=5)
        
        # زر الحذف
        delete_button = ttk.Button(
            button_frame, 
            text="Delete Reservation", 
            command=self.delete_reservation
        )
        delete_button.pack(side=tk.LEFT, padx=5)
        
        # زر العودة
        back_button = ttk.Button(
            button_frame, 
            text="Back to Reservations", 
            command=lambda: controller.show_frame("ReservationsPage")
        )
        back_button.pack(side=tk.LEFT, padx=5)
        
        # تخزين مرجع وحدة التحكم
        self.controller = controller
        
        # تكوين الأعمدة للتوسعة
        form_frame.columnconfigure(1, weight=1)
    
    def load_reservation(self, reservation_id):
        """تحميل بيانات الحجز للتعديل"""
        conn = self.controller.get_conn()
        reservation = db.select_reservation_by_id(conn, reservation_id)
        
        if reservation:
            # تعيين معرف الحجز
            self.id_label.config(text=str(reservation[0]))
            
            # تعيين القيم في حقول الإدخال
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, reservation[1])
            
            self.flight_number_entry.delete(0, tk.END)
            self.flight_number_entry.insert(0, reservation[2])
            
            self.departure_entry.delete(0, tk.END)
            self.departure_entry.insert(0, reservation[3])
            
            self.destination_entry.delete(0, tk.END)
            self.destination_entry.insert(0, reservation[4])
            
            self.date_entry.delete(0, tk.END)
            self.date_entry.insert(0, reservation[5])
            
            self.seat_number_entry.delete(0, tk.END)
            self.seat_number_entry.insert(0, reservation[6])
        else:
            messagebox.showerror("Error", "Reservation not found")
            self.controller.show_frame("ReservationsPage")
    
    def update_reservation(self):
        """تحديث بيانات الحجز في قاعدة البيانات"""
        # الحصول على معرف الحجز
        reservation_id = self.id_label.cget("text")
        
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
        
        # تحديث الحجز في قاعدة البيانات
        conn = self.controller.get_conn()
        reservation = (name, flight_number, departure, destination, date, seat_number, reservation_id)
        db.update_reservation(conn, reservation)
        
        messagebox.showinfo("Success", "Reservation updated successfully")
        self.controller.show_frame("ReservationsPage")
    
    def delete_reservation(self):
        """حذف الحجز الحالي"""
        # الحصول على معرف الحجز
        reservation_id = self.id_label.cget("text")
        
        # تأكيد الحذف
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this reservation?"):
            # حذف الحجز من قاعدة البيانات
            conn = self.controller.get_conn()
            db.delete_reservation(conn, reservation_id)
            
            messagebox.showinfo("Success", "Reservation deleted successfully")
            self.controller.show_frame("ReservationsPage")