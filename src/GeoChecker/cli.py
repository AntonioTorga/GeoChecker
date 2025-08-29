import typer
from typing_extensions import Annotated
from pathlib import Path
from rich import print
import sys
import subprocess

python_grass_path = subprocess.check_output(["grass", "--config", "python_path"], text=True).strip()
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
        typer.Option(exists=True, dir_okay=True, file_okay=False, resolve_path=True),
    ] = Path("./").resolve(),
):
    run(linkage_file, arcs, nodes, results_folder=results_folder)



