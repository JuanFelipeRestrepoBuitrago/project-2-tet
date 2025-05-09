from flask import Blueprint, render_template, request, redirect, url_for, session, current_app, flash
from utils.utils import check_user_auth
import requests

delivery = Blueprint('delivery', __name__)

@delivery.route('/delivery/<int:purchase_id>', methods=['GET', 'POST'])
def select_delivery(purchase_id):
    """
    Render delivery provider selection form and handle assignment.
    """
    user = check_user_auth(session.get('token'))
    if not user:
        return redirect(url_for('auth.login'))
    response = requests.get(
        f'{current_app.config["PURCHASE_SERVICE_URL"]}/delivery/providers',
    )
    if not response.ok:
        flash('Error fetching delivery providers' + str(response.json()), 'error')
        return redirect(url_for('book.catalog'))
    providers = response.json()
    
    if request.method == 'POST':
        selected_provider_id = request.form.get('provider')
        
        response = requests.post(
            f'{current_app.config["PURCHASE_SERVICE_URL"]}/delivery/assignment',
            json={
                'purchase_id': purchase_id,
                'selected_provider_id': selected_provider_id
            }
        )
        
        if not response.ok:
            flash('Error assigning delivery provider' + str(response.json()), 'error')
            return redirect(url_for('book.catalog'))

        return redirect(url_for('book.catalog'))

    return render_template('delivery_options.html', providers=providers, purchase_id=purchase_id, my_user=user)
