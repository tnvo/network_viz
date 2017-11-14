# Graph 1 = distribution of AS classes - 20150801 dataset - see Graph1 Code
# Graph 2 = historygram of AS node degree dist in historygram - 20170991
# Graph 3 = historgram of IP space assigned to each AS - routeviews
# Graph 4 = Recreate pie chart show % distr of ASes to 3 classes

# p2c link: <provider-AS>|<customer-AS>| -1 |<source>
# p2p link: <peer-AS>|<peer-AS>| 0 |<source>
# node degrees= # customers + # peers + # providers
# ASes to which ASi is a provider (direct customers of ASi)
# IP prefixes associated with ASi.

# 2.1 - uses a different file - code is separate

# 2.2 and so on

def read_files(data):
    fileIn = "20170901.as-rel2.txt"

    #Example:
    # 0 | 1 | 2 | 3
    # 5690|40191|0|bgp
    # 5690|395127|-1|bgp
    # 0 and -1 is in index[2]

    # Create a list to lookup data for determining provider node
    # This list negates the need to reopen the file
    lookupProvider = []

    #open AS file and read through each line, splitting each by pipe

    with open(fileIn) as file:

        for line in file:
            line = line.rstrip('\n')
            index = line.split('|')
            indexQ = [] # this local list is inserted into the lookup Queue


            if index[0] not in data:

                data[index[0]] = {'as_links': {'p2c': [],
                                               'p2p': [],
                                               'prov': []
                                              },
                                       'prefix': 'NA', # if data doesn't exist
                                       'length': 'NA'}
            # figure out the link
            # customer (p2c link)
            if index[2] == '-1':
                data[index[0]]['as_links']['p2c'].append(index[1])
                # create a lookup list for the provider from this parsed line
                indexQ.append(index[0])
                indexQ.append(index[1])
                indexQ.append(index[2])
                lookupProvider.append(indexQ)

            # peers - p2p-link
            elif index[2] == '0':
                data[index[0]]['as_links']['p2p'].append(index[1])
    file.close()
    print ("Print lookupProvider")
    # Iterate in parent loop through each a_s value of data at index 0
    for a_s in data: #MS
        # Iterate through each node of the lookup list
        for x in lookupProvider: #MS
            # If the AS value is a customer at offset 1, then add its provider
            # to key value list for 'prov' in data
            if a_s == x[1]: #MS
                data[a_s]['as_links']['prov'].append(x[0]) #MS

    # open NEW route file
    # Example:
    # 0         1   2
    # 1.3.45.0	24	133741_133948
    # 1.3.54.0	24	133741
    # 36.85.84.0	24	7713_65245 <- prefix_as

    fileIn = "routeviews-rv2-20171105-1200.txt"
    with open(fileIn) as file:
        for line in file:
            index = line.split()
            prefix_as = index[2].split('_')
            # getting the range of the IP prefixes
            # once split, index[0] is min and index[1] is max
            for a_s in prefix_as:
                if ',' in a_s:
                    set_as = a_s.split(',')
                    for sub_as in set_as:
                        if sub_as in data:
                            data[sub_as]['prefix'] = index[0]
                            data[sub_as]['length'] = index[1]
                elif a_s in data:
                    data[a_s]['prefix'] = index[0]
                    data[a_s]['length'] = index[1]
    file.close()

# create a new file with info that we actually use
def write_new_file(data, t1):
    output_data_file = "AS.txt"
    with open(output_data_file, "w+") as w:
        # writing each line to a new txt file
        for a_s in data:
            print('AS: {} | n_node_degree: {} | IP_prefix: {}'.format(a_s, data[a_s]['degree'], data[a_s]['prefix'] + '/' + data[a_s]['length']), file=w)
    w.close()

    # writing out to this file
    output_data_file = "2.3 - t1_inference.txt"
    with open(output_data_file, "w+") as w:
        # size of T1 list and first (or up to) 10 ASes that were added to S
        for a_s in range(10):
            if t1[a_s]:
                print('#{} - {}'.format(a_s + 1, t1[a_s]), file=w)
        print('{}'.format(len(t1)), file=w)
    w.close()

# 2.2 - Historgram of node degree
# figure out the numbers of node degree in the dataset
def n_degree(data):
    for a_s in data:
        data[a_s]['degree'] = len(data[a_s]['as_links']['p2c']) + len(data[a_s]['as_links']['p2p'])+len(data[a_s]['as_links']['pro']) #MS

# Sort to rank all ASes according to their degree and place them to set R later
def sort_degree(data):
    as_list = list(data.keys())
    sorted_as = []
    print("Sorting through all AS degrees...")
    while as_list:
        maximum = as_list[0]
        for a_s in as_list:
            if data[a_s]['degree'] > data[maximum]['degree']:
                maximum = a_s
        sorted_as.append(maximum)
        as_list.remove(maximum)
    print("Finishing the sorting process for AS degrees...")
    return sorted_as

# 2.3 - Inference of T1 ASes
def t1(data):
    # rank all ASes according to degree
    # initialize S
    R = sort_degree(data)
    S = [R[0]]
    next_as = 1
    connected = True
    print ("Applying simple greedy heuristic now...")
    # running simple greedy heuristic
    # If AS2 is connected to AS1, add it to S
    # If AS3 is connected to AS1 and AS2, add it to S.
    while connected:
        for a_s in S:
            if (R[next_as] not in data[a_s]['as_links']['p2p']) and (R[next_as] not in data[a_s]['as_links']['p2c'] and (a_s not in data[R[next_as]]['as_links']['p2p']) and (a_s not in data[R[next_as]]['as_links']['p2c'])):
                connected = False
                break
        if connected:
            S.append(R[next_as])
            next_as += 1
    return S

# p2c customers cone links
# calculate # of cone
def n_cone(all):
    print("Almost there....")
    def dfs(data, current_node, cone_size):
        if current_node in data:
            for child in data[current_node]['as_links']['p2c']:
                dfs(data, child, cone_size)
        return cone_size + 1

    print("Half way done with cone stuffs ...")

    for a_s in all:
        total_cone = 0
        total_cone = dfs(all, a_s, total_cone)
        all[a_s]['cone_size'] = total_cone

def n_Ips(all):
    print("Calculating IPs")
    total = 0
    for pf in prefix:
        sub_bits = int(pf.split('/')[1])
        total += pow(2, 32 - sub_bits)


# Calling and running function from above now
print("Running functions now")
# Run functions
# all of the data now
all = {}
prefix = set()
read_data(all, prefix)

print("Reading files")
read_files(all)

print("Calculating number of node degree...")
n_degree(all)

print("Running t1")
print("This step might take awhile...")
t1 = t1(all)

print("Running numbers of cone...")
print("Might take another little while...")
n_cone(all)

print("Writing useful data to a new file...")
write_new_file(all, t1)

print("Finished")
