from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TimeField, SelectField
from wtforms.validators import DataRequired, URL
import csv


app = Flask(__name__)
# this secret key is not secret, was provided with starting files for the project
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField("Location URL", validators=[DataRequired(), URL()])
    open_time = TimeField("opening time", validators=[DataRequired()])
    closing_time = TimeField("closing time", validators=[DataRequired()])
    coffee_rating = SelectField("Coffee rating", choices=[('☕', '☕'), ('☕☕', '☕☕'), ('☕☕☕', '☕☕☕'), ('☕☕☕☕', '☕☕☕☕'), ('☕☕☕☕☕', '☕☕☕☕☕')], validators=[DataRequired()])
    wifi_rating = SelectField("wifi rating", choices=[('✘', '✘'), ('💪', '💪'), ('💪💪', '💪💪'), ('💪💪💪', '💪💪💪'), ('💪💪💪💪', '💪💪💪💪'), ('💪💪💪💪💪', '💪💪💪💪💪')], validators=[DataRequired()])
    power_rating = SelectField("power rating", choices=[('✘', '✘'),('🔌', '🔌'), ('🔌🔌', '🔌🔌'), ('🔌🔌🔌', '🔌🔌🔌'), ('🔌🔌🔌🔌', '🔌🔌🔌🔌'), ('🔌🔌🔌🔌🔌', '🔌🔌🔌🔌🔌')], validators=[DataRequired()])
    submit = SubmitField('Submit')


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["POST", "GET"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        with open('cafe-data.csv', newline='', encoding="utf8", mode="a") as csv_file:
            csv_row = f"{form.cafe.data}," \
                      f"{form.location.data},"  \
                      f"{form.open_time.data.strftime('%H:%M %p')}," \
                      f"{form.closing_time.data.strftime('%H:%M %p')}," \
                      f"{form.coffee_rating.data}," \
                      f"{form.wifi_rating.data}," \
                      f"{form.power_rating.data}\r"
            csv_file.write(csv_row,)
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding="utf8") as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
