#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 15:41:38 2025

@author: vifr
"""

import xarray as xr
import pandas as pd
import datetime
import glob
import os

mode=['SWOT','Sent6','Sent3b','Sent3a','Jason3','HiYang2c','HiYang2b','CFOsat','CryoSat2','SAltika']

def hround(t):
    # Rounds to nearest hour by adding a timedelta hour if minute >= 30
    return (t.replace(second=0, microsecond=0, minute=0, hour=t.hour)
               +datetime.timedelta(hours=t.minute//30))
"""
swot0=pd.read_csv('/data/projects/claim/arctic2023/cmems_obs-wave_glo_phy-swh_nrt_swon-l3_PT1S_1739871479911.csv',skiprows=5)
swot0=swot0[swot0['parameter']=='VAVH']
swot0['dt']=[hround(datetime.datetime.strptime(swot0['time'][i],'%Y-%m-%dT%H:%M:%S.000Z')) for i in range(len(swot0['time']))]
swot0['day']=[swot0['dt'][i].day for i in range(len(swot0['time']))]
swot0['hour']=[swot0['dt'][i].hour for i in range(len(swot0['time']))]
swot0['month']=[swot0['dt'][i].month for i in range(len(swot0['time']))]
swot0['mod']='SWOT'
print('SWOT finished')

all_files = glob.glob(os.path.join('/data/projects/claim/arctic2023/', "cmems_obs-wave_glo_phy-swh_nrt_s6a-l3_PT1S_??.csv"))
swot1=pd.concat((pd.read_csv(f,skiprows=5) for f in all_files), ignore_index=True)
swot1['dt']=[hround(datetime.datetime.strptime(swot1['time'][i],'%Y-%m-%dT%H:%M:%S.000Z')) for i in range(len(swot1['time']))]
swot1['day']=[swot1['dt'][i].day for i in range(len(swot1['time']))]
swot1['hour']=[swot1['dt'][i].hour for i in range(len(swot1['time']))]
swot1['month']=[swot1['dt'][i].month for i in range(len(swot1['time']))]
swot1['mod']='Sent6'
print('Sent6 finished')

all_files = glob.glob(os.path.join('/data/projects/claim/arctic2023/', "cmems_obs-wave_glo_phy-swh_nrt_s3b-l3_PT1S_??.csv"))
swot2=pd.concat((pd.read_csv(f,skiprows=5) for f in all_files), ignore_index=True)
swot2['dt']=[hround(datetime.datetime.strptime(swot2['time'][i],'%Y-%m-%dT%H:%M:%S.000Z')) for i in range(len(swot2['time']))]
swot2['day']=[swot2['dt'][i].day for i in range(len(swot2['time']))]
swot2['hour']=[swot2['dt'][i].hour for i in range(len(swot2['time']))]
swot2['month']=[swot2['dt'][i].month for i in range(len(swot2['time']))]
swot2['mod']='Sent3b'
print('Sent3b finished')

all_files = glob.glob(os.path.join('/data/projects/claim/arctic2023/', "cmems_obs-wave_glo_phy-swh_nrt_s3a-l3_PT1S_??.csv"))
swot3=pd.concat((pd.read_csv(f,skiprows=5) for f in all_files), ignore_index=True)
swot3['dt']=[hround(datetime.datetime.strptime(swot3['time'][i],'%Y-%m-%dT%H:%M:%S.000Z')) for i in range(len(swot3['time']))]
swot3['day']=[swot3['dt'][i].day for i in range(len(swot3['time']))]
swot3['hour']=[swot3['dt'][i].hour for i in range(len(swot3['time']))]
swot3['month']=[swot3['dt'][i].month for i in range(len(swot3['time']))]
swot3['mod']='Sent3a'
print('Sent3a finished')

all_files = glob.glob(os.path.join('/data/projects/claim/arctic2023/', "cmems_obs-wave_glo_phy-swh_nrt_j3-l3_PT1S_??.csv"))
swot4=pd.concat((pd.read_csv(f,skiprows=5) for f in all_files), ignore_index=True)
swot4['dt']=[hround(datetime.datetime.strptime(swot4['time'][i],'%Y-%m-%dT%H:%M:%S.000Z')) for i in range(len(swot4['time']))]
swot4['day']=[swot4['dt'][i].day for i in range(len(swot4['time']))]
swot4['hour']=[swot4['dt'][i].hour for i in range(len(swot4['time']))]
swot4['month']=[swot4['dt'][i].month for i in range(len(swot4['time']))]
swot4['mod']='Jason3'
print('Jason3 finished')

swot5=pd.read_csv('/data/projects/claim/arctic2023/cmems_obs-wave_glo_phy-swh_nrt_h2c-l3_PT1S_1739867660349.csv',skiprows=5)
swot5=swot5[swot5['parameter']=='VAVH']
swot5['dt']=[hround(datetime.datetime.strptime(swot5['time'][i],'%Y-%m-%dT%H:%M:%S.000Z')) for i in range(len(swot5['time']))]
swot5['day']=[swot5['dt'][i].day for i in range(len(swot5['time']))]
swot5['hour']=[swot5['dt'][i].hour for i in range(len(swot5['time']))]
swot5['month']=[swot5['dt'][i].month for i in range(len(swot5['time']))]
swot5['mod']='HiYang2c'
print('HiYang2c finished')

swot6=pd.read_csv('/data/projects/claim/arctic2023/cmems_obs-wave_glo_phy-swh_nrt_h2b-l3_PT1S_1739867412324.csv',skiprows=5)
swot6=swot6[swot6['parameter']=='VAVH']
swot6['dt']=[hround(datetime.datetime.strptime(swot6['time'][i],'%Y-%m-%dT%H:%M:%S.000Z')) for i in range(len(swot6['time']))]
swot6['day']=[swot6['dt'][i].day for i in range(len(swot6['time']))]
swot6['hour']=[swot6['dt'][i].hour for i in range(len(swot6['time']))]
swot6['month']=[swot6['dt'][i].month for i in range(len(swot6['time']))]
swot6['mod']='HiYang2b'
print('HiYang2b finished')

swot7=pd.read_csv('/data/projects/claim/arctic2023/cmems_obs-wave_glo_phy-swh_nrt_cfo-l3_PT1S_1739802615768.csv',skiprows=5)
swot7=swot7[swot7['parameter']=='VAVH']
swot7['dt']=[hround(datetime.datetime.strptime(swot7['time'][i],'%Y-%m-%dT%H:%M:%S.000Z')) for i in range(len(swot7['time']))]
swot7['day']=[swot7['dt'][i].day for i in range(len(swot7['time']))]
swot7['hour']=[swot7['dt'][i].hour for i in range(len(swot7['time']))]
swot7['month']=[swot7['dt'][i].month for i in range(len(swot7['time']))]
swot7['mod']='CFOsat'
print('CFOsat finished')

all_files = glob.glob(os.path.join('/data/projects/claim/arctic2023/', "cmems_obs-wave_glo_phy-swh_nrt_c2-l3_PT1S_??.csv"))
swot8=pd.concat((pd.read_csv(f,skiprows=5) for f in all_files), ignore_index=True)
swot8['dt']=[hround(datetime.datetime.strptime(swot8['time'][i],'%Y-%m-%dT%H:%M:%S.000Z')) for i in range(len(swot8['time']))]
swot8['day']=[swot8['dt'][i].day for i in range(len(swot8['time']))]
swot8['hour']=[swot8['dt'][i].hour for i in range(len(swot8['time']))]
swot8['month']=[swot8['dt'][i].month for i in range(len(swot8['time']))]
swot8['mod']='CryoSat2'
print('CryoSat2 finished')

all_files = glob.glob(os.path.join('/data/projects/claim/arctic2023/', "cmems_obs-wave_glo_phy-swh_nrt_al-l3_PT1S_??.csv"))
swot9=pd.concat((pd.read_csv(f,skiprows=5) for f in all_files), ignore_index=True)
swot9['dt']=[hround(datetime.datetime.strptime(swot9['time'][i],'%Y-%m-%dT%H:%M:%S.000Z')) for i in range(len(swot9['time']))]
swot9['day']=[swot9['dt'][i].day for i in range(len(swot9['time']))]
swot9['hour']=[swot9['dt'][i].hour for i in range(len(swot9['time']))]
swot9['month']=[swot9['dt'][i].month for i in range(len(swot9['time']))]
swot9['mod']='SAltika'
print('SAltika finished')

swot=pd.concat([swot0,swot1,swot2,swot3,swot4,swot5,swot6,swot7,swot8,swot9] , ignore_index=True)
swot.to_pickle('/data/users/vifr/Aggreg/swot.pkl')
"""
swot=pd.read_pickle('/data/users/vifr/Aggreg/swot.pkl')

#ds=xr.open_dataset('/data/users/vifr/Aggreg/aggreg_All_2023101811.nc', engine='netcdf4')
#ds=xr.open_dataset('/data/users/vifr/Aggreg/cmems_mod_glo_wav_anfc_0.083deg_PT3H-i_VHM0_22.00W-43.00E_23.00N-67.00N_2023-01-01-2024-01-01.nc', engine='netcdf4')
#ds=ds.isel(time=slice(1499,2930))
#ds=ds.resample(time="1H").interpolate(kind="linear")
#ds=xr.open_dataset('/data/users/vifr/Aggreg/idf/swh/wam.idf.nc', engine='netcdf4')
#ds=xr.open_dataset('/data/users/vifr/Aggreg/nsb/swh/wam.nsb.nc', engine='netcdf4')
#ds=ds.rename({'lat':'latitude','lon':'longitude','swh':'VHM0'})
#ds=xr.open_dataset('/data/users/vifr/Aggreg/cmems_mod_bal_wav_anfc_PT1H-i_VHM0_9.01E-30.21E_53.01N-65.91N_2023-01-01-2024-01-01.nc', engine='netcdf4')
#ds=xr.open_dataset('/data/users/vifr/Aggreg/cmems_mod_blk_wav_anfc_2.5km_PT1H-i_VHM0_27.25E-42.00E_40.50N-47.33N_2023-01-01-2024-01-01.nc', engine='netcdf4')
#ds=xr.open_dataset('/data/users/vifr/Aggreg/cmems_mod_ibi_wav_anfc_0.027deg_PT1H-i_VHM0_19.00W-5.00E_26.00N-56.00N_2023-01-01-2024-01-01.nc', engine='netcdf4')
#ds=xr.open_dataset('/data/users/vifr/Aggreg/cmems_mod_med_wav_anfc_4.2km_PT1H-i_VHM0_18.12W-36.29E_30.19N-45.98N_2023-01-01-2024-01-01.nc', engine='netcdf4')
ds=xr.open_dataset('/data/users/vifr/Aggreg/cmems_mod_nws_wav_anfc_0.027deg_PT1H-i_VHM0_16.00W-10.00E_46.00N-61.31N_2023-01-01-2024-01-01.nc', engine='netcdf4')
#ds=xr.open_mfdataset('/data/projects/claim/arctic2023/cba202301????_MyWaveWam3_b*.nc', engine='netcdf4')
#ds=xr.open_dataset('/data/projects/claim/arctic2023/carctic2023.nc', engine='netcdf4')
#ds=ds.rename({'lat':'latitude','lon':'longitude'})
#ds1=ds['VHM0'][0]
#ds1=ds1.assign(tmp1=ds1['VHM0'] * np.nan)
#ds1=ds1.assign(wght1=ds1['VHM0'] * np.nan)
#swot=swot[(swot['month']==1)]

lat0=ds['latitude'].values[0]
latn=ds['latitude'].values[-1]
if lat0>latn:
    latv=lat0
    lat0=latn
    latn=latv
nlat=len(ds['latitude'].values)
dlat=(latn-lat0)/(nlat-1)
print(lat0,latn,nlat,dlat)
lon0=ds['longitude'].values[0]
lonn=ds['longitude'].values[-1]
nlon=len(ds['longitude'].values)
dlon=(lonn-lon0)/(nlon-1)
print(lon0,lonn,nlon,dlon)

df = pd.DataFrame()
tmp=[]
for i in range(len(ds.time)): #range(50,52):#   
    dsc=ds['VHM0'].isel(time=i)
    swotd=swot[(swot['month']==pd.to_datetime(ds.time[i].values).month) & (swot['day']==pd.to_datetime(ds.time[i].values).day) & (swot['hour']==pd.to_datetime(ds.time[i].values).hour) &
               (swot['longitude']>lon0) & (swot['longitude']<lonn) & (swot['latitude']>lat0) & (swot['latitude']<latn) ]
    swotd=swotd.reset_index()
    print(i,ds.time[i].values,len(swotd['latitude']))
    sate=set([])
    try:
        for j in range(len(swotd['value'])):
            tmp.extend([{'lon': swotd['longitude'][j], 'lat':swotd['latitude'][j], 'obs': swotd['value'][j], 'mod': dsc.sel(latitude=swotd['latitude'][j],longitude=swotd['longitude'][j],method='nearest',tolerance=dlon).values,'sat':swotd['mod'][j],'dt':swotd['dt'][j]}]) #, ignore_index=True)
    except:
        print('except 0', i)
    del swotd
df = pd.concat([df, pd.DataFrame(tmp)], ignore_index=True)
df=df[(df['obs']>0.01) & (df['mod']>0.01)]
print(df)
df.to_pickle('/data/users/vifr/Aggreg/nws2023.pkl')
