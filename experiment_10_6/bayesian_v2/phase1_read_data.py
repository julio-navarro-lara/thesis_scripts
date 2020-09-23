#Copyright 2018 Julio Navarro
#Built at the University of Strasbourg (France). CSTB team @ ICube laboratory
#12/06/2018
from library import *

def read_logs(input_filepath):
    #list_logs = extract_csv_file(input_filepath)
    list_logs = extract_csv_pandas(input_filepath)
    return list_logs



def read_aasg_set(input_filepath):
    aasg_set = read_json(input_filepath)

    return aasg_set["aasgs"]

    #Para mirar la consistencia de un arbol:
    #- El id se corresponde con la posicion del nodo en la lista
    #- Las pheromonas van sumandose hasta la raiz (esto se podria comprobar y forzar)
    #- Luego ya ver que los caminos esten bien hechos y que sea un DAG

    #we need to transform the Morwilog aasgs in a Bayesian aasg
    # print("Transforming aasg to Bayesian")
    # new_aasg_set = from_morwilog_aasg_to_bayesian(aasg_set)
    # for aasg in new_aasg_set["aasgs"]:
    #     for node in aasg["nodes"]:
    #         if node["prob"]:
    #             print str(node["id"])+" - "+str(node["ph"])+" - "+str(node["prob"])
    #         else:
    #             print "NO PROB "+str(node["id"])
    #
    # return new_aasg_set["aasgs"]

def initialization_probabilities(aasg_set):
    for aasg in aasg_set:
        for arc_set in aasg["arcs"]:
            num_children = len(arc_set["children"])
            for child in arc_set["children"]:
                child["prob"] = 1.0/float(num_children)

    return aasg_set

def adding_arcs_optional_nodes(aasg_set):
    for aasg in aasg_set:
        list_optional_nodes = []

        for node in aasg["nodes"]:
            if "optional" in node and node["optional"]:
                list_optional_nodes.append(node["id"])

        #print "LIST OPTIONALS"
        #print list_optional_nodes

        for optional_node_id in list_optional_nodes:
            #We need to look for the arcs going in and out of that node
            list_children = []

            for arc_set in aasg["arcs"]:
                if arc_set["start"] == optional_node_id:
                    for child in arc_set["children"]:
                        list_children.append(child["id"])

            if len(list_children) > 0:
                #We add new arcs, directly from parents to children
                for arc_set in aasg["arcs"]:
                    for child in arc_set["children"]:
                        if child["id"] == optional_node_id:
                            for element in list_children:
                                arc_set["children"].append({"id":element})
                            break

            #print list_children

    return aasg_set

def read_parameters(input_filepath):
    print "Hola"
