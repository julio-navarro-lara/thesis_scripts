#Copyright 2018 Julio Navarro
#Built at the University of Strasbourg (France). CSTB team @ ICube laboratory
import numpy as np
from difflib import SequenceMatcher

def from_ip_to_binary_string(ip):
    output = ''.join([bin(int(x)+256)[3:] for x in ip.split('.')])
    return output

def calculate_common_bits(ip1,ip2):
    result = 0
    len1 = len(ip1)
    len2 = len(ip2)
    if len1 == len2:
        for i in range(0,len1):
            if ip1[i] == ip2[i]:
                result += 1
            else:
                break
    return result

def prefix_similarity(ip1,ip2):
    bitip1 = from_ip_to_binary_string(ip1)
    bitip2 = from_ip_to_binary_string(ip2)

    l = calculate_common_bits(bitip1,bitip2)
    print l

    return float(l)/float(len(bitip1))

if __name__ == "__main__":
    print prefix_similarity("192.168.128.1","192.168.0.0")
