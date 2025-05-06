from extensions import db

class Payment(db.Model):
    __tablename__ = 'payment'

    id = db.Column(db.Integer, primary_key=True)
    purchase_id = db.Column(db.Integer, db.ForeignKey('purchase.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)
    payment_status = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<Payment ${self.amount} via {self.payment_method} - {self.payment_status}>"
