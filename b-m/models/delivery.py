from extensions import db

class DeliveryProvider(db.Model):
    __tablename__ = 'delivery_provider'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    coverage_area = db.Column(db.String(150), nullable=False)
    cost = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<DeliveryProvider {self.name} (${self.cost})>"
