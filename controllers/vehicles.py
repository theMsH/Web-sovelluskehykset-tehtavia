from flask import request, jsonify
from werkzeug.exceptions import NotFound
from decorators.db_conn import get_db_conn
from decorators.repository_decorator import init_repository
from models import Vehicle

"""
Käytän samaa logiikkaa kuin productseissa.
"""

@get_db_conn
@init_repository('vehicles')
def request_vehicles(con):
    try:
        if request.method == "GET":
            return get_vehicles(con)

        elif request.method == "POST":
            return create_vehicle(con)

    except NotFound:
        return jsonify({'err': 'vehicles not found'}), 404

    except Exception as e:
        return jsonify({'err': str(e)}), 500


def get_vehicles(con):
    vehicles = con.get_all()
    if not vehicles:
        raise NotFound
    return jsonify(Vehicle.list_to_json(vehicles)), 200

def create_vehicle(con):
    data = request.get_json()
    vehicle = Vehicle(_id=0, make=data['make'], model=data['model'])
    con.save(vehicle)
    return jsonify(Vehicle.to_json(vehicle)), 201


@get_db_conn
@init_repository('vehicles')
def request_vehicle_by_id(con, vehicle_id):
    try:
        if request.method == "GET":
            return get_vehicle_by_id(con, vehicle_id)

        elif request.method == "PUT":
            return update_vehicle_by_id(con, vehicle_id)

        elif request.method == "DELETE":
            return delete_vehicle_by_id(con, vehicle_id)

    except NotFound:
        return jsonify({'err': 'vehicle not found'}), 404

    except Exception as e:
        return jsonify({'err': str(e)}), 500


def get_vehicle_by_id(con, vehicle_id):
    vehicle = con.get_by_id(vehicle_id)
    if vehicle is None:
        raise NotFound
    return jsonify(Vehicle.to_json(vehicle)), 200

def update_vehicle_by_id(con, vehicle_id):
    vehicle: Vehicle = con.get_by_id(vehicle_id)
    data = request.get_json()
    vehicle.make = data["make"]
    vehicle.model = data["model"]
    con.save(vehicle)
    return jsonify(Vehicle.to_json(vehicle)), 200

def delete_vehicle_by_id(con, vehicle_id):
    con.delete_by_id(vehicle_id)
    return jsonify(), 204
