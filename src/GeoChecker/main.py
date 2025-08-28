from grass.pygrass.vector import VectorTopo
from grass_session import Session
from pathlib import Path
from utils.UtilMisc import UtilMisc
from utils.GrassCoreAPI import GrassCoreAPI
from check import GeoChecker, SuperpositionCheck

def run(linkage: Path, arc: Path, node: Path):
    location = UtilMisc.generate_word(length=10)

    with Session(gisdb="/tmp", location=location, create_opts="EPSG:32719"):
        GrassCoreAPI.import_map(linkage, "linkage_map")
        GrassCoreAPI.import_map(arc, "arc_map")
        GrassCoreAPI.import_map(node, "node_map")