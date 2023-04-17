from flask import jsonify, request
from flask.views import MethodView
from models import Advertisements
from models import Advertisements, Session
import requests
from schema import CreateAdvertisements, PatchAdvertisements
from server import HttpError, get_advertisements, validate
from sqlalchemy.exc import IntegrityError



class AdvertisementsView(MethodView):

    def get(self, advertisements_id: int):

        with Session as session:
            advertisement = get_advertisements(advertisements_id, session)
            return jsonify({
                'id': advertisement.id,
                'header': advertisement.header,
                'description': advertisement.description,
                'creation_time': advertisement.creation_time.isoformat(),
                'owner': advertisement.owner
                            })


    def post(self):

        json_data = validate(request.json, CreateAdvertisements)
        with Session as session:
            new_advertisement = Advertisements(**json_data)
            session.add(new_advertisement)
            try:
                session.commit()
            except IntegrityError as err:
                raise HttpError(409, 'advertisement already exist')
            return jsonify({
                        'id': new_advertisement.id

                            })

    def patch(self, advertisements_id: int):
                 
        json_data = validate(request.json, PatchAdvertisements)      
        with Session as session:
            advertisement = get_advertisements(advertisements_id, session)
            for field, value in json_data.items():
                setattr(advertisement, field, value)
                session.commit()

            return jsonify({
                'header': advertisement.header,
                'description': advertisement.description,
                'creation_time': advertisement.creation_time.isoformat(),
                'owner': advertisement.owner
                            })




    def delete(self, advertisements_id: int):
        with Session as session:
            advertisement = get_advertisements(advertisements_id, session)
            session.delete(advertisement)
            session.commit()

            return jsonify({
                    'status': 'success'
                           })













