from grass.pygrass.modules import Module
from subprocess import PIPE

class GrassCoreAPI:
    @staticmethod
    def import_map(map_name, map_path):
        in_ogr = Module('v.in.ogr', run_=False, stdout_=PIPE, stderr_=PIPE, overwrite=True)
        in_ogr.inputs.input = str(map_path)
        in_ogr.outputs.output = map_name
        in_ogr.flags.o = True

        in_ogr.run()