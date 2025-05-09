from flask import Blueprint, request, jsonify

from models.delivery import DeliveryProvider
from models.delivery_assignment import DeliveryAssignment
from extensions import db

delivery = Blueprint('delivery', __name__)

@delivery.route('/delivery/assignment', methods=['POST'])
def select_delivery():
    """
    Render delivery provider selection form and handle assignment.
    """
    try: 
        data = request.get_json()
        purchase_id = data.get('purchase_id')
        selected_provider_id = data.get('selected_provider_id')

        assignment = DeliveryAssignment(
            purchase_id=purchase_id,
            provider_id=selected_provider_id
        )

        db.session.add(assignment)
        db.session.commit()

        return jsonify({
            'message': 'Delivery provider assigned successfully.',
            'assignment_id': assignment.id
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'message': 'Error assigning delivery provider.',
            'error': str(e)
        }), 500

@delivery.route('/delivery/providers', methods=['GET'])
def list_delivery_providers():
    """
    List all delivery providers.
    """    
    providers = DeliveryProvider.query.all()
    return jsonify([{
            'id': provider.id,
            'name': provider.name,
            'coverage_area': provider.coverage_area,
            'cost': provider.cost
        } for provider in providers])
