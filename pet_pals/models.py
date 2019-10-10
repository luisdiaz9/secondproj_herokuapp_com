from .app import db


class Pet(db.Model):
    __tablename__ = 'pets'

    id = db.Column(db.Integer, primary_key=True)
    no = db.Column(db.String(64))
    hora_salida = db.Column(db.String(64))
    origen = db.Column(db.String(64))
    destino = db.Column(db.String(64))
    hora_llegada = db.Column(db.String(64))
    desde = db.Column(db.Float)
    name = db.Column(db.String(64))
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)
    mxn = db.Column(db.Float)
    dmxn = db.Column(db.String(64))
    def __repr__(self):
        return '<Pet %r>' % (self.name)
