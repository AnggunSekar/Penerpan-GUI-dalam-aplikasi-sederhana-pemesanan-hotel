from flask import Flask, render_template, request
import mysql.connector
import qrcode
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'static/qrcodes'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    id_booking = None
    if request.method == "POST":
        nama = request.form["nama"]
        no_hp = request.form["no_hp"]
        jumlah_kamar = int(request.form["jumlah_kamar"])
        tipe_kamar = request.form["tipe_kamar"]
        checkin = request.form["checkin"]
        checkout = request.form["checkout"]

        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="hotel_db"
            )
            cursor = conn.cursor()
            sql = "INSERT INTO pemesanan (nama, no_hp, jumlah_kamar, tipe_kamar, tgl_checkin, tgl_checkout) VALUES (%s, %s, %s, %s, %s, %s)"
            val = (nama, no_hp, jumlah_kamar, tipe_kamar, checkin, checkout)
            cursor.execute(sql, val)
            conn.commit()
            id_booking = cursor.lastrowid

            # QR untuk pembayaran
            qr_data_pembayaran = f"BOOKING#{id_booking}|NAMA:{nama}|TIPE:{tipe_kamar}|TOTAL:{jumlah_kamar * 300000}"
            img_pembayaran = qrcode.make(qr_data_pembayaran)
            img_pembayaran.save(os.path.join(UPLOAD_FOLDER, f'payment_{id_booking}.png'))

            # QR untuk akses kamar
            qr_data_akses = f"AKSES-KAMAR|NAMA:{nama}|TIPE:{tipe_kamar}|CHECKIN:{checkin}"
            img_akses = qrcode.make(qr_data_akses)
            img_akses.save(os.path.join(UPLOAD_FOLDER, f'access_{id_booking}.png'))

        except mysql.connector.Error as err:
            return f"Gagal: {err}"
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    return render_template("index.html", id_booking=id_booking)

if __name__ == "__main__":
    app.run(debug=True)
