#Copyright 2018 Julio Navarro
#Built at the University of Strasbourg (France). CSTB team @ ICube laboratory
import numpy as np
from difflib import SequenceMatcher



list_types = [
'(POP) Unknown POP3 command',
'(ftp_telnet) Invalid FTP Command',
'(http_inspect) NON-RFC DEFINED CHAR',
'ET DOS Microsoft Remote Desktop (RDP) Syn then Reset 30 Second DoS Attempt',
'ET EXPLOIT HP OpenView Network Node Manager Toolbar.exe CGI Buffer Overflow Attempt',
'ET EXPLOIT Wscript Shell Run Attempt - Likely Hostile',
'ET FTP Suspicious Percentage Symbol Usage in FTP Username',
'ET POLICY Incoming Basic Auth Base64 HTTP Password detected unencrypted',
'ET POLICY Python-urllib/ Suspicious User Agent',
'ET SCAN Potential VNC Scan 5800-5820',
'ET SCAN Potential VNC Scan 5900-5920',
'ET SCAN Toata Scanner User-Agent Detected',
'ET TROJAN Double HTTP/1.1 Header Inbound - Likely Hostile Traffic',
'ET WEB_SERVER HP OpenView Network Node Manager OvWebHelp.exe Heap Buffer Overflow Attempt',
'ET WEB_SERVER HTTP POST Generic eval of base64_decode',
'ET WEB_SERVER PHP tags in HTTP POST',
'ET WEB_SERVER Possible Cookie Based BackDoor Used in Drupal Attacks',
'ET WEB_SERVER Possible DD-WRT Metacharacter Injection Command Execution Attempt',
'ET WEB_SERVER SQL Errors in HTTP 200 Response (SqlException)',
'ET WEB_SPECIFIC_APPS Possible HP Power Manager Management Web Server Login Remote Buffer Overflow Attempt',
'SERVER-WEBAPP JBoss JMX console access attempt',
'(IMAP) Unknown IMAP4 command',
'ET FTP Suspicious Quotation Mark Usage in FTP Username',
'ET SCAN Potential FTP Brute-Force attempt response',
'ET SHELLCODE Rothenburg Shellcode',
'PROTOCOL-DNS domain not found containing random-looking hostname - possible DGA detected',
'(http_inspect) UNKNOWN METHOD',
'(spp_ssh) Protocol mismatch',
'Limit on number of overlapping TCP packets reached',
'(http_inspect) POST W/O CONTENT-LENGTH OR CHUNKS',
'(http_inspect) UNESCAPED SPACE IN HTTP URI',
'ET POLICY Suspicious inbound to Oracle SQL port 1521',
'ET POLICY Suspicious inbound to mySQL port 3306',
'ET POLICY Suspicious inbound to MSSQL port 1433',
'ET POLICY Suspicious inbound to PostgreSQL port 5432',
'ET WEB_SERVER /bin/sh In URI Possible Shell Command Execution Attempt',
'ET WEB_SERVER Possible SQLi xp_cmdshell POST body',
'(http_inspect) SIMPLE REQUEST',
'(http_inspect) JAVASCRIPT WHITESPACES EXCEEDS MAX ALLOWED',
'(ftp_telnet) TELNET CMD on FTP Command Channel',
'ET SCAN Potential SSH Scan',
'ET WEB_SERVER HTTP 414 Request URI Too Large',
'Bad segment, adjusted size <= 0',
'(http_inspect) OVERSIZE REQUEST-URI DIRECTORY',
'ET POLICY GNU/Linux APT User-Agent Outbound likely related to package management',
'INDICATOR-SHELLCODE Shikata Ga Nai x86 polymorphic shellcode decoder detected',
'(http_inspect) LONG HEADER',
'(http_inspect) SERVER CONSECUTIVE SMALL CHUNK SIZES',
'Reset outside window',
'ICMP test detected',
'(http_inspect) INVALID CONTENT-LENGTH OR CHUNK SIZE',
'Consecutive TCP small segments exceeding threshold',
'PROTOCOL-DNS potential dns cache poisoning attempt - mismatched txid',
'(spp_sdf) SDF Combination Alert',
'PROTOCOL-DNS TMG Firewall Client long host entry exploit attempt',
'(ftp_telnet) FTP command parameters were too long',
'(http_inspect) NO CONTENT-LENGTH OR TRANSFER-ENCODING IN HTTP RESPONSE'
]

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def levenshtein(seq1, seq2):
    size_x = len(seq1) + 1
    size_y = len(seq2) + 1
    matrix = np.zeros ((size_x, size_y))
    for x in xrange(size_x):
        matrix [x, 0] = x
    for y in xrange(size_y):
        matrix [0, y] = y

    for x in xrange(1, size_x):
        for y in xrange(1, size_y):
            if seq1[x-1] == seq2[y-1]:
                matrix [x,y] = min(
                    matrix[x-1, y] + 1,
                    matrix[x-1, y-1],
                    matrix[x, y-1] + 1
                )
            else:
                matrix [x,y] = min(
                    matrix[x-1,y] + 1,
                    matrix[x-1,y-1] + 1,
                    matrix[x,y-1] + 1
                )
    #print (matrix)
    #return (matrix[size_x - 1, size_y - 1])
    #return 1-(matrix[size_x - 1, size_y - 1])/max(size_x,size_y)
    return (matrix[size_x - 1, size_y - 1])/max(size_x,size_y)

def get_jaccard_sim(str1, str2):
    a = set(str1.split())
    b = set(str2.split())
    c = a.intersection(b)
    return float(len(c)) / (len(a) + len(b) - len(c))

def comparison_against_list(input_string):
    for element in list_types:
        jaccard_index = get_jaccard_sim(input_string,element)
        if jaccard_index > 0.0:
            print element
            print jaccard_index

if __name__ == "__main__":
    #comparison_against_list("SQL")
    comparison_against_list("EXPLOIT Attempt")
    #print get_jaccard_sim("SQL", "This is a SQL injection attack")
    #print get_jaccard_sim("SQL", "CSS attack")
    #print get_jaccard_sim("failure SSH", "Authentication failure SSH")
