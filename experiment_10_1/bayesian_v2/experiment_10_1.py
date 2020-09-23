#Copyright 2018 Julio Navarro
#Built at the University of Strasbourg (France). CSTB team @ ICube laboratory

from bayesian_main import *
from library import write_csv_file

if __name__=="__main__":

    #file_logs = "../../datasets/eventgen/eventgen_dataset/eventgen.log.parsed.csv" #66 attacks
    #file_logs = "../../datasets/eventgen/prop_attacks/prop_attacks_50/prop_attacks_50.log.parsed.csv"
    file_logs = "../../datasets/eventgen/prop_attacks/prop_attacks_500/prop_attacks_500.log.parsed.csv"

    #file_aasg = "../aasg/eventgen_aasg/eventgen_aasg_1branch.json"
    #file_aasg = "../aasg/eventgen_aasg/prop_attacks_change_1branch_50.json"
    file_aasg = "../aasg/eventgen_aasg/prop_attacks_change_1branch_500.json"

    dict_var = {
        "p_t_max":20,
        "p_learning_rate":0.4
    }


    header = ["Tmax","learning_rate","P","N","TP","FP","Alerts","B[0,1,3]","B[0,1,4]","B[0,2,5]","B[0,2,6]"]


    list_learning_rate = [0.0,0.025,0.05,0.075,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]

    list_results = [header]
    for learning_rate in list_learning_rate:
        dict_var["p_learning_rate"] = learning_rate

        result = main(dict_var,file_logs,file_aasg)
        list_results.append(result)

    write_csv_file("results_experiment_10_1.csv",list_results)
