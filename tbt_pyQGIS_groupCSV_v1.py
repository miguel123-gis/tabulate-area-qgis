import csv
import itertools
from collections import defaultdict

file = r'C:\Users\imper\Desktop\tbt_pyQGIS_v1_result.csv'

result = defaultdict(list)
d = {}; new_dict = {} 

with open (file) as f:
    csvreader = csv.reader(f)
    for row in csvreader:
        result[row[1]].append(row[0])
        result[row[1]].append(row[2])
"""
# WRONG - dict (sub list of classes and its area) are same for each key (zone)
for key,sub_list in result.items(): 
    for r in range(2, len(sub_list), 2): 
        if sub_list[r] not in new_dict:
            new_dict[sub_list[r]] = float(sub_list[r+1]) 
        new_dict[sub_list[r]] += float(sub_list[r+1]) 
        d[key] = new_dict
print(d)    

# WRONG - doesn't add values of the same keys, only retains one value for each key
for i in result:
    d = dict(itertools.zip_longest(*[iter(result[i])] * 2, fillvalue=""))
    print(d)
"""