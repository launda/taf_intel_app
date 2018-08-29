
def get_avlocs():

    import pandas as pd
    import os

    cur_dir = os.path.dirname(__file__)
    
    '''get TAF codes for airports in diff states from minima file at web.bom.gov.au
    http://web.bom.gov.au/spb/adpo/aviation/LocationDatabase/minima.xls
    "state" "Location" "Ident"  "HAM (cld (ft))" "HAM (vis (m))" 
    "SAM (cld (ft))"  "SAM (vis (m))"   "MSA (ft)" '''
    minima_path = os.path.join(cur_dir,'static', 'minima.xls')
    with open(minima_path, 'rb') as m:
        minima = pd.read_excel(m, usecols=list(range(8)), skiprows=list(range(10)))
    
    '''get PCA locs in diff states from pca file at web.bom.gov.au
    http://web.bom.gov.au/spb/adpo/aviation/LocationDatabase/pca.txt
    fixed width col format - so have to give width of each col, skips 1st and 3rd row
    "LOC_ID" "AREA" "LOCATION_NAME" "Lat" "Long" "Type" "Reg" "State"'''
    pca_path = os.path.join(cur_dir,'static', 'pca.txt')
    with open(pca_path, 'r') as p:
        pca = pd.read_fwf(p, widths=[7,5,33,10,11,5,4,5], skiprows=[0,2])


    '''merge the two data sets into one 
    left join ensures we keep all airport minima info 
    and supplment these with extra info from pca database, lat, long etc''' 
    locs  = pd.merge(left=minima, right=pca, left_on='Ident', right_on='LOC_ID', how='left')\
            .drop(['state','Ident','LOCATION_NAME'], axis=1)\
            [['LOC_ID', 'AREA', 'Lat', 'Long', 'Type','Reg', 'State',\
            'Location','HAM (cld (ft))', 'HAM (vis (m))', \
            'SAM (cld (ft))','SAM (vis (m))', ' MSA (ft)']]\
            .set_index('LOC_ID')

    # ensure numeric data is forced to be numeric
    for col in  [ 'AREA', 'Lat', 'Long','HAM (cld (ft))', 'HAM (vis (m))', \
            'SAM (cld (ft))','SAM (vis (m))', ' MSA (ft)']:
        locs[col] = pd.to_numeric(locs[col], errors='coerce')

    # convert text data to string
    cols_str = ['Location', 'Type', 'Reg', 'State']
    locs[cols_str] = locs[cols_str].astype(str)
    
    return locs
