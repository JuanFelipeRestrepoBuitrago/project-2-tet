from extensions import db

class DeliveryAssignment(db.Model):
    __tablename__ = 'delivery_assignment'

    id = db.Column(db.Integer, primary_key=True)
    purchase_id = db.Column(db.Integer, db.ForeignKey('purchase.id'), nullable=False)
    provider_id = db.Column(db.Integer, db.ForeignKey('delivery_provider.id'), nullable=False)

    def __repr__(self):
        return f"<DeliveryAssignment purchase_id={self.purchase_id} provider_id={self.provider_id}>"
