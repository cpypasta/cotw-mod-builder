from deca.file import ArchiveFile
from deca.fast_file_2 import *
from deca.hashes import hash32_func
import struct
from enum import IntEnum
from typing import List, Optional


class PropType(IntEnum):
    type_none = 0
    type_u32 = 1
    type_f32 = 2
    type_str = 3
    type_vec2 = 4
    type_vec3 = 5
    type_vec4 = 6
    type_mat3x3 = 7  # DEPRECIATED?
    type_mat4x4 = 8
    type_array_u32 = 9
    type_array_f32 = 10
    type_array_u8 = 11
    type_depreciated_12 = 12
    type_objid = 13
    type_event = 14
    type_unk_15 = 15
    type_unk_16 = 16


k_type_none = PropType.type_none.value
k_type_u32 = PropType.type_u32.value
k_type_f32 = PropType.type_f32.value
k_type_str = PropType.type_str.value
k_type_vec2 = PropType.type_vec2.value
k_type_vec3 = PropType.type_vec3.value
k_type_vec4 = PropType.type_vec4.value
k_type_mat3x3 = PropType.type_mat3x3.value
k_type_mat4x4 = PropType.type_mat4x4.value
k_type_array_u32 = PropType.type_array_u32.value
k_type_array_f32 = PropType.type_array_f32.value
k_type_array_u8 = PropType.type_array_u8.value
k_type_depreciated_12 = PropType.type_depreciated_12.value
k_type_objid = PropType.type_objid.value
k_type_event = PropType.type_event.value
k_type_unk_15 = PropType.type_unk_15.value
k_type_unk_16 = PropType.type_unk_16.value


PropType_names = [
    'none',
    'u32',
    'f32',
    'str',
    'vec2',
    'vec3',
    'vec4',
    'mat3x3',
    'mat4x4',
    'A[u32]',
    'A[f32]',
    'A[u8]',
    'd12',
    'objid',
    'event',
    'unk_15',
    'unk_16',
]

h_prop_class = hash32_func('_class')
h_prop_class_hash = hash32_func('_class_hash')
h_prop_name = hash32_func('name')
h_prop_world = hash32_func('world')
h_prop_script = hash32_func('script')
h_prop_border = hash32_func('border')
h_prop_object_id = hash32_func('_object_id')
h_prop_label_key = hash32_func('label_key')
h_prop_note = hash32_func('note')
h_prop_spline = hash32_func('spline')
h_prop_spawn_tags = hash32_func('spawn_tags')
h_prop_model_skeleton = hash32_func('model_skeleton')
h_prop_skeleton = hash32_func('skeleton')
h_prop_need_type = hash32_func('need_type')
h_prop_start_time = hash32_func('start_time')

h_prop_item_item_id = hash32_func('[Item]  Item ID')
h_prop_ref_apex_identifier = hash32_func('[ref] apex identifier')

# guess at naming these fields
h_prop_deca_crafting_type = 0xa949bc65
h_prop_deca_cpoi_desc = 0xe6b6b3f9

class RtpcProperty:
    __slots__ = ('pos', 'name_hash', 'data_pos', 'data_raw', 'data', 'type')

    def __init__(self):
        self.pos = None
        self.name_hash = None
        self.data_pos = None
        self.data_raw = None
        self.data = None
        self.type = None

    def __repr__(self):
        data = self.data
        if self.type == k_type_objid:
            data = 'id:0x{:012X}'.format(data)
        elif self.type == k_type_event:
            data = ['ev:0x{:012X}'.format(d) for d in data]

        return '@0x{:08x}({: 8d}) 0x{:08x} 0x{:08x} 0x{:02x} {:6s} = @0x{:08x}({: 8d}) {} '.format(
            self.pos, self.pos,
            self.name_hash,
            self.data_raw,
            self.type,
            PropType_names[self.type],
            self.data_pos, self.data_pos,
            data)
        # return '0x{:08x}: {} = {}'.format(self.name_hash, PropType.type_names[self.type], self.data,)


class RtpcNode:
    __slots__ = (
        'name_hash', 'data_offset', 'prop_count', 'child_count', 'prop_table', 'prop_map', 'child_table', 'child_map'
    )

    def __init__(self):
        self.name_hash = None
        self.data_offset = None
        self.prop_count = None
        self.child_count = None
        self.prop_table: List[RtpcProperty] = []
        self.prop_map = {}
        self.child_table: List[RtpcNode] = []
        self.child_map = {}

    def __repr__(self):
        return '{:08x} pc:{} cc:{} @ {} {:08x}'.format(
            self.name_hash, self.prop_count, self.child_count, self.data_offset, self.data_offset)

    def repr_with_name(self):
        name = f'0x{self.name_hash:08x}'
        return 'n:{} pc:{} cc:{} @ {} {:08x}'.format(
            name, self.prop_count, self.child_count, self.data_offset, self.data_offset)


class Rtpc:
    def __init__(self):
        self.magic = None
        self.version = None
        self.root_node: Optional[RtpcNode] = None


def rtpc_prop_from_binary(f, prop):
    prop.pos = f.tell()
    prop.name_hash = f.read_u32()
    prop.data_pos = f.tell()
    prop.data_raw = f.read_u32()
    prop.type = f.read_u8()

    prop.data = prop.data_raw

    raw_buf = struct.pack('I', prop.data_raw)
    if prop.type == k_type_none:
        pass
    elif prop.type == k_type_u32:
        prop.data = struct.unpack('I', raw_buf)[0]
    elif prop.type == k_type_f32:
        prop.data = struct.unpack('f', raw_buf)[0]
    elif prop.type == k_type_str:
        opos = f.tell()
        prop.data_pos = prop.data_raw
        f.seek(prop.data_raw)
        prop.data = f.read_strz()
        f.seek(opos)
    elif prop.type == k_type_vec2:
        opos = f.tell()
        prop.data_pos = prop.data_raw
        f.seek(prop.data_raw)
        prop.data = list(f.read_f32(2))
        f.seek(opos)
    elif prop.type == k_type_vec3:
        opos = f.tell()
        prop.data_pos = prop.data_raw
        f.seek(prop.data_raw)
        prop.data = list(f.read_f32(3))
        f.seek(opos)
    elif prop.type == k_type_vec4:
        opos = f.tell()
        prop.data_pos = prop.data_raw
        f.seek(prop.data_raw)
        prop.data = list(f.read_f32(4))
        f.seek(opos)
    elif prop.type == k_type_mat3x3:
        opos = f.tell()
        prop.data_pos = prop.data_raw
        f.seek(prop.data_raw)
        prop.data = list(f.read_f32(9))
        f.seek(opos)
    elif prop.type == k_type_mat4x4:
        opos = f.tell()
        prop.data_pos = prop.data_raw
        f.seek(prop.data_raw)
        prop.data = list(f.read_f32(16))
        f.seek(opos)
    elif prop.type == k_type_array_u32:
        opos = f.tell()
        prop.data_pos = prop.data_raw
        f.seek(prop.data_raw)
        n = f.read_u32()
        prop.data = []
        if n > 0:
            prop.data = list(f.read_u32(n))
        f.seek(opos)
    elif prop.type == k_type_array_f32:
        opos = f.tell()
        prop.data_pos = prop.data_raw
        f.seek(prop.data_raw)
        n = f.read_u32()
        prop.data = []
        if n > 0:
            prop.data = list(f.read_f32(n))
        f.seek(opos)
    elif prop.type == k_type_array_u8:
        opos = f.tell()
        prop.data_pos = prop.data_raw
        f.seek(prop.data_raw)
        n = f.read_u32()
        prop.data = []
        if n > 0:
            prop.data = list(f.read_u8(n))
        f.seek(opos)
    elif prop.type == k_type_objid:
        opos = f.tell()
        prop.data_pos = prop.data_raw
        f.seek(prop.data_raw)
        prop.data = f.read_u64()
        f.seek(opos)
    elif prop.type == k_type_event:
        opos = f.tell()
        prop.data_pos = prop.data_raw
        f.seek(prop.data_raw)
        n = f.read_u32()
        prop.data = []
        for i in range(n):
            prop.data.append(f.read_u64())
        f.seek(opos)
    elif prop.type == k_type_unk_15:
        pass
    elif prop.type == k_type_unk_16:
        pass
    else:
        raise Exception('NOT HANDLED {}'.format(prop.type))


def rtpc_node_from_binary(f, node):
    node.name_hash = f.read_u32()
    node.data_offset = f.read_u32()
    node.prop_count = f.read_u16()
    node.child_count = f.read_u16()

    old_p = f.tell()
    f.seek(node.data_offset)
    # read properties
    node.prop_table = []
    for i in range(node.prop_count):
        prop = RtpcProperty()
        rtpc_prop_from_binary(f, prop)
        node.prop_table.append(prop)
        node.prop_map[prop.name_hash] = prop

    #  children 4-byte aligned
    pos = f.tell()
    f.seek(pos + (4 - (pos % 4)) % 4)

    # read children
    node.child_table = []
    for i in range(node.child_count):
        child = RtpcNode()
        rtpc_node_from_binary(f, child)
        node.child_table.append(child)
        node.child_map[child.name_hash] = child

    f.seek(old_p)


def rtpc_from_binary(f_raw, rtpc: Optional[Rtpc] = None):
    if rtpc is None:
        rtpc = Rtpc()

    f = ArchiveFile(f_raw)

    rtpc.magic = f.read_strl(4)
    if rtpc.magic != b'RTPC':
        raise Exception('Bad MAGIC {}'.format(rtpc.magic))

    rtpc.version = f.read_u32()

    rtpc.root_node = RtpcNode()
    rtpc_node_from_binary(f, rtpc.root_node)

    return rtpc
