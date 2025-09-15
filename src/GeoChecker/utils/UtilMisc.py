import random
import re
from grass.pygrass.vector import VectorTopo

def _clear_string(string):
    if string == None: return None
    cleared = re.sub(r" (\(\d*\))", "", string)

    return cleared

class UtilMisc:

    @staticmethod
    def generate_word(length: int = 5, prefix: str = "mapset_"):
        _signs = "abcdefghijklmnopqrstuvwxyz1234567890"

        word = ""
        for i in range(length):
            word += random.choice(_signs)

        return prefix + word

    @staticmethod
    def structure_creation(
        linkage_map: str,
        arc_map: str,
        node_map: str,
        catch_name: str,
        gw_name: str,
        ds_prefix: str,
    ):
        """_summary_

        Parameters
        ----------
        linkage_map : str
            Name assigned to the map created when Linkage file was imported to the mapset.
        arc_map : str
            Name assigned to the map created when the WEAP Arc file was imported to the mapset.
        node_map : str
            Name assigned to the map created when the WEAP Arc file was imported to the mapset.

        Returns
        -------

        dict
            Dict representing the cells of the linkage file. Has the following structure:
            {Cell ID :
                {
                    'catchment': catchment name,
                    'groundwater': groundwater name,
                    'demand_site': list of demand site names,
                    'cell_area': float of the area
                }
            }
        dict
            Dict representing the cells Arcs of the WEAP Model. Has the following structure:
            {Arc ID :
                {
                    'type_id': geometry type ID of the arc,
                    'src_id': source node ID (or None),
                    'dst_id': destination node ID (or None)
                }
            }
        dict
            Dict representing the Nodes of the WEAP Model. Has the following structure:
            {Node ID :
                {
                    'type_id': geometry type ID,
                    'name': node name,
                    'cat': node internal ID (used by 'pygrass library')
                }
            }
        """
        cells = dict()
        linkage_vt = VectorTopo(linkage_map)
        linkage_vt.open("r")

        for cell in linkage_vt.viter("areas"):

            cat = cell.cat
            catch = _clear_string(cell.attrs[catch_name])
            gw = _clear_string(cell.attrs[gw_name])
            area = cell.area()

            demand_attrs = [
                attr for attr in cell.attrs.keys() if attr.startswith(ds_prefix)
            ]
            demand_sites = list(set([_clear_string(cell.attrs[attr]) for attr in demand_attrs]))
            if None in demand_sites:
                demand_sites.remove(None)

            cells[cat] = {
                "catchment": [catch],
                "groundwater": [gw],
                "demand_site": demand_sites,
                "cell_area": area,
            }

        arcs = dict()
        arc_vt = VectorTopo(arc_map)
        arc_vt.open("r")

        for arc in arc_vt.viter("lines"):
            obj_id = arc.attrs["ObjID"]
            type_id = arc.attrs["TypeID"]
            src_id = arc.attrs["SrcObjID"]
            dst_id = arc.attrs["DestObjID"]
            arcs[obj_id] = {
                "type_id": type_id,
                "src_id": src_id,
                "dst_id": dst_id,
            }
        nodes = dict()
        node_vt = VectorTopo(node_map)
        node_vt.open("r")

        for node in node_vt.viter("points"):
            obj_id = node.attrs["ObjID"]
            type_id = node.attrs["TypeID"]
            name = node.attrs["name2"] if node.attrs["name2"]!=None else node.attrs["Name"]
            name = re.sub(r" (\(\d*\))", "", name) if name!=None else None

            cat = node.cat
            nodes[obj_id] = {
                "type_id": type_id,
                "name": name,
                "cat": cat,
            }

        return cells, arcs, nodes
