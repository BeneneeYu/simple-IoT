# automatically generated by the FlatBuffers compiler, do not modify

# namespace: CustomAppProto

import flatbuffers
from flatbuffers.compat import import_numpy
np = import_numpy()

class DrinkType(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAs(cls, buf, offset=0):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = DrinkType()
        x.Init(buf, n + offset)
        return x

    @classmethod
    def GetRootAsDrinkType(cls, buf, offset=0):
        """This method is deprecated. Please switch to GetRootAs."""
        return cls.GetRootAs(buf, offset)
    # DrinkType
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # DrinkType
    def Name(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.String(o + self._tab.Pos)
        return None

    # DrinkType
    def Quantity(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            x = self._tab.Vector(o)
            x += flatbuffers.number_types.UOffsetTFlags.py_type(j) * 4
            x = self._tab.Indirect(x)
            from CustomAppProto.DrinkDetail import DrinkDetail
            obj = DrinkDetail()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # DrinkType
    def QuantityLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # DrinkType
    def QuantityIsNone(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        return o == 0

def DrinkTypeStart(builder): builder.StartObject(2)
def Start(builder):
    return DrinkTypeStart(builder)
def DrinkTypeAddName(builder, name): builder.PrependUOffsetTRelativeSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(name), 0)
def AddName(builder, name):
    return DrinkTypeAddName(builder, name)
def DrinkTypeAddQuantity(builder, quantity): builder.PrependUOffsetTRelativeSlot(1, flatbuffers.number_types.UOffsetTFlags.py_type(quantity), 0)
def AddQuantity(builder, quantity):
    return DrinkTypeAddQuantity(builder, quantity)
def DrinkTypeStartQuantityVector(builder, numElems): return builder.StartVector(4, numElems, 4)
def StartQuantityVector(builder, numElems):
    return DrinkTypeStartQuantityVector(builder, numElems)
def DrinkTypeEnd(builder): return builder.EndObject()
def End(builder):
    return DrinkTypeEnd(builder)