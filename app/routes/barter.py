from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app.models import BarterItem
from app import db
from app.utils import upload_image

barter = Blueprint('barter', __name__)

@barter.route('/')
def index():
    query = request.args.get('q')
    if query:
        items = BarterItem.query.filter(
            (BarterItem.title.ilike(f'%{query}%')) | 
            (BarterItem.desired_item.ilike(f'%{query}%'))
        ).filter_by(status='active').order_by(BarterItem.created_at.desc()).all()
    else:
        items = BarterItem.query.filter_by(status='active').order_by(BarterItem.created_at.desc()).all()
        
    return render_template('barter/index.html', items=items)

@barter.route('/<int:item_id>')
def details(item_id):
    item = BarterItem.query.get_or_404(item_id)
    return render_template('barter/details.html', item=item)

@barter.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        desired_item = request.form.get('desired_item')
        location = request.form.get('location')
        image = request.files.get('image')
        
        if not all([title, description, desired_item, location]):
            flash('All fields are required.', 'danger')
            return redirect(url_for('barter.add'))
            
        image_url = None
        if image and image.filename != '':
            image_url = upload_image(image)
            if not image_url:
                flash('Image upload failed. Please try a valid image file.', 'danger')
                return redirect(url_for('barter.add'))
                
        new_item = BarterItem(
            user_id=current_user.id,
            title=title,
            description=description,
            desired_item=desired_item,
            location=location,
            image_url=image_url
        )
        
        db.session.add(new_item)
        db.session.commit()
        
        flash('Barter item listed successfully!', 'success')
        return redirect(url_for('barter.details', item_id=new_item.id))
        
    return render_template('barter/add.html')
