import json

from flask import Flask, render_template, redirect, url_for, request
from flask_wtf import FlaskForm
from requests.exceptions import ConnectionError
from wtforms import IntegerField, SelectField
from wtforms.validators import DataRequired, NumberRange

from post import data, send_json


class ClientDataForm(FlaskForm):
    id = IntegerField("ID", validators=[DataRequired()])
    age = IntegerField("Возраст водителя",
                       validators=[DataRequired(), NumberRange(min=16, max=90, message="Неверный возраст")])
    lic_age = IntegerField("Водительский стаж (лет)",
                           validators=[DataRequired(),  NumberRange(min=0, max=74, message="Неверный стаж")])
    gender = SelectField("Пол", choices=[("Male", "М"), ("Female", "Ж")])
    mari_stat = SelectField("Семейное положение", choices=[("Alone", "Холост/Не замужем"), ("Other", "В браке")])
    veh_age = IntegerField("Возраст автомобиля", validators=[DataRequired()])
    bonus_malus = IntegerField("Бонус-малус", validators=[DataRequired()])
    soc_categ = SelectField("Сфера деятельности", choices=[("CSP5", "Сотрудник"),
                                                           ("CSP1", "Сельское хозяйство"),
                                                           ("CSP2", "Промышленность и торговля"),
                                                           ("CSP3", "Управленческий персонал"),
                                                           ("CSP4", "Руководитель"),
                                                           ("CSP6", "Работник"),
                                                           ("CSP7", "Обслуживание"),
                                                           ("CSP8", "Другое")])
    veh_usage = SelectField("Количество поездок в неделю", choices=[("Private+trip to office", "10 - 20"),
                                                                    ("Private", "< 10"),
                                                                    ("Professional", "21 - 30"),
                                                                    ("Professional run", "> 30")])
    risk_area = IntegerField("Зона риска")


app = Flask(__name__)
app.config.update(CSRF_ENABLED=True, SECRET_KEY="you-will-never-guess")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/predicted/<response>")
def predicted(response):
    response = json.loads(response)
    return render_template("predicted.html", response=response)


@app.route("/predict_form", methods=["GET", "POST"])
def predict_form():
    form = ClientDataForm()
    if request.method == "POST":
        data["ID"] = int(request.form.get("id"))
        data["DrivAge"] = int(request.form.get("age"))
        data["LicAge"] = float(request.form.get("lic_age"))
        data["Gender"] = request.form.get("gender")
        data["MariStat"] = request.form.get("mari_stat")
        data["VehAge"] = float(request.form.get("veh_age"))
        data["BonusMalus"] = int(request.form.get("bonus_malus"))
        data["SocioCateg"] = request.form.get("soc_categ")
        data["VehUsage"] = request.form.get("veh_usage")
        data["RiskArea"] = int(request.form.get("risk_area"))
        try:
            response = send_json(data)
            response = response.text
        except ConnectionError:
            response = json.dumps({"error": "ConnectionError"})
        return redirect(url_for("predicted", response=response))
    return render_template("form.html", form=form)


if __name__ == "__main__":
    app.run(host="127.0.0.2", debug=True)
