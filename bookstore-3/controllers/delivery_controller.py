from flask import Blueprint, render_template, request, redirect, url_for, session
from utils.utils import check_user_auth

from models.delivery import DeliveryProvider
from models.delivery_assignment import DeliveryAssignment
from extensions import db

delivery = Blueprint('delivery', __name__)

@delivery.route('/delivery/<int:purchase_id>', methods=['GET', 'POST'])
def select_delivery(purchase_id):
    """
    Render delivery provider selection form and handle assignment.
    """
    user = check_user_auth(session.get('token'))
    if not user:
        return redirect(url_for('auth.login'))
    providers = DeliveryProvider.query.all()

    if request.method == 'POST':
        selected_provider_id = request.form.get('provider')

        assignment = DeliveryAssignment(
            purchase_id=purchase_id,
            provider_id=selected_provider_id
        )

        db.session.add(assignment)
        db.session.commit()

        return redirect(url_for('book.catalog'))

    return render_template('delivery_options.html', providers=providers, purchase_id=purchase_id, my_user=user)
