#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 16:27:36 2025

@author: vifr
"""

#import xarray as xr
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import warnings
warnings.simplefilter(action='ignore', category=pd.errors.SettingWithCopyWarning)

mode=['SWOT','Sent6','Sent3b','Sent3a','Jason3','HiYang2c','HiYang2b','CFOsat','CryoSat2','SAltika']

model=['global','nsb','idf','arctic','baltic','black','ibi','med','nws']
"""
df=pd.read_pickle('/data/users/vifr/Aggreg/'+model[0]+'2023.pkl')
df.rename(columns={'mod':'mod_'+model[0]}, inplace=True)

for mo in model[1:]:
    print(mo)
    dfp=pd.read_pickle('/data/users/vifr/Aggreg/'+mo+'2023.pkl')
    dfp.rename(columns={'mod':'mod_'+mo}, inplace=True)
    df=df.merge(dfp, on=['lon', 'lat', 'obs', 'sat', 'dt'], how='outer')
df.to_pickle('/data/users/vifr/Aggreg/all2023.pkl')
"""
df=pd.read_pickle('/data/users/vifr/Aggreg/all2023.pkl')
df=df.drop(['sat'], axis=1)
df['lat0']=round(df['lat'],0)
df['lon0']=round(df['lon'],0)
dfg=df.groupby([df['lat0'],df['lon0']]).mean().reset_index() 
print(dfg[['lat0','lon0','obs']])

#df=df[(df['dt'].dt.month==3) | (df['dt'].dt.month==4) | (df['dt'].dt.month==5)]
#satmod=6
#df=df[df['sat']==mode[satmod]]
#df=df[(df['sat']!=mode[0]) &  (df['sat']!=mode[5]) & (df['sat']!=mode[6])]
#df=df.reset_index()
#df=df.drop_duplicates(['lon', 'lat', 'obs', 'sat', 'dt'])
for mo in model:
    print(mo)
    dfg['a_'+mo]=None
df['mod']=None
dfi=df.set_index(['lon','lat','obs','dt'])
#df1=df[(df['mod_baltic']>0.001) & (df['mod_idf']>0.001) & (df['mod_global']>0.001) & (df['mod_nsb']>0.001) & (df['mod_nws']>0.001) & (df['mod_arctic']>0.001)]

for ind,dfgg in dfg.iterrows():
    df1=df[(abs(round(df['lat0'],0)-dfgg['lat0'])<0.01) & (abs(round(df['lon0'],0)-dfgg['lon0'])<0.01)]
    print(df1['obs'].count(),df1['mod_'+model[0]].count(),df1['mod_'+model[1]].count(),df1['mod_'+model[2]].count(),df1['mod_'+model[3]].count(),dfgg['lat0'],dfgg['lon0'])
    if (not(np.isnan(dfgg['obs']))) & (df1['obs'].count()>9):
        modn=[0,1,2,3,4,5,6,7,8]
        iscor=False
        while not(iscor):
            iscor=True
            for mon in modn:
                if (df1['mod_'+model[mon]].count()==0) & (not(modn is None)) & (iscor):
                    modn.remove(mon)
                    #print(mon,modn,df1['mod_'+model[mon]].count())
                    iscor=False
        #for mon in modn:
        #    df1=df1[df1['mod_'+model[mon]]>0.001]
        #print(not(modn is None))
        if (not(modn is None)):
            iscor=False
            while not(iscor):
                print(modn,dfgg['lat0'],dfgg['lon0'])
                matr = np.empty((len(modn), len(modn)))
                resr = np.empty(len(modn))
                for idr,mor in enumerate(modn):
                    resr[idr]=(df1['mod_'+model[mor]] * df1['obs']).sum(skipna=True)
                    for idc,moc in enumerate(modn):
                        matr[idr,idc]=(df1['mod_'+model[mor]] * df1['mod_'+model[moc]]).sum(skipna=True)
                try:
                    sol = np.linalg.solve(matr, resr)
                except:
                    sol,re = np.linalg.lstsq(matr, resr)
                iscor=True
                for idr,mor in enumerate(modn):
                    if (sol[idr]<0) & (iscor):
                        iscor=False
                        modn.remove(mor)    
                        if modn is None:
                            iscor=True
            if (iscor) & (not(modn is None)):
                solsum=sol.sum()
                print(sol,solsum)
                df1['mod']=0
                for idr,mor in enumerate(modn):
                    df1.loc[:,'a_'+model[mor]] = sol[idr]
                    df1['mod']=df1['mod']+sol[idr]*df1['mod_'+model[mor]]
                    dfg.loc[ind,'a_'+model[mor]]=sol[idr]
                #df.set_index(['lon','lat','obs','dt'], inplace=True)
                dfi.update(df1.set_index(['lon','lat','obs', 'dt']))
                df=dfi.reset_index()
    del(df1)

dfg.to_pickle('/data/users/vifr/Aggreg/all_group_2023.pkl')
df.to_pickle('/data/users/vifr/Aggreg/all_group_model_2023.pkl')

for mo in model:
    print(mo)
    fig = plt.figure(figsize=(6,4),dpi=200)
    ax1 = fig.add_subplot()
    sca=plt.scatter(dfg['lon0'], dfg['lat0'], c=dfg['a_'+mo],s=5,marker="s")
    plt.colorbar(sca)
    plt.title('local coefficient for model='+mo)
    plt.savefig('/data/users/vifr/Aggreg/pic_coeff/coeff_local_'+mo+'.png')
    #plt.title('coefficient for model='+mo+' satellite=asim')
    #plt.savefig('/data/users/vifr/Aggreg/pic_coeff_spring/coeff_asim.png')

    plt.close()
    #plt.show() 
"""
df=pd.read_pickle('/data/users/vifr/Aggreg/all_mod2023.pkl')
df['dif']=df['mod']-df['obs']
df['dif2']=df['dif']**2
df['lat0']=round(df['lat'],0)
df['lon0']=round(df['lon'],0)
dfg=df.groupby([df['lat0'],df['lon0'],pd.Grouper(key="dt",freq='Y')]).mean().reset_index()  

fig = plt.figure(figsize=(6,4),dpi=200)
ax1 = fig.add_subplot()
sca=plt.scatter(dfg['lon0'],dfg['lat0'],c=np.sqrt(dfg['dif2']),s=1)
plt.colorbar(sca)
plt.savefig('/data/users/vifr/Aggreg/pic_coeff/rmsd.png')
plt.close() 
"""
