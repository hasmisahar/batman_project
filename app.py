from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
conn = 'sqlite:///gjy.db'
app.config['SQLALCHEMY_DATABASE_URI'] = conn
api = Api(app)
db = SQLAlchemy(app)

todos = {}


class Pegawai(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(50))
    alamat = db.Column(db.String(50))
    nomor_telepon = db.Column(db.String(20))
    gaji_borongan = db.Column(db.Integer)

    def serialize(self):
        return {
            'id': self.id,
            'nama': self.nama,
            'alamat': self.alamat,
            'nomor_telepon': self.nomor_telepon,
            'gaji_borongan': self.gaji_borongan
        }


class Produk(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(20))
    harga = db.Column(db.Integer)
    satuan = db.Column(db.String(20))

    def serialize(self):
        return {
            'id': self.id,
            'nama': self.nama,
            'harga': self.harga,
            'satuan': self.satuan
        }


class Stok(db.Model):
    id_stok = db.Column(db.Integer, primary_key=True)
    id_barang = db.Column(db.String(25))
    tanggal = db.Column(db.DateTime)
    Jam = db.Column(db.String(20))
    jumlah_stok = db.Column(db.Integer)

    def serialize(self):
        return {
            'id_stok': self.id_stok,
            'id_barang': self.id_barang,
            'tanggal': self.tanggal,
            'jam': self.Jam,
            'jumlah_stok': self.jumlah_stok
        }


class Orderan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tanggal = db.Column(db.DateTime)
    nama_customer = db.Column(db.String(25))
    alamat = db.Column(db.String(50))
    nomor_telepon = db.Column(db.String(20))
    produk = db.Column(db.String(25))
    jumlah = db.Column(db.Integer)
    satuan = db.Column(db.String(20))
    uang_muka = db.Column(db.Integer)
    total_bayar = db.Column(db.Integer)
    status_bayar = db.Column(db.String(25))
    status_kirim = db.Column(db.String(25))
    prioritas = db.Column(db.Integer)

    def serialize(self):
        return {
            'id': self.id,
            'tanggal': self.tanggal,
            'nama_customer': self.nama_customer,
            'alamat': self.alamat,
            'nomor_telepon': self.nomor_telepon,
            'produk': self.produk,
            'jumlah': self.jumlah,
            'satuan': self.satuan,
            'uang_muka': self.uang_muka,
            'total_bayar': self.total_bayar,
            'status_bayar': self.status_bayar,
            'status_kirim': self.status_kirim,
            'prioritas': self.prioritas
        }


class Gajian(db.Model):
    id_gaji = db.Column(db.Integer, primary_key=True)
    id_pegawai = db.Column(db.Integer)
    tanggal = db.Column(db.DateTime)
    hari = db.Column(db.String(75))
    id_barang = db.Column(db.Integer)
    jumlah_barang = db.Column(db.Integer)
    upah = db.Column(db.Integer)
    potongan_upah = db.Column(db.Integer)
    gaji = db.Column(db.Integer)

    def serialize(self):
        return {
            'id_gaji': self.id_gaji,
            'id_pegawai': self.id_pegawai,
            'tanggal': self.tanggal,
            'hari': self.hari,
            'id_barang': self.id_barang,
            'jumlah_barang': self.jumlah_barang,
            'upah': self.upah,
            'potongan_upah': self.potongan_upah,
            'gaji': self.gaji
        }


class Bon(db.Model):
    id_bon = db.Column(db.Integer, primary_key=True)
    id_pegawai = db.Column(db.Integer)
    tanggal = db.Column(db.DateTime)
    jumlah = db.Column(db.Integer)
    terbayar = db.Column(db.Integer)
    sisa = db.Column(db.Integer)
    status = db.Column(db.String(25))

    def serialize(self):
        return {
            'id_bon': self.id_bon,
            'id_pegawai': self.id_pegawai,
            'tanggal': self.tanggal,
            'jumlah': self.jumlah,
            'terbayar': self.terbayar,
            'sisa': self.sisa,
            'status': self.status
        }


parser = reqparse.RequestParser(bundle_errors=True)


class Daftar_Pegawai(Resource):
    def get(self):
        records = Pegawai.query.all()
        return jsonify([Pegawai.serialize(record) for record in records])

    def post(self):
        pegawai = Pegawai(
            nama=request.form['nama'],
            alamat=request.form['alamat'],
            nomor_telepon=request.form['nomor_telepon'],
            gaji_borongan=request.form['gaji_borongan']
        )
        db.session.add(pegawai)
        db.session.commit()


class Data_Pegawai(Resource):
    def get(self, id_pegawai):
        pegawai = Pegawai.query.filter_by(id=id_pegawai).first()
        return jsonify(
            Pegawai.serialize(pegawai)
        )

    def delete(self, id_pegawai):
        pegawai = Pegawai.query.filter_by(id=id_pegawai).first()
        db.session.delete(pegawai)
        db.session.commit()

    def put(self, id_pegawai):
        pegawai = Pegawai.query.filter_by(id=id_pegawai).first()
        pegawai.nama = request.form['nama']
        pegawai.alamat = request.form['alamat']
        pegawai.nomor_telepon = request.form['nomor_telepon']
        pegawai.gaji_borongan = request.form['gaji_borongan']
        db.session.commit()


class Daftar_Produk(Resource):
    def get(self):
        produks = Produk.query.all()
        return jsonify([Produk.serialize(produk) for produk in produks])

    def post(self):
        produk = Produk(
            nama=request.form['nama'],
            harga=request.form['harga'],
            satuan=request.form['satuan']
        )
        db.session.add(produk)
        db.session.commit()


class Data_Produk(Resource):
    def get(self, id_produk):
        produk = Produk.query.filter_by(id=id_produk).first()
        return jsonify(
            Produk.serialize(produk)
        )

    def delete(self, id_produk):
        produk = Produk.query.filter_by(id=id_produk).first()
        db.session.delete(produk)
        db.session.commit()

    def put(self, id_produk):
        produk = Produk.query.filter_by(id=id_produk).first()
        produk.nama = request.form['nama']
        produk.harga = request.form['harga']
        produk.satuan = request.form['satuan']
        db.session.commit()


class Daftar_Stok(Resource):
    def get(self):
        stoks = Stok.query.all()
        return jsonify(
            [Stok.serialize(stok) for stok in stoks]
        )

    def post(self):
        stok = Stok(
            id_barang=request.form['id_barang'],
            tanggal=request.form['tanggal'],
            jam=request.form['jam'],
            jumlah_stok=request.form['jumlah_stok']
        )
        db.session.add(stok)
        db.session.commit()


class Data_Stok(Resource):
    def get(self, id):
        stok = Stok.query.filter_by(id_stok=id).firrst()
        return jsonify(
            Stok.serialize(stok)
        )

    def delete(self, id):
        stok = Stok.query.filter_by(id_stok=id).first()
        db.session.delete(stok)
        db.session.commit()

    def put(self, id):
        stok = Stok.query.filter_by(id_stok=id).first()
        stok.tanggal = request.form['tanggal']
        stok.jam = request.form['jam']
        stok.jumlah_stok = request.form['jumlah_stok']
        db.session.commit()


class Daftar_Order(Resource):
    def get(self):
        Orders = Orderan.query.all()
        return jsonify(
            [Orderan.serialize(order) for order in Orders]
        )

    def post(self):
        order = Orderan(
            tanggal=request.form['tanggal'],
            nama_customer=request.form['nama_customer'],
            alamat=request.form['alamat'],
            nomor_telepon=request.form['nomor_telepon'],
            produk=request.form['produk'],
            jumlah=request.form['jumlah'],
            satuan=request.form['satuan'],
            uang_muka=request.form['uang_muka'],
            total_bayar=request.form['total_bayar'],
            status_bayar=request.form['status_bayar'],
            status_kirim=request.form['status_kirim'],
            prioritas=request.form['prioritas']
        )
        db.session.add(order)
        db.session.commit()


class Data_Order(Resource):
    def get(self, id_order):
        order = Orderan.query.filter_by(id=id_order).first()
        return jsonify(
            Orderan.serialize(order)
        )

    def delete(self, id_order):
        order = Orderan.query.filter_by(id=id_order).first()
        db.session.delete(order)
        db.session.commit()

    def put(self, id_order):
        order = Orderan.query.filter_by(id=id_order).first()
        order.tanggal = request.form['tanggal']
        order.nama_customer = request.form['nama_customer']
        order.alamat = request.form['alamat']
        order.nomor_telepon = request.form['nomor_telepon']
        order.produk = request.form['produk']
        order.jumlah = request.form['jumlah']
        order.satuan = request.form['satuan']
        order.uang_muka = request.form['uang_muka']
        order.total_bayar = request.form['total_bayar']
        order.status_bayar = request.form['status_bayar']
        order.status_kirim = request.form['status_kirim']
        order.prioritas = request.form['prioritas']
        db.session.commit()


# api.add_resource(index, '/')
api.add_resource(Daftar_Pegawai, '/pegawai')
api.add_resource(Data_Pegawai, '/pegawai/<id_pegawai>')
api.add_resource(Daftar_Stok, '/stok')
api.add_resource(Data_Stok, '/stok/<id>')
api.add_resource(Daftar_Produk, '/produk')
api.add_resource(Data_Produk, '/produk/<id_produk>')
api.add_resource(Daftar_Order, '/order')
api.add_resource(Data_Order, '/order/<id_order>')
# def index():
#    return render_template("index.html")

# def user(name):
#    return render_template("user.html", user_name=name)


if __name__ == "__main__":
    app.run()
