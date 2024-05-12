import io
from PIL import Image
from decouple import config
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from googleapiclient.http import MediaIoBaseUpload
from werkzeug.utils import secure_filename

from Google import Create_Service

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


def add_cafe_data(img, name, location, map_url, currency, price, seats_min, seats_max, wifi, sockets, toilet, calls,
                  mysterious, contributor_name, contributor_email):
    folder_id = FOLDER_ID

    def image_to_byte_array(image: Image) -> bytes:
        # BytesIO is a file-like buffer stored in memory
        imgbytearr = io.BytesIO()
        # image.save expects a file-like as a argument
        image.save(imgbytearr, format=image.format)
        # Turn the BytesIO object back into a bytes object
        imgbytearr = imgbytearr.getvalue()
        return imgbytearr

    def allowed_file(file_name):
        """ takes the last part of the filename (extension) and checks if it is part of ALLOWED_EXTENSIONS"""
        return '.' in file_name and file_name.rsplit('.', 1)[1].lower() in {'jpg', 'jpeg', 'png'}

    def compress_img(image):
        if len(image.fp.read()) > 3000000:
            width, height = image.size
            new_size = (width // 2, height // 2)
            compressed_img = image.resize(new_size, resample=1)
            compressed_img.save(io.BytesIO(request_img_content), format=image.format, optimize=True, quality=80)
        return image

    def boolean_to_binary(var):
        if var == 'on':
            return 1
        else:
            return 0

    def mime_type_identify(file_n):
        file_type = '.' in file_n and file_n.rsplit('.', 1)[1].lower()
        if file_type == 'jpeg' or file_type == 'jpg':
            return 'image/jpeg'
        elif file_type == 'png':
            return 'image/png'

    def seat_data_format(_seat_min, _seat_max):
        return f"{eval(_seat_min.replace('{', '').replace('}', '').replace('<', '').replace(' ', ''))}-{eval(_seat_max.replace('{', '').replace('}', '').replace('<', '').replace(' ', ''))}"

    filename = secure_filename(img.filename)

    has_wifi = boolean_to_binary(wifi)
    has_sockets = boolean_to_binary(sockets)
    has_toilets = boolean_to_binary(toilet)
    can_take_calls = boolean_to_binary(calls)

    if allowed_file(filename):
        request_img_content = img.read()
        with Image.open(io.BytesIO(request_img_content), mode='r') as opened_image:
            request_img_content = image_to_byte_array(compress_img(opened_image))
            mime_type = mime_type_identify(filename)
            file_metadata = {
                'name': filename,
                'parents': [folder_id]
            }
            media_content = MediaIoBaseUpload(io.BytesIO(request_img_content), mimetype=mime_type)

            uploaded = service.files().create(
                body=file_metadata,
                media_body=media_content,
            ).execute()

        new_contributor = 'None'
        new_contributor_email = 'None'
        if mysterious != 'on':
            new_contributor = contributor_name
            new_contributor_email = contributor_email

        new_cafe = Cafe(
            name=name,
            map_url=map_url,
            img_name=uploaded['id'],
            location=location,
            has_sockets=has_sockets,
            has_toilet=has_toilets,
            has_wifi=has_wifi,
            can_take_calls=can_take_calls,
            seats=seat_data_format(seats_min, seats_max),
            coffee_price=f'{currency}{price}',
            contributor_name=new_contributor,
            contributor_email=new_contributor_email,
        )
        db.session.add(new_cafe)
        db.session.commit()
        return True

    elif not allowed_file(filename):
        return False


def search_algorithms(search_data, base_data):
    list_search = [*search_data]
    modified_search = [x.lower() for x in [word for word in list_search if word != ' ']]
    response_data = []

    for data in base_data:
        if modified_search == [y.lower() for y in [word for word in [*data.name] if word != ' ']]:
            response_data.append(data)
            return response_data
        else:
            pass

    sub_list = []
    words_data = []
    words_data_base = []
    words_list_search = []
    data_index = []
    response_data_index = []
    for _ in list_search[:-1]:
        if _ != " ":
            sub_list.append(_.lower())
        elif _ == " ":
            words_list_search.append(sub_list)
            sub_list = []
    for _ in list_search[-1:]:
        sub_list.append(_.lower())
        words_list_search.append(sub_list)
        sub_list = []
    for data in base_data:
        for _ in [*data.name]:
            if _ != " ":
                sub_list.append(_.lower())
            elif _ == " ":
                words_data.append(sub_list)
                sub_list = []
        words_data.append(sub_list)
        sub_list = []
        words_data_base.append(words_data)
        words_data = []
    for _ in words_data_base:
        for word in words_list_search:
            if word in _:
                data_index.append(words_data_base.index(_))
    if len(data_index) > 0:
        [response_data_index.append(x) for x in data_index if x not in response_data_index]
        for _ in response_data_index:
            response_data.append(base_data[_])
        return response_data
    elif len(data_index) == 0:
        return response_data


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
    data = db.session.execute(db.select(Cafe))
    chunks = data.scalars().all()
    return render_template("base.html", all_cafes=chunks, filter_id=1, no_data=0, total_cafe_no=total_cafe_no)


@app.route('/filtered/<filter>', methods=['GET', 'POST'])
def filter_cafes(filter):
    total_cafe_no = len(db.session.execute(db.select(Cafe)).scalars().all())
    if request.method == "POST":
        if request.form.get('search') == 'search':
            return redirect(url_for('search_cafes', search=request.form.get('search-data')))
    if filter == 'has_wifi':
        chunks = Cafe.query.filter_by(has_wifi=1).all()
        return render_template("base.html", all_cafes=chunks, filter_id=2, no_data=0, total_cafe_no=total_cafe_no)
    if filter == 'has_sockets':
        chunks = Cafe.query.filter_by(has_sockets=1).all()
        return render_template("base.html", all_cafes=chunks, filter_id=3, no_data=0, total_cafe_no=total_cafe_no)
    if filter == 'has_toilet':
        chunks = Cafe.query.filter_by(has_toilet=1).all()
        return render_template("base.html", all_cafes=chunks, filter_id=4, no_data=0, total_cafe_no=total_cafe_no)
    if filter == 'can_take_calls':
        chunks = Cafe.query.filter_by(can_take_calls=1).all()
        return render_template("base.html", all_cafes=chunks, filter_id=5, no_data=0, total_cafe_no=total_cafe_no)


@app.route('/search/<search>', methods=['GET', 'POST'])
def search_cafes(search):
    total_cafe_no = len(db.session.execute(db.select(Cafe)).scalars().all())
    if request.method == "POST":
        if request.form.get('search') == 'search':
            return redirect(url_for('search_cafes', search=request.form.get('search-data')))
    data = db.session.execute(db.select(Cafe))
    chunks = search_algorithms(search_data=search, base_data=data.scalars().all())
    if len(chunks) > 0:
        return render_template("base.html", all_cafes=chunks, filter_id='search', no_data=0,
                               total_cafe_no=total_cafe_no, searchvalue=search)
    elif len(chunks) == 0:
        return render_template("base.html", all_cafes=chunks, filter_id='search', no_data=1,
                               total_cafe_no=total_cafe_no, searchvalue=search)


@app.route('/contribution/add-cafe', methods=['GET', 'POST'])
def add_cafe():
    return render_template('base.html', form_id=1)


@app.route('/contribution/success', methods=['GET', 'POST'])
def cafe_added():
    if request.method == "POST":
        img_file = request.files['img-file']
        if request.form.get('submit') == 'submit':
            if check_if_exists(request.form.get('cafe-name')):
                flash("Cafe already exists (●'◡'●)", "already_exist_error")
                return redirect(url_for('add_cafe'))

            elif add_cafe_data(img=img_file,
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
                               contributor_email=request.form.get('contributor-email')
                               ):
                return render_template('base.html', form_id=1, success=1)
            else:
                flash("The file type is not allowed >:(", "file_type_error")
                return redirect(url_for('add_cafe'))


if __name__ == "__main__":
    app.run(debug=True)
