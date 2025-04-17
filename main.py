import base64  # for image processing
import werkzeug  # for data and exception handling
from decouple import config  # for retrieving secrets from .env
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
# from Google import Create_Service
from backendfunctions import SearchAlgorithm, CafeSubmission, DataBaseHandler

# ====== GOOGLE DRIVE API AUTH =======
# CLIENT_SECRET_FILE = config('GOOGLE_API_CLIENT_SECRETS')
# API_NAME = 'drive'
# API_VERSION = 'v3'
# SCOPES = ['https://www.googleapis.com/auth/drive']
# FOLDER_ID = config('IMG_FOLDER_ID')
# service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

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
    country = db.Column(db.String(500), nullable=False)
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


handler = DataBaseHandler()


@app.route('/loading', methods=['GET', 'POST'])
def loader():
    # j = db.session.execute(db.select(Cafe)).scalars().all()
    #
    # initial_handler.cafe_no = len(j)
    # initial_handler.country_code = request.args['country']
    # initial_handler.code_to_name()
    try:
        print(request.args['load'])
        if request.args['load']:
            return render_template("base.html", loading=1)

    except werkzeug.exceptions.BadRequestKeyError:
        country = request.args['country']
        print(country)
        if country == 'NA' or country == 'all':
            handler.db = db.session.execute(db.select(Cafe)).scalars().all()
        else:
            handler.db = db.session.execute(db.select(Cafe).where(Cafe.country == country)).scalars().all()
        handler.initial_db = db.session.execute(db.select(Cafe)).scalars().all()

        return redirect(url_for('get_all_cafes'))


@app.route('/', methods=['GET', 'POST'])
def get_all_cafes():
    # if initial_handler.cafe_no is None:
    #     initial_handler.data_var(db.session.execute(db.select(Cafe)).scalars().all())

    # total_cafe_no = initial_handler.cafe_no

    total_cafe_no = len(db.session.execute(db.select(Cafe)).scalars().all())

    if request.method == "POST":
        country = request.form.get('country-filter')
        if country is not None:
            return redirect(url_for('loader', country=country))
        else:
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

    # chunks = db.session.execute(db.select(Cafe).where(Cafe.country == initial_handler.country)).scalars().all()
    print(handler.country_list_generator())
    chunks = handler.db
    cafe_images = [base64.b64encode(cafe.img).decode('ascii') for cafe in chunks]

    return render_template("base.html", all_cafes=chunks, cafe_images=cafe_images,
                           filter_id=0, no_data=0,
                           total_cafe_no=total_cafe_no,
                           country_select=handler.country_list_generator(),
                           )


@app.route('/filtered/<filter>', methods=['GET', 'POST'])
def filter_cafes(filter):
    total_cafe_no = len(db.session.execute(db.select(Cafe)).scalars().all())
    chunks = None
    filter_id = None
    seats = None
    no_data = 0

    if request.method == "POST":
        if request.form.get('search') == 'search':
            return redirect(url_for('search_cafes', search=request.form.get('search-data')))
    elif filter == 'has_wifi':
        chunks = handler.filter('has_wifi')
        filter_id = 2

    elif filter == 'has_sockets':
        chunks = handler.filter('has_sockets')
        filter_id = 3

    elif filter == 'has_toilet':
        chunks = handler.filter('has_toilet')
        filter_id = 4

    elif filter == 'can_take_calls':
        chunks = handler.filter('can_take_calls')
        filter_id = 5

    elif filter == 'seats':
        seats = int(request.args['seat_amount'])
        if type(seats) is not int:
            seats = int(session['seat_amount'])
        chunks = SeatsFilter(seats, handler.db).seats_filter()
        filter_id = 6

    cafe_images = [base64.b64encode(cafe.img).decode('ascii') for cafe in chunks]
    return render_template("base.html", all_cafes=chunks, cafe_images=cafe_images,
                           filter_id=filter_id, no_data=no_data,
                           seats=seats, total_cafe_no=total_cafe_no)


@app.route('/search/<search>', methods=['GET', 'POST'])
def search_cafes(search):
    total_cafe_no = len(db.session.execute(db.select(Cafe)).scalars().all())
    if request.method == "POST":
        if request.form.get('search') == 'search':
            return redirect(url_for('search_cafes', search=request.form.get('search-data')))
    data = handler.db
    chunks = SearchAlgorithm(search_data=search, base_data=data).search()
    cafe_images = [base64.b64encode(cafe.img).decode('ascii') for cafe in chunks]
    if len(chunks) > 0:
        return render_template("base.html", all_cafes=chunks, cafe_images=cafe_images,
                               filter_id='search', no_data=0,
                               total_cafe_no=total_cafe_no, searchvalue=search)
    elif len(chunks) == 0:
        return render_template("base.html", all_cafes=chunks, cafe_images=cafe_images,
                               filter_id='search', no_data=1,
                               total_cafe_no=total_cafe_no, searchvalue=search)


@app.route('/contribution/add-cafe', methods=['GET', 'POST'])
def add_cafe():
    return render_template('base.html', form_id=1)


@app.route('/contribution/success', methods=['GET', 'POST'])
def cafe_added():
    if request.method == "POST":
        img_file = request.files['img-file']
        img_size = len(img_file.read())

        if request.form.get('submit') == 'submit':
            new_submission = CafeSubmission()
            if check_if_exists(request.form.get('cafe-name')):
                flash("Cafe already exists (●'◡'●)", "already_exist_error")
                return redirect(url_for('add_cafe'))
            elif new_submission.add_cafe_data(img=img_file,
                                              img_size=img_size,
                                              name=request.form.get('cafe-name'),
                                              country=request.form.get('country'),
                                              location=request.form.get('location'),
                                              map_url=request.form.get('map-link'),
                                              currency=request.form.get('currency'),
                                              price=request.form.get('coffee-price'),
                                              seats=request.form.get('seats'),
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
    cafe_img = base64.b64encode(requested_cafe.img).decode('ascii')
    if cafe_name == requested_cafe.name:
        return render_template('base.html', cafe=1, cafe_img=cafe_img, requested_cafe=requested_cafe)


if __name__ == "__main__":
    app.run(debug=True)
