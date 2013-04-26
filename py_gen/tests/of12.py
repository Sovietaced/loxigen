#!/usr/bin/env python
# Copyright 2013, Big Switch Networks, Inc.
#
# LoxiGen is licensed under the Eclipse Public License, version 1.0 (EPL), with
# the following special exception:
#
# LOXI Exception
#
# As a special exception to the terms of the EPL, you may distribute libraries
# generated by LoxiGen (LoxiGen Libraries) under the terms of your choice, provided
# that copyright and licensing notices generated by LoxiGen are not altered or removed
# from the LoxiGen Libraries and the notice provided below is (i) included in
# the LoxiGen Libraries, if distributed in source code form and (ii) included in any
# documentation for the LoxiGen Libraries, if distributed in binary form.
#
# Notice: "Copyright 2013, Big Switch Networks, Inc. This library was generated by the LoxiGen Compiler."
#
# You may not use this file except in compliance with the EPL or LOXI Exception. You may obtain
# a copy of the EPL at:
#
# http://www.eclipse.org/legal/epl-v10.html
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# EPL for the specific language governing permissions and limitations
# under the EPL.
import unittest

try:
    import loxi.of12 as ofp
except ImportError:
    exit("loxi package not found. Try setting PYTHONPATH.")

class TestImports(unittest.TestCase):
    def test_toplevel(self):
        import loxi
        self.assertTrue(hasattr(loxi, "ProtocolError"))
        self.assertEquals(loxi.version_names[3], "1.2")
        ofp = loxi.protocol(3)
        self.assertEquals(ofp.OFP_VERSION, 3)
        self.assertTrue(hasattr(ofp, "action"))
        self.assertTrue(hasattr(ofp, "common"))
        self.assertTrue(hasattr(ofp, "const"))
        self.assertTrue(hasattr(ofp, "message"))
        self.assertTrue(hasattr(ofp, "oxm"))

    def test_version(self):
        import loxi
        self.assertTrue(hasattr(loxi.of12, "ProtocolError"))
        self.assertTrue(hasattr(loxi.of12, "OFP_VERSION"))
        self.assertEquals(loxi.of12.OFP_VERSION, 3)
        self.assertTrue(hasattr(loxi.of12, "action"))
        self.assertTrue(hasattr(loxi.of12, "common"))
        self.assertTrue(hasattr(loxi.of12, "const"))
        self.assertTrue(hasattr(loxi.of12, "message"))
        self.assertTrue(hasattr(loxi.of12, "oxm"))

class TestCommon(unittest.TestCase):
    sample_empty_match_buf = ''.join([
        '\x00\x01', # type
        '\x00\x04', # length
        '\x00\x00\x00\x00', # padding
    ])

    def test_empty_match_pack(self):
        obj = ofp.match()
        self.assertEquals(self.sample_empty_match_buf, obj.pack())

    def test_empty_match_unpack(self):
        obj = ofp.match.unpack(self.sample_empty_match_buf)
        self.assertEquals(len(obj.oxm_list), 0)

class TestOXM(unittest.TestCase):
    def test_oxm_in_phy_port_pack(self):
        import loxi.of12 as ofp
        obj = ofp.oxm.in_phy_port(value=42)
        expected = ''.join([
            '\x80\x00', # class
            '\x02', # type/masked
            '\x04', # length
            '\x00\x00\x00\x2a' # value
        ])
        self.assertEquals(expected, obj.pack())

    def test_oxm_in_phy_port_masked_pack(self):
        import loxi.of12 as ofp
        obj = ofp.oxm.in_phy_port_masked(value=42, value_mask=0xaabbccdd)
        expected = ''.join([
            '\x80\x00', # class
            '\x03', # type/masked
            '\x08', # length
            '\x00\x00\x00\x2a', # value
            '\xaa\xbb\xcc\xdd' # mask
        ])
        self.assertEquals(expected, obj.pack())

    def test_oxm_ipv6_dst_pack(self):
        import loxi.of12 as ofp
        obj = ofp.oxm.ipv6_dst(value='\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0d\x0f')
        expected = ''.join([
            '\x80\x00', # class
            '\x36', # type/masked
            '\x10', # length
            '\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0d\x0f', # value
        ])
        self.assertEquals(expected, obj.pack())

class TestAllOF12(unittest.TestCase):
    """
    Round-trips every class through serialization/deserialization.
    Not a replacement for handcoded tests because it only uses the
    default member values.
    """

    def setUp(self):
        mods = [ofp.action,ofp.message,ofp.common,ofp.oxm]
        self.klasses = [klass for mod in mods
                              for klass in mod.__dict__.values()
                              if hasattr(klass, 'show')]
        self.klasses.sort(key=lambda x: str(x))

    def test_serialization(self):
        expected_failures = [
            ofp.common.flow_stats_entry,
            ofp.common.group_desc_stats_entry,
            ofp.common.instruction,
            ofp.common.instruction_apply_actions,
            ofp.common.instruction_clear_actions,
            ofp.common.instruction_experimenter,
            ofp.common.instruction_goto_table,
            ofp.common.instruction_header,
            ofp.common.instruction_write_actions,
            ofp.common.instruction_write_metadata,
            ofp.common.table_stats_entry,
            ofp.message.flow_add,
            ofp.message.flow_delete,
            ofp.message.flow_delete_strict,
            ofp.message.flow_modify,
            ofp.message.flow_modify_strict,
            ofp.message.group_desc_stats_reply,
            ofp.message.group_mod,
            ofp.message.group_stats_reply,
            ofp.message.packet_in,
        ]
        for klass in self.klasses:
            def fn():
                obj = klass()
                if hasattr(obj, "xid"): obj.xid = 42
                buf = obj.pack()
                obj2 = klass.unpack(buf)
                self.assertEquals(obj, obj2)
            if klass in expected_failures:
                self.assertRaises(Exception, fn)
            else:
                fn()

    def test_show(self):
        expected_failures = [
            ofp.common.table_stats_entry,
        ]
        for klass in self.klasses:
            def fn():
                obj = klass()
                if hasattr(obj, "xid"): obj.xid = 42
                obj.show()
            if klass in expected_failures:
                self.assertRaises(Exception, fn)
            else:
                fn()

if __name__ == '__main__':
    unittest.main()
