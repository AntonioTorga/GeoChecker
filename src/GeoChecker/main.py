from grass.pygrass.vector import VectorTopo
from grass_session import Session
from pathlib import Path
from utils.UtilMisc import UtilMisc
from check import GeoChecker, SuperpositionCheck

def run(linkage: Path, arc: Path, node: Path):
    location = UtilMisc.generate_word(length=10)

    with Session(gisdb="/tmp", location=location, create_opts="EPSG:32719"):