import pandas as pd

list_codart = []
list_codfab = []
list_description = []

def get_dataframe(codart,codfab,description):
    #
    list_codart.append(codart)
    list_codfab.append(codfab)
    list_description.append(description)
    
    df = pd.DataFrame(zip(list_codart,list_codfab,list_description), columns=['codart','codfab','description'])
    df.to_csv('list_vins_dt.csv', header=True, index=False)
    