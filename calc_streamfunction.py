# Calculates streamfunction field from u and v components of wind.
# File pathways set to ERA5, 250hPa. This could be altered.
#
# Note: input grids must be global. Sensitive to mising data but will not throw errors - check data e.g. by corr with z500
#
# conda activate butterfly
#
# original: Vikki Thompson 01/03/2023
import os
import cdsapi
import subprocess

# Inputs
udir = '/net/pc200023/nobackup/users/thompson/ERA5/u250'
vdir = '/net/pc200023/nobackup/users/thompson/ERA5/v250'

# Outputs
outdir = '/net/pc200023/nobackup/users/thompson/ERA5/psi250' # psi = streamfunction
tmpdir = '/net/pc200023/nobackup/users/thompson/ERA5/tmp'

print('Beginning calculations')
# Produce list of months 
def generate_yrmonths():
	years = range(1959,1960) #range(1950,2024)
	months = ['01','02','03','04','05','06','07','08','09','10','11','12']
	yrmonths = [ int("%s%s" % (year,month)) for year in years for month in months]
	return yrmonths

yrmonths = generate_yrmonths()
#yrmonths = ['195901'] # use this line to select specific YYYYMM (can be list)

for yrmonth in yrmonths:
    year = str(yrmonth)[:4]
    mon  = str(yrmonth)[4:6]
    print('Processing:',year,mon)
    tmpfile = os.path.join(tmpdir,'ERA5_psi_'+year+mon+'.nc')
    u_wind = os.path.join(udir,'ERA5_u250_day_'+year+mon+'.nc')
    v_wind = os.path.join(vdir,'ERA5_v250_day_'+year+mon+'.nc')
    outfile = os.path.join(outdir, 'ERA5_psi250_day_'+year+mon+'.nc')
    cdo_cmd = ['cdo','-b','F32','sp2gp', '-dv2ps', '-uv2dv', '-remapbil,F360', '-merge', u_wind, v_wind, tmpfile]
    print(' '.join(cdo_cmd))
    ret = subprocess.call(cdo_cmd)
    ret = subprocess.call(cdo_cmd)
    if not ret==0:
        raise Exception('Error with first cdo command')
    cdo_cmd = ['cdo','selvar,stream', tmpfile, outfile]
    print(' '.join(cdo_cmd))
    ret = subprocess.call(cdo_cmd)
    if not ret==0:
        raise Exception('Error with second cdo command')
    os.remove(tmpfile)
    print('Generated streamfunction file')
    print('Finished:',year,mon)
