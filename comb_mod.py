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
df['dif']=df['mod_global']-df['obs']
df['dif2']=df['dif']**2
dfgm=df.groupby(['sat']).mean().reset_index()
dfgs=df.groupby(['sat']).sum().reset_index()
dfgm['cnt']=dfgs['lat']/dfgm['lat']
dfgm['dif2']=np.sqrt(dfgm['dif2']+1e-12)
dfgm[['sat','cnt','dif2','dif']]
"""
modnum=6
satmod1=['Sent6','Sent3b','Sent3a','Jason3','HiYang2b','CFOsat','CryoSat2','SAltika']
satmod2=['SWOT','HiYang2c']
df1=df[(df['sat'].isin(satmod1)) & (df['mod_'+model[modnum]]>0.001)]
df2=df[(df['sat'].isin(satmod2)) & (df['mod_'+model[modnum]]>0.001)]
fig = plt.figure(figsize=(9,8))
ax1 = fig.add_subplot()
ax1.scatter(df2['obs'],df2['mod_'+model[modnum]],s=1,label='non-assimilated sat.')
ax1.scatter(df1['obs'],df1['mod_'+model[modnum]],s=1,label='assimilated sat.')
ax1.legend()
ax1.set_xlabel('obs. significant wave height')
ax1.set_ylabel('mod. significant wave height')
plt.title('IBI model vs. observations, 2023')
plt.grid()
plt.show()
plt.close()
"""
"""
df=df[(df['dt']>pd.to_datetime('2023-06-01')) & (df['dt']<pd.to_datetime('2023-10-30'))]
df['cnt']=0
for mo in model:
    print(mo)
    df['cnt']=np.where(df['mod_'+mo]>0.001,df['cnt']+1,df['cnt'])

fig = plt.figure(figsize=(14,10))
ax1 = fig.add_subplot()
sca=ax1.scatter(df['lon'],df['lat'],c=df['cnt'],cmap=plt.cm.gist_ncar,vmin=0.9,vmax=6.1,s=1)
plt.colorbar(sca)
ax1.label_outer()
plt.tight_layout()
plt.savefig('/data/users/vifr/Aggreg/weight_new.png')
plt.close()
fig.clear()
"""
#df=df[(df['dt'].dt.month==3) | (df['dt'].dt.month==4) | (df['dt'].dt.month==5)]
satmod=9
#df=df[df['sat']==mode[satmod]]
mnth=12
#df=df[(df['dt'].dt.month==mnth)]
df=df[(df['sat']==mode[satmod])]
#df=df[(df['sat']==mode[0]) | (df['sat']==mode[5])] # & (df['sat']!=mode[6])]
#df=df[(df['obs']>11.00) & (df['obs']<=21.00)]
#df=df.reset_index()
#df=df.drop_duplicates(['lon', 'lat', 'obs', 'sat', 'dt'])
for mo in model:
    print(mo)
    df['a_'+mo]=None
df['mod']=None
#df1=df[(df['mod_baltic']>0.001) & (df['mod_idf']>0.001) & (df['mod_global']>0.001) & (df['mod_nsb']>0.001) & (df['mod_nws']>0.001) & (df['mod_arctic']>0.001)]

modnn=[]
def  submodel(modn=[0]):
    global df
    global modnn
    print(modn)
    df1=df
    for mon in modn:
        df1=df1[df1['mod_'+model[mon]]>0.001]
    if len(df1['obs'])>0:
        matr = np.empty((len(modn), len(modn)))
        resr = np.empty(len(modn))
        rsqm = np.empty(len(modn)) 
        rsqmsum=0
        for idr,mor in enumerate(modn):
            resr[idr]=(df1['mod_'+model[mor]] * df1['obs']).sum()
            rsqm[idr]=np.sqrt(((df1['mod_'+model[mor]] - df1['obs'])**2).sum()/len(df1['obs']))
            rsqmsum=rsqmsum+1/rsqm[idr]
            for idc,moc in enumerate(modn):
                matr[idr,idc]=(df1['mod_'+model[mor]] * df1['mod_'+model[moc]]).sum()
        sol = np.linalg.solve(matr, resr)
        iscor=True
        for idr,mor in enumerate(modn):
            if sol[idr]<0:
                iscor=False
        if iscor:
            solsum=sol.sum()
            if len(modn)>1:
                print(sol,solsum,sol[1]/sol[0])
            else:
                print(sol,solsum)
            df1['difb']=-df1['obs']
            df1['difbn']=-df1['obs']
            df1['difq']=-df1['obs']
            df1['mod']=0
            for idr,mor in enumerate(modn):
                df1['difb']=df1['difb']+sol[idr]*df1['mod_'+model[mor]]
                df1['difbn']=df1['difbn']+sol[idr]/solsum*df1['mod_'+model[mor]]
                df1['difq']=df1['difq']+1/rsqm[idr]/rsqmsum*df1['mod_'+model[mor]]
                df1['a_'+model[mor]] = sol[idr]
                df1['mod']=df1['mod']+sol[idr]*df1['mod_'+model[mor]]
                #mdict = df1.set_index(['dt']).to_dict()
                #df['a_'+model[mor]] = df['a_'+model[mor]].map(lambda x: mdict.get(x,None))
                #df['a_'+model[mor]] = df['a_'+model[mor]].map(df1.set_index(['lon', 'lat', 'obs', 'sat', 'dt'])['a_'+model[mor]])
            df.set_index(['lon','lat','obs','sat', 'dt'], inplace=True)
            df.update(df1.set_index(['lon','lat','obs','sat', 'dt']))
            df=df.reset_index()
            rsqmb=np.sqrt(((df1['difb'])**2).sum()/len(df1['obs']))
            rsqmbn=np.sqrt(((df1['difbn'])**2).sum()/len(df1['obs']))
            rsqmq=np.sqrt(((df1['difq'])**2).sum()/len(df1['obs']))
            print(rsqm,rsqmb,rsqmbn,rsqmq)
    del(df1)

submodel(modn=[8])
submodel(modn=[7])
submodel(modn=[6])
submodel(modn=[5])
submodel(modn=[4])
submodel(modn=[3])
submodel(modn=[2])
submodel(modn=[1])
submodel(modn=[0])
submodel(modn=[0,8])
submodel(modn=[0,7])
submodel(modn=[0,6])
submodel(modn=[0,5])
submodel(modn=[0,4])
submodel(modn=[0,3])
submodel(modn=[0,2])
submodel(modn=[0,1])
submodel(modn=[1,2])
submodel(modn=[1,3])
submodel(modn=[1,4])
submodel(modn=[1,6])
submodel(modn=[1,8])
submodel(modn=[2,3])
submodel(modn=[2,4])
submodel(modn=[2,8])
submodel(modn=[3,4])
submodel(modn=[3,6])
submodel(modn=[3,7])
submodel(modn=[3,8])
submodel(modn=[4,8])
submodel(modn=[6,7])
submodel(modn=[6,8])
submodel(modn=[0,1,2])
submodel(modn=[0,1,3])
submodel(modn=[0,1,4])
submodel(modn=[0,1,6])
submodel(modn=[0,1,8])
submodel(modn=[0,2,3])
submodel(modn=[0,2,4])
submodel(modn=[0,2,8])
submodel(modn=[0,3,4])
submodel(modn=[0,3,6])
submodel(modn=[0,3,7])
submodel(modn=[0,3,8])
submodel(modn=[0,4,8])
submodel(modn=[0,6,7])
submodel(modn=[0,6,8])
submodel(modn=[1,2,3])
submodel(modn=[1,2,4])
submodel(modn=[1,2,8])
submodel(modn=[1,3,4])
submodel(modn=[1,3,6])
submodel(modn=[1,3,8])
submodel(modn=[1,4,8])
submodel(modn=[1,6,8])
submodel(modn=[2,3,4])
submodel(modn=[2,3,8])
submodel(modn=[2,4,8])
submodel(modn=[3,4,8])
submodel(modn=[3,6,7])
submodel(modn=[3,6,8])
submodel(modn=[0,1,2,3])
submodel(modn=[0,1,2,4])
submodel(modn=[0,1,2,8])
submodel(modn=[0,1,3,4])
submodel(modn=[0,1,3,6])
submodel(modn=[0,1,3,8])
submodel(modn=[0,1,4,8])
submodel(modn=[0,1,6,8])
submodel(modn=[0,2,3,4])
submodel(modn=[0,2,3,8])
submodel(modn=[0,2,4,8])
submodel(modn=[0,3,4,8])
submodel(modn=[0,3,6,8])
submodel(modn=[1,2,3,4])
submodel(modn=[1,2,3,8])
submodel(modn=[1,2,4,8])
submodel(modn=[1,3,4,8])
submodel(modn=[1,3,6,8])
submodel(modn=[2,3,4,8])
submodel(modn=[0,1,2,3,4])
submodel(modn=[0,1,2,3,8])
submodel(modn=[0,1,2,4,8])
submodel(modn=[0,1,3,4,8])
submodel(modn=[0,1,3,6,8])
submodel(modn=[0,2,3,4,8])
submodel(modn=[1,2,3,4,8])
submodel(modn=[0,1,2,3,4,8])

#df.to_pickle('/data/users/vifr/Aggreg/all_mod2023.pkl')

"""
df['lat0']=round(df['lat'],0)
df['lon0']=round(df['lon'],0)
dfg=df.groupby([df['lat0'],df['lon0'],pd.Grouper(key="dt",freq='Y')]).mean().reset_index()  #


fig = plt.figure(figsize=(6,4),dpi=200)
ax1 = fig.add_subplot()
sca=plt.scatter(dfg['lon0'],dfg['lat0'],c=dfg['mod_global']-dfg['obs'],s=2,vmin=-1,vmax=1)
plt.colorbar(sca)
plt.show() 
"""

for mo in model:
    print(mo)
    fig = plt.figure(figsize=(6,4),dpi=200)
    ax1 = fig.add_subplot()
    sca=plt.scatter(df['lon'], df['lat'], c=df['a_'+mo],s=1)
    plt.colorbar(sca)
    #plt.title('coefficient for model='+mo+' satellite='+str(mode[satmod]))
    #plt.savefig('/data/users/vifr/Aggreg/pic_coeff_spring/coeff_'+mo+'_sat_'+str(satmod)+'.png')
    plt.title('coefficient for model='+mo+' month='+str(mnth))
    plt.savefig('/data/users/vifr/Aggreg/pic_coeff_spring/coeff_'+mo+'_month_'+str(mnth)+'.png')
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
