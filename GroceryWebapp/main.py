from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import login_required, current_user
from . import db
from .models import Categories
from .models import Products
import json

main = Blueprint("main", __name__)


@main.route('/')
def base():
    return render_template("base.html")


@main.route('/user-home')
def userhome():

    return render_template("home_user.html")


@main.route('/admin-home<bool1>',methods=['GET', 'POST'])
def adminhome(bool1):
    bool_value = bool1.lower() in ['true', '1', 'yes']
    result = Categories.query.first()
    bool = False
    if result:
        bool = True
    else:
        bool = False
        if(bool_value == True):
            bool = True
    return render_template("home_admin.html", bool=bool)


# @main.route('/adminhomecategories', methods=['GET', 'POST'])
# def adminhomecategories():
#     if request.method == 'POST':
#         cat_name = request.form['category_name']

#         # Save the data to the Categories table
    # cname = Categories.query.filter_by(cat_name=cat_name).first()
    # if cname:  
    #     return redirect(url_for('main.adminhomecategories'))
#     new_cat = Categories(cat_name=cat_name)

#     db.session.add(new_cat)
#     db.session.commit()

#     # Query data from the Categories table
#     # data = Categories.query.filter_by(cat_name=cat_name).first()
#     # with app.app_context():
#     #     data = Categories.query.all()

#     return render_template("home_admin.html", bool=True,data=data )


@main.route('/adminhomecategories', methods=['GET', 'POST'])
def adminhomecategories():
    if request.method == 'POST':
        cat_name = request.form['category_name']
        if cat_name:
                cname = Categories.query.filter_by(cat_name=cat_name).first()
                if cname:  
                    return redirect(url_for('main.adminhome',bool1=False))
                new_cat = Categories(cat_name=cat_name)
                db.session.add(new_cat)
                db.session.commit()
    data = Categories.query.all()
    return render_template("home_admin.html", bool=True,data=data )

@main.route('/adminshowcategories', methods=['GET', 'POST'])
def adminshowcategories():
    data= Categories.query.all()
    return render_template("home_admin.html", bool=True,data=data,boolcat=True )      
    


@main.route("/Categoryupdate/<string:categories_id>", methods=['GET', 'POST'])
def update_category(categories_id):
    ncat = Categories.query.get_or_404(categories_id)
    if request.method == "POST":
        ncat.cat_name = request.form['ncategory']
        db.session.commit()
        flash('Your post has been updated!')
        return redirect(url_for('main.adminhome',bool1=False))

    return render_template('update_categories.html', categories=ncat)

@main.route("/additem/<string:categories_id>", methods=['GET', 'POST'])
def add_item(categories_id):
    # ncat = Categories.query.get_or_404(categories_id)
    if request.method == "POST":
        pname = request.form.get('product_name')
        mandate = request.form.get('manufacture_date')
        expdate = request.form.get('expiry_date')
        pperunit = request.form.get('price_per_unit')
        new_item=Products(product_name=pname, manufacture=mandate, expiry=expdate, p_per_u=pperunit,c_id=categories_id)
        db.session.add(new_item)
        db.session.commit()
        # return redirect(url_for('main.adminhome',bool1=False))

    return render_template('additem.html', cid=categories_id)

@main.route('/viewitems/<string:categories_id>/<string:type>', methods=['GET', 'POST'])
def view_items(categories_id,type):
    data = Products.query.filter_by(c_id=categories_id).all()
    return render_template("views_items.html",prod=data,check=type) 

@main.route("/Itemupdate/<string:item_id>/<string:type>", methods=['GET', 'POST'])
def update_item(item_id,type):
    nitem = Products.query.get_or_404(item_id)
    if request.method == "POST":
        nitem.product_name = request.form['product_name']
        nitem.manufacture = request.form['manufacture_date']
        nitem.expiry = request.form['expiry_date']
        nitem.p_per_u = request.form['price_per_unit']
        db.session.commit()
        flash('Your post has been updated!')
        categories_id=nitem.c_id
        data = Products.query.filter_by(c_id=categories_id).all()
        return render_template('views_items.html',prod=data,check='1')

    return render_template('views_items.html', item_id=item_id, check=type)

@main.route('/revertitem/<string:item_id>/<string:type>', methods=['GET', 'POST'])
def revert_item(item_id,type):
    nitem = Products.query.get_or_404(item_id)
    categories_id=nitem.c_id
    data = Products.query.filter_by(c_id=categories_id).all()
    return render_template("views_items.html",prod=data,check=type) 

@main.route("/delitem/<string:item_id>", methods=['GET', 'POST'])
def delete_item(item_id):
    nitem = Products.query.get_or_404(item_id)
    db.session.delete(nitem)
    db.session.commit()
    flash('Your post has been deleted!')
    categories_id=nitem.c_id
    data = Products.query.filter_by(c_id=categories_id).all()
    return render_template("views_items.html",prod=data,check='1')

@main.route("/deletecategory/<string:categories_id>", methods=['GET', 'POST'])
@login_required
def delete_category(categories_id):
    data = Products.query.filter_by(c_id=categories_id).all()
    for item in data:
        db.session.delete(item)
        db.session.commit()
    cname = Categories.query.filter_by(id=categories_id).first()
    db.session.delete(cname)
    db.session.commit()
    datacat= Categories.query.all()
    return render_template("home_admin.html", bool=True,data=datacat,boolcat=True )  
