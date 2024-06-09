import io
from PIL import Image
from decouple import config
# ========= used for img cloud storage
# from googleapiclient.http import MediaIoBaseUpload
from werkzeug.utils import secure_filename


class SeatsFilter:
    def __init__(self, seats, base_data):
        self.seats = seats
        self.base_data = base_data
        self.response_data = []

    def seats_filter(self):
        for data in self.base_data:
            if 0 <= self.seats <= int(data.seats.split('-')[-1]):
                self.response_data.append(data)
        return self.response_data


class SearchAlgorithm:
    def __init__(self, search_data, base_data):
        self.search_data = search_data
        self.base_data = base_data
        self.response_data = []

    def search(self):
        list_search = [*self.search_data]
        modified_search = [x.lower() for x in [word for word in list_search if word != ' ']]

        for data in self.base_data:
            if modified_search == [y.lower() for y in [word for word in [*data.name] if word != ' ']]:
                self.response_data.append(data)
                return self.response_data
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
        for data in self.base_data:
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
                self.response_data.append(self.base_data[_])
            return self.response_data
        elif len(data_index) == 0:
            return self.response_data


# Used to check if the uploaded img is in the allowed file in which manipulates the filename which is not a proper way
# Changed it by using the flask file.mimetype

# def allowed_file(filename):
#     """ takes the last part of the filename (extension) and checks if it is part of ALLOWED_EXTENSIONS"""
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'jpg', 'jpeg', 'png'}


def boolean_to_binary(var):
    if var == 'on':
        return 1
    else:
        return 0


def seat_data_format(_seat_min, _seat_max):
    return f"{eval(_seat_min.replace('{', '').replace('}', '').replace('<', '').replace(' ', ''))}-{eval(_seat_max.replace('{', '').replace('}', '').replace('<', '').replace(' ', ''))}"

# ====================== Used for cloud storage of cafe images with GOOGLE DRIVE API =========================#
# #===================== but changed it to storing images in the database as a blob ==========================#

# def staging_and_upload(img, filename, folder_id, service):
#     def compress_img(image):
#         if len(image.fp.read()) > 3000000:
#             width, height = image.size
#             new_size = (width // 2, height // 2)
#             compressed_img = image.resize(new_size, resample=1)
#             compressed_img.save(io.BytesIO(request_img_content), format=image.format, optimize=True, quality=80)
#         return image
#
#     request_img_content = img.read()
#     with Image.open(io.BytesIO(request_img_content), mode='r') as opened_image:
#         request_img_content = image_to_byte_array(compress_img(opened_image))
#         mime_type = mime_type_identify(filename)
#         file_metadata = {
#             'name': filename,
#             'parents': [folder_id]
#         }
#         media_content = MediaIoBaseUpload(io.BytesIO(request_img_content), mimetype=mime_type)
#
#         uploaded = service.files().create(
#             body=file_metadata,
#             media_body=media_content,
#         ).execute()
#         return uploaded

# ======================= previous version of mime type identifier =========================== #
# def mime_type_identify(file_n):
#     file_type = '.' in file_n and file_n.rsplit('.', 1)[1].lower()
#     if file_type == 'jpeg' or file_type == 'jpg':
#         return 'image/jpeg'
#     elif file_type == 'png':
#         return 'image/png'

# used for converting an filestorage image file to a bytes file =========================== #
# def image_to_byte_array(image: Image) -> bytes:
#     # BytesIO is a file-like buffer stored in memory
#     imgbytearr = io.BytesIO()
#     # image.save expects a file-like as an argument
#     image.save(imgbytearr, format=image.format)
#     # Turn the BytesIO object back into a bytes object
#     imgbytearr = imgbytearr.getvalue()
#     return imgbytearr


def img_handler(image, img_size):
    pillow_img = Image.open(image).convert("RGB")
    fake_file = io.BytesIO()
    if img_size > 2000000:
        pillow_img.save(fake_file, format=Image.open(image).format, optimize=True, quality=50)
    else:
        pillow_img.save(fake_file, format=Image.open(image).format, optimize=True)
    return fake_file


class CafeSubmission:
    def __init__(self):
        self.allowed_file_type = ['image/jpg', 'image/jpeg', 'image/png']
        self.folder_id = config('IMG_FOLDER_ID')

    def add_cafe_data(self, img, img_size, name, location, map_url, currency, price, seats_min, seats_max, wifi, sockets, toilet,
                      calls, mysterious, contributor_name, contributor_email, db, cafe):
        filename = secure_filename(img.filename)
        mimetype = img.mimetype
        cafe_img_size = img_size

        has_wifi = boolean_to_binary(wifi)
        has_sockets = boolean_to_binary(sockets)
        has_toilets = boolean_to_binary(toilet)
        can_take_calls = boolean_to_binary(calls)

        if mimetype in self.allowed_file_type:
            # uploaded = staging_and_upload(img=img, filename=filename, folder_id=self.folder_id, service=service)
            cafe_img = img_handler(img, cafe_img_size).getvalue()

            new_contributor = 'None'
            new_contributor_email = 'None'
            if mysterious != 'on':
                new_contributor = contributor_name
                new_contributor_email = contributor_email

            new_cafe = cafe(
                name=name,
                map_url=map_url,
                img=cafe_img,
                img_name=filename,
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

        else:
            return False
