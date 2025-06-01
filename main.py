from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3  # ✅ This is the missing line!

app = Flask(__name__)
app.secret_key = 'secretkey'  # Required for session handling

# Home page
@app.route("/")
def home():
    return render_template("index.html")

# Menu page
@app.route("/menu")
def menu():
    conn = sqlite3.connect('canteen.db')
    cursor = conn.cursor()
    cursor.execute("SELECT item, price FROM menu")
    rows = cursor.fetchall()
    conn.close()

    menu_items = [{"name": row[0], "price": row[1]} for row in rows]
    return render_template("menu.html", items=menu_items)

# Parcel booking form
@app.route("/parcel", methods=["GET", "POST"])
def parcel():
    if request.method == "POST":
        name = request.form.get("name")
        phone = request.form.get("phone")
        item_and_quantity = request.form.get("item_and_quantity")

        conn = sqlite3.connect('canteen.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO parcels (name, item, quantity, phone) VALUES (?, ?, ?, ?)",
                       (name, item_and_quantity, "", phone))
        conn.commit()
        conn.close()

        return "Parcel Booked Successfully!"
    return render_template("parcel.html")

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == "admin" and password == "1234":
            session["admin_logged_in"] = True
            return redirect(url_for("view_parcels"))
        else:
            error = "Invalid username or password"
    return render_template("login.html", error=error)

@app.route("/admin/parcels")
def view_parcels():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    conn = sqlite3.connect('canteen.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name, item, quantity, phone FROM parcels")
    rows = cursor.fetchall()
    conn.close()

    bookings = [{"name": row[0], "item": row[1], "quantity": row[2], "phone": row[3]} for row in rows]
    return render_template("admin_parcels.html", bookings=bookings)

# Run the app
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)