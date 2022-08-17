# -*- coding: utf-8 -*-
# @Time    : 2022/8/17 4:15 PM
# @FileName: build_xml.py
# @Software: PyCharm
import os.path
from xml.etree.ElementTree import ElementTree


def change_node_properties(nodelist, kv_map, is_delete=False):
    for node in nodelist:
        for key in kv_map:
            if is_delete:
                if key in node.attrib:
                    del node.attrib[key]
            else:
                node.set(key, kv_map.get(key))


def read_xml(in_path):
    tree = ElementTree()
    tree.parse(in_path)
    return tree


def find_nodes(tree, path):
    return tree.findall(path)


def get_node_by_key_value(nodelist, kv_map):
    result_nodes = []
    for node in nodelist:
        if if_match(node, kv_map):
            result_nodes.append(node)
    return result_nodes


def if_match(node, kv_map):
    for key in kv_map:
        if node.get(key) != kv_map.get(key):
            return False
    return True


def del_node(parent_nodes, child_nodes):
    for child_node in child_nodes:
        if child_node in parent_nodes:
            parent_nodes.remove(child_node)
    return parent_nodes


def write_xml(tree, out_path):
    tree.write(out_path, encoding="utf-8", xml_declaration=True)


def check_web_dir(out_path):
    return os.path.exists(os.path.join(out_path, "src2", "BOOT-INF"))


def check_tomcat_dir(tomcat_path):
    return os.path.exists(tomcat_path)


def build_ant_xml(xml_path, out_path, tomcat_path):
    tree = read_xml(xml_path)

    property_nodes = find_nodes(tree, "property")
    web_dir_property_node = get_node_by_key_value(property_nodes, {"name": "web.dir"})
    tomcat_dir_property_node = get_node_by_key_value(property_nodes, {"name": "tomcat.dir"})

    pathelement_nodes = find_nodes(tree, "pathelement")
    web_dir_pathelement_node = get_node_by_key_value(pathelement_nodes, {"path": "${web.dir}/classes"})
    tomcat_dir_pathelement_node = get_node_by_key_value(pathelement_nodes, {"path": "${tomcat.home}/lib"})

    fileset_nodes = find_nodes(tree, "fileset")
    web_dir_fileset_node = get_node_by_key_value(fileset_nodes, {"dir": "${web.dir}/lib"})
    tomcat_dir_fileset_lib_node = get_node_by_key_value(fileset_nodes, {"dir": "${tomcat.home}/lib"})
    tomcat_dir_fileset_bin_node = get_node_by_key_value(fileset_nodes, {"dir": "${tomcat.home}/bin"})
    if check_web_dir(out_path):
        change_node_properties(web_dir_property_node, {"value": "src2/BOOT-INF"})
    else:
        del_node(property_nodes, web_dir_property_node)
        del_node(pathelement_nodes, web_dir_pathelement_node)
        del_node(fileset_nodes, web_dir_fileset_node)

    if tomcat_path is False or check_tomcat_dir(tomcat_path) is False:
        del_node(property_nodes, tomcat_dir_property_node)
        del_node(pathelement_nodes, tomcat_dir_pathelement_node)
        del_node(fileset_nodes, tomcat_dir_fileset_bin_node)
        del_node(fileset_nodes, tomcat_dir_fileset_lib_node)
    else:
        change_node_properties(tomcat_dir_property_node, {"value", tomcat_path})

    write_xml(tree, os.path.join(out_path, "build.xml"))