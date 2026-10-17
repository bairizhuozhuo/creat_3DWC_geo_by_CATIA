

from copy import error

import numpy as np
from pathlib import Path
import os
import sys
import time
time_start = time.time()
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)
macro_dir = script_dir


from user_scripts.ToolFunctions import constants
from user_scripts.ToolFunctions.colour import set_colour
from user_scripts.ToolFunctions.geometrical_sets import (
    create_geometrical_set,
)
from user_scripts.ToolFunctions.hide_show import (hide_the_shape,
                                                  hide_the_shapes)
from user_scripts.ToolFunctions.origin_elements import (
    get_ref_origin_elements,
)
from user_scripts.ToolFunctions.parameters import create_parameters

from pycatia import catia
from pycatia.mec_mod_interfaces.part_document import PartDocument
from pycatia.product_structure_interfaces.product import Product
from pycatia.scripts.vba import vba_nothing
from pycatia.in_interfaces.reference import Reference
from pycatia.mec_mod_interfaces.part import Part
from pycatia.mec_mod_interfaces.hybrid_bodies import HybridBodies
from pycatia.mec_mod_interfaces.hybrid_body import HybridBody
from pycatia.hybrid_shape_interfaces.hybrid_shape_factory import HybridShapeFactory
from pycatia.hybrid_shape_interfaces.hybrid_shape_loft import HybridShapeLoft
from pycatia.in_interfaces.vis_property_set import VisPropertySet



caa = catia()  
app = caa.application  
app.refresh_display = False  
app.Visible = False  

docs = app.documents



angle_deg = 0.0
cell_height = 0.6988
file_name_end = '13-24-24_0'
n_warp_y = 6
n_warp_z = 10
n_weft_x = 6
n_weft_z = 11
periodic_weft_degree_nor = 0.0

print("periodic_weft_degree_nor:", periodic_weft_degree_nor)
print("angle_deg:", angle_deg)

current_work_dir = os.getcwd()
print('Current working directory:', current_work_dir)




point_dir_path = os.path.join(current_work_dir, "geo_point_files" + str(file_name_end))

yarn_path_dirs = [os.path.join(point_dir_path, "weft_path_files"), os.path.join(point_dir_path, "warp_path_files")]
yarn_section_dirs = [os.path.join(point_dir_path, "weft_section_files"), os.path.join(point_dir_path, "warp_section_files")]

yarn_names = ["weft", "warp"]
yarn_nums_per_layer = [n_weft_x, n_warp_y]   
yarn_layers = [n_weft_z, n_warp_z]  
angle_symbols = [1, -1]  
yarn_kinds = len(yarn_names)


program = "BuildYarnLoft.CATScript"  
func = "BuildYarnLoft"

Z_add = cell_height  
geo_check = False  

if docs.count == 0:
    part_doc = docs.add("Part")  
else:
    part_doc = app.active_document

selection = part_doc.selection  
part_number = file_name_end + '-Geo'

product = Product(part_doc.product.com_object)

product.part_number = part_number

part = part_doc.part
update_object = part.update_object

bodies = part.bodies

part_body = bodies.item("零件几何体")

part_body.name = "PartBody"  


shape_factory = part.shape_factory

hybrid_shape_factory = part.hybrid_shape_factory

hybrid_bodies = part.hybrid_bodies
ss = caa.system_service

dir_z = hybrid_shape_factory.add_new_direction_by_coord(0.0, 0.0, 1.0)










gs_master_geometry = create_geometrical_set(hybrid_bodies, "YarnLofts")
hbs_master_geometry = gs_master_geometry.hybrid_bodies

gs_construction_geometry = create_geometrical_set(hybrid_bodies, "YarnConstructionGeometry")
hbs_construction_geometry = gs_construction_geometry.hybrid_bodies




for i in [1,0]:  
    app.refresh_display = False  
    yarn_num = yarn_nums_per_layer[i]
    yarn_layer = yarn_layers[i]
    yarn_name = yarn_names[i]
    angle_symbol = angle_symbols[i]
    yarn_path_dir = yarn_path_dirs[i]
    yarn_section_dir = yarn_section_dirs[i]
    
    section_standard_path = os.path.join(yarn_section_dir, rf"section_points_{yarn_name}_standard{file_name_end}.csv")
    section_standard_uv = np.loadtxt(section_standard_path, delimiter=',',skiprows=1)
    

    section_point_num = section_standard_uv.shape[0]
    print(f"{yarn_name} section point number: {section_point_num}.")
    
    yarn_surface_name = f"{yarn_name}_surface"
    yarn_surface = create_geometrical_set(hbs_master_geometry, yarn_surface_name)
    yarn_surface_hss = yarn_surface.hybrid_shapes
    for yarn_idx in range(1, yarn_num+1):  
        
        
        yarn_path_csv = os.path.join(yarn_path_dir, rf"{yarn_name}-{yarn_idx}_path_xyz_angle{file_name_end}.csv")  
        data = np.loadtxt(yarn_path_csv, delimiter=',',skiprows=1)

        
        yarn_path_xyz = data[:, :3]
        xyz = tuple(tuple(map(float, row)) for row in yarn_path_xyz)  
        
        yarn_section_angle = angle_symbol*data[:, 3]
        
        angles = tuple((float(a),) for a in yarn_section_angle)

        path_node_num = yarn_path_xyz.shape[0]
        print(f"{yarn_name}-{yarn_idx} path node number: {path_node_num}.")

        print(f"{yarn_name}-{yarn_idx} surface is building now ...")
        
        
        
        
        loft_name = f"{yarn_name}_{yarn_idx}_surface"
        args = [
            gs_construction_geometry.com_object,
            xyz, angles,
            yarn_section_dir, section_point_num, yarn_name, yarn_idx,
            yarn_surface.com_object, file_name_end
        ]
        ss.execute_script(macro_dir, 1, program, func, args)

        
        loft_name_out_frozen = f"{loft_name}_frozen"  
        
        loft_frozen = yarn_surface_hss.get_item_by_name(loft_name_out_frozen)

        ref_loft = part.create_reference_from_object(loft_frozen)
        print(f"{yarn_name}_{yarn_idx} loft_frozen is create!")
        
        
        
        
        
        
        
        
        """
        # # 1. 第一次尝试获取
        # loft = None
        # try:
        #     loft = yarn_surface_hss.get_item_by_name(loft_name)
        # except:
        #     pass
        # 
        # # 2. 如果没获取到 (loft 是 None)，尝试“抢救”一下
        # if loft is None:
        #     print(f"[Warn] '{loft_name}' not found immediately. Updating Part and retrying...")
        # 
        #     # 关键步骤 A: 强制刷新 CATIA 计算树
        #     part.update()
        # 
        #     # 关键步骤 B: 稍微等待 CATIA 内存同步
        #     time.sleep(2)
        # 
        #     # 关键步骤 C: 【最重要】必须重新执行获取语句！
        #     try:
        #         loft = yarn_surface_hss.get_item_by_name(loft_name)
        #     except:
        #         pass
        # 
        # # 3. 最终操作 (必须判空，防止崩溃)
        # if loft is not None:
        #     if geo_check:
        #         selection.clear()
        #         selection.add(loft)
        #         selection.delete()
        #         print(f"[-] Deleted: {loft_name}")
        #     else:
        #         # 隐藏
        #         selection.clear()
        #         try:
        #             hide_the_shape(selection, [loft])
        #             print(f"[-] Hidden: {loft_name}")
        #         except Exception as e:
        #             # 万一这里还报错，捕获它，并打印出来，停止脚本继续运行
        #             print(f"[!] Error hiding {loft_name}: {e}")
        #             # raise ValueError(f"Cannot hide {loft_name}, aborting.")
        # else:
        #     # 如果救了之后还是 None，说明真的生成失败了，或者名字变了
        #     print(f"[!] CRITICAL: Could not find '{loft_name}' after retry. Skipping hide/delete.")
        #     # raise ValueError(f"Cannot hide {loft_name}, aborting.")
        hide_the_shape(selection, [loft_frozen], flag=False)
        """


        
        
        for layer_idx in range(1, yarn_layer):  
            
            loft_geo = hybrid_shape_factory.add_new_translate(ref_loft, dir_z, float(Z_add) * layer_idx)  
            loft_geo.name = f"{loft_name}_frozen_copy_z{layer_idx}"
            yarn_surface.append_hybrid_shape(loft_geo)
            update_object(loft_geo)
            print(f"{loft_name}_frozen_copy_z{layer_idx} is created!")
            
            
            
            
            
            
            
            


hide_the_shape(selection, [gs_construction_geometry])













export_path = os.path.join(current_work_dir, f"{part_number}.CATPart")
part_doc.save_as(export_path,True)
part_doc.save()

print(f"Done. CATPart saved to: {export_path}")

time_end = time.time()
print(f"All batches done. Total time taken: {time_end - time_start:.2f} seconds.")


































