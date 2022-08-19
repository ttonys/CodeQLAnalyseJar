# -*- coding: utf-8 -*-
# @Time    : 2022/8/17 4:15 PM
# @FileName: build_xml.py
# @Software: PyCharm
import os.path
from xml.etree.ElementTree import ElementTree, Element


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


def add_child_node(nodelist, element):
    for node in nodelist:
        node.append(element)


def create_node(tag, property_map, content):
    element = Element(tag, property_map)
    element.text = content
    return element


def check_web_dir(out_path):
    return os.path.exists(os.path.join(out_path, "src2", "BOOT-INF"))


def check_tomcat_dir(tomcat_path):
    return os.path.exists(tomcat_path)


def build_ant_xml(xml_path, out_path, tomcat_path):
    tree = read_xml(xml_path)

    property_nodes = find_nodes(tree, "property")
    web_dir_property_node = get_node_by_key_value(property_nodes, {"name": "web.dir"})
    tomcat_dir_property_node = get_node_by_key_value(property_nodes, {"name": "tomcat.dir"})

    if check_web_dir(out_path):
        change_node_properties(web_dir_property_node, {"value": "src2/BOOT-INF"})
        node1 = create_node("pathelement", {"path": "${web.dir}/classes"}, "")
        node2 = create_node("fileset", {"dir": "${web.dir}/lib"}, "")
        add_child_node(tree.getroot().findall(".//path"), node1)
        add_child_node(tree.getroot().findall(".//path"), node2)

    if tomcat_path:
        change_node_properties(tomcat_dir_property_node, {"value": tomcat_path})
        node1 = create_node("pathelement", {"path": "${tomcat.dir}/lib"}, "")
        node2 = create_node("fileset", {"dir": "${tomcat.dir}/lib"}, "")
        node3 = create_node("fileset", {"dir": "${tomcat.dir}/bin"}, "")

        add_child_node(tree.getroot().findall(".//path"), node1)
        add_child_node(tree.getroot().findall(".//path"), node2)
        add_child_node(tree.getroot().findall(".//path"), node3)

    if check_web_dir(out_path) or tomcat_path:
        node = create_node("include", {"name": "*.jar"}, "")
        add_child_node(tree.getroot().findall(".//path/fileset"), node)

    write_xml(tree, os.path.join(out_path, "build.xml"))
