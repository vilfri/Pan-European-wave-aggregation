#!/usr/bin/env python3
import datetime
import numpy as np
import pandas as pd
import xarray as xr
import sys
import glob
import gc
import os #, psutil
import dask
import pickle as pkl
#import xesmf as xe
import warnings
warnings.filterwarnings('ignore')


model=['global','nsb','idf','baltic','black','ibi','med','nws','frontex']
binss=[0.1,0.5,1.25,2.5,4,6,9,14]
binff=[44,88,132,240]
with open('/data/users/vifr/Aggreg/oper/aArr.pkl','rb') as f: aArr = pkl.load(f)

dask.config.set({"array.slicing.split_large_chunks": True})
#dask.config.set(scheduler='synchronous')

date1=glob.glob('/data/users/vifr/SWH/global_*.nc')#[-1]
date1 = max(date1, key=lambda n: n[-13:-3])
date1=date1[-13:-3]


#date0=str(sys.argv[1])
date0=date1   #'2026082618'
os.chdir('/data/users/vifr/Aggreg/')
date0n='??????????'
print(date0)
base=datetime.datetime.strptime(date0, '%Y%m%d%H')
print(base)

nhours=169     #total number of hours in the forecast
smhours=48     #Number or processed hours per data block, any integer number >=1.
               #If smhours>nhours then there will be just 1 data block as before.
               #Small number leads to many blocks, low RAM memory consumption but larger combined processing time.
               #Large number needs more RAM memory, but will be done in fewer blocks with less combined processing time.
ithours=(nhours//smhours)+1     #number of blocks
print(ithours)

# mask insert
lat_new = np.arange(23.5, 66.3, 0.1)  #0.04
lon_new = np.arange(-21, 42.1, 0.1)   #0.04

par='VHM0'

ibf=0
ihours=0
for ihours in range(ithours):
    ds_gl=xr.open_dataset('/data/users/vifr/SWH/global_'+date0+'.nc', engine='netcdf4')[['VHM0']]  #,chunks={"time":1},"longitude":200
    ds_gl=ds_gl.resample(time="1h").interpolate(kind="linear")
    print(ihours,ihours*smhours,min((ihours+1)*smhours,nhours)) 
    if binff[ibf]<=ihours*smhours and ibf<len(binff)-2:
        ibf=ibf+1
    time_new = [base + datetime.timedelta(hours=x) for x in range(ihours*smhours,min((ihours+1)*smhours,nhours))]   #169
    ds_fn=ds_gl.reindex(latitude=lat_new, longitude=lon_new, time=time_new, method='nearest')
    ds_fn['VHM0']=ds_gl['VHM0'].interp(latitude=lat_new,longitude=lon_new,time=time_new)
    
    ds_fn=ds_fn.load()
    ds_gl.close()

    gc.collect()

    ds_fn=ds_fn.assign(tmp=ds_fn["VHM0"] * np.nan)
    ds_fn=ds_fn.assign(tmp1=ds_fn["VHM0"] * np.nan)
    ds_fn=ds_fn.assign(tmp2=ds_fn["VHM0"] * np.nan)
    ds_fn=ds_fn.assign(tmp3=ds_fn["VHM0"] * np.nan)
    ds_fn=ds_fn.assign(tmp4=ds_fn["VHM0"] * np.nan)
    ds_fn=ds_fn.assign(tmp5=ds_fn["VHM0"] * np.nan)
    ds_fn=ds_fn.assign(tmp6=ds_fn["VHM0"] * np.nan)
    ds_fn=ds_fn.assign(tmp7=ds_fn["VHM0"] * np.nan)
    ds_fn=ds_fn.assign(wght0=ds_fn["VHM0"] * np.nan)
    ds_fn=ds_fn.assign(wght=ds_fn["VHM0"] * np.nan)
    ds_fn=ds_fn.assign(wght1=ds_fn["VHM0"] * np.nan)
    ds_fn=ds_fn.assign(wght2=ds_fn["VHM0"] * np.nan)
    ds_fn=ds_fn.assign(wght3=ds_fn["VHM0"] * np.nan)
    ds_fn=ds_fn.assign(wght4=ds_fn["VHM0"] * np.nan)
    ds_fn=ds_fn.assign(wght5=ds_fn["VHM0"] * np.nan)
    ds_fn=ds_fn.assign(wght6=ds_fn["VHM0"] * np.nan)
    ds_fn=ds_fn.assign(wght7=ds_fn["VHM0"] * np.nan)
    dr_gofs=xr.open_dataset('wght/gofs_DEM.tif',engine='rasterio').isel(band=0).drop_vars('band')['band_data']
    dr_gofs=dr_gofs.rename({'x':'longitude','y':'latitude'})
    dr_gofs=dr_gofs.interp(latitude=lat_new,longitude=lon_new)
    dr_nsbs=xr.open_dataset('wght/wam_nsbs_DEM.tif',engine='rasterio').isel(band=0).drop_vars('band')['band_data']
    dr_nsbs=dr_nsbs.rename({'x':'longitude','y':'latitude'})
    dr_nsbs=dr_nsbs.interp(latitude=lat_new,longitude=lon_new)
    dr_idf=xr.open_dataset('wght/idf_DEM.tif',engine='rasterio').isel(band=0).drop_vars('band')['band_data']
    dr_idf=dr_idf.rename({'x':'longitude','y':'latitude'})
    dr_idf=dr_idf.interp(latitude=lat_new,longitude=lon_new)
    dr_med=xr.open_dataset('wght/med_DEM.tif',engine='rasterio').isel(band=0).drop_vars('band')['band_data']
    dr_med=dr_med.rename({'x':'longitude','y':'latitude'})
    dr_med=dr_med.interp(latitude=lat_new,longitude=lon_new)
    dr_black=xr.open_dataset('wght/black_DEM.tif',engine='rasterio').isel(band=0).drop_vars('band')['band_data']
    dr_black=dr_black.rename({'x':'longitude','y':'latitude'})
    dr_black=dr_black.interp(latitude=lat_new,longitude=lon_new)
    dr_ns_cmems=xr.open_dataset('wght/ns_cmems_DEM.tif',engine='rasterio').isel(band=0).drop_vars('band')['band_data']
    dr_ns_cmems=dr_ns_cmems.rename({'x':'longitude','y':'latitude'})
    dr_ns_cmems=dr_ns_cmems.interp(latitude=lat_new,longitude=lon_new)
    dr_bs_cmems=xr.open_dataset('wght/bs_cmems_DEM.tif',engine='rasterio').isel(band=0).drop_vars('band')['band_data']
    dr_bs_cmems=dr_bs_cmems.rename({'x':'longitude','y':'latitude'})
    dr_bs_cmems=dr_bs_cmems.interp(latitude=lat_new,longitude=lon_new)
    dr_ibi_cmems=xr.open_dataset('wght/ibi_DEM.tif',engine='rasterio').isel(band=0).drop_vars('band')['band_data']
    dr_ibi_cmems=dr_ibi_cmems.rename({'x':'longitude','y':'latitude'})
    dr_ibi_cmems=dr_ibi_cmems.interp(latitude=lat_new,longitude=lon_new)

    print('a')

    # mask insert

    gc.collect()

    try:
        date1=glob.glob('/net/isilon/ifs/arch/home/wamopr/uwcw/frontex/arkiv/'+date0[0:4]+'/'+date0[4:6]+'/wam.nc.*.EUROPE')#[-1]
        date1 = max(date1, key=lambda n: n[-17:-7])
        date1=date1[-17:-7]
        print(date1,'frontex_'+date1+'.nc')        
        ds_nsbs=xr.open_dataset('/net/isilon/ifs/arch/home/wamopr/uwcw/frontex/arkiv/'+date0[0:4]+'/'+date0[4:6]+'/wam.nc.'+date1+'.EUROPE', engine='netcdf4')
        ds_nsbs=ds_nsbs.rename({'lat':'latitude','lon':'longitude'})
        datsub=pd.to_datetime(ds_nsbs['time'].values[0])
        diff=datsub-base
        hours = int(np.round(diff.total_seconds()/3600.0+0.5))
        it_frontex=len(ds_nsbs['time'].values)+hours
        print(datsub,hours,it_frontex,len(ds_nsbs['time'].values))
        ds_fn['tmp']=ds_nsbs['hs'].interp(latitude=lat_new,longitude=lon_new,time=time_new)
        ds_nsbs.close()
    except:
        it_frontex=25
        print('problem reading Frontex')
        with open("warnings", "a") as myfile:
            myfile.write(datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')+" Frontex not readable, disregarding it \n")

    print('b')

    try:
        date1=glob.glob('/data/users/vifr/SWH/bal_*.nc')#[-1]
        date1 = max(date1, key=lambda n: n[-13:-3])
        date1=date1[-13:-3]
        print(date1,'bal_'+date1+'.nc')
        ds_nsbs=xr.open_dataset('/data/users/vifr/SWH/bal_'+date1+'.nc', engine='netcdf4')
        datsub=pd.to_datetime(ds_nsbs['time'].values[0])
        diff=datsub-base
        hours = int(np.round(diff.total_seconds()/3600.0+0.5))
        it_bal=len(ds_nsbs['time'].values)+hours
        print(datsub,hours,it_bal,len(ds_nsbs['time'].values))
        ds_fn['tmp1']=ds_nsbs['VHM0'].interp(latitude=lat_new,longitude=lon_new,time=time_new)
        ds_nsbs.close()
    except:
        it_bal=25
        print('problem reading bal')
        with open("warnings", "a") as myfile:
            myfile.write(datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')+" baltic *.nc not readable, disregarding it \n")

    def add_time_dim(xda):
        xda = xda.expand_dims(time = [datetime.datetime.now()])
        return xda

    print('c')

    try:
        ds_nsbs=xr.open_dataset('/net/isilon/ifs/arch/home/wamopr/uwcw/arkiv_2.0/'+date0[0:4]+'/'+date0[4:6]+'/wam.grib.'+date0+'.NSB', engine='cfgrib',decode_timedelta=False)
        #ds_nsbs=ds_nsbs.rename({'lat':'latitude','lon':'longitude'})
        tim=[pd.to_datetime(ds_nsbs.time.values)+pd.Timedelta(ds_nsbs.step.values[i],unit='hours') for i in range(len(ds_nsbs.step))]
        #print(ds_nsbs.step)
        #print(tim)
        ds_nsbs=ds_nsbs.assign_coords({"time":tim})
        ds_nsbs['swh']=ds_nsbs['swh'].swap_dims({'step':'time'})
        datsub=pd.to_datetime(ds_nsbs['time'].values[0])
        #print(ds_nsbs['time'].values)
        #print(ds_nsbs['time'].values[0],ds_nsbs['time'].values[-1])
        diff=datsub-base
        hours = int(np.round(diff.total_seconds()/3600.0+0.5))
        it_nsbs=len(ds_nsbs['time'].values)+hours
        print(datsub,hours,it_nsbs,len(ds_nsbs['time'].values))
        ds_fn['tmp2']=ds_nsbs['swh'].interp(latitude=lat_new,longitude=lon_new,time=time_new)
        ds_nsbs.close()
    except:
        it_nsbs=25
        print('problem reading NSBS')
        with open("warnings", "a") as myfile:
            myfile.write(datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')+" NSBS *.nc not readable, disregarding it \n")

    try:
        ds_nsbs=xr.open_dataset('/net/isilon/ifs/arch/home/wamopr/uwcw/arkiv_2.0/'+date0[0:4]+'/'+date0[4:6]+'/wam.grib.'+date0+'.IDF', engine='cfgrib',decode_timedelta=False)
        #ds_nsbs=ds_nsbs.rename({'lat':'latitude','lon':'longitude'})
        tim=[pd.to_datetime(ds_nsbs.time.values)+pd.Timedelta(ds_nsbs.step.values[i],unit='hours') for i in range(len(ds_nsbs.step))]
        ds_nsbs=ds_nsbs.assign_coords({"time":tim})
        ds_nsbs['swh']=ds_nsbs['swh'].swap_dims({'step':'time'})
        datsub=pd.to_datetime(ds_nsbs['time'].values[0])
        diff=datsub-base
        hours = int(np.round(diff.total_seconds()/3600.0+0.5))
        it_idf=len(ds_nsbs['time'].values)+hours
        print(datsub,hours,it_idf,len(ds_nsbs['time'].values))
        ds_fn['tmp3']=ds_nsbs['swh'].interp(latitude=lat_new,longitude=lon_new,time=time_new)
        ds_nsbs.close()
    except:
        it_idf=25
        print('problem reading IDF')
        with open("warnings", "a") as myfile:
            myfile.write(datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')+" IDF *.nc not readable, disregarding it \n")

    print('d')

    try:
        date1=glob.glob('/data/users/vifr/SWH/nws_*.nc')#[-1]
        date1 = max(date1, key=lambda n: n[-13:-3])
        date1=date1[-13:-3]
        print(date1,'nws_'+date1+'.nc')
        datsub=datetime.datetime.strptime(date1, '%Y%m%d%H')
        diff=datsub-base
        print(diff.total_seconds()/3600.0)
        hours = int(np.round(diff.total_seconds()/3600.0))
        print(hours)
        ds_nsbs=xr.open_dataset('/data/users/vifr/SWH/nws_'+date1+'.nc', engine='netcdf4')
        datsub=pd.to_datetime(ds_nsbs['time'].values[0])
        diff=datsub-base
        hours = int(np.round(diff.total_seconds()/3600.0+0.5))
        it_nws=len(ds_nsbs['time'].values)+hours
        print(datsub,hours,it_nws,len(ds_nsbs['time'].values))
        ds_fn['tmp4']=ds_nsbs['VHM0'].interp(latitude=lat_new,longitude=lon_new,time=time_new)
        ds_nsbs.close()
    except:
        it_nws=25
        print('problem reading NWS')
        with open("warnings", "a") as myfile:
            myfile.write(datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')+" NWS *.nc not readable, disregarding it \n")

    print('h')

    try:
        date1=glob.glob('/data/users/vifr/SWH/ibi_*.nc')#[-1]
        date1 = max(date1, key=lambda n: n[-13:-3])
        date1=date1[-13:-3]
        print(date1,'ibi_'+date1+'.nc')
        ds_nsbs=xr.open_dataset('/data/users/vifr/SWH/ibi_'+date1+'.nc', engine='netcdf4')
        datsub=pd.to_datetime(ds_nsbs['time'].values[0])
        diff=datsub-base
        hours = int(np.round(diff.total_seconds()/3600.0+0.5))
        it_ibi=len(ds_nsbs['time'].values)+hours
        print(datsub,hours,it_ibi,len(ds_nsbs['time'].values))
        ds_fn['tmp5']=ds_nsbs['VHM0'].interp(latitude=lat_new,longitude=lon_new,time=time_new)
        ds_nsbs.close()
    except:
        it_ibi=25
        print('problem reading IBI')
        with open("warnings", "a") as myfile:
            myfile.write(datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')+" IBI *.nc not readable, disregarding it \n")

    try:
        date1=glob.glob('/data/users/vifr/SWH/med_*.nc')#[-1]
        date1 = max(date1, key=lambda n: n[-13:-3])
        date1=date1[-13:-3]
        print(date1,'med_'+date1+'.nc')
        ds_nsbs=xr.open_dataset('/data/users/vifr/SWH/med_'+date1+'.nc', engine='netcdf4')
        datsub=pd.to_datetime(ds_nsbs['time'].values[0])
        diff=datsub-base
        hours = int(np.round(diff.total_seconds()/3600.0+0.5))
        it_med=len(ds_nsbs['time'].values)+hours
        print(datsub,hours,it_med,len(ds_nsbs['time'].values))
        ds_fn['tmp6']=ds_nsbs['VHM0'].interp(latitude=lat_new,longitude=lon_new,time=time_new)
        ds_nsbs.close()
    except:
        it_med=25
        print('problem reading Med')
        with open("warnings", "a") as myfile:
            myfile.write(datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')+" Med *.nc not readable, disregarding it \n")

    try:
        date1=glob.glob('/data/users/vifr/SWH/black_*.nc')#[-1]
        date1 = max(date1, key=lambda n: n[-13:-3])
        date1=date1[-13:-3]
        print(date1,'black_'+date1+'.nc')
        ds_nsbs=xr.open_dataset('/data/users/vifr/SWH/black_'+date1+'.nc', engine='netcdf4')
        datsub=pd.to_datetime(ds_nsbs['time'].values[0])
        diff=datsub-base
        hours = int(np.round(diff.total_seconds()/3600.0+0.5))
        it_black=len(ds_nsbs['time'].values)+hours
        print(datsub,hours,it_black,len(ds_nsbs['time'].values))
        ds_fn['tmp7']=ds_nsbs['VHM0'].interp(latitude=lat_new,longitude=lon_new,time=time_new)
        ds_nsbs.close()
    except:
        it_black=25
        print('problem reading Black')
        with open("warnings", "a") as myfile:
            myfile.write(datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')+" Black sea *.nc not readable, disregarding it \n")

    print('i')

    del ds_nsbs

    def timefunc(j):
        timemul=xr.Dataset(data_vars={'mul':(['time'], [0.0001]*len(time_new))}, coords={'time':(['time'],time_new)})['mul']
        if j<nhours: #len(time_new):  #min((ihours+1)*smhours,nhours)
            for jj in range(len(time_new)): #range(j):
                if jj+ihours*smhours<=j-24:
                    timemul[jj]=1.0
                else:
                    timemul[jj]=((j-jj-ihours*smhours)/24.0)**2+0.0001
        else:
            timemul[:]=1.0
        return timemul

    #ds_fn=ds_fn.chunk({"time":12})

    ds_fn['wght0']=xr.where(~np.isnan(ds_fn['VHM0']),1,np.nan)
    timul=timefunc(it_frontex+1)
    ds_fn['wght']=xr.where(~np.isnan(ds_fn['tmp']),1,np.nan)
    ds_fn['wght']=ds_fn['wght']*dr_gofs*timul
    ds_fn['tmp']=ds_fn['tmp']*dr_gofs*timul
    #dr_gofs.close()
    #del dr_gofs
    timul=timefunc(it_bal+1)
    ds_fn['wght1']=xr.where(~np.isnan(ds_fn['tmp1']),1,np.nan)
    ds_fn['wght1']=ds_fn['wght1']*dr_bs_cmems*timul
    ds_fn['tmp1']=ds_fn['tmp1']*dr_bs_cmems*timul
    #dr_bs_cmems.close()
    #del dr_bs_cmems
    timul=timefunc(it_nsbs+1)
    ds_fn['wght2']=xr.where(~np.isnan(ds_fn['tmp2']),1,np.nan)
    ds_fn['wght2']=ds_fn['wght2']*dr_nsbs*timul
    ds_fn['tmp2']=ds_fn['tmp2']*dr_nsbs*timul
    #dr_nsbs.close()
    ds_fn['wght3']=xr.where(~np.isnan(ds_fn['tmp3']),1,np.nan)
    ds_fn['wght3']=ds_fn['wght3']*dr_idf*timul
    ds_fn['tmp3']=ds_fn['tmp3']*dr_idf*timul
    #dr_idf.close()
    #del dr_idf
    timul=timefunc(it_nws+1)
    ds_fn['wght4']=xr.where(~np.isnan(ds_fn['tmp4']),1,np.nan)
    ds_fn['wght4']=ds_fn['wght4']*dr_ns_cmems*timul
    ds_fn['tmp4']=ds_fn['tmp4']*dr_ns_cmems*timul
    #dr_ns_cmems.close()
    #del dr_ns_cmems    
    timul=timefunc(it_ibi+1)
    ds_fn['wght5']=xr.where(~np.isnan(ds_fn['tmp5']),1,np.nan)
    ds_fn['wght5']=ds_fn['wght5']*dr_ibi_cmems*timul
    ds_fn['tmp5']=ds_fn['tmp5']*dr_ibi_cmems*timul
    #dr_ibi_cmems.close()
    #del dr_ibi_cmems
    timul=timefunc(it_med+1)
    ds_fn['wght6']=xr.where(~np.isnan(ds_fn['tmp6']),1,np.nan)
    ds_fn['wght6']=ds_fn['wght6']*dr_med*timul
    ds_fn['tmp6']=ds_fn['tmp6']*dr_med*timul
    #dr_med.close()
    #del dr_med
    timul=timefunc(it_black+1)
    ds_fn['wght7']=xr.where(~np.isnan(ds_fn['tmp7']),1,np.nan)
    ds_fn['wght7']=ds_fn['wght7']*dr_black*timul
    ds_fn['tmp7']=ds_fn['tmp7']*dr_black*timul
    #dr_black.close()
    #del dr_black

    #del timul
    gc.collect()
    
    mre=['VHM0','tmp2','tmp3','tmp1','tmp7','tmp5','tmp6','tmp4','tmp']
    mrw=['wght0','wght2','wght3','wght1','wght7','wght5','wght6','wght4','wght']
    ds_fn=ds_fn.assign(sumvar=ds_fn[['tmp7','tmp6','tmp5','tmp4','tmp3','tmp2','tmp1','tmp','VHM0']].to_array(dim='new').sum('new'))
    ds_fn=ds_fn.assign(idg=ds_fn[['wght7','wght6','wght5','wght4','wght3','wght2','wght1','wght','wght0']].to_array(dim='new').sum('new'))
    ds_fn['idg'] = ds_fn['idg'].where(ds_fn['idg'] > 0)
    ds_fn['sumvar']=ds_fn['sumvar']/ds_fn['idg']
    ds_fn['idg'].loc[:]=0
    for j in range(len(binss)):
        if j>1:
            ds_fn['idg']=xr.where((ds_fn['sumvar']<binss[j])&(ds_fn['sumvar']>=binss[j-1]),j,ds_fn['idg'])
    ds_fn=ds_fn.drop_vars(['sumvar'])

    def submodel(modn=[0]):
        global ds_fn
        global kmodn
        global aArr
        ds_fn=ds_fn.assign(res=ds_fn["VHM0"] * np.nan)
        ds_fn['res'].loc[:] = 1
        for mon in range(len(model)):
            if mon in modn:
                ds_fn['res']=ds_fn['res']*xr.where(ds_fn[mrw[mon]]>0.001,1,np.nan)
            else:
                ds_fn['res']=ds_fn['res']*xr.where(ds_fn[mrw[mon]]>0.001,np.nan,1)   #np.isnan(ds_fn[mrw[mon]])
        if np.nanmean(ds_fn['res'])>0.001:
            print(modn)
            for idr,mo in enumerate(model):
                if mo in modn:
                    ds_fn[mre[mo]]=xr.where(ds_fn['res']>0.001,ds_fn[mre[mo]]*aArr[kmodn,ibf,round(ds_fn['idg']),mo],ds_fn[mre[mo]])
                    ds_fn[mrw[mo]]=xr.where(ds_fn['res']>0.001,ds_fn[mrw[mo]]*aArr[kmodn,ibf,round(ds_fn['idg']),mo],ds_fn[mrw[mo]])
        ds_fn=ds_fn.drop_vars(['res'])
        kmodn=kmodn+1

    kmodn=0
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
    submodel(modn=[1,5])
    submodel(modn=[1,7])
    submodel(modn=[1,8])
    submodel(modn=[2,3])
    submodel(modn=[2,7])
    submodel(modn=[2,8])
    submodel(modn=[3,7])
    submodel(modn=[3,8])
    submodel(modn=[4,8])
    submodel(modn=[5,6])
    submodel(modn=[5,7])
    submodel(modn=[5,8])
    submodel(modn=[6,8])
    submodel(modn=[7,8])
    submodel(modn=[0,1,2])
    submodel(modn=[0,1,3])
    submodel(modn=[0,1,5])
    submodel(modn=[0,1,7])
    submodel(modn=[0,1,8])
    submodel(modn=[0,2,3])
    submodel(modn=[0,2,7])
    submodel(modn=[0,2,8])
    submodel(modn=[0,3,7])
    submodel(modn=[0,3,8])
    submodel(modn=[0,4,8])
    submodel(modn=[0,5,6])
    submodel(modn=[0,5,7])
    submodel(modn=[0,5,8])
    submodel(modn=[0,6,8])
    submodel(modn=[0,7,8])
    submodel(modn=[1,2,3])
    submodel(modn=[1,2,7])
    submodel(modn=[1,2,8])
    submodel(modn=[1,3,7])
    submodel(modn=[1,3,8])
    submodel(modn=[1,5,7])
    submodel(modn=[1,5,8])
    submodel(modn=[1,7,8])
    submodel(modn=[2,3,7])
    submodel(modn=[2,3,8])
    submodel(modn=[2,7,8])
    submodel(modn=[3,7,8])
    submodel(modn=[5,6,8])
    submodel(modn=[5,7,8])
    submodel(modn=[0,1,2,3])
    submodel(modn=[0,1,2,7])
    submodel(modn=[0,1,2,8])
    submodel(modn=[0,1,3,7])
    submodel(modn=[0,1,3,8])
    submodel(modn=[0,1,5,7])
    submodel(modn=[0,1,5,8])
    submodel(modn=[0,1,7,8])
    submodel(modn=[0,2,3,7])
    submodel(modn=[0,2,3,8])
    submodel(modn=[0,3,7,8])
    submodel(modn=[0,5,6,8])
    submodel(modn=[0,5,7,8])
    submodel(modn=[1,2,3,7])
    submodel(modn=[1,2,3,8])
    submodel(modn=[1,2,7,8])
    submodel(modn=[1,3,7,8])
    submodel(modn=[1,5,7,8])
    submodel(modn=[2,3,7,8])
    submodel(modn=[0,1,2,3,7])
    submodel(modn=[0,1,2,3,8])
    submodel(modn=[0,1,2,7,8])
    submodel(modn=[0,1,3,7,8])
    submodel(modn=[0,1,5,7,8])
    submodel(modn=[0,2,3,7,8])
    submodel(modn=[1,2,3,7,8])
    submodel(modn=[0,1,2,3,7,8])

    ds_fn=ds_fn.drop_vars(['idg'])
    
    timul=timefunc(it_frontex+1)
    ds_fn['wght']=ds_fn['wght']*dr_gofs*timul
    ds_fn['tmp']=ds_fn['tmp']*dr_gofs*timul
    dr_gofs.close()
    del dr_gofs
    timul=timefunc(it_bal+1)
    ds_fn['wght1']=ds_fn['wght1']*dr_bs_cmems*timul
    ds_fn['tmp1']=ds_fn['tmp1']*dr_bs_cmems*timul
    dr_bs_cmems.close()
    del dr_bs_cmems
    timul=timefunc(it_nsbs+1)
    ds_fn['wght2']=ds_fn['wght2']*dr_nsbs*timul
    ds_fn['tmp2']=ds_fn['tmp2']*dr_nsbs*timul
    dr_nsbs.close()
    del dr_nsbs
    ds_fn['wght3']=ds_fn['wght3']*dr_idf*timul
    ds_fn['tmp3']=ds_fn['tmp3']*dr_idf*timul
    dr_idf.close()
    del dr_idf
    timul=timefunc(it_nws+1)
    ds_fn['wght4']=ds_fn['wght4']*dr_ns_cmems*timul
    ds_fn['tmp4']=ds_fn['tmp4']*dr_ns_cmems*timul
    dr_ns_cmems.close()
    del dr_ns_cmems    
    timul=timefunc(it_ibi+1)
    ds_fn['wght5']=ds_fn['wght5']*dr_ibi_cmems*timul
    ds_fn['tmp5']=ds_fn['tmp5']*dr_ibi_cmems*timul
    dr_ibi_cmems.close()
    del dr_ibi_cmems
    timul=timefunc(it_med+1)
    ds_fn['wght6']=ds_fn['wght6']*dr_med*timul
    ds_fn['tmp6']=ds_fn['tmp6']*dr_med*timul
    dr_med.close()
    del dr_med
    timul=timefunc(it_black+1)
    ds_fn['wght7']=ds_fn['wght7']*dr_black*timul
    ds_fn['tmp7']=ds_fn['tmp7']*dr_black*timul
    del timul
    
    ds_fn=ds_fn.assign(sumvar=ds_fn[['tmp7','tmp6','tmp5','tmp4','tmp3','tmp2','tmp1','tmp','VHM0']].to_array(dim='new').sum('new'))
    ds_fn=ds_fn.drop_vars(['VHM0'])
    ds_fn=ds_fn.rename({'sumvar':'VHM0'})
    ds_fn=ds_fn.assign(wght=ds_fn[['wght7','wght6','wght5','wght4','wght3','wght2','wght1','wght','wght0']].to_array(dim='new').sum('new'))
    ds_fn['wght'] = ds_fn['wght'].where(ds_fn['wght'] > 0)
    ds_fn['VHM0']=ds_fn['VHM0']/ds_fn['wght']
    ds_fn=ds_fn.drop_vars(['tmp','tmp1','tmp2','tmp3','tmp4','tmp5','tmp6','tmp7','wght7','wght6','wght5','wght4','wght3','wght2','wght1','wght0','wght','forecast_period']) #   

    # mask insert
    ds_fn[par]=ds_fn[par].transpose('time','latitude','longitude')

    ds_fn.attrs.clear()
    try:
        ds_fn['time'].attrs.pop('valid_min')
        ds_fn['time'].attrs.pop('valid_max')
        ds_fn['latitude'].attrs.pop('valid_min')
        ds_fn['latitude'].attrs.pop('valid_max')
        ds_fn['longitude'].attrs.pop('valid_min')
        ds_fn['longitude'].attrs.pop('valid_max')
    except:
        print('minmax attributes not present')
        
    # attribute insert
    ds_fn['latitude'].attrs['units']='degrees_north'
    ds_fn['longitude'].attrs['units']='degrees_east'
    ds_fn['latitude'].attrs['standard_name']='latitude'
    ds_fn['longitude'].attrs['standard_name']='longitude'
    ds_fn['latitude'].attrs['long_name']='latitude'
    ds_fn['longitude'].attrs['long_name']='longitude'
    ds_fn['latitude'].attrs['_CoordinateAxisType']='Lat'
    ds_fn['longitude'].attrs['_CoordinateAxisType']='Lon'
    ds_fn[par].attrs['coordinates']='spatial_ref'
    # attribute insert

    print('j')

    comp = dict(zlib=True, complevel=7) #, dtype = "float32")
    print('1')
    encoding = {var: comp for var in ds_fn.data_vars}
    print('2')
    encoding['latitude']={'dtype': 'f4', "zlib": True, "complevel":5}
    print('3')
    encoding['longitude']={'dtype': 'f4', "zlib": True, "complevel":5}
    print('4')
    encoding[par]={'dtype': 'f4', "zlib": True, "complevel":5}
    print('5')
    encoding['time']={'dtype': 'i4', "zlib": True, "complevel":5}
    print('8')
    print(ds_fn)
    print('9')
    gc.collect()
    print('0')
    ds_fn.to_netcdf('aggreg_'+date0+'_'+str(ihours)+'.nc',encoding=encoding)
    print('1')
    ds_fn.close()
    print('2')
    gc.collect()
    print('3')

# Section for combining all iterations to the single forecast. 

if ithours>0:   
    ds_fn=xr.open_mfdataset('aggreg_'+date0+'_*.nc', engine='netcdf4', combine='by_coords')        

    comp = dict(zlib=True, complevel=7) #, dtype = "float32")
    encoding = {var: comp for var in ds_fn.data_vars}
    encoding['latitude']={'dtype': 'f4', "zlib": True, "complevel":7}
    encoding['longitude']={'dtype': 'f4', "zlib": True, "complevel":7}
    encoding[par]={'dtype': 'f4', "zlib": True, "complevel":7}
    encoding['time']={'dtype': 'i4', "zlib": True, "complevel":7}
    print(ds_fn)
    gc.collect()
    ds_fn.to_netcdf('aggreg_'+date0+'.nc',encoding=encoding)
    ds_fn.close()
    gc.collect()    
    fileList = glob.glob('aggreg_'+date0+'_*.nc')
    for filePath in fileList:
        try:
            os.remove(filePath)
        except:
            print("Error while deleting file : ", filePath)           
else:
    os.replace('aggreg_'+date0+'_0.nc', 'aggreg_'+date0+'.nc')

#"""
 
open('fin_aggr', mode='w').close()
