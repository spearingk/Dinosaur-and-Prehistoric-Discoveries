from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.discovery import Discovery
from flask_app.models.user import User

# dashboard
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect ('/logout')
    user = User.check_id({'id': session['user_id']})
    if not user:
        return redirect('/logout')
    data = {
        'id': session['user_id']
    }
    return render_template('dashboard.html', user= User.check_id(data), discoveries = Discovery.get_all(data))

# create discovery
@app.route('/discovery/new')
def create_discovery_form():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['user_id']
    }
    return render_template('new_discovery.html', user= User.check_id(data))

@app.route('/discovery/create', methods = ['POST'])
def create_discovery():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Discovery.validate_discovery_form(request.form):
        return redirect('/discovery/new')
    
    data = {
        'user_id': session['user_id'], 
        'discovery_name': request.form['discovery_name'],
        'discovery_location': request.form['discovery_location'],
        'discovery_date': request.form['discovery_date'],
        'discovery_details': request.form['discovery_details']
    }

    Discovery.create_discovery(data)
    return redirect('/dashboard')


# disovery details
@app.route('/discovery/<int:id>')
def discovery_details_page(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['user_id']
    }
    return render_template('discovery_details.html', user= User.check_id(data), discovery = Discovery.get_one_by_id({'id': id}))


# edit discovery
@app.route('/discovery/edit/<int:id>')
def edit_discovery_form(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['user_id']
    }
    return render_template('edit_discovery.html', user= User.check_id(data), discovery = Discovery.get_one_by_id({'id': id}))

@app.route('/discovery/update/<int:id>', methods = ['POST'])
def edit_discovery(id):
    if 'user_id' not in session:
        return redirect('/logout')
    if not Discovery.validate_discovery_form(request.form):
        return redirect(f'/discovery/edit/{id}')
    
    data = {
        'id': id, 
        'discovery_name': request.form['discovery_name'],
        'discovery_location': request.form['discovery_location'],
        'discovery_date': request.form['discovery_date'],
        'discovery_details': request.form['discovery_details']
    }

    Discovery.edit_discovery(data)
    return redirect('/dashboard')


# delete discovery
@app.route('/discovery/delete/<int:id>')
def delete_discovery(id):
    if 'user_id' not in session:
        return redirect('/logout')

    Discovery.delete_discovery({'id': id})
    return redirect('/dashboard')


