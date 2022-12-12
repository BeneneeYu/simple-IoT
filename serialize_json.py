#  Author: Aniruddha Gokhale
#  Created: Fall 2022
#  (based on code developed for Distributed Systems course in Fall 2019)
#
#  Purpose: demonstrate serialization of user-defined packet structure
#  using JSON
#
#  Here our packet or message format comprises a sequence number, a timestamp,
#  and a data buffer of several uint32 numbers (whose value is not relevant to us)

import os
import sys

import json  # JSON package

from applnlayer.ApplnMessageTypes import HealthStatusMessage, GroceryOrderMessage, ResponseMessage, \
    Message  # our custom message in native format


# This is the method we will invoke from our driver program to convert a data structure
# in native format to JSON


def serialize_to_json(mes):
    # create a JSON representation from the original data structure
    if isinstance(mes, GroceryOrderMessage):
        json_buf = serializeOrder(mes)
    elif isinstance(mes, HealthStatusMessage):
        json_buf = serializeHealth(mes)
    elif isinstance(mes, ResponseMessage):
        json_buf = serializeResponse(mes)
    else:
        json_buf = serializeCustom(mes)
    # return the underlying jsonified buffer
    return json_buf


def serialize(mes):
    return bytes(serialize_to_json(mes), "utf-8")


# deserialize the incoming serialized structure into native data type
def deserialize(buf):
    json_buf = json.loads(buf)
    mt = json_buf["message_type"]
    if mt == "ORDER":
        mes = deserializeOrder(json_buf)
    elif mt == "HEALTH":
        mes = deserializeHealth(json_buf)
    elif mt == "RESPONSE":
        mes = deserializeResponse(json_buf)
    else:
        pass
    return mes


def serializeOrder(om):
    json_buf = {
        "message_type": "ORDER",
        "ts": om.ts,
        "veggies": om.veggies,
        "drinks": om.drinks,
        "milk": om.milk,
        "bread": om.bread,
        "meat": om.meat,
    }
    return json.dumps(json_buf)


def serializeHealth(ho):
    json_buf = {
        "message_type": "HEALTH",
        "ts": ho.ts,
        "dispenser": ho.dispenser,
        "icemaker": ho.icemaker,
        "lightbulb": ho.lightbulb,
        "fridge_temp": ho.fridge_temp,
        "freezer_temp": ho.freezer_temp,
        "sensor_status": ho.sensor_status
    }
    return json.dumps(json_buf)


def serializeResponse(rm):
    json_buf = {
        "message_type": "RESPONSE",
        "ts": rm.ts,
        "code": rm.code,
        "contents": rm.contents
    }
    return json.dumps(json_buf)


def deserializeOrder(json_buf):
    om = GroceryOrderMessage()
    om.ts = json_buf["ts"]
    om.message_type = json_buf["message_type"]
    om.veggies = json_buf["veggies"]
    om.drinks = json_buf["drinks"]
    om.milk = json_buf["milk"]
    om.bread = json_buf["bread"]
    om.meat = json_buf["meat"]
    return om


def deserializeHealth(json_buf):
    hm = HealthStatusMessage()
    hm.ts = json_buf["ts"]
    hm.message_type = json_buf["message_type"]
    hm.dispenser = json_buf["dispenser"]
    hm.icemaker = json_buf["icemaker"]
    hm.lightbulb = json_buf["lightbulb"]
    hm.fridge_temp = json_buf["fridge_temp"]
    hm.freezer_temp = json_buf["freezer_temp"]
    hm.sensor_status = json_buf["sensor_status"]
    return hm


def deserializeResponse(json_buf):
    rm = ResponseMessage()
    rm.ts = json_buf["ts"]
    rm.message_type = json_buf["message_type"]
    rm.code = json_buf["code"]
    rm.contents = json_buf["contents"]
    return rm


def serializeCustom(cm):
    # create a JSON representation from the original data structure
    json_buf = {
        "seq_num": cm.seq_num,
        "timestamp": cm.ts,
        "name": cm.name,
        "vector": cm.vec,
        "message_type": cm.message_type
    }

    # return the underlying jsonified buffer
    return json.dumps(json_buf)
