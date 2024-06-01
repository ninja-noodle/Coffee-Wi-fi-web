import base64

from decouple import config
from flask import Flask, render_template, redirect, url_for, flash, request, session
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from Google import Create_Service
from backendfunctions import SeatsFilter, SearchAlgorithm, CafeSubmission

# ====== GOOGLE DRIVE API AUTH =======
CLIENT_SECRET_FILE = config('GOOGLE_API_CLIENT_SECRETS')
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']
FOLDER_ID = config('IMG_FOLDER_ID')
service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

# ====== CREATING FOLDER IN GOOGLE DRIVE =======
# file_metadata = {
#     'name': 'cafe-images',
#     'mimeType': 'application/vnd.google-apps.folder'
# }
# service.files().create(body=file_metadata).execute()


# ====== FLASK APP CONFIG =======
app = Flask(__name__)
app.config['SECRET_KEY'] = config('SECRET_KEY')
Bootstrap5(app)

# ====== DATABASE CONNECTION =======
app.config['SQLALCHEMY_DATABASE_URI'] = config('DB_URI')
db = SQLAlchemy()
db.init_app(app)


# ====== DATABASE MODEL =======
class Cafe(db.Model):
    __tablename__ = 'cafe'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img = db.Column(db.BLOB, unique=True, nullable=False)
    img_name = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    coffee_price = db.Column(db.String(250), nullable=False)
    contributor_name = db.Column(db.String(250), nullable=False)
    contributor_email = db.Column(db.String(250), unique=False, nullable=False)


with app.app_context():
    db.create_all()


def check_if_exists(cafe_name):
    if db.session.execute(db.select(Cafe).where(Cafe.name == cafe_name)).first() is None:
        return False
    elif db.session.execute(db.select(Cafe).where(Cafe.name == cafe_name)).first() is not None:
        return True


@app.route('/', methods=['GET', 'POST'])
def get_all_cafes():
    total_cafe_no = len(db.session.execute(db.select(Cafe)).scalars().all())
    if request.method == "POST":
        if request.form.get('logo-home') == 'home':
            return redirect(url_for('get_all_cafes'))
        elif request.form.get('search') == 'search':
            return redirect(url_for('search_cafes', search=request.form.get('search-data')))
        elif request.form.get('filter') == 'filter-wifi':
            return redirect(url_for('filter_cafes', filter='has_wifi'))
        elif request.form.get('filter') == 'filter-sockets':
            return redirect(url_for('filter_cafes', filter='has_sockets'))
        elif request.form.get('filter') == 'filter-toilet':
            return redirect(url_for('filter_cafes', filter='has_toilet'))
        elif request.form.get('filter') == 'filter-phone':
            return redirect(url_for('filter_cafes', filter='can_take_calls'))
        elif request.form.get('filter') == 'filter-seats':
            return redirect(url_for('filter_cafes', filter='seats', seat_amount=request.form.get('seatAmount')))
    data = db.session.execute(db.select(Cafe))
    chunks = data.scalars().all()
    cafe_images = [base64.b64encode(cafe.img).decode('ascii') for cafe in chunks]
    return render_template("base.html", all_cafes=chunks, cafe_images=cafe_images, filter_id=1, no_data=0, total_cafe_no=total_cafe_no)


@app.route('/filtered/<filter>', methods=['GET', 'POST'])
def filter_cafes(filter):
    total_cafe_no = len(db.session.execute(db.select(Cafe)).scalars().all())
    if request.method == "POST":
        if request.form.get('search') == 'search':
            return redirect(url_for('search_cafes', search=request.form.get('search-data')))
    if filter == 'has_wifi':
        chunks = Cafe.query.filter_by(has_wifi=1).all()
        cafe_images = [base64.b64encode(cafe.img).decode('ascii') for cafe in chunks]
        return render_template("base.html", all_cafes=chunks, cafe_images=cafe_images, filter_id=2, no_data=0, total_cafe_no=total_cafe_no)
    if filter == 'has_sockets':
        chunks = Cafe.query.filter_by(has_sockets=1).all()
        cafe_images = [base64.b64encode(cafe.img).decode('ascii') for cafe in chunks]
        return render_template("base.html", all_cafes=chunks, cafe_images=cafe_images, filter_id=3, no_data=0, total_cafe_no=total_cafe_no)
    if filter == 'has_toilet':
        chunks = Cafe.query.filter_by(has_toilet=1).all()
        cafe_images = [base64.b64encode(cafe.img).decode('ascii') for cafe in chunks]
        return render_template("base.html", all_cafes=chunks, cafe_images=cafe_images, filter_id=4, no_data=0, total_cafe_no=total_cafe_no)
    if filter == 'can_take_calls':
        chunks = Cafe.query.filter_by(can_take_calls=1).all()
        cafe_images = [base64.b64encode(cafe.img).decode('ascii') for cafe in chunks]
        return render_template("base.html", all_cafes=chunks, cafe_images=cafe_images, filter_id=5, no_data=0, total_cafe_no=total_cafe_no)
    if filter == 'seats':
        seats = int(request.args['seat_amount'])
        if type(seats) is not int:
            seats = int(session['seat_amount'])
        data = db.session.execute(db.select(Cafe))
        chunks = SeatsFilter(seats, data.scalars().all()).seats_filter()
        cafe_images = [base64.b64encode(cafe.img).decode('ascii') for cafe in chunks]
        return render_template("base.html", all_cafes=chunks, cafe_images=cafe_images, filter_id=6, no_data=0, total_cafe_no=total_cafe_no,
                               seats=seats)


@app.route('/search/<search>', methods=['GET', 'POST'])
def search_cafes(search):
    total_cafe_no = len(db.session.execute(db.select(Cafe)).scalars().all())
    if request.method == "POST":
        if request.form.get('search') == 'search':
            return redirect(url_for('search_cafes', search=request.form.get('search-data')))
    data = db.session.execute(db.select(Cafe))
    chunks = SearchAlgorithm(search_data=search, base_data=data.scalars().all()).search()
    cafe_images = [base64.b64encode(cafe.img).decode('ascii') for cafe in chunks]
    if len(chunks) > 0:
        return render_template("base.html", all_cafes=chunks, cafe_images=cafe_images, filter_id='search', no_data=0,
                               total_cafe_no=total_cafe_no, searchvalue=search)
    elif len(chunks) == 0:
        return render_template("base.html", all_cafes=chunks, cafe_images=cafe_images, filter_id='search', no_data=1,
                               total_cafe_no=total_cafe_no, searchvalue=search)


@app.route('/contribution/add-cafe', methods=['GET', 'POST'])
def add_cafe():
    return render_template('base.html', form_id=1)


@app.route('/contribution/success', methods=['GET', 'POST'])
def cafe_added():
    if request.method == "POST":
        img_file = request.files['img-file']
        if request.form.get('submit') == 'submit':
            new_submission = CafeSubmission()
            if check_if_exists(request.form.get('cafe-name')):
                flash("Cafe already exists (●'◡'●)", "already_exist_error")
                return redirect(url_for('add_cafe'))
            elif new_submission.add_cafe_data(img=img_file,
                                              name=request.form.get('cafe-name'),
                                              location=request.form.get('location'),
                                              map_url=request.form.get('map-link'),
                                              currency=request.form.get('currency'),
                                              price=request.form.get('coffee-price'),
                                              seats_min=request.form.get('min-seats'),
                                              seats_max=request.form.get('max-seats'),
                                              wifi=request.form.get('has-wifi'),
                                              sockets=request.form.get('has-sockets'),
                                              toilet=request.form.get('has-toilet'),
                                              calls=request.form.get('can-take-calls'),
                                              mysterious=request.form.get('anonymous'),
                                              contributor_name=request.form.get('contributor-name'),
                                              contributor_email=request.form.get('contributor-email'),
                                              db=db,
                                              cafe=Cafe):
                return render_template('base.html', form_id=1, success=1)
            else:
                flash("The file type is not allowed >:(", "file_type_error")
                return redirect(url_for('add_cafe'))


@app.route('/cafes/<cafe_name>', methods=['GET', 'POST'])
def show_cafe(cafe_name):
    cafe_id = request.args['cafe_id']
    requested_cafe = db.get_or_404(Cafe, cafe_id)
    if cafe_name == requested_cafe.name:
        return render_template('base.html', cafe=1, requested_cafe=requested_cafe)


if __name__ == "__main__":
    app.run(debug=True)
