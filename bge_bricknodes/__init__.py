import bpy
import nodeitems_utils
import os
import sys

bl_info = {
    "name": "Bricky Nodes",
    "description": (
        "A node based view for logic bricks."
    ),
    "author": "Leopold A-C (Iza Zed)",
    "version": (1, 0, 0),
    "blender": (2, 91, 0),
    "location": "View Menu",
    "category": "Game Engine"
}


def _abs_import(module_name, full_path):
    python_version = sys.version_info
    major = python_version[0]
    minor = python_version[1]
    if (major < 3) or (major == 3 and minor < 3):
        import imp
        return imp.load_source(module_name, full_path)
    elif (major == 3) and (minor < 5):
        from importlib.machinery import SourceFileLoader
        return SourceFileLoader(module_name, full_path).load_module()
    else:
        import importlib.util
        spec = importlib.util.spec_from_file_location(module_name, full_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        return module


def _abs_path(*relative_path_components):
    relative_path = os.path.sep.join(relative_path_components)
    this_file = __file__
    this_dir = this_file
    bugger = 0

    def is_existing_directory(path):
        if not os.path.exists(path):
            return False
        else:
            return not os.path.isfile(path)

    while (not is_existing_directory(this_dir)) and (bugger < 100):
        this_dir = os.path.dirname(this_dir)
        bugger += 1
    assert bugger < 100
    abs_path = os.path.join(this_dir, relative_path)
    return abs_path


ui = _abs_import("ui", _abs_path("ui.py"))
ops = _abs_import("ops", _abs_path("ops.py"))
nodes = _abs_import("nodes", _abs_path("nodes.py"))

@bpy.app.handlers.persistent
def establish_synching(dummy):
    filter(lambda a: a is not nodes.update_all_trees, bpy.app.handlers.undo_post)
    filter(lambda a: a is not nodes.update_all_trees, bpy.app.handlers.game_post)
    bpy.app.handlers.undo_post.append(nodes.update_all_trees)
    bpy.app.handlers.game_post.append(nodes.update_all_trees)


filter(lambda a: a is not establish_synching, bpy.app.handlers.load_post)
bpy.app.handlers.load_post.append(establish_synching)


class NodeCategory():

    def __init__(self, identifier, name, description="", items=None):
        self.identifier = identifier
        self.name = name
        self.description = description

        if items is None:
            self.items = lambda context: []
        elif callable(items):
            self.items = items
        else:
            def items_gen(context):
                for item in items:
                    if item.poll is None or item.poll(context):
                        yield item
            self.items = items_gen

    @classmethod
    def poll(cls, context):
        enabled = (context.space_data.tree_type == ui.BGEBrickTree.bl_idname)
        return enabled

    def draw(self, item, layout, context):
        layout.menu("NODE_MT_category_%s" % self.identifier)


register_classes = [
    ops.BNUpdateTree,
    ops.BNRemoveLogicBrickSensor,
    ops.BNRemoveLogicBrickController,
    ops.BNRemoveLogicBrickActuator,
    ops.BNDuplicateBrick,
    ops.BNConvertBricks,
    ops.NLAddPropertyOperator,
    ops.NLMovePropertyOperator,
    ops.NLRemovePropertyOperator,
    ui.BGE_PT_GamePropertyPanel,
    ui.BGE_PT_BrickyTreeOptions,
    ui.BGEBN_PT_GameComponentPanel,
    # ui.BGE_PT_BrickyObjectSensors,
    # ui.BGE_PT_BrickyObjectControllers,
    # ui.BGE_PT_BrickyObjectActuators,
    # ui.BGE_PT_BrickyTreeInfo,
    ui.BGEBrickTree
]

register_classes.extend(nodes._nodes)
register_classes.extend(nodes._sen_nodes)
register_classes.extend(nodes._con_nodes)
register_classes.extend(nodes._act_nodes)
register_classes.extend(nodes._sockets)

def register():
    print(f'Registering Bricky Nodes...')
    for c in register_classes:
        bpy.utils.register_class(c)

    node_items = []
    sensor_items = []
    controller_items = []
    actuator_items = []
    filter(lambda a: a is not nodes.update_all_trees, bpy.app.handlers.undo_post)
    filter(lambda a: a is not nodes.update_all_trees, bpy.app.handlers.game_post)
    bpy.app.handlers.undo_post.append(nodes.update_all_trees)
    bpy.app.handlers.game_post.append(nodes.update_all_trees)

    for n in nodes._nodes:
        node_items.append(nodeitems_utils.NodeItem(n.bl_idname))
    
    for n in nodes._sen_nodes:
        sensor_items.append(nodeitems_utils.NodeItem(n.bl_idname))
    
    for n in nodes._con_nodes:
        controller_items.append(nodeitems_utils.NodeItem(n.bl_idname))
    
    for n in nodes._act_nodes:
        actuator_items.append(nodeitems_utils.NodeItem(n.bl_idname))
    
    layout_items = [
        nodeitems_utils.NodeItem('NodeReroute'),
        nodeitems_utils.NodeItem('NodeFrame')
    ]

    node_categories = [
        NodeCategory('BrickNodes', 'Brick Pointers', items=node_items),
        NodeCategory('Sensors', 'Create Sensors', items=sensor_items),
        NodeCategory('Controllers', 'Create Controllers', items=controller_items),
        NodeCategory('Actuators', 'Create Actuators', items=actuator_items)
        # NodeCategory('LayoutNodes', 'Layout', items=layout_items)
    ]

    nodeitems_utils.register_node_categories("BRICK_NODES", node_categories)


def unregister():
    filter(lambda a: a is not nodes.update_all_trees, bpy.app.handlers.undo_post)
    filter(lambda a: a is not nodes.update_all_trees, bpy.app.handlers.game_post)
    nodeitems_utils.unregister_node_categories("BRICK_NODES")
    for c in register_classes:
        bpy.utils.unregister_class(c)