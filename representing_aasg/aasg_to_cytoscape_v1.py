#Copyright 2018 Julio Navarro
#Built at the University of Strasbourg (France). CSTB team @ ICube laboratory
#24/10/2018
#script to transform from AASG JSON format to Cytoscape JSON format
import sys
import json

def read_json(filename):
    data = json.load(open(filename))
    return data

def output_to_json_file(content, filename):
    with open(filename, 'w') as outfile:
        json.dump(content, outfile)

def node_conversion_aasg_to_cy(input_node):
    output_node = {}

    list_e_star = []
    name_node = ""
    for condition in input_node["e_star"]:
        string_e_star = condition["function"]+'#'
        if "att" in condition:
            string_e_star += condition["att"]
            if isinstance(condition["r"], basestring):
                string_e_star += '#'+condition["r"]
                if not name_node:
                    name_node = condition["r"]
            else:
                string_e_star += '#'
                for element in condition["r"]:
                    string_e_star += '$_'+element
        elif "attP" in condition:
            if isinstance(condition["attP"],basestring):
                string_e_star += '$_'+condition["attP"]

            else:
                for element in condition["attP"]:
                    string_e_star += '$_'+element

            string_e_star += '#'
            if isinstance(condition["attC"],basestring):
                string_e_star += '$_'+condition["attC"]

            else:
                for element in condition["attC"]:
                    string_e_star += '$_'+element
        list_e_star.append(string_e_star)

    if not name_node:
        name_node = str(input_node["id"])

    output_node["data"] = {
        "id":str(input_node["id"]),
        "selected":False,
        "e_star": list_e_star,
        "name": name_node
    }

    return output_node

def edge_conversion_aasg_to_cy(input_edge,start):

    output_edge = {}

    target = input_edge["id"]

    output_edge["data"] = {
        "id": str(start)+"_"+str(target),
        "source": str(start),
        "target": str(target)
    }

    return output_edge

def main_aasg_to_cytoscape(input_filepath,output_filepath):

    aasg_json = read_json(input_filepath)

    set_aasg = aasg_json["aasgs"]

    cytoscape_json = {"elements":{"nodes":[],"edges":[]}}

    for aasg in set_aasg:
        for node in aasg["nodes"]:
            cytoscape_json["elements"]["nodes"].append(node_conversion_aasg_to_cy(node))

        for set_arcs in aasg["arcs"]:
            start = set_arcs["start"]
            for arc in set_arcs["children"]:
                cytoscape_json["elements"]["edges"].append(edge_conversion_aasg_to_cy(arc,start))

    output_to_json_file(cytoscape_json,output_filepath)


if __name__=="__main__":
    main_aasg_to_cytoscape(sys.argv[1],sys.argv[2])
