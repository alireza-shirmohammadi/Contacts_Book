from flask import (
    Blueprint,
    request,
    render_template,
    redirect,
    url_for,
    Response,
    make_response,
)
from myproject.models import Contacts
from myproject import db
from wtforms.validators import ValidationError
import csv
from io import StringIO


contacts_bluprint = Blueprint(
    "contacts",
    __name__,
    template_folder="templates/contacts",
)


@contacts_bluprint.route("/list")
def contacts_list():
    contacts = Contacts.query.all()

    return render_template("contacts_list.html", contacts=contacts)


@contacts_bluprint.route("/add", methods=["POST", "GET"])
def contacts_add():

    if request.method == "POST":
        name = request.form.get("name")
        phone = request.form.get("phone")
        contact = Contacts(name=name, phone=phone)
        db.session.add(contact)

        db.session.commit()
        return redirect(url_for("contacts.contacts_list"))
    return render_template("contacts_add.html")


@contacts_bluprint.route("/del/<id>")
def contacts_del(id):
    try:
        contact = Contacts.query.get(id)
        db.session.delete(contact)
        db.session.commit()
        return redirect(url_for("contacts.contacts_list"))
    except:
        pass
    return None


@contacts_bluprint.route("/edit/<id>", methods=["POST", "GET"])
def contacts_edit(id):
    try:
        contact = Contacts.query.get(id)

        if request.method == "POST":
            name = request.form.get("name")
            phone = request.form.get("phone")
            contact.name = name
            contact.phone = phone

            db.session.commit()
            return redirect(url_for("contacts.contacts_list"))
    except:
        raise ValidationError("you're already registered")
    return render_template("contacts_edit.html", contact=contact, id=id)


@contacts_bluprint.route("/export")
def export_contacts_csv():
    si = StringIO()

    writer = csv.writer(si)
    writer.writerow(["name", "phone"])
    for i in Contacts.query.all():
        writer.writerow([i.name, i.phone])
    responde = make_response(si.getvalue())
    responde.headers["Content_Disposition"] = 'attachment;filename="contactslist.csv"'
    responde.headers["Content-type"] = "text/csv"

    return responde

