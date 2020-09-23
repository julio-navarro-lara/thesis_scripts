#Copyright 2018 Julio Navarro
#Built at the University of Strasbourg (France). CSTB team @ ICube laboratory
from morwilog_main import *
from library import write_csv_file

if __name__=="__main__":

    #file_logs = "../../datasets/eventgen/eventgen_dataset/eventgen.log.parsed.csv" #66 attacks
    file_logs = "../../datasets/eventgen/prop_attacks/prop_attacks_50/prop_attacks_50.log.parsed.csv"
    #file_logs = "../../datasets/eventgen/prop_attacks/prop_attacks_500/prop_attacks_500.log.parsed.csv"

    #file_aasg = "../aasg/eventgen_aasg/eventgen_aasg_1branch.json"
    file_aasg = "../aasg/eventgen_aasg/prop_attacks_change_1branch_50.json"
    #file_aasg = "../aasg/eventgen_aasg/prop_attacks_change_1branch_500.json"

    dict_var = {"p_t_max" : 20,
                "p_evap_rate" : 0.02,
                "p_omega" : 1000.0,
                "p_delta_ph_0" : 500.0,
                "p_minimum_ph" : 100.0,
                "p_minimum_ph_attack" : 200.0,
                "p_initial_ph": 1000.0
                }


    header = ["initial_ph","minimum_ph","delta_ph_0","Tmax","rho","omega","P","N","TP","FP","Alerts","B[0,1,3]","B[0,1,4]","B[0,2,5]","B[0,2,6]"]

    list_rho = [0.0,0.02,0.03,0.04,0.05,0.06,0.07,0.08]
    list_omega = [200.0,300.0,400.0,500.0,600.0,700.0,800.0,900.0,1000.0,1100.0,1200.0,1300.0,1400.0,1500.0,1600.0,1700.0,1800.0,1900.0,2000.0,2100.0,2200.0,2300.0,2400.0,2500.0,2600.0,2700.0,2800.0,2900.0,3000.0,3100.0,3200.0]

    list_results = [header]
    for rho in list_rho:
        dict_var["p_evap_rate"] = rho
        for omega in list_omega:
            dict_var["p_omega"] = omega
            result = main(dict_var,file_logs,file_aasg)
            list_results.append(result)

    write_csv_file("results_experiment_10_1.csv",list_results)
