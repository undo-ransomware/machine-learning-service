import json
from marshmallow import pprint
from flask import Blueprint, request
from flask import Response
from sqlalchemy import exc
from application.models.detection_schema import DetectionSchema
from application.models.detection import db, Detection

detection_api = Blueprint('detection_api', __name__)

@detection_api.route("")
def findAll(userId = None):
    schema = DetectionSchema(many=True)
    userId = request.args.get('userId', default = None)
    if userId is not None:
        detections = Detection.query.all()
    else:
        detections = Detection.query.filter_by(userId = userId)
    return Response(schema.dumps(detections), status=200, mimetype='application/json')

@detection_api.route("/<int:id>")
def find(id):
    schema = DetectionSchema()
    detection = Detection.query.get(id)
    if detection is None:
        return Response(status=404, mimetype='application/json')
    else:
        return Response(schema.dumps(detection), status=200, mimetype='application/json')

@detection_api.route("/<int:id>", methods=['DELETE'])
def delete(id):
    detection = Detection.query.get(id)
    if detection is None:
        return Response(status=404, mimetype='application/json')
    else:
        db.session.delete(detection)
        db.session.commit()
        return Response('', status=200, mimetype='application/json')