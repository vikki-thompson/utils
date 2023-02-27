Àŀ꠰ڏle滰ڏths may need changing
#
# This script gets ERA5 temperature data that is missing from the /badc store
#
# Uses conda environment 'ecmwf-cds', within jaspy
# Setup by:
# export PATH=/apps/contrib/jaspy/miniconda_envs/jaspy3.7/m3-4.6.14/bin:$PATH
# source activate jaspy3.7-m3-4.6.14-r20190627
# original: Peter Uhe 2020/01/21
# edited: Emily Vosper 12/08/2021
# edited: Vikki Thompson 27/02/2023
# cdo tutorial northern hemisphere https://code.mpimet.mpg.de/projects/cdo/wiki/Tutorial
# remap https://nicojourdain.github.io/students_dir/students_netcdf_cdo/
# needs cdsapi installed: https://confluence.ecmwf.int/display/CKB/How+to+install+and+use+CDS+API+on+Windows
import os
import cdsapi
import subprocess
# import utils

outdir = '/net/pc200023/nobackup/users/thompson/ERA5'
tmpdir = '/net/pc200023/nobackup/users/thompson/ERA5/tmp'

print('beginning download')
# Produce list of months 
def generate_yrmonths():
	years = range(1959,1969) #range(1950,2024)
	months = ['01','02','03','04','05','06','07','08','09','10','11','12']
	yrmonths = [ int("%s%s" % (year,month)) for year in years for month in months]
	return yrmonths

yrmonths = generate_yrmonths()
#yrmonths = ['202203'] # use this line to select specific YYYYMM (can be list)
c = cdsapi.Client()

for yrmonth in yrmonths:
    year = str(yrmonth)[:4]
    mon  = str(yrmonth)[4:6]
    print('Processing:',year,mon)
    
    tmpfile = os.path.join(tmpdir,'ERA_tas_hrly_'+year+mon+'.nc')
    request = {'product_type': 'reanalysis',
               'format': 'netcdf',
               'variable': 'u_component_of_wind',
               'pressure_level': '250',
               'year': year,
               'month': mon,
               'day': ['01', '02', '03',
                       '04', '05', '06',
                       '07', '08', '09',
                       '10', '11', '12',
                       '13', '14', '15',
                       '16', '17', '18',
                       '19', '20', '21',
                       '22', '23', '24',
                       '25', '26', '27',
                       '28', '29', '30',
                       '31',],
               'time': ['00:00', '01:00', '02:00',
                        '03:00', '04:00', '05:00',
                        '06:00', '07:00', '08:00',
                        '09:00', '10:00', '11:00',
                        '12:00', '13:00', '14:00',
                        '15:00', '16:00', '17:00',
                        '18:00', '19:00', '20:00',
                        '21:00', '22:00', '23:00',],}
    print(request)
    c.retrieve('reanalysis-era5-pressure-levels',request,tmpfile)
    print('Downloaded',tmpfile)
    ftas = os.path.join(outdir,'u250','ERA5_u250_day_'+year+mon+'.nc')
    cdo_cmd = ['cdo','-O','-b','F32','daymean',tmpfile,ftas]
    print(' '.join(cdo_cmd))
    ret = subprocess.call(cdo_cmd)
    if not ret==0:
        raise Exception('Error with cdo command')
    os.remove(tmpfile)
    print('Finished')
    
'''ftasmin = os.path.join(outdir,'tasmin','ERA5_tasmin_day_'+year+mon+'.nc')
	cdo_cmd = ['cdo','-O','-b','F32','daymin',tmpfile,ftasmin]
	print(' '.join(cdo_cmd))
	ret = subprocess.call(cdo_cmd)
	if not ret==0:
		raise Exception('Error with cdo command')

	ftasmax = os.path.join(outdir,'tasmax','ERA5_tasmax_day_'+year+mon+'.nc')
	cdo_cmd = ['cdo','-O','-b','F32','daymax',tmpfile,ftasmax]
	print(' '.join(cdo_cmd))
	ret = subprocess.call(cdo_cmd)
	if not ret==0:
		raise Exception('Error with cdo command')
'''
