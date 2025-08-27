import typer
from typing_extensions import Annotated
from pathlib import Path
from rich import print
import sys
import subprocess


app = typer.Typer(
    name="GeoChecker",
    help="GeoChecker Command Line Interface",
    pretty_exceptions_enable=False,
)

sys.path.append(
    subprocess.check_output(["grass", "--config", "python_path"], text=True).strip()
)  # add pygrass to path

@app.command()
def check(
    linkage_file: Annotated[
        Path,
        typer.Argument(exists=True, dir_okay=False, file_okay=True, resolve_path=True),
    ],
    arcs: Annotated[
        Path,
        typer.Argument(exists=True, dir_okay=False, file_okay=True, resolve_path=True),
    ],
    nodes: Annotated[
        Path,
        typer.Argument(exists=True, dir_okay=False, file_okay=True, resolve_path=True),
    ],
    results_folder: Annotated[
        Path,
        typer.Option(exists=True, dir_okay=False, file_okay=True, resolve_path=True),
    ] = Path("./").resolve(),
):
    geochecker = GeoChecker(
        [
            SuperpositionCheck("groundwater", "demand_site"),
            SuperpositionCheck("groundwater", "catchment"),
        ],
        folder_path=results_folder,
    )


