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
import sys

mode=['SWOT','Sent6','Sent3b','Sent3a','Jason3','HiYang2c','HiYang2b','CFOsat','CryoSat2','SAltika']

model=['global','nsb','idf','arctic','baltic','black','ibi','med','nws']
    
modnum=0

df=pd.read_pickle('/data/users/vifr/Aggreg/all_mod2023.pkl')
"""
df=df[(df['sat']==mode[0]) | (df['sat']==mode[5])]
df=df.drop(['sat'], axis=1)
df=df.drop(['dt'], axis=1)
#df['obsr']=round(df['obs'],0)
for mo in model:
    df1=df[(df['mod_'+mo]>0.001) & (df['mod_global']>0.001) & (df['mod']>0.001) & (df['obs']>0.001)].reset_index().copy()
    df1['dif']=df1['mod_'+mo]-df1['obs']
    df1['dif__']=df1['mod_global']-df1['obs']
    df1['dif_']=df1['mod']-df1['obs']
    df1['dif2']=df1['dif']**2
    df1['dif2__']=df1['dif__']**2
    df1['dif2_']=df1['dif_']**2
    dfgm=df1.mean()#.reset_index()
    #print(dfgm)
    dfgmcnt=df1['lat'].count()
    #print(df1['mod'].count(),df1['mod_global'].count(),df1['mod'].count(),df1['obs'])
    dfgmdif2=np.sqrt(dfgm['dif2']+1e-12)
    dfgmdif2__=np.sqrt(dfgm['dif2__']+1e-12)
    dfgmdif2_=np.sqrt(dfgm['dif2_']+1e-12)
    print(mo,dfgmcnt,dfgmdif2,dfgmdif2__,dfgmdif2_,dfgm['dif'],dfgm['dif__'],dfgm['dif_'])
    del(df1)

sys.exit()
"""
lat=55
lon=13
#df1=df[(abs(df['lat']-lat)<0.05) & (abs(df['lon']-lon)<0.05)]
df1=df[df['sat']=='SWOT']
fig = plt.figure(figsize=(7,5),dpi=200)
ax1 = fig.add_subplot()
plt.plot(df1['dt'],df1['obs'],label='obs',ls='',marker='*')
ax1.plot(df1['dt'],df1['mod'],label='multi model',ls='',marker='o')
ax1.plot(df1['dt'],df1['mod_global'],label='global')
ax1.plot(df1['dt'],df1['mod_nsb'],label='nsb')
ax1.plot(df1['dt'],df1['mod_idf'],label='idf')
ax1.plot(df1['dt'],df1['mod_arctic'],label='arctic')
ax1.plot(df1['dt'],df1['mod_baltic'],label='baltic')
ax1.plot(df1['dt'],df1['mod_ibi'],label='ibi')
ax1.plot(df1['dt'],df1['mod_nws'],label='nws')

ax1.legend()
#plt.title('RMSD, model='+model[modnum])
ax1.set_xlim(pd.to_datetime('2023-10-22'),pd.to_datetime('2023-10-27'))
plt.title('SWH for satellte SWOT')
plt.savefig('/data/users/vifr/Aggreg/pic_coeff/SWH_time_SWOT.png')
plt.close() 

sys.exit


#df=df[(df['sat']==mode[0]) | (df['sat']==mode[5])]
df=df.drop(['sat'], axis=1)
#df=pd.read_pickle('/data/users/vifr/Aggreg/all_group_model_2023.pkl')
df['dif']=df['mod_'+model[modnum]]-df['obs']
df['dif_']=df['mod']-df['obs']
df['dif2']=df['dif']**2
df['dif2_']=df['dif_']**2
df['obs2']=df['obs']**2
df['lat0']=round(df['lat'],0)
df['lon0']=round(df['lon'],0)
dfg=df.groupby([df['lat0'],df['lon0']]).mean().reset_index() 
dfg['dif2']=dfg['dif2'].astype(float)
dfg['dif2_']=dfg['dif2_'].astype(float)
dfg['obs2']=dfg['obs2'].astype(float)
dfg=dfg[dfg['dif2'].notna()]
dfg=dfg[dfg['dif2_'].notna()]
dfg=dfg[dfg['obs2'].notna()]
dfg['dif2']=np.sqrt(dfg['dif2']+1e-12)
dfg['dif2_']=np.sqrt(dfg['dif2_']+1e-12)
dfg['obs2']=np.sqrt(dfg['obs2']+1e-12-dfg['obs']**2)

fig = plt.figure(figsize=(6,4),dpi=200)
ax1 = fig.add_subplot()
sca=plt.scatter(dfg['lon0'],dfg['lat0'],c=dfg['obs2'],s=5,marker="s") #,vmin=0.04,vmax=0.515)
plt.colorbar(sca)
#plt.title('RMSD, model='+model[modnum])
plt.title('SWH variability of observations')
plt.savefig('/data/users/vifr/Aggreg/pic_coeff/var.png')
plt.close() 

fig = plt.figure(figsize=(6,4),dpi=200)
ax1 = fig.add_subplot()
sca=plt.scatter(dfg['lon0'],dfg['lat0'],c=dfg['dif2_']/dfg['obs2'],s=5,marker="s",vmin=0,vmax=1)
plt.colorbar(sca)
#plt.title('RMSD, model='+model[modnum])
plt.title('RMSD of multi model scaled to SWH variability')
plt.savefig('/data/users/vifr/Aggreg/pic_coeff/rmsd_var.png')
plt.close() 

fig = plt.figure(figsize=(6,4),dpi=200)
ax1 = fig.add_subplot()
sca=plt.scatter(dfg['lon0'],dfg['lat0'],c=dfg['dif2']/dfg['obs2'],s=5,marker="s",vmin=0,vmax=1)
plt.colorbar(sca)
#plt.title('RMSD, model='+model[modnum])
plt.title('RMSD of global model scaled to SWH variability')
plt.savefig('/data/users/vifr/Aggreg/pic_coeff/rmsd_var_global.png')
plt.close() 

fig = plt.figure(figsize=(6,4),dpi=200)
ax1 = fig.add_subplot()
sca=plt.scatter(dfg['lon0'],dfg['lat0'],c=dfg['dif2']-dfg['dif2_'],cmap='seismic',s=5,marker="s",vmin=-0.2,vmax=0.2)
plt.colorbar(sca)
#plt.title('RMSD, model='+model[modnum])
plt.title('RMSD of model='+model[modnum]+' - multimodel RMSD for non-assimilated satellites')
plt.savefig('/data/users/vifr/Aggreg/pic_coeff/rmsd_dif_non_'+model[modnum]+'.png')
plt.close() 

"""
fig = plt.figure(figsize=(6,4),dpi=200)
ax1 = fig.add_subplot()
sca=plt.scatter(dfg['lon0'],dfg['lat0'],c=dfg['dif']-dfg['dif_'],cmap='seismic',s=5,marker="s",vmin=-0.2,vmax=0.2)
plt.colorbar(sca)
plt.title('Bias, model='+model[modnum])
plt.title('bias of model='+model[modnum]+' - bias of multimodel')
plt.savefig('/data/users/vifr/Aggreg/pic_coeff/bias_dif_'+model[modnum]+'.png')
plt.close() 

"""