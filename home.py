import tkinter as tk
from tkinter import ttk

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        # عنوان الصفحة
        label = ttk.Label(self, text="Flight Reservation System", font=("Arial", 24))
        label.pack(pady=20, padx=20)
        
        # إطار للأزرار
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=20)
        
        # زر حجز رحلة
        booking_button = ttk.Button(
            button_frame, 
            text="Book Flight", 
            command=lambda: controller.show_frame("BookingPage")
        )
        booking_button.pack(pady=10, padx=10, fill=tk.X)
        
        # زر عرض الحجوزات
        reservations_button = ttk.Button(
            button_frame, 
            text="View Reservations", 
            command=lambda: controller.show_frame("ReservationsPage")
        )
        reservations_button.pack(pady=10, padx=10, fill=tk.X)
        
        # زر الخروج
        exit_button = ttk.Button(
            button_frame, 
            text="Exit", 
            command=controller.quit
        )
        exit_button.pack(pady=10, padx=10, fill=tk.X)