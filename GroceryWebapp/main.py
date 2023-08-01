from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from os import path
from . import db
from .models import User
from .models import Categories
from .models import Products
from .models import Cart
from datetime import datetime

main = Blueprint("main", __name__)


@main.route("/")
def base():
    return render_template("base.html")


@main.route("/userhome/<int:userid>")
def userhome(userid):
    categories = Categories.query.all()
    for category in categories:
        category.products = Products.query.filter_by(c_id=category.id).all()
    return render_template("home_user.html", categories=categories, userid=userid)


@main.route("/admin-home<bool1>", methods=["GET", "POST"])
def adminhome(bool1):
    bool_value = bool1.lower() in ["true", "1", "yes"]
    result = Categories.query.first()
    bool = False
    if result:
        bool = True
    else:
        bool = False
        if bool_value == True:
            bool = True
    return render_template("home_admin.html", bool=bool)


@main.route("/adminhomecategories", methods=["GET", "POST"])
def adminhomecategories():
    if request.method == "POST":
        cat_name = request.form["category_name"]
        if cat_name:
            cname = Categories.query.filter_by(cat_name=cat_name).first()
            if cname:
                return redirect(url_for("main.adminhome", bool1=False))
            new_cat = Categories(cat_name=cat_name)
            db.session.add(new_cat)
            db.session.commit()
    data = Categories.query.all()
    return render_template("home_admin.html", bool=True, data=data)


@main.route("/adminshowcategories", methods=["GET", "POST"])
def adminshowcategories():
    data = Categories.query.all()
    return render_template("home_admin.html", bool=True, data=data, boolcat=True)


@main.route("/Categoryupdate/<string:categories_id>", methods=["GET", "POST"])
def update_category(categories_id):
    ncat = Categories.query.get_or_404(categories_id)
    if request.method == "POST":
        ncat.cat_name = request.form["ncategory"]
        db.session.commit()
        flash("Your post has been updated!")
        return redirect(url_for("main.adminhome", bool1=False))

    return render_template("update_categories.html", categories=ncat)


@main.route("/additem/<string:categories_id>", methods=["GET", "POST"])
def add_item(categories_id):
    # ncat = Categories.query.get_or_404(categories_id)
    if request.method == "POST":
        pname = request.form.get("product_name")
        mandate = request.form.get("manufacture_date")
        expdate = request.form.get("expiry_date")
        pperunit = request.form.get("price_per_unit")
        itemstock = request.form.get("stock")
        new_item = Products(
            product_name=pname,
            manufacture=mandate,
            expiry=expdate,
            p_per_u=pperunit,
            stock=itemstock,
            c_id=categories_id,
        )
        db.session.add(new_item)
        db.session.commit()
        # return redirect(url_for('main.adminhome',bool1=False))

    return render_template("additem.html", cid=categories_id)


@main.route("/viewitems/<string:categories_id>/<string:type>", methods=["GET", "POST"])
def view_items(categories_id, type):
    data = Products.query.filter_by(c_id=categories_id).all()
    return render_template("views_items.html", prod=data, check=type)


@main.route("/Itemupdate/<string:item_id>/<string:type>", methods=["GET", "POST"])
def update_item(item_id, type):
    nitem = Products.query.get_or_404(item_id)
    if request.method == "POST":
        nitem.product_name = request.form["product_name"]
        nitem.manufacture = request.form["manufacture_date"]
        nitem.expiry = request.form["expiry_date"]
        nitem.p_per_u = request.form["price_per_unit"]
        nitem.stock = request.form["stock"]
        db.session.commit()
        flash("Your post has been updated!")
        categories_id = nitem.c_id
        data = Products.query.filter_by(c_id=categories_id).all()
        return render_template("views_items.html", prod=data, check="1")

    return render_template("views_items.html", item_id=item_id, check=type)


@main.route("/revertitem/<string:item_id>/<string:type>", methods=["GET", "POST"])
def revert_item(item_id, type):
    nitem = Products.query.get_or_404(item_id)
    categories_id = nitem.c_id
    data = Products.query.filter_by(c_id=categories_id).all()
    return render_template("views_items.html", prod=data, check=type)


@main.route("/delitem/<string:item_id>", methods=["GET", "POST"])
def delete_item(item_id):
    nitem = Products.query.get_or_404(item_id)
    db.session.delete(nitem)
    db.session.commit()
    flash("Your post has been deleted!")
    categories_id = nitem.c_id
    data = Products.query.filter_by(c_id=categories_id).all()
    return render_template("views_items.html", prod=data, check="1")


@main.route("/deletecategory/<string:categories_id>", methods=["GET", "POST"])
def delete_category(categories_id):
    data = Products.query.filter_by(c_id=categories_id).all()
    for item in data:
        db.session.delete(item)
        db.session.commit()
    cname = Categories.query.filter_by(id=categories_id).first()
    db.session.delete(cname)
    db.session.commit()
    datacat = Categories.query.all()
    return render_template("home_admin.html", bool=True, data=datacat, boolcat=True)


@main.route("/addtocart/<string:product_id>/<int:userid>", methods=["GET", "POST"])
def addtocart(product_id, userid):
    product_id = int(product_id)
    product = Products.query.get(product_id)
    total_quantity = 0
    total_price = 0

    if request.method == "POST":
        product = Products.query.get(product_id)
        quantity = int(request.form["quantity"])
        total = product.p_per_u * quantity

        # Calculate total quantity and price based on form submission
        total_quantity += quantity
        total_price += total
        return render_template(
            "addtocart.html",
            product=product,
            product_id=product_id,
            total=total,
            total_quantity=total_quantity,
            total_price=total_price,
            userid=userid,
        )

    return render_template(
        "addtocart.html",
        product=product,
        product_id=product_id,
        total_quantity=total_quantity,
        total_price=total_price,
        userid=userid,
    )


@main.route(
    "/savecart/<string:productid>/<int:quantity>/<int:total>/<int:userid>",
    methods=["GET", "POST"],
)
def savecart(productid, quantity, total, userid):
    items = Products.query.get_or_404(productid)
    categoryid = items.c_id
    cartentry = Cart.query.filter_by(
        cart_user_id=userid, cart_item_id=productid
    ).first()
    if cartentry:
        if quantity + cartentry.cart_quantity <= items.stock and quantity >= 1:
            cartentry.cart_quantity += quantity
            cartentry.cart_amount = cartentry.cart_amount + total
            db.session.commit()
            items.stock = items.stock - quantity
            db.session.commit()

        elif quantity + cartentry.cart_quantity > items.stock and quantity >= 1:
            cartentry.cart_quantity = items.stock
            cartentry.cart_amount = cartentry.cart_amount + total
            db.session.commit()
            items.stock = 0
            db.session.commit()
    elif quantity >= 1:
        new_cart = Cart(
            cart_item_id=productid,
            cart_user_id=userid,
            cart_cat_id=categoryid,
            cart_quantity=quantity,
            cart_amount=total,
        )
        db.session.add(new_cart)
        db.session.commit()
        items.stock = items.stock - quantity
        db.session.commit()

    return redirect(url_for("main.addtocart", product_id=productid, userid=userid))


@main.route("/showcart/<string:productid>/<int:userid>", methods=["GET", "POST"])
def showcart(productid, userid):
    cartdata = Cart.query.filter_by(cart_user_id=userid).all()
    user = User.query.get_or_404(userid)
    items = Products.query.get_or_404(productid)
    categoryid = items.c_id
    usercartrecord = Cart.query.filter_by(cart_user_id=userid).all()
    totalprice = 0
    for i in usercartrecord:
        totalprice = totalprice + (i.cart_amount)
    return render_template(
        "cart.html", cartdata=cartdata, user=user, totalprice=totalprice
    )


@main.route("/delcart/<int:cartid>/<int:userid>", methods=["GET", "POST"])
def delete_cart(cartid, userid):
    ncart = Cart.query.get_or_404(cartid)
    restock = ncart.cart_quantity
    prodid = ncart.cart_item_id
    user = User.query.get_or_404(userid)
    db.session.delete(ncart)
    db.session.commit()
    items = Products.query.get_or_404(prodid)
    items.stock = items.stock + restock
    db.session.commit()

    cartdata = Cart.query.filter_by(cart_user_id=userid).all()
    flash("Your post has been deleted!")
    usercartrecord = Cart.query.filter_by(cart_user_id=userid).all()
    totalprice = 0
    for i in usercartrecord:
        totalprice = totalprice + (i.cart_amount)
    return render_template(
        "cart.html", user=user, cartdata=cartdata, totalprice=totalprice
    )


@main.route("/usercart/<int:userid>", methods=["GET", "POST"])
def usercart(userid):
    cartdata = Cart.query.filter_by(cart_user_id=userid).all()
    user = User.query.get_or_404(userid)
    usercartrecord = Cart.query.filter_by(cart_user_id=userid).all()
    totalprice = 0
    for i in usercartrecord:
        totalprice = totalprice + (i.cart_amount)

    return render_template(
        "cart.html", cartdata=cartdata, user=user, totalprice=totalprice
    )


@main.route("/purchase/<int:userid>", methods=["GET", "POST"])
def purchase(userid):
    cartdata = Cart.query.filter_by(cart_user_id=userid).all()
    for cart in cartdata:
        db.session.delete(cart)
        db.session.commit()
    user = User.query.get_or_404(userid)
    return render_template("cart.html", user=user, purchbool=True)


@main.route("/searchcat/<int:userid>", methods=["GET", "POST"])
def searchcat(userid):
    return render_template(
        "Search_elems.html", userid=userid, role="searchcateg"
    )


@main.route("/search_categ/<int:userid>", methods=["GET", "POST"])
def search_categ(userid):
    catname = request.form.get("category_name")
    categories = Categories.query.all()
    for cat in categories:
        if catname == cat.cat_name:
            return render_template(
                "showsearch.html", role="found", category=cat, userid=userid,search="categories"
            )
    return render_template(
        "showsearch.html", role="notfound", userid=userid, search="categories"
    )


@main.route("/searchitem/<int:userid>", methods=["GET", "POST"])
def searchitem(userid):
    return render_template("Search_elems.html", userid=userid, role="searchitems")


@main.route("/search_item/<int:userid>", methods=["GET", "POST"])
def search_item(userid):
    itemname = request.form.get("product_name")
    itemprice = request.form.get("price")
    if(itemprice):
        itemprice=int(itemprice)
    item_manu = request.form.get("manufacture_date")
    if(item_manu):
        item_manu_date = datetime.strptime(item_manu, "%Y-%m-%d").date()
    item_exp = request.form.get("expiry_date")
    if(item_exp):
       item_exp_date = datetime.strptime(item_exp, "%Y-%m-%d").date()

    data = Products.query.filter_by(product_name=itemname).all()
    prods = []
    if data:
        if itemname and itemprice and item_manu and item_exp:
            for i in data:
                table_manu = datetime.strptime(i.manufacture, "%Y-%m-%d").date()
                table_exp = datetime.strptime(i.expiry, "%Y-%m-%d").date()
                if (
                    i.p_per_u >= itemprice
                    and table_manu <= item_manu_date
                    and table_exp >= item_exp_date
                ):
                    prods.append(i)
        elif itemname and itemprice and item_manu:
            for i in data:
                table_manu = datetime.strptime(i.manufacture, "%Y-%m-%d").date()
                if i.p_per_u >= itemprice and table_manu <= item_manu_date:
                    prods.append(i)
        elif itemname and itemprice and item_exp:
            for i in data:
                table_exp = datetime.strptime(i.expiry, "%Y-%m-%d").date()
                if i.p_per_u >= itemprice and table_exp >= item_exp_date:
                    prods.append(i)
        elif itemname and itemprice:
            for i in data:
                if i.p_per_u >= itemprice:
                    prods.append(i)
        else:
            for i in data:
                prods.append(i)
        return render_template("showsearch.html", userid=userid, products=prods,search="items",role="found")
    return render_template("showsearch.html", userid=userid,search="items",role="notfound")
