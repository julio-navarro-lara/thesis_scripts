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


def get_list_of_identifiers(set_nodes):
    output_list = []
    for node in set_nodes:
        id = node["data"]["id"]
        output_list.append(id)

    return output_list

def get_list_of_targets(set_arcs):
    output_list = []
    for arc in set_arcs:
        target = arc["data"]["target"]
        output_list.append(target)

    return output_list

def extract_absolute_condition(split_condition):
    cond = {}
    cond["function"] = split_condition[0]
    cond["att"] = split_condition[1]

    r = split_condition[2]

    #It can be a vector of reference values or not
    if '$_' in r:
        r_list = r.split('$_')
        cond["r"] = r_list
    else:
        cond["r"] = r

    return cond

def extract_relative_condition(split_condition):
    cond = {}
    cond["function"] = split_condition[0]
    attP = split_condition[1].split('$_')
    attC = split_condition[2].split('$_')

    #There is always an empty space due to the excess of separators $_
    attP[:] = [item for item in attP if item != '']
    attC[:] = [item for item in attC if item != '']

    if len(attP) == 1:
        cond["attP"] = attP[0]
    else:
        cond["attP"] = attP

    if len(attC) == 1:
        cond["attC"] = attC[0]
    else:
        cond["attC"] = attC

    return cond


def extract_e_star(e_star_cy):
    e_star = []

    for condition in e_star_cy:
        split_condition = condition.split("#")

        function = split_condition[0]

        cond = {}
        if "SIM" in function:
            cond = extract_relative_condition(split_condition)
        else:
            cond = extract_absolute_condition(split_condition)

        e_star.append(cond)

    return e_star

def extract_nodes(set_nodes):

    nodes_aasg = []

    for node in set_nodes:

        list_e_star = node["data"]["e_star"]
        e_star = extract_e_star(list_e_star)

        node = {"id":node["data"]["id"],"e_star":e_star}
        nodes_aasg.append(node)

    return nodes_aasg

def extract_arcs(set_arcs):
    #This is a dict with the structure: {source:[t1,t2],source:[t1,t2]}.
    #Each source with its targets but still with cytoscape names
    dict_source_targets = {}

    for arc in set_arcs:
        source = arc["data"]["source"]
        target = arc["data"]["target"]
        if source not in dict_source_targets:
            dict_source_targets[source] = [target]
        else:
            dict_source_targets[source].append(target)

    return dict_source_targets

def get_root_nodes(dict_source_targets):

    list_targets = []
    list_sources = []
    for key,value in dict_source_targets.iteritems():
        if key not in list_sources:
            list_sources.append(key)
        for target in value:
            if target not in list_targets:
                list_targets.append(target)

    list_root_nodes = []
    for source in list_sources:
        if source not in list_targets:
            list_root_nodes.append(source)

    return list_root_nodes

def separate_dict_source_targets(dict_source_targets,list_root_nodes):

    separated_dict_source_targets = []
    for root_node in list_root_nodes:
        list_sources = [root_node]
        sub_dict_source_targets = {}
        while list_sources:
            source_to_search = list_sources.pop()
            if source_to_search in dict_source_targets:
                list_targets = dict_source_targets[source_to_search]
                for target in list_targets:
                    list_sources.append(target)
                sub_dict_source_targets[source_to_search] = dict_source_targets[source_to_search]
        separated_dict_source_targets.append(sub_dict_source_targets)

    return separated_dict_source_targets

def new_arc(source,list_target):
    output = {"start":source,"children":[]}

    for target in list_target:
        output["children"].append({"id":target})

    return output

def look_for_node(nodes_aasg,id):
    for node in nodes_aasg:
        if id == node["id"]:
            return node

def create_aasg(nodes_aasg,dict_source_targets,counter,list_root_nodes):
    aasg = {"id":counter,"nodes":[],"arcs":[]}

    added_nodes = []

    for key,value in dict_source_targets.iteritems():
        aasg["arcs"].append(new_arc(key,value))

        if key not in added_nodes:
            aasg["nodes"].append(look_for_node(nodes_aasg,key))
            added_nodes.append(key)

        for node_id in value:
            if node_id not in added_nodes:
                aasg["nodes"].append(look_for_node(nodes_aasg,node_id))
                added_nodes.append(node_id)

    output_aasg = translate_identifiers(aasg,list_root_nodes)

    return output_aasg

def translate_identifiers(aasg,list_root_nodes):

    output_aasg = aasg.copy()

    dict_translation = {}

    counter = 1

    for i in range(0,len(output_aasg["nodes"])):

        identifier = output_aasg["nodes"][i]["id"]

        if identifier in list_root_nodes:
            output_aasg["nodes"][i]["id"] = 0
            dict_translation[identifier] = 0
        else:
            output_aasg["nodes"][i]["id"] = counter
            dict_translation[identifier] = counter
            counter += 1

    for i in range(0,len(output_aasg["arcs"])):

        output_aasg["arcs"][i]["start"] = dict_translation[output_aasg["arcs"][i]["start"]]

        for j in range(0,len(output_aasg["arcs"][i]["children"])):

            output_aasg["arcs"][i]["children"][j]["id"] = dict_translation[output_aasg["arcs"][i]["children"][j]["id"]]

    return output_aasg



def main_cytoscape_to_aasg(input_filepath,output_filepath):

    cy_json = read_json(input_filepath)

    set_nodes = cy_json["elements"]["nodes"]
    set_arcs = cy_json["elements"]["edges"]

    nodes_aasg = extract_nodes(set_nodes)
    dict_source_targets = extract_arcs(set_arcs)

    list_root_nodes = get_root_nodes(dict_source_targets)
    separated_dict_source_targets = separate_dict_source_targets(dict_source_targets,list_root_nodes)

    set_aasg_json = {"aasgs":[]}
    counter = 1
    for dict in separated_dict_source_targets:
        set_aasg_json["aasgs"].append(create_aasg(nodes_aasg,dict,counter,list_root_nodes))
        counter += 1

    #aasg_json = {"id":,"nodes":[],"arcs":[]}


    output_to_json_file(set_aasg_json,output_filepath)


if __name__=="__main__":
    main_cytoscape_to_aasg(sys.argv[1],sys.argv[2])
