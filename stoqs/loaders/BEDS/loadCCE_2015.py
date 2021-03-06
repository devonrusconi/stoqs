#!/usr/bin/env python
'''

Master loader for all Coordinated Canyon Experiment data
from October 2015 through 2016

Mike McCann
MBARI 26 January March 2016
'''

import os
import sys
import datetime
parent_dir = os.path.join(os.path.dirname(__file__), "../")
sys.path.insert(0, parent_dir)  # settings.py is one dir up

from BEDS import BEDSLoader

bl = BEDSLoader('stoqs_cce2015', 'Coordinated Canyon Experiment',
                                description = 'Coordinated Canyon Experiment - Measuring turbidity flows in Monterey Submarine Canyon',
                                x3dTerrains = { 
                                    'http://stoqs.mbari.org/terrain/MontereyCanyonBeds_1m+5m_1x_src/MontereyCanyonBeds_1m+5m_1x_src_scene.x3d': {
                                        'position': '2232.80938 10346.25515 3543.76722',
                                        'orientation': '-0.98394 0.16804 -0.06017 1.25033',
                                        'centerOfRotation': '0 0 0',
                                        'VerticalExaggeration': '1',
                                        'geoOrigin': '36.80, -121.87, -400',
                                        'speed': '1.0',
                                        'zNear': '100.0',
                                        'zFar': '30000.0',
                                    },
                                 },
                                 # Do not check in .grd files to the repository, keep them in the loaders directory
                                 grdTerrain=os.path.join(parent_dir, 'MontereyCanyonBeds_1m+5m.grd'),
               )

# Base OPeNDAP server
bl.bed_base = 'http://elvis64.shore.mbari.org/opendap/data/CCE_Processed/BEDs/'

# Copied from ProjectLibrary to BEDs SVN working dir for netCDF conversion, and then copied to elvis.
# See BEDs/BEDs/Visualization/py/makeBEDNetCDF_CCE.sh

bl.bed_parms = ['XA', 'YA', 'ZA', 'A', 'XR', 'YR', 'ZR', 'ROTRATE', 'ROTCOUNT', 'P', 'P_ADJUSTED', 'DEPTH']

# Several BED files: 30200078 to 3020080
# bed_files, bed_platforms, bed_depths must have same number of items; they are zipped together in the load
##bl.bed_files = [('CanyonEvents/BED3/20151001_20160115/{}.nc').format(n) for n in range(30200078, 30200081)]
##bl.bed_platforms = ['BED03'] * len(bl.bed_files)
##bl.bed_depths = [201] * len(bl.bed_files)

# Just the event files for the CCE
bl.bed_files = [
                'BED5/MBCCE_BED5_20151027_Event20151201/netcdf/50200024_decimated_trajectory.nc',
                'BED3/20151001_20160115/netcdf/30200078_trajectory.nc',
                'BED6/20151001_20160115/netcdf/60100068_trajectory.nc',
                'BED3/MBCCE_BED3_20160212_Event20170217/netcdf/30300004_trajectory.nc',
               ]
bl.bed_platforms = ['BED05', 'BED03', 'BED06', 'BED03']
bl.bed_depths = [388, 201, 521, 289.3]
bl.bed_framegrabs = [
                'http://search.mbari.org/ARCHIVE/frameGrabs/Ventana/stills/2015/vnta3873/00_29_56_03.html',
                'http://search.mbari.org/ARCHIVE/frameGrabs/Ventana/stills/2015/vnta3874/00_21_23_28.html',
                'http://search.mbari.org/ARCHIVE/frameGrabs/Ventana/stills/2015/vnta3870/00_15_38_23.html',
                '',
                    ]


# Execute the load for trajectory representation
bl.process_command_line()

if bl.args.test:
    bl.loadBEDS(stride=1, featureType='trajectory')

elif bl.args.optimal_stride:
    bl.loadBEDS(stride=1, featureType='trajectory')

else:
    bl.stride = bl.args.stride
    bl.loadBEDS(featureType='trajectory')

# Add any X3D Terrain information specified in the constructor to the database - must be done after a load is executed
bl.addTerrainResources()

print "All Done."

