from grass.pygrass.vector import VectorTopo
from grass_session import Session
from pathlib import Path
from .utils.UtilMisc import UtilMisc
from .utils.GrassCoreAPI import GrassCoreAPI
from .check.GeoChecker import GeoChecker
from .check.SuperpositionCheck import SuperpositionCheck


def run(
    linkage: Path,
    arc: Path,
    node: Path,
    results_folder: Path,
    catchment_name: str,
    groundwater_name: str,
    ds_prefix: str,
):
    location = UtilMisc.generate_word(length=10)

    with Session(gisdb="/tmp", location=location, create_opts="EPSG:32719"):
        GrassCoreAPI.import_map("linkage_map", linkage)
        GrassCoreAPI.import_map("arc_map", arc)
        GrassCoreAPI.import_map("node_map", node)

        linkage = VectorTopo("linkage_map")
        linkage.open("r")

        cells, arcs, nodes = UtilMisc.structure_creation(
            "linkage_map",
            "arc_map",
            "node_map",
            catch_name=catchment_name,
            gw_name=groundwater_name,
            ds_prefix=ds_prefix,
        )

        geochecker = GeoChecker(
            [
                SuperpositionCheck("groundwater", "demand_site"),
                SuperpositionCheck("groundwater", "catchment"),
            ],
            folder_path=results_folder,
        )

        geochecker.setup(cells, arcs, nodes)
        geochecker.run()
