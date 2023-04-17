from flask import Flask, jsonify, request
from flask.views import MethodView
from models import Advertisements, Session
from views import AdvertisementsView
import pydantic
from schema import PatchAdvertisements, CreateAdvertisements
from typing import Type


app = Flask('app')

def validate(json_data: dict, model_class: Type[CreateAdvertisements] | Type[CreateAdvertisements]):
    try:
        model_item = model_class(**json_data)
        return model_item.dict(exclude_none=True)
    except pydantic.ValidationError as err:
        raise HttpError(400, err.errors())

class HttpError(Exception):

    def __init__(self, status_code: int, message: dict | list | str):
        status_code = self.status_code
        message = self.message

@app.errorhandler
def error_handler(error: HttpError):
    
    response = jsonify({'status':'error', 'message': error.message})
    response.status_code = error.status_code

    return response

def get_advertisements(advertisements_id: int, session: Session):

    advertisement = session.get(Advertisements, advertisements_id)
    if advertisement is None:
        raise HttpError(404, message='advertisement not found')

    return advertisement




app.add_url_rule('/advertisements/<int:advertisements_id>/', view_func=AdvertisementsView.as_view('advertisements_exist'), methods=['GET', 'PATCH', 'DELETE'])
app.add_url_rule('/advertisements/', view_func=AdvertisementsView.as_view('advertisements_create'), methods=['POST'])


if __name__  == '__main__':
    app.run()