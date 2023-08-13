from flask import Blueprint, render_template, request, flash, redirect, url_for
from . import db
from .models import User,Categories,Products,Cart
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required, current_user


global_user=None
# Create a blueprint named 'main'
main = Blueprint("main", __name__)


# Route for the base page
@main.route("/")
def base():
    return render_template("base.html")


# Route for the user home page

@main.route("/userhome/<int:userid>")
@login_required

def userhome(userid):
    
    if(current_user.id==userid):
        global global_user
        global_user=userid
        # Retrieve all categories from the database
        categories = Categories.query.all()
        for category in categories:
            # Fetch all products related to each category and store them in the category object
            category.products = Products.query.filter_by(c_id=category.id).all()
        return render_template("home_user.html", categories=categories, userid=userid)


# Route for the admin home page
@main.route("/admin-home<bool1>/<int:userid>", methods=["GET", "POST"])
@login_required
def adminhome(bool1,userid):
    if(current_user.id==userid):
        global global_user
        global_user=userid
        # Convert the 'bool1' parameter to a boolean value
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

@main.route('/adminhomecategories', methods=['GET', 'POST'])
@login_required
def adminhomecategories():
    global global_user
    if current_user.is_authenticated and current_user.id == global_user:
        
        if request.method == 'POST':
            cat_name = request.form['category_name']
            if cat_name:
                cname = Categories.query.filter_by(cat_name=cat_name).first()
                if cname:
                    return redirect(url_for('main.adminhome', bool1=False))
                new_cat = Categories(cat_name=cat_name)
                db.session.add(new_cat)
                db.session.commit()
        data = Categories.query.all()
        return render_template("home_admin.html", bool=True, data=data)
    else:
        return("<center><h1>Access Denied</h1></center>")    


# Route to display all categories in the admin home page
@main.route("/adminshowcategories", methods=["GET", "POST"])
@login_required
def adminshowcategories():
    global global_user
    if current_user.is_authenticated and current_user.id == global_user:
        data = Categories.query.all()
        return render_template("home_admin.html", bool=True, data=data, boolcat=True)


# Route to update a category
@main.route("/Categoryupdate/<string:categories_id>", methods=["GET", "POST"])
@login_required
def update_category(categories_id):
    global global_user
    if current_user.is_authenticated and current_user.id == global_user:
    # Retrieve the category object based on the provided ID
        ncat = Categories.query.get_or_404(categories_id)
        if request.method == "POST":
            # Update the category name based on the form submission
            ncat.cat_name = request.form["ncategory"]
            db.session.commit()
            flash("Your post has been updated!")
            return redirect(url_for("main.adminhome", bool1=False))

        return render_template("update_categories.html", categories=ncat)
    else:
        return("<center><h1>Access Denied</h1></center>")

# Route to add a new item to a category
@main.route("/additem/<string:categories_id>", methods=["GET", "POST"])
@login_required
def add_item(categories_id):
    global global_user
    if current_user.is_authenticated and current_user.id == global_user:
        if request.method == "POST":
            # Retrieve the product details from the form submission
            pname = request.form.get("product_name")
            mandate = request.form.get("manufacture_date")
            expdate = request.form.get("expiry_date")
            pperunit = request.form.get("price_per_unit")
            itemstock = request.form.get("stock")

            # Create a new product object and add it to the database
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

        return render_template("additem.html", cid=categories_id)
    else:
        return("<center><h1>Access Denied</h1></center>")

@main.route("/viewitems/<string:categories_id>/<string:type>", methods=["GET", "POST"])
@login_required
def view_items(categories_id, type):
    global global_user
    if current_user.is_authenticated and current_user.id == global_user:
        data = Products.query.filter_by(c_id=categories_id).all()
        return render_template("views_items.html", prod=data, check=type)


# Route to update an item
@main.route("/Itemupdate/<string:item_id>/<string:type>", methods=["GET", "POST"])
@login_required
def update_item(item_id, type):
    global global_user
    if current_user.is_authenticated and current_user.id == global_user:
        # Retrieve the item object based on the provided ID
        nitem = Products.query.get_or_404(item_id)
        if request.method == "POST":
            # Update the item details based on the form submission
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
    else:
        return("<center><h1>Access Denied</h1></center>")

# Route to revert changes to an item
@main.route("/revertitem/<string:item_id>/<string:type>", methods=["GET", "POST"])
@login_required
def revert_item(item_id, type):
    global global_user
    if current_user.is_authenticated and current_user.id == global_user:
        nitem = Products.query.get_or_404(item_id)
        categories_id = nitem.c_id
        data = Products.query.filter_by(c_id=categories_id).all()
        return render_template("views_items.html", prod=data, check=type)
    else:
        return("<center><h1>Access Denied</h1></center>")

# Route to delete an item
@main.route("/delitem/<string:item_id>", methods=["GET", "POST"])
@login_required
def delete_item(item_id):
    global global_user
    if current_user.is_authenticated and current_user.id == global_user:
        nitem = Products.query.get_or_404(item_id)
        db.session.delete(nitem)
        db.session.commit()
        flash("Your post has been deleted!")
        categories_id = nitem.c_id
        data = Products.query.filter_by(c_id=categories_id).all()
        return render_template("views_items.html", prod=data, check="1")
    else:
        return("<center><h1>Access Denied</h1></center>")

# Route to delete a category and all associated items
@main.route("/deletecategory/<string:categories_id>", methods=["GET", "POST"])
@login_required
def delete_category(categories_id):
    global global_user
    if current_user.is_authenticated and current_user.id == global_user:
        try:
            # Delete associated products first
            data = Products.query.filter_by(c_id=categories_id).all()
            for item in data:
                db.session.delete(item)
            cname = Categories.query.filter_by(id=categories_id).first()
            db.session.delete(cname)
            db.session.commit()
            datacat = Categories.query.all()
            return render_template("home_admin.html", bool=True, data=datacat, boolcat=True)
        except Exception as e:
            print(f"Error: {e}")
            db.session.rollback()  
            datacat = Categories.query.all()
            return render_template("home_admin.html", bool=True, data=datacat, boolcat=True)
    else:
        return("<center><h1>Access Denied</h1></center>")


# Route to add an item to the cart
@main.route("/addtocart/<string:product_id>/<int:userid>", methods=["GET", "POST"])
@login_required
def addtocart(product_id, userid):
    global global_user
    if current_user.is_authenticated and current_user.id == global_user:
        # Retrieve the product based on the provided ID
        product_id = int(product_id)
        product = Products.query.get(product_id)
        total_quantity = 0
        total_price = 0

        if request.method == "POST":
            # Process the form submission to calculate total quantity and price
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
    else:
        return("<center><h1>Access Denied</h1></center>")

# Route to save the cart after adding items
@main.route(
    "/savecart/<string:productid>/<int:quantity>/<int:total>/<int:userid>",
    methods=["GET", "POST"],
)
@login_required
def savecart(productid, quantity, total, userid):
    global global_user
    if current_user.is_authenticated and current_user.id == global_user:
        # Retrieve the product based on the provided ID
        items = Products.query.get_or_404(productid)
        categoryid = items.c_id

        # Check if the item is already present in the cart
        cartentry = Cart.query.filter_by(
            cart_user_id=userid, cart_item_id=productid
        ).first()

        if cartentry:
            # If the item is present, update the cart entry
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
            # If the item is not present, create a new cart entry
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
    else:
        return("<center><h1>Access Denied</h1></center>")

# Route to show the cart items for a user
@login_required
@main.route("/showcart/<string:productid>/<int:userid>", methods=["GET", "POST"])
def showcart(productid, userid):
    global global_user
    if current_user.is_authenticated and current_user.id == global_user:
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
    else:
        return("<center><h1>Access Denied</h1></center>")


# Route to delete an item from the cart
@login_required
@main.route("/delcart/<int:cartid>/<int:userid>", methods=["GET", "POST"])
def delete_cart(cartid, userid):
    global global_user
    if current_user.is_authenticated and current_user.id == global_user:

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
    else:
        return("<center><h1>Access Denied</h1></center>")

# Route to view cart items for a user
@main.route("/usercart/<int:userid>", methods=["GET", "POST"])
@login_required
def usercart(userid):
    global global_user
    if current_user.is_authenticated and current_user.id == global_user:
        cartdata = Cart.query.filter_by(cart_user_id=userid).all()
        user = User.query.get_or_404(userid)
        usercartrecord = Cart.query.filter_by(cart_user_id=userid).all()
        totalprice = 0
        for i in usercartrecord:
            totalprice = totalprice + (i.cart_amount)

        return render_template(
            "cart.html", cartdata=cartdata, user=user, totalprice=totalprice
        )
    else:
        return("<center><h1>Access Denied</h1></center>")

# Route to complete the purchase and clear the cart
@main.route("/purchase/<int:userid>", methods=["GET", "POST"])
@login_required
def purchase(userid):
    global global_user
    if current_user.is_authenticated and current_user.id == global_user:
        cartdata = Cart.query.filter_by(cart_user_id=userid).all()
        for cart in cartdata:
            db.session.delete(cart)
            db.session.commit()
        user = User.query.get_or_404(userid)
        return render_template("cart.html", user=user, purchbool=True)
    else:
        return("<center><h1>Access Denied</h1></center>")

@main.route("/searchcat/<int:userid>", methods=["GET", "POST"])
@login_required
def searchcat(userid):
    global global_user
    if current_user.is_authenticated and current_user.id == global_user:
        return render_template("Search_elems.html", userid=userid, role="searchcateg")
    else:
        return("<center><h1>Access Denied</h1></center>")

# Route to perform a search based on a category name
@main.route("/search_categ/<int:userid>", methods=["GET", "POST"])
@login_required
def search_categ(userid):
    global global_user
    if current_user.is_authenticated and current_user.id == global_user:
        catname = request.form.get("category_name")
        categories = Categories.query.all()
        for cat in categories:
            if catname == cat.cat_name:
                return render_template(
                    "showsearch.html",
                    role="found",
                    category=cat,
                    userid=userid,
                    search="categories",
                )
        return render_template(
            "showsearch.html", role="notfound", userid=userid, search="categories"
        )
    else:
        return("<center><h1>Access Denied</h1></center>")

# Route to search for items
@main.route("/searchitem/<int:userid>", methods=["GET", "POST"])
@login_required
def searchitem(userid):
    global global_user
    if(current_user.id==global_user):
        return render_template("Search_elems.html", userid=userid, role="searchitems")
    else:
        return("<center><h1>Access Denied</h1></center>")

# Route to perform a search based on item name, price, manufacture date, and expiry date
@login_required
@main.route("/search_item/<int:userid>", methods=["GET", "POST"])
def search_item(userid):
    global global_user
    if current_user.is_authenticated and current_user.id == global_user:
        itemname = request.form.get("product_name")
        itemprice = request.form.get("price")
        if itemprice:
            itemprice = int(itemprice)
        item_manu = request.form.get("manufacture_date")
        if item_manu:
            item_manu_date = datetime.strptime(item_manu, "%Y-%m-%d").date()
        item_exp = request.form.get("expiry_date")
        if item_exp:
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
            return render_template(
                "showsearch.html",
                userid=userid,
                products=prods,
                search="items",
                role="found",
            )
        return render_template(
            "showsearch.html", userid=userid, search="items", role="notfound"
        )
    else:
        return("<center><h1>Access Denied</h1></center>")