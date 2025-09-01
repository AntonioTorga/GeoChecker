import random
from grass.pygrass.vector import VectorTopo
class UtilMisc:
    
    @staticmethod
    def generate_word(length: int = 5, prefix: str = 'mapset_'):
        _signs = "abcdefghijklmnopqrstuvwxyz1234567890"

        word = ""
        for i in range(length):
            word += random.choice(_signs)

        return prefix + word
    
    @staticmethod
    def structure_creation(linkage_map, arc_map, node_map, catch_name = "CATCHMEN", gw_name= "GROUNDWA", ds_prefix = "D_"):
        """_summary_

        Parameters
        ----------
        linkage_map : _type_
            _description_
        arc_map : _type_
            _description_
        node_map : _type_
            _description_

        Returns
        -------
        dict

            {Cell ID :
                {
                    'catchment': catchment name,
                    'groundwater': groundwater name,
                    'demand_site': list of demand site names,
                    'cell_area': float of the area
                }
            }
        dict

            {Node ID : 
                {   
                    'type_id': geometry type ID, 
                    'name': node name, 
                    'cat': node internal ID (used by 'pygrass library')
                }
            }
        dict

            {Arc ID :
                {
                    'type_id': geometry type ID of the arc,
                    'src_id': source node ID (or None),
                    'dst_id': destination node ID (or None)
                }
            }
        """
        cells = dict()
        linkage_vt = VectorTopo(linkage_map)
        linkage_vt.open("r")

        for cell in linkage_vt.viter("areas"):

            cat = cell.cat
            catch = cell.attrs[catch_name]
            gw = cell.attrs[gw_name]
            area = cell.area()

            demand_attrs = [attr for attr in cell.attrs.keys() if attr.startswith(ds_prefix)]
            demand_sites = list(set([cell.attrs[attr] for attr in demand_attrs]))
            demand_sites.remove(None)

            cells[cat] = {
                "catchment": catch,
                "groundwater": gw,
                "demand_site": demand_sites,
                "cell_area":area,
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
                            "type_id":type_id,
                            "src_id":src_id,
                            "dst_id":dst_id,
                            }
        nodes = dict()
        node_vt = VectorTopo(node_map)
        node_vt.open("r")

        for node in node_vt.viter("points"):
            obj_id = node.attrs["ObjID"]
            type_id = node.attrs["TypeID"]
            name = node.attrs["Name"]
            cat = node.cat
            nodes[obj_id] = {
                            "type_id":type_id,
                            "name":name,
                            "cat":cat,
                            }
        
        return cells, arcs, nodes