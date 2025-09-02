# GEOCHECKER
GeoChecker is a CLI tool that checks for mistakes in linkage files for WEAP-MODFLOW integrated models.

## Installation:
To install you need to clone this repository. Once it is cloned start a terminal inside the repository folder. Then create a Virtual Environment and activate it. Finally install the local copy of GeoChecker.
```
python -m venv venv
source venv\bin\activate
pip install .
```

## How to execute:
Once GeoChecker has been installed you just need to run the following command to run:
```
geochecker linkage_file_path arc_file_path node_file_path
```
optionally you can also include the names of the Groundwater and Catchment attributes on the .dbf file of the shapefile. Also the demand site attribute prefix, used to find all the demand site columns on the .dbf file. You can provide this as it follows:

```
geochecker linkage_file_path arc_file_path node_file_path --catchment-name catchment_name --groundwater_name groundwater_name --ds-prefix ds_prefix
```

## Input:
GeoChecker takes three files as input. The Linkage file, the WEAP Arc file and the WEAP Node file. The two latter extracted directly from the .WEAP file.

### Contact
Feel free to contact the developer for any questions or proposals at antonio.torga@ug.uchile.cl
