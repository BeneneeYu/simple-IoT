#  Author: Aniruddha Gokhale
#  Created: Fall 2021
#  (based on code developed for Distributed Systems course in Fall 2019)
#  Modified: Fall 2022 (changed packet name to not confuse with pub/sub Messages)
#
#  Purpose: demonstrate serialization of user-defined packet structure
#  using flatbuffers
#
#  Here our packet or message format comprises a sequence number, a timestamp,
#  and a data buffer of several uint32 numbers (whose value is not relevant to us)

import os
import sys

# this is needed to tell python where to find the flatbuffers package
# make sure to change this path to where you have compiled and installed
# flatbuffers.  If the python package is installed in your system wide files
# or virtualenv, then this may not be needed
sys.path.append(os.path.join(os.path.dirname(__file__), '/home/zhengyu/Apps/flatbuffers/python'))
import flatbuffers  # this is the flatbuffers package we import
import time  # we need this get current time
import numpy as np  # to use in our vector field

import zmq  # we need this for additional constraints provided by the zmq serialization
from applnlayer.ApplnMessageTypes import HealthStatusMessage, GroceryOrderMessage, ResponseMessage, Message  # our custom message in native format
import Serialization.FlatBuffers.CustomAppProto.HealthStatusMessage as hmsg  # this is the generated code by the flatc compiler
import Serialization.FlatBuffers.CustomAppProto.ResponseMessage as rmsg
import Serialization.FlatBuffers.CustomAppProto.GroceryOrderMessage as omsg
import Serialization.FlatBuffers.CustomAppProto.VeggieDetail as vd
import Serialization.FlatBuffers.CustomAppProto.DrinkType as dt
import Serialization.FlatBuffers.CustomAppProto.DrinkDetail as dd
import Serialization.FlatBuffers.CustomAppProto.MilkDetail as mkd
import Serialization.FlatBuffers.CustomAppProto.BreadDetail as bd
import Serialization.FlatBuffers.CustomAppProto.MeatDetail as mtd
import Serialization.FlatBuffers.CustomAppProto.Message as msg
import Serialization.FlatBuffers.CustomAppProto.Any as Any


# This is the method we will invoke from our driver program
# Note that if you have have multiple different message types, we could have
# separate such serialize/deserialize methods, or a single method can check what
# type of message it is and accordingly take actions.
# def serializeCustom(cm):
#     # first obtain the builder object that is used to create an in-memory representation
#     # of the serialized object from the custom message
#     builder = flatbuffers.Builder(0);
#     # create the name string for the name field using
#     # the parameter we passed
#     name_field = builder.CreateString(cm.name)
#     # serialize our dummy array. The sample code in Flatbuffers
#     # describes doing this in reverse order
#     msg.StartDataVector(builder, len(cm.vec))
#     for i in reversed(range(len(cm.vec))):
#         builder.PrependUint32(cm.vec[i])
#     data = builder.EndVector()
#     # let us create the serialized msg by adding contents to it.
#     # Our custom msg consists of a seq num, timestamp, name, and an array of uint32s
#     msg.Start(builder)  # serialization starts with the "Start" method
#     msg.AddSeqNo(builder, cm.seq_num)
#     msg.AddTs(builder, cm.ts)  # serialize current timestamp
#     msg.AddName(builder, name_field)  # serialize the name
#     msg.AddData(builder, data)  # serialize the dummy data
#     serialized_msg = msg.End(builder)  # get the topic of all these fields
#     # end the serialization process
#     builder.Finish(serialized_msg)
#     # get the serialized buffer
#     buf = builder.Output()
#     # return this serialized buffer to the caller
#     return buf

def serialize(mes):
    builder = flatbuffers.Builder(0)
    if isinstance(mes, GroceryOrderMessage):
        message_type = "ORDER"
        message_type_field = builder.CreateString(message_type)
        serialized_msg_data = serialize_order(builder, mes)
        msg.Start(builder)
        msg.AddMessageType(builder, message_type_field)
        msg.AddDataType(builder, Any.Any().GroceryOrderMessage)
    elif isinstance(mes, HealthStatusMessage):
        message_type = "HEALTH"
        message_type_field = builder.CreateString(message_type)
        serialized_msg_data = serialize_health(builder, mes)
        msg.Start(builder)
        msg.AddMessageType(builder, message_type_field)
        msg.AddDataType(builder, Any.Any().HealthStatusMessage)
    elif isinstance(mes, ResponseMessage):
        message_type = "RESPONSE"
        message_type_field = builder.CreateString(message_type)
        serialized_msg_data = serialize_response(builder, mes)
        msg.Start(builder)
        msg.AddMessageType(builder, message_type_field)
        msg.AddDataType(builder, Any.Any().ResponseMessage)

    msg.AddData(builder, serialized_msg_data)
    serialized_msg = msg.End(builder)
    builder.Finish(serialized_msg)
    buf = builder.Output()
    return buf


def serialize_health(bud, hm):
    # builder = flatbuffers.Builder(0)
    builder = bud
    dispenser_field = builder.CreateString(hm.dispenser)
    lightbulb_field = builder.CreateString(hm.lightbulb)
    sensor_status_field = builder.CreateString(hm.sensor_status)
    hmsg.Start(builder)
    hmsg.AddTs(builder, hm.ts)
    hmsg.AddDispenser(builder, dispenser_field)
    hmsg.AddIcemaker(builder, hm.icemaker)
    hmsg.AddLightbulb(builder, lightbulb_field)
    hmsg.AddFridgeTemp(builder, hm.fridge_temp)
    hmsg.AddFreezerTemp(builder, hm.freezer_temp)
    hmsg.AddSensorStatus(builder, sensor_status_field)
    serialized_hmsg = hmsg.End(builder)
    return serialized_hmsg
    # builder.Finish(serialized_hmsg)
    # buf = builder.Output()
    # return buf


def serialize_response(bud, rm):
    # builder = flatbuffers.Builder(0)
    builder = bud
    type_field = builder.CreateString(rm.message_type)
    code_field = builder.CreateString(rm.code)
    content_field = builder.CreateString(rm.content)

    rmsg.Start(builder)
    rmsg.AddTs(builder, rm.ts)
    rmsg.AddCode(builder, code_field)
    rmsg.AddContents(builder, content_field)
    serialized_rmsg = rmsg.End(builder)
    return serialized_rmsg
    # builder.Finish(serialized_rmsg)
    # buf = builder.Output()
    #
    # return buf


def serialize_order(bud, om):
    # builder = flatbuffers.Builder(0)
    builder = bud
    mkdmsgs = []
    for i in range(len(om.milk)):
        milkName = builder.CreateString(om.milk[i][0])
        mkd.Start(builder)
        mkd.AddName(builder, milkName)
        mkd.AddQuantity(builder, om.milk[i][1])
        mkdmsgs.append(mkd.End(builder))
    # start a vector
    omsg.StartMilkVector(builder, len(om.milk))
    # for every elem, prepend offset
    for i in range(len(mkdmsgs)):
        builder.PrependUOffsetTRelative(mkdmsgs[i])
    # use builder to finish milk array generation
    milk = builder.EndVector()

    bdmsgs = []
    for i in range(len(om.bread)):
        breadName = builder.CreateString(om.bread[i][0])
        bd.Start(builder)
        bd.AddName(builder, breadName)
        bd.AddQuantity(builder, om.bread[i][1])
        bdmsgs.append(bd.End(builder))
    omsg.StartMilkVector(builder, len(om.bread))
    for i in range(len(bdmsgs)):
        builder.PrependUOffsetTRelative(bdmsgs[i])
    bread = builder.EndVector()

    mtmsgs = []
    for i in range(len(om.meat)):
        meatName = builder.CreateString(om.meat[i][0])
        mtd.Start(builder)
        mtd.AddName(builder, meatName)
        mtd.AddQuantity(builder, om.meat[i][1])
        mtmsgs.append(mtd.End(builder))
    omsg.StartMilkVector(builder, len(om.meat))
    for i in range(len(mtmsgs)):
        builder.PrependUOffsetTRelative(mtmsgs[i])
    meat = builder.EndVector()

    vdmsgs = []
    for name, quantity in om.veggies.items():
        veggieName = builder.CreateString(name)
        vd.Start(builder)
        vd.AddName(builder, veggieName)
        vd.AddQuantity(builder, quantity)
        vdmsgs.append(vd.End(builder))

    omsg.StartMilkVector(builder, len(om.veggies))
    for i in range(len(vdmsgs)):
        builder.PrependUOffsetTRelative(vdmsgs[i])
    veggies = builder.EndVector()

    dtmsgs = []
    for name, dts in om.drinks.items():
        drink_type_name = builder.CreateString(name)
        dds = []
        for dd_name, dd_quantity in dts.items():
            drink_detail_name = builder.CreateString(dd_name)
            dd.Start(builder)
            dd.AddName(builder, drink_detail_name)
            dd.AddQuantity(builder, dd_quantity)
            dds.append(dd.End(builder))
        dt.StartQuantityVector(builder, len(dds))
        for i in range(len(dds)):
            builder.PrependUOffsetTRelative(dds[i])
        drink_details = builder.EndVector()
        dt.Start(builder)
        dt.AddName(builder, drink_type_name)
        dt.AddQuantity(builder, drink_details)
        dtmsgs.append(dt.End(builder))
    omsg.StartDrinksVector(builder, len(dtmsgs))
    for i in range(len(dtmsgs)):
        builder.PrependUOffsetTRelative(dtmsgs[i])
    drinks = builder.EndVector()

    omsg.Start(builder)
    omsg.AddTs(builder, om.ts)
    omsg.AddMilk(builder, milk)
    omsg.AddBread(builder, bread)
    omsg.AddMeat(builder, meat)
    omsg.AddVeggies(builder, veggies)
    omsg.AddDrinks(builder, drinks)
    serialized_omsg = omsg.End(builder)
    return serialized_omsg
    # builder.Finish(serialized_omsg)
    # buf = builder.Output()
    # return buf


# deserialize the incoming serialized structure into native data type
# def deserialize(buf):
#     cm = CustomMessage()
#
#     packet = msg.Message.GetRootAs(buf, 0)
#
#     # sequence number
#     cm.seq_num = packet.SeqNo()
#
#     # timestamp received
#     cm.ts = packet.Ts()
#
#     # name received
#     cm.name = packet.Name()
#
#     # received vector data
#     # We can obtain the vector like this but it changes the
#     # type from List to NumpyArray, which may not be what one wants.
#     # cm.vec = packet.DataAsNumpy ()
#     cm.vec = [packet.Data(j) for j in range(packet.DataLength())]
#
#     return cm

def deserialize(buf):
    packet = msg.Message.GetRootAs(buf, 0)
    message_data_type = packet.MessageType().decode()
    if message_data_type == "ORDER":
        om = omsg.GroceryOrderMessage()
        om.Init(packet.Data().Bytes, packet.Data().Pos)
        return deserialize_order(om)
    elif message_data_type == "HEALTH":
        hm = hmsg.HealthStatusMessage()
        hm.Init(packet.Data().Bytes, packet.Data().Pos)
        return deserialize_health(hm)
    elif message_data_type == "RESPONSE":
        rm = omsg.ResponseMessage()
        rm.Init(packet.Data().Bytes, packet.Data().Pos)
        return deserialize_response(rm)

def deserialize_order(buf):
    om = GroceryOrderMessage()
    packet = buf
    # dt_packet = dt.DrinkType.GetRootAs(buf, 0)
    om.veggies = {}
    for j in range(packet.VeggiesLength() - 1, -1, -1):
        om.veggies[packet.Veggies(j).Name().decode()] = packet.Veggies(j).Quantity()
    # om.drinks = packet.Drinks()
    om.drinks = {}
    for j in range(packet.DrinksLength() - 1, -1, -1):
        drink_detail_dict = {}
        drink_type_tmp = packet.Drinks(j)  # drink detail list
        drink_type_name = packet.Drinks(j).Name().decode()  # bottle, can
        for k in range(drink_type_tmp.QuantityLength() - 1, -1, -1):
            drink_detail_tmp = drink_type_tmp.Quantity(k)
            drink_detail_dict[drink_detail_tmp.Name().decode()] = drink_detail_tmp.Quantity()
        om.drinks[drink_type_name] = drink_detail_dict
    om.milk = [(packet.Milk(j).Name().decode(), packet.Milk(j).Quantity()) for j in range(packet.MilkLength() - 1, -1, -1)]
    om.bread = [(packet.Bread(j).Name().decode(), packet.Bread(j).Quantity()) for j in range(packet.BreadLength() - 1, -1, -1)]
    om.meat = [(packet.Meat(j).Name().decode(), packet.Meat(j).Quantity()) for j in range(packet.MeatLength() - 1, -1, -1)]
    om.ts = packet.Ts()
    return om


# deserialize the incoming serialized structure into native data type
def deserialize_health(buf):
    hm = HealthStatusMessage()

    packet = buf
    hm.dispenser = packet.Dispenser().decode()
    hm.icemaker = packet.Icemaker()
    hm.lightbulb = packet.Lightbulb().decode()
    hm.fridge_temp = packet.FridgeTemp()
    hm.freezer_temp = packet.FreezerTemp()
    hm.sensor_status = packet.SensorStatus().decode()
    hm.ts = packet.Ts()
    return hm


def deserialize_response(buf):
    rm = ResponseMessage()
    packet = buf
    rm.code = packet.Code()
    rm.contents = packet.Contents()
    rm.ts = packet.Ts()
    return rm


def deserialize_from_frames(recvd_seq):
    """ This is invoked on list of frames by zmq """

    # For this sample code, since we send only one frame, hopefully what
    # comes out is also a single frame. If not some additional complexity will
    # need to be added.
    assert (len(recvd_seq) == 1)
    # print ("type of each elem of received seq is {}".format (type (recvd_seq[i])))
    print("received data over the wire = {}".format(recvd_seq[0]))
    mes = deserialize(recvd_seq[0])  # hand it to our deserialize method

    # assuming only one frame in the received sequence, we just send this deserialized
    # custom message
    return mes


# serialize the custom message to iterable frame objects needed by zmq
def serialize_to_frames(mes):
    """ serialize into an interable format """
    # We had to do it this way because the send_serialized method of zmq under the hood
    # relies on send_multipart, which needs a list or sequence of frames. The easiest way
    # to get an iterable out of the serialized buffer is to enclose it inside []
    print("serialize custom message to iterable list")
    return [serialize(mes)]


# def deserialize(buf):
#     cm = CustomMessage()
#
#     packet = msg.Message.GetRootAs(buf, 0)
#
#     # sequence number
#     cm.seq_num = packet.SeqNo()
#
#     # timestamp received
#     cm.ts = packet.Ts()
#
#     # name received
#     cm.name = packet.Name()
#
#     # received vector data
#     # We can obtain the vector like this but it changes the
#     # type from List to NumpyArray, which may not be what one wants.
#     # cm.vec = packet.DataAsNumpy ()
#     cm.vec = [packet.Data(j) for j in range(packet.DataLength())]
#
#     return cm