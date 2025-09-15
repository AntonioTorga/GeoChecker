import typer
from typing_extensions import Annotated
from pathlib import Path
from rich import print
import sys
import subprocess

lib_grass_path = (
    subprocess.check_output(["grass", "--config", "path"], text=True).strip() + "/lib"
)

python_grass_path = subprocess.check_output(
    ["grass", "--config", "python_path"], text=True
).strip()
sys.path.append(lib_grass_path)
sys.path.append(python_grass_path)  # add pygrass to path

from .check.GeoChecker import GeoChecker
from .check.SuperpositionCheck import SuperpositionCheck
from .main import run

app = typer.Typer(
    name="GeoChecker",
    help="GeoChecker Command Line Interface",
    pretty_exceptions_enable=False,
)


@app.command()
def check(
    linkage_file: Annotated[
        Path,
        typer.Argument(
            exists=True,
            dir_okay=False,
            file_okay=True,
            resolve_path=True,
            help="Linkage file (.shp) relative or absolute path",
        ),
    ],
    arcs: Annotated[
        Path,
        typer.Argument(
            exists=True,
            dir_okay=False,
            file_okay=True,
            resolve_path=True,
            help="WEAP Arc (.shp) relative or absolute path",
        ),
    ],
    nodes: Annotated[
        Path,
        typer.Argument(
            exists=True,
            dir_okay=False,
            file_okay=True,
            resolve_path=True,
            help="WEAP Node (.shp) relative or absolute path",
        ),
    ],
    results_folder: Annotated[
        Path,
        typer.Option(
            exists=True,
            dir_okay=True,
            file_okay=False,
            resolve_path=True,
            help="Folder in which to leave the check results.",
        ),
    ] = Path("./"),
    catchment_name: Annotated[
        str,
        typer.Option(help="Catchment attribute name in the .dbf file"),
    ] = "CATCHMEN",
    groundwater_name: Annotated[
        str,
        typer.Option(help="Groundwater attribute name in the .dbf file"),
    ] = "GROUNDWA",
    ds_prefix: Annotated[
        str,
        typer.Option(help="Demand site attributes prefix in the .dbf file"),
    ] = "D_",
):
    """GeoChecker runs checks over the linkage file, contrasting it to the WEAP model. It provides
    reports in .csv, .pdf and .txt format, made to assist the modeler in the correction of the
    Linkage file.
    """
    run(
        linkage_file,
        arcs,
        nodes,
        results_folder=results_folder,
        catchment_name=catchment_name,
        groundwater_name=groundwater_name,
        ds_prefix=ds_prefix,
    )
