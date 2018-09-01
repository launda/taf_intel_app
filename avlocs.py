
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


    '''merge the two data sets into one dataframe
    left join ensures we keep all airport minima info 
    and supplment these with extra info from pca database, lat, long etc''' 
    locs  = pd.merge(left=minima, right=pca, left_on='Ident', right_on='LOC_ID', how='left')\
            .drop(['state','Ident','LOCATION_NAME'], axis=1)\
            [['LOC_ID', 'AREA', 'Lat', 'Long', 'Type','Reg', 'State',\
            'Location','HAM (cld (ft))', 'HAM (vis (m))', \
            'SAM (cld (ft))','SAM (vis (m))', ' MSA (ft)']]\
            .set_index('LOC_ID')

    cols_flt = ['Lat', 'Long','HAM (cld (ft))', 'HAM (vis (m))', \
            'SAM (cld (ft))','SAM (vis (m))', ' MSA (ft)'] 

    # ensure numeric data is forced to be numeric
    for col in  ['Lat', 'Long', 'HAM (cld (ft))', 'HAM (vis (m))', \
            'SAM (cld (ft))','SAM (vis (m))', ' MSA (ft)']:
        locs[col] = pd.to_numeric(locs[col], downcast='integer',errors='coerce')

    # 'AREA' shud be an int not float, NaN is compatible with float but no int
    # columns in minima.xls can't be missing - drop rows with NaNs in these cols 
    # else Raises ValueError: ('cannot convert float NaN to integer') 
    locs.dropna(subset=['State','Location','HAM (cld (ft))', 'HAM (vis (m))'],inplace=True)

    locs['AREA'] = locs['AREA'].astype(int)
    # locs['AREA'] = locs['AREA'].apply(lambda x: int(x) if x == x else np.NaN)
   
    decimals = pd.Series([4,4],index=['Lat', 'Long'])  # lat/long to 4 dec plc
    locs = locs.round(decimals)

    # force convert text data to string
    cols_str = ['Location', 'Type', 'Reg', 'State']
    locs[cols_str] = locs[cols_str].astype(str)

    # (x,y) coord system x is longitude , y is latitude 
    # shorten longer names
    locs.rename(columns= {
         'HAM (cld (ft))':'HAM_cld_ft', 'HAM (vis (m))':'HAM_vis_m', \
         'SAM (cld (ft))':'SAM_cld_ft','SAM (vis (m))':'SAM_vis_m', ' MSA (ft)':'MSA'}, inplace=True)
    
    return locs