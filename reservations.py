import tkinter as tk
from tkinter import ttk, messagebox
import database as db

class ReservationsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        # عنوان الصفحة
        label = ttk.Label(self, text="Flight Reservations", font=("Arial", 20))
        label.pack(pady=10, padx=10)
        
        # إطار الجدول
        table_frame = ttk.Frame(self)
        table_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        # إنشاء Treeview لعرض البيانات
        self.tree = ttk.Treeview(table_frame, columns=("ID", "Name", "Flight Number", "Departure", "Destination", "Date", "Seat Number"), show="headings")
        
        # تعيين عناوين الأعمدة
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Passenger Name")
        self.tree.heading("Flight Number", text="Flight Number")
        self.tree.heading("Departure", text="Departure")
        self.tree.heading("Destination", text="Destination")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Seat Number", text="Seat Number")
        
        # إعداد أبعاد الأعمدة
        self.tree.column("ID", width=40)
        self.tree.column("Name", width=150)
        self.tree.column("Flight Number", width=100)
        self.tree.column("Departure", width=100)
        self.tree.column("Destination", width=100)
        self.tree.column("Date", width=100)
        self.tree.column("Seat Number", width=100)
        
        # إضافة شريط تمرير
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # إطار الأزرار
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=10)
        
        # زر التعديل
        edit_button = ttk.Button(
            button_frame, 
            text="Edit Selected", 
            command=self.edit_reservation
        )
        edit_button.pack(side=tk.LEFT, padx=5)
        
        # زر الحذف
        delete_button = ttk.Button(
            button_frame, 
            text="Delete Selected", 
            command=self.delete_reservation
        )
        delete_button.pack(side=tk.LEFT, padx=5)
        
        # زر التحديث
        refresh_button = ttk.Button(
            button_frame, 
            text="Refresh List", 
            command=self.refresh_list
        )
        refresh_button.pack(side=tk.LEFT, padx=5)
        
        # زر العودة
        back_button = ttk.Button(
            button_frame, 
            text="Back to Home", 
            command=lambda: controller.show_frame("HomePage")
        )
        back_button.pack(side=tk.LEFT, padx=5)
        
        # تخزين مرجع وحدة التحكم
        self.controller = controller
        
        # تحميل البيانات عند بدء التشغيل
        self.refresh_list()
    
    def refresh_list(self):
        """تحديث قائمة الحجوزات"""
        # مسح البيانات الحالية
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # الحصول على البيانات من قاعدة البيانات
        conn = self.controller.get_conn()
        reservations = db.select_all_reservations(conn)
        
        # إضافة البيانات إلى الجدول
        for reservation in reservations:
            self.tree.insert("", tk.END, values=reservation)
    
    def edit_reservation(self):
        """تعديل الحجز المحدد"""
        # الحصول على العنصر المحدد
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a reservation to edit")
            return
        
        # الحصول على معرف الحجز
        reservation_id = self.tree.item(selected_item, "values")[0]
        
        # الانتقال إلى صفحة التعديل مع تمرير معرف الحجز
        self.controller.show_frame("EditReservationPage")
        # تمرير معرف الحجز إلى صفحة التعديل
        self.controller.frames["EditReservationPage"].load_reservation(reservation_id)
    
    def delete_reservation(self):
        """حذف الحجز المحدد"""
        # الحصول على العنصر المحدد
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a reservation to delete")
            return
        
        # الحصول على معرف الحجز
        reservation_id = self.tree.item(selected_item, "values")[0]
        
        # تأكيد الحذف
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this reservation?"):
            # حذف الحجز من قاعدة البيانات
            conn = self.controller.get_conn()
            db.delete_reservation(conn, reservation_id)
            
            # تحديث القائمة
            self.refresh_list()
            
            messagebox.showinfo("Success", "Reservation deleted successfully")