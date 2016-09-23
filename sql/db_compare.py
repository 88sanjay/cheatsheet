import pandas as pd

file_name = "column_mapping.csv"
key_set = ['import_group', 'class', 'source_table', 'target_column','source_column']
ignore_list = ['last_updated','created_on','id']

dev_file_base = "/disk1/tenx/skumar/lab_dev/lab/"
lab_file_base = "/disk1/tenx/skumar/lab_dev/dev/"
out_file_base = "/disk1/tenx/skumar/lab_dev/out/"

dev = pd.read_csv(dev_file_base+file_name)
lab = pd.read_csv(lab_file_base+file_name)

# Find columns that are missing in lab and have to be removed from dev
columns_to_remove = (set(dev.columns) - set(lab.columns)) 

# Find columns that are new in lab and have to be added in dev 
columns_to_add = (set(lab.columns) - set(dev.columns))

# Set dev and lab to exactly the intersection of lab and dev columns.
# Prepare for joining.
final_dev_col = list(set(dev.columns) - columns_to_remove)

final_lab_col = list(set(lab.columns) - columns_to_add)

if set(final_lab_col) - set(final_dev_col):
    print("*******************error ****************\n\n\n\n")

dev = dev[final_dev_col]
lab = lab[final_lab_col]

# join 
dev.columns =  dev.columns.map(lambda x: x+"_dev" if x not in key_set else x)
lab.columns =  lab.columns.map(lambda x: x+"_lab" if x not in key_set else x)

final=pd.merge(dev,lab, on=key_set,how="outer")


def calculate(s):
    out = "equivalent"
    missing_in_dev_flag = True
    missing_in_lab_flag = True
    updated_fields = []
    for i in dev.columns:
        if ((i not in key_set) & (not pd.isnull(s[i]))):
            missing_in_dev_flag = False
            break
    for i in lab.columns:
        if ((i not in key_set) & (not pd.isnull(s[i]))):
            missing_in_lab_flag = False
            break
    if ( (not missing_in_dev_flag) and (not missing_in_lab_flag)):
        for i in dev.columns:
            if (i not in key_set+[j+"_dev" for j in ignore_list]):
                lab_eq_col = i.replace("_dev","_lab")
                if (not pd.isnull(s[i])) or (not pd.isnull(s[lab_eq_col])):
                    if s[i] != s[lab_eq_col]:
                        updated_fields = updated_fields+[i.replace("_dev"," ")]
    out = "missing in dev" if missing_in_dev_flag else out
    out = "missing in lab" if missing_in_lab_flag else out
    out = updated_fields if (updated_fields != []) else out
    return pd.Series(dict(diff=out))

diff = final.apply(calculate,axis=1)
final["diff"] = diff

# filter missing in dev
md = final[final['diff'] == "missing in dev"]
ml = final[final['diff'] == "missing in lab"]
e  = final[final['diff'] == "equivalent"]

a = dev.apply(lambda x: " ".join([x[i] for i in key_set]),axis=1).value_counts()
id1 = a[a>1]

b = e.apply(lambda x: " ".join([x[i] for i in key_set]),axis=1).value_counts()
id2 = b[b>1]

filter_out = []
for i in id1.index :
    try :
        if (id1[i] == id2[i]) :
           filter_out = filter_out +[i]
    except Exception, exception:
        pass

u  = final[(final['diff'] != "equivalent") & (final['diff'] != "missing in dev") & (final['diff'] != "missing in lab")]

index_col = u.apply(lambda x: " ".join([x[i] for i in key_set]) not in filter_out,axis=1)

u = u[index_col]

rows=[]

def make_row(row):
    for d in row['diff']:
        rows.append([row[i] for i in u.columns[:-1]] + [d])

for i in u.index:
    make_row(u.ix[i])

u_fin = pd.DataFrame(rows, columns=u.columns)


# filter out the records with duplicate key entries and that have been accounted for in 
cols = sorted([i for i in final.columns if (i not in key_set+['diff'])])
df_set = [md,ml,e,u_fin]
file_name_tail = ["_missing_in_dev.csv","_missing_in_lab.csv","_equivalent.csv","_updates.csv"]

for i,j in enumerate(df_set):
    j[key_set+['diff'] + cols].to_csv(out_file_base+file_name+file_name_tail[i])

print(columns_to_remove)
print(columns_to_add)

