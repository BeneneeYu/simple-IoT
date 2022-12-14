# automatically generated by the FlatBuffers compiler, do not modify

# namespace: CustomAppProto

import flatbuffers
from flatbuffers.compat import import_numpy
np = import_numpy()

class MilkDetail(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAs(cls, buf, offset=0):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = MilkDetail()
        x.Init(buf, n + offset)
        return x

    @classmethod
    def GetRootAsMilkDetail(cls, buf, offset=0):
        """This method is deprecated. Please switch to GetRootAs."""
        return cls.GetRootAs(buf, offset)
    # MilkDetail
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # MilkDetail
    def Name(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.String(o + self._tab.Pos)
        return None

    # MilkDetail
    def Quantity(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Float32Flags, o + self._tab.Pos)
        return 0.0

def MilkDetailStart(builder): builder.StartObject(2)
def Start(builder):
    return MilkDetailStart(builder)
def MilkDetailAddName(builder, name): builder.PrependUOffsetTRelativeSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(name), 0)
def AddName(builder, name):
    return MilkDetailAddName(builder, name)
def MilkDetailAddQuantity(builder, quantity): builder.PrependFloat32Slot(1, quantity, 0.0)
def AddQuantity(builder, quantity):
    return MilkDetailAddQuantity(builder, quantity)
def MilkDetailEnd(builder): return builder.EndObject()
def End(builder):
    return MilkDetailEnd(builder)