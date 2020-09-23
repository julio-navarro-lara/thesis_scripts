#Copyright 2018 Julio Navarro
#Built at the University of Strasbourg (France). CSTB team @ ICube laboratory
#29/11/2018
from pprint import pprint
from morwilog_main import main
from library import *

def extract_stat_dict(input_list):
    dict_result = {}
    for element in input_list:
        if element in dict_result:
            dict_result[element]+=1
        else:
            dict_result[element] = 1

    return dict_result

def execution_experiment_one_time():
    #json_results = main()
    #branches = json_results["results"][1]["branches_found"]
    #sequences = json_results["results"][1]["sequences_found"]
    #pos_seq = json_results["results"][1]["pos_seq_found"]

    #dict_branches = extract_stat_dict(branches)
    #dict_sequences = extract_stat_dict(sequences)
    #dict_pos_seq = extract_stat_dict(pos_seq)

    #print dict_branches
    #print dict_sequences
    #print dict_pos_seq

    dict_results = main()

    return dict_results

def is_alert_sequence_equal(alert_seq1,alert_seq2):
    if len(alert_seq1[0])!=len(alert_seq2[0]):
        return False

    if alert_seq1[1] != alert_seq2[1]:
        return False

    for i in range(0,len(alert_seq1[0])):
        if alert_seq1[0][i] != alert_seq2[0][i]:
            return False

    return True

def is_already_in_list_alert_sequence(list_alert_sequences,alert_sequence):
    if not list_alert_sequences:
        return None

    for i in range(0,len(list_alert_sequences)):
        if is_alert_sequence_equal(list_alert_sequences[i],alert_sequence):
            return i

    return None

def execution_experiment_several_times(n_times):
    #To take out the statistic of possibilities in Morwilog. But this time, having into account the
    #position number of the logs in the sequences.
    global_dict_results = {}
    list_seq_alerts = []
    for i in range(0,n_times):

        print "*****"
        print i
        print ""

        dict_results = execution_experiment_one_time()
        list_cases = ""
        sequence_alert = []
        #Each element in the sequence of alert has the following format: [sequence, pos_alert]
        for element in sorted(dict_results.keys()):
            new_result = dict_results[element]
            if element in global_dict_results:
                found = False
                for j in range(0,len(global_dict_results[element])):
                    if check_list_equal(new_result["pos_seq"],global_dict_results[element][j]["pos_seq"]):
                        global_dict_results[element][j]["counter"]+=1
                        found = True
                        break
                if not found:
                    new_result["counter"] = 1
                    global_dict_results[element].append(new_result)
            else:
                new_result["counter"] = 1
                global_dict_results[element] = [new_result]

            sequence_alert.append([new_result["pos_seq"],new_result["moment_alert"]])

        #We check if the alert sequence is already there or not
        found = False
        if list_seq_alerts:
            for j in range(0,len(list_seq_alerts)):
                #Structure: [list_sequences, number_of_times]
                #Inside list_sequences: [[pos_seq,moment_alert]....[pos_seq,moment_alert]]
                found_partial = True
                if len(list_seq_alerts[j][0]) != len(sequence_alert):
                    found_partial = False
                else:
                    for individual_sequence in sequence_alert:
                        position = is_already_in_list_alert_sequence(list_seq_alerts[j][0],individual_sequence)
                        if not position:
                            found_partial = False
                            break

                if found_partial:
                    list_seq_alerts[j][1]+=1
                    found = True
                    break

        if not found:
            list_seq_alerts.append([sequence_alert,1])


    return [global_dict_results,list_seq_alerts]

def print_global_dict_results(global_dict_results):
    print "\n\n"
    print "RESULTS"
    for element in sorted(global_dict_results.keys()):
        print "**********"
        print "KEY "+str(element)
        for instance in global_dict_results[element]:
            print "------------"
            print instance["counter"]
            print instance["pos_seq"]
            print instance["branch"]
            print instance["sequence_ids"]
            print "Alert "+str(instance["moment_alert"])



if __name__=="__main__":
    [global_dict_results,list_seq_alerts] = execution_experiment_several_times(1000)
    print_global_dict_results(global_dict_results)
    # print ""
    # print "+++++++++++"
    # print ""
    # for element in list_seq_alerts:
    #     print element
