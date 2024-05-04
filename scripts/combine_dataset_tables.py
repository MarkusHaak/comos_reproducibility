import os
import glob

import pandas as pd

scipt_path = os.path.dirname(__file__)

required_cols = [
    'dataset', 'sample', 'NAT_source', 'ref_source'#, 'WGA_source', 'priority'
    ]

# parse individual dataframes
dfs = []
for fp in glob.glob(os.path.join(scipt_path, "../datasets/*.csv")):
    d = pd.read_csv(fp, index_col=0)
    d['ID'] = d['dataset'] + "/" + d['sample']
    d = d.set_index('ID', drop=True)
    dfs.append(d)
df = pd.concat(dfs)

# parse dataset information from manual curation or other sources
for fp in glob.glob(os.path.join(scipt_path, "../manual_curation/*.csv")):
    d = pd.read_csv(fp)
    d['ID'] = d['dataset'] + "/" + d['sample']
    d = d.set_index('ID', drop=True)
    for col in d.columns:
        if col not in ['ID', 'dataset', 'sample']:
            df.loc[d.index, col] = d[col]

sel = ~pd.isna(df[required_cols[0]])
for col in required_cols:
    sel &= ~pd.isna(df[col])
df.loc[sel].to_csv(os.path.join(scipt_path, "../all_datasets.csv"))