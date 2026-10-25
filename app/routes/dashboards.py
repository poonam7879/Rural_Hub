from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app.models import ScrapItem, Bid, Service, ServiceBooking, BarterItem
from app import db
from app.utils import role_required

dashboards = Blueprint('dashboards', __name__)

@dashboards.route('/')
@login_required
def index():
    if current_user.role == 'admin':
        return redirect(url_for('admin.index'))
    elif current_user.role == 'dealer':
        return render_template('dashboards/dealer.html')
    elif current_user.role == 'service_provider':
        return render_template('dashboards/provider.html')
    else:
        # Default user
        scrap_listings = ScrapItem.query.filter_by(user_id=current_user.id).all()
        service_bookings = ServiceBooking.query.filter_by(customer_id=current_user.id).all()
        barter_listings = BarterItem.query.filter_by(user_id=current_user.id).all()
        return render_template('dashboards/user.html', 
                               scrap_listings=scrap_listings,
                               service_bookings=service_bookings,
                               barter_listings=barter_listings)

# Dealer Dashboard Data Endpoint
@dashboards.route('/dealer-data')
@login_required
@role_required('dealer')
def dealer_data():
    my_bids = Bid.query.filter_by(dealer_id=current_user.id).all()
    won_bids = [bid for bid in my_bids if bid.status == 'accepted']
    return render_template('dashboards/partials/_dealer_bids.html', my_bids=my_bids, won_bids=won_bids)

# Provider Dashboard Data Endpoint
@dashboards.route('/provider-data')
@login_required
@role_required('service_provider')
def provider_data():
    my_services = Service.query.filter_by(provider_id=current_user.id).all()
    
    # Get all bookings for this provider's services
    service_ids = [s.id for s in my_services]
    bookings = ServiceBooking.query.filter(ServiceBooking.service_id.in_(service_ids)).all() if service_ids else []
    
    return render_template('dashboards/partials/_provider_data.html', my_services=my_services, bookings=bookings)

@dashboards.route('/booking/<int:booking_id>/update', methods=['POST'])
@login_required
@role_required('service_provider')
def update_booking(booking_id):
    booking = ServiceBooking.query.get_or_404(booking_id)
    if booking.service.provider_id != current_user.id:
        flash('Unauthorized action.', 'danger')
        return redirect(url_for('dashboards.index'))
        
    status = request.form.get('status')
    if status in ['accepted', 'rejected', 'completed', 'cancelled']:
        booking.status = status
        db.session.commit()
        flash('Booking status updated.', 'success')
    else:
        flash('Invalid status.', 'danger')
        
    return redirect(url_for('dashboards.index'))
