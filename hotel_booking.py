import tkinter as tk
from tkinter import messagebox, Toplevel, Label
import mysql.connector
import qrcode
from PIL import ImageTk, Image
from io import BytesIO
from datetime import datetime

# Fungsi menampilkan QR di popup
def tampilkan_qr(qr_img, judul):
    top = Toplevel()
    top.title(judul)
    qr_photo = ImageTk.PhotoImage(qr_img)
    label = Label(top, image=qr_photo)
    label.image = qr_photo
    label.pack()

# Fungsi simpan data
def simpan_data():
    nama = entry_nama.get()
    no_hp = entry_hp.get()
    jumlah_kamar = entry_jumlah.get()
    tipe_kamar = var_tipe.get()
    checkin = entry_checkin.get()
    checkout = entry_checkout.get()

    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  # default password XAMPP
            database="hotel_db"
        )
        cursor = conn.cursor()
        sql = "INSERT INTO pemesanan (nama, no_hp, jumlah_kamar, tipe_kamar, tgl_checkin, tgl_checkout) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (nama, no_hp, jumlah_kamar, tipe_kamar, checkin, checkout)
        cursor.execute(sql, val)
        conn.commit()

        # Ambil ID terakhir
        id_booking = cursor.lastrowid

        # QR Code untuk Pembayaran
        qr_data_pembayaran = f"BOOKING#{id_booking}|NAMA:{nama}|TIPE:{tipe_kamar}|TOTAL:{int(jumlah_kamar)*300000}"
        img_pembayaran = qrcode.make(qr_data_pembayaran)

        # QR Code untuk Akses Pintu
        qr_data_akses = f"AKSES-KAMAR|NAMA:{nama}|TIPE:{tipe_kamar}|CHECKIN:{checkin}"
        img_akses = qrcode.make(qr_data_akses)

        # Tampilkan hasil
        messagebox.showinfo("Berhasil", f"Data berhasil disimpan.\nID Booking: {id_booking}")
        tampilkan_qr(img_pembayaran, "QR Pembayaran")
        tampilkan_qr(img_akses, "QR Akses Kamar")

    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Terjadi kesalahan: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# GUI Tkinter
root = tk.Tk()
root.title("Aplikasi Pemesanan Hotel")
root.geometry("400x420")

tk.Label(root, text="Nama Lengkap").pack()
entry_nama = tk.Entry(root)
entry_nama.pack()

tk.Label(root, text="No HP").pack()
entry_hp = tk.Entry(root)
entry_hp.pack()

tk.Label(root, text="Jumlah Kamar").pack()
entry_jumlah = tk.Entry(root)
entry_jumlah.pack()

tk.Label(root, text="Tipe Kamar").pack()
var_tipe = tk.StringVar()
var_tipe.set("Standard")
tk.OptionMenu(root, var_tipe, "Standard", "Deluxe", "Suite").pack()

tk.Label(root, text="Tanggal Check-in (YYYY-MM-DD)").pack()
entry_checkin = tk.Entry(root)
entry_checkin.pack()

tk.Label(root, text="Tanggal Check-out (YYYY-MM-DD)").pack()
entry_checkout = tk.Entry(root)
entry_checkout.pack()

tk.Button(root, text="Simpan", command=simpan_data, bg="green", fg="white").pack(pady=10)

root.mainloop()
