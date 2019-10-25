import csv
import collections

class RulesTreeNode:
    def __init__(self, data):
        self.left = None
        self.child = []
        self.data = data

class RulesTree:

    def create_ip_range(self, ip_range):
        if '-' in ip_range:
            arr_1 = [None]*256
            arr_2 = [None]*256
            arr_3 = [None]*256
            arr_4 = [None]*256
            ip_arr = [arr_1, arr_2, arr_3, arr_4]
            ip_vals = ip_range.split('-')
            ip_vals[0] = ip_vals[0].split('.')
            ip_vals[1] = ip_vals[1].split('.')
            for i in range(len(ip_vals[0])):
                for j in range(int(ip_vals[0][i]), int(ip_vals[1][i]) + 1):
                    ip_arr[i][j] = 1
            return ip_arr
        else:
            arr_1 = [None]*256
            arr_2 = [None]*256
            arr_3 = [None]*256
            arr_4 = [None]*256
            ip_arr = [arr_1, arr_2, arr_3, arr_4]
            ip = ip_range.split('.')
            pos = 0
            for partition in ip:
                ip_arr[pos][int(partition)] = 1
                pos = pos + 1
            return ip_arr

    def insert_ip_range(self, ip_range, ip_arr):
        if '-' in ip_range:
            ip_vals = ip_range.split('-')
            ip_vals[0] = ip_vals[0].split('.')
            ip_vals[1] = ip_vals[1].split('.')
            for i in range(len(ip_vals[0])):
                for j in range(int(ip_vals[0][i]), int(ip_vals[1][i]) + 1):
                    if ip_arr[i][j] == None:
                        ip_arr[i][j] = 1
        else:
            ip = ip_range.split('.')
            pos = 0
            for partition in ip:
                if ip_arr[pos][int(partition)] == None:
                    ip_arr[pos][int(partition)] = 1
                pos = pos + 1

    def find_ip(self, ip, ip_arr):
        ip_vals = ip.split('.')
        for i in range(len(ip_vals)):
            if ip_arr[i][int(ip_vals[i])] == None:
                return False
        return True

    def expand_range(self, string_range):
        if len(string_range.split('-')) == 2:
            port_range = range(int(string_range.split('-')[0]),int(string_range.split('-')[1])+1)
        else:
            port_range = [int(string_range)]
        return port_range

    def createNode(self, data):
        return RulesTreeNode(data)

    def insert(self, node, firewall_list):
        is_match = False
        pos = 0
        nums = 1
        for rule in firewall_list:
            is_match = False
            if pos == 2:
                for port in self.expand_range(rule):
                    if len(node.child) == 0:
                        node.child = [None] * 65535
                        node.child[port-1] = self.createNode(self.create_ip_range(firewall_list[pos+1]))
                    else:
                        if node.child[port-1] == None:
                            node.child[port-1] = self.createNode(self.create_ip_range(firewall_list[pos+1]))
                        else:
                            node.child[port-1].data = self.insert_ip_range(firewall_list[pos+1],node.child[port-1].data)
                break
            else:
                if len(node.child) == 0:
                    node.child.append(self.createNode(rule))
                    node = node.child[0]
                else:
                    for child in node.child:
                        if(child.data == rule):
                            node = child
                            is_match = True
                            break
                    if not is_match:
                        node.child.append(self.createNode(rule))
                        node = node.child[len(node.child) - 1]
            
            pos = pos + 1
    
    def search_with_range_consideration(self, node, packet_list):
        has_matched = False
        pos = 0
        for rule in packet_list:
            if pos == 2:
                if node.child[int(rule) - 1] == None:
                    return False
                else:
                    node = node.child[int(rule) - 1]
                    return self.find_ip(packet_list[pos+1], node.data)
            else:
                for child in node.child: 
                    has_matched = False
                    if child.data == str(rule):
                        node = child
                        has_matched = True
                        break
                if not has_matched:
                    return False
            pos = pos + 1
        return True

class Firewall:
    def __init__(self, path_to_csv):
        self.rules = RulesTree()
        self.root = RulesTreeNode("")
        with open(path_to_csv, "r") as csv_reading:
            reader = csv.reader(csv_reading, delimiter=",")
            for line in reader:
                self.rules.insert(self.root, line)

    def expand_rule(self, line):
        rules_list = []

        return line

    def accept_packet(self, direction, protocol, port, ip_address):
        packet_list = [direction, protocol, port, ip_address]
        return self.rules.search_with_range_consideration(self.root, packet_list)


fw = Firewall("test.csv")
print(fw.accept_packet("inbound", "udp", 83, "192.168.1.6")) # matches first rule
#print(fw.accept_packet("inbound", "udp", 53, "192.168.2.1")) # matches third rule
#print(fw.accept_packet("outbound", "tcp", 10234, "192.168.10.11")) # matches second rule
#print(fw.accept_packet("inbound", "tcp", 81, "192.168.1.2"))
#print(fw.accept_packet("inbound", "udp", 24, "52.12.48.92"))
#print(fw.accept_packet("outbound","tcp",10020,"192.168.1.2"))

