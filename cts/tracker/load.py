import os

from django.contrib.gis.utils import LayerMapping
from .models import ProvisionalSeedZone, WorldBorder

# Auto-generated `LayerMapping` dictionary for ProvisionalSeedZone model
provisionalseedzone_mapping = {
    'objectid': 'OBJECTID',
    'fid_level_field': 'FID_Level_',
    'area': 'AREA',
    'perimeter': 'PERIMETER',
    'eco': 'ECO',
    'level3': 'LEVEL3',
    'level3_nam': 'LEVEL3_NAM',
    'fid_2017_n': 'FID_2017_N',
    'tmin_class': 'Tmin_Class',
    'ahm_class': 'AHM_class',
    'seed_zone': 'seed_zone',
    'new_label': 'New_label',
    'ahm_name': 'AHM_Name',
    'geom': 'MULTIPOLYGON',

}

world_mapping = {
    'fips': 'FIPS',
    'iso2': 'ISO2',
    'iso3': 'ISO3',
    'un': 'UN',
    'name': 'NAME',
    'area': 'AREA',
    'pop2005': 'POP2005',
    'region': 'REGION',
    'subregion': 'SUBREGION',
    'lon': 'LON',
    'lat': 'LAT',
    'mpoly': 'MULTIPOLYGON',
}

world_shp = os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'data', 'TM_WORLD_BORDERS-0.3.shp')
)

psz_shp = os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'data/provision_seed_zones',
                 '2017_New_Labels_LIII_EcoRegions_14June17-colored.shp')
)


def load_psz(verbose=True):
    psz_lm = LayerMapping(
        ProvisionalSeedZone, psz_shp, provisionalseedzone_mapping,
        encoding='iso-8859-1',
    )
    psz_lm.save(strict=True, verbose=verbose)


def load_wb(verbose=True):
    wb_lm = LayerMapping(
        WorldBorder, world_shp, world_mapping,
        transform=False, encoding='iso-8859-1',
    )
    wb_lm.save(strict=True, verbose=verbose)
