#Copyright 2018 Julio Navarro
#Built at the University of Strasbourg (France). CSTB team @ ICube laboratory
from bayesian_main import *
from library import write_csv_file

if __name__=="__main__":

    beginning_file_logs = "../../datasets/eventgen/prop_attacks/prop_attacks_"
    beginning_file_aasg = "../aasg/eventgen_aasg/prop_attacks_change/prop_attacks_change_1branch_"
    dict_var = {
        "p_t_max":20,
        "p_learning_rate":0.4
    }

    list_prop_attack = [50,100,250,500,750,1000,1500,2000]

    dict_number_attacks = {
            50:1,
            100:3,
            250:8,
            500:16,
            750:25,
            1000:33,
            1500:50,
            2000:66
    }

    header = ["prop_attacks","num_attacks","Tmax","learning_rate","P","N","TP","FP","Alerts","B[0,1,3]","B[0,1,4]","B[0,2,5]","B[0,2,6]"]

    list_results = [header]
    for prop_attack in list_prop_attack:
        file_logs = beginning_file_logs + str(prop_attack) +"/prop_attacks_"+str(prop_attack)+".log.parsed.notags.csv"
        file_aasg = beginning_file_aasg +str(prop_attack)+".json"

        result = main(dict_var,file_logs,file_aasg)
        list_results.append([prop_attack, dict_number_attacks[prop_attack]]+result)

    write_csv_file("results_experiment_10_6.csv",list_results)
