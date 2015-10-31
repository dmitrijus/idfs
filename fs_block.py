#'data_tree': 'b-tree-node' of 'data_node or data_tree',
#'data_node': '....',
#'directory_content:' 'filename atime ctime mtime file_size data_id unix_perm unix_owner unix_gruop tag1=x tab2=b ....', ...

import xdrlib

from collections import namedtuple

DirectoryEntry = namedtuple('DirectoryEntry', 'filename data_id atime ctime mtime file_size unix_perm unix_owner unix_group tags')
FileEntry = namedtuple('FileEntry', 'bytes')

class PackerException(Exception):
    pass

class Packer(object):
    __types__ = {
        0x0100: DirectoryEntry,
        0x0200: FileEntry,
    }

    def __init__(self):
        pass

    def pack_directory_entry(self, de):
        p = xdrlib.Packer()
        p.pack_uint(0x0100)

        p.pack_string(de.filename)
        p.pack_string(de.data_id)

        p.pack_uhyper(de.atime)
        p.pack_uhyper(de.ctime)
        p.pack_uhyper(de.mtime)
        p.pack_uhyper(de.file_size)

        p.pack_uint(de.unix_perm)
        p.pack_uint(de.unix_owner)
        p.pack_uint(de.unix_group)

        p.pack_opaque(de.tags)
        return p.get_buffer()

    def unpack_directory_entry(self, data):
        """
            >>> de = DirectoryEntry('test', 'key_id', 0, 0, 0, 15, 01777, 0, 0, "")
            >>> b1 = Packer().pack_directory_entry(de)
            >>> len(b1) > 0
            True
            >>> de1 = Packer().unpack_directory_entry(b1)
            >>> de == de1
            True
        """

        p = xdrlib.Unpacker(data)
        assert p.unpack_uint() == 0x0100

        value_tuple = (
            p.unpack_string(),  # filename
            p.unpack_string(),  # data_id
            p.unpack_uhyper(),  # atime
            p.unpack_uhyper(),  # ctime
            p.unpack_uhyper(),  # mtime
            p.unpack_uhyper(),  # file_size
            p.unpack_uint(),    # unix_perm
            p.unpack_uint(),    # unix_owner
            p.unpack_uint(),    # unix_group
            p.unpack_opaque(),    # tags
        )

        return DirectoryEntry(*value_tuple)

    def pack_file_entry(self, fe):
        """
       """

        p = xdrlib.Packer()
        p.pack_uint(0x0200)
        p.pack_fopaque(len(fe.bytes), fe.bytes, )

        return p.get_buffer()

    def unpack_file_entry(self, data):
        """
            >>> fe = FileEntry(bytes='hello world!')
            >>> b1 = Packer().pack_file_entry(fe)
            >>> fe1 = Packer().unpack_file_entry(b1)
            >>> fe == fe1
            True
        """

        p = xdrlib.Unpacker(data)
        assert p.unpack_uint() == 0x0200

        value_tuple = (
            p.unpack_fopaque(len(data) - 4),  # bytes
        )

        return FileEntry(*value_tuple)

    #def unpack_any(self, data):
    #    p = xdrlib.Unpacker()

    #    obj_type = p.unpack_uint()
    #    if __types__.has_key(obj_type):
    #        print obj_type

    #    else:
    #        raise PackerException("Unknown data type")
