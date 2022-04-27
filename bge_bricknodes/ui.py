import bpy
import bge_bricknodes


class BGE_PT_BrickyTreeOptions(bpy.types.Panel):
    bl_label = "Administration"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Dashboard"
    _current_tree = None

    @classmethod
    def poll(cls, context):
        enabled = (context.space_data.tree_type == BGEBrickTree.bl_idname)
        return enabled

    def draw(self, context):
        layout = self.layout
        r = layout.row()
        r.operator('bge_bricknodes.update_all')
        r.operator('bge_bricknodes.convert_bricks')


class BGE_PT_BrickyObjectSensors(bpy.types.Panel):
    bl_label = "Object Sensors"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Item"
    _current_tree = None

    @classmethod
    def poll(cls, context):
        enabled = (context.space_data.tree_type == BGEBrickTree.bl_idname) and context.object
        return enabled

    def draw(self, context):
        layout = self.layout
        for s in context.object.game.sensors:
            b = layout.box()
            r = b.row()
            r.label(text=s.name)
            op = r.operator('bge_bricknodes.remove_sensor', text='', icon='X')
            op.target_brick = s.name


class BGE_PT_BrickyObjectControllers(bpy.types.Panel):
    bl_label = "Object Controllers"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Item"
    _current_tree = None

    @classmethod
    def poll(cls, context):
        enabled = (context.space_data.tree_type == BGEBrickTree.bl_idname) and context.object
        return enabled

    def draw(self, context):
        layout = self.layout
        for c in context.object.game.controllers:
            b = layout.box()
            r = b.row()
            r.label(text=c.name)
            op = r.operator('bge_bricknodes.remove_controller', text='', icon='X')
            op.target_brick = c.name


class BGE_PT_BrickyObjectActuators(bpy.types.Panel):
    bl_label = "Object Actuators"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Dashboard"
    _current_tree = None

    @classmethod
    def poll(cls, context):
        enabled = (context.space_data.tree_type == BGEBrickTree.bl_idname) and context.object
        return enabled

    def draw(self, context):
        layout = self.layout
        for a in context.object.game.actuators:
            b = layout.box()
            r = b.row()
            r.label(text=a.name)
            op = r.operator('bge_bricknodes.remove_actuator', text='', icon='X')
            op.target_brick = a.name


class BGE_PT_BrickyTreeInfo(bpy.types.Panel):
    bl_label = "Info"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Item"
    _current_tree = None

    @classmethod
    def poll(cls, context):
        enabled = (context.space_data.tree_type == BGEBrickTree.bl_idname)
        return enabled

    def draw(self, context):
        layout = self.layout
        node = bpy.context.active_node
        obj = bpy.context.object
        msg = 'selected object'
        if isinstance(node, bpy.types.NodeFrame) or isinstance(node, bpy.types.NodeReroute):
            return
        if node and node.target_object:
            obj = node.target_object
            msg = "node's target"
        box = layout.box()
        box.label(text=f"Sensors on {msg}: {len(obj.game.sensors)}")
        box = layout.box()
        box.label(text=f"Controllers on {msg}: {len(obj.game.controllers)}")
        box = layout.box()
        box.label(text=f"Actuators on {msg}: {len(obj.game.actuators)}")


class BGEBrickTree(bpy.types.NodeTree):
    bl_idname = "BGEBrickTree"
    bl_label = "Logic Brick Node View"
    bl_icon = "LOGIC"
    bl_category = "Scripting"
    compare_bricks = {}
    compare_links = {}

    @classmethod
    def poll(cls, context):
        return True

    def update(self):

        compare_bricks = {}
        for n in self.nodes:
            if isinstance(n, bge_bricknodes.nodes.BNBasicNode):
                if n.brick_name != n.target_brick:
                    n.brick_name = n.target_brick
                if n.get_brick() not in compare_bricks:
                    compare_bricks[n.get_brick()] = n.target_object.name

        for b in self.compare_bricks:
            if b not in compare_bricks:
                n = self.compare_bricks[b]
                if isinstance(b, bpy.types.Sensor):
                    bpy.ops.logic.sensor_remove(sensor=b.name, object=n)
                if isinstance(b, bpy.types.Controller):
                    bpy.ops.logic.controller_remove(controller=b.name, object=n)
                if isinstance(b, bpy.types.Actuator):
                    bpy.ops.logic.actuator_remove(actuator=b.name, object=n)

        self.compare_bricks = compare_bricks

        compare_links = {'reroutes': {}}
        for link in self.links:
            fn = link.from_node
            tn = link.to_node
            while isinstance(fn, bpy.types.NodeReroute):
                if not fn.inputs[0].links:
                    fn = None
                fn = fn.inputs[0].links[0].from_node
                compare_links['reroutes'][link] = [fn]
            if fn is None or tn is None:
                continue
            if (
                fn.bn_type == 'SensorNode' and tn.bn_type == 'ActuatorNode' or
                fn.bn_type == tn.bn_type
            ):
                self.links.remove(link)
                con = self.nodes.new('BNControllerAndNode')
                con.location = (fn.location.x + fn.bl_width_default + 80, fn.location.y)

                sens = fn.get_brick()
                cont = con.get_brick()
                act = tn.get_brick()
                tn.location = (con.location.x + con.bl_width_default + 80, fn.location.y)
                l1 = self.links.new(con.inputs[0], fn.outputs[0])
                sens.link(cont)
                compare_links[l1] = [sens, cont]
                l2 = self.links.new(tn.inputs[0], con.outputs[0])
                cont.link(actuator=act)
                compare_links[l2] = [cont, act]

            else:
                from_brick = fn.get_brick()
                to_brick = tn.get_brick()
                compare_links[link] = [from_brick, to_brick]

        for link in self.compare_links:
            if link == 'reroutes':
                continue
            from_brick = self.compare_links[link][0]
            to_brick = self.compare_links[link][1]
            if from_brick and to_brick:
                if isinstance(from_brick, bpy.types.Controller):
                    from_brick.unlink(actuator=to_brick)
                else:
                    from_brick.unlink(to_brick)

        for link in self.links:
            if not link.is_valid:
                continue
            fn = link.from_node
            tn = link.to_node
            while isinstance(fn, bpy.types.NodeReroute):
                fn = fn.inputs[0].links[0].from_node
            while isinstance(tn, bpy.types.NodeReroute):
                tn = tn.outputs[0].links[0].to_node
            if fn is None or tn is None:
                continue

            from_brick = fn.get_brick()
            to_brick = tn.get_brick()
            if from_brick and to_brick:
                if isinstance(from_brick, bpy.types.Controller):
                    from_brick.link(actuator=to_brick)
                else:
                    from_brick.link(to_brick)

        self.compare_links = compare_links

class BGE_PT_GamePropertyPanel(bpy.types.Panel):
    bl_label = "Game Properties"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Dashboard"

    @classmethod
    def poll(cls, context):
        ob = context.active_object
        enabled = (context.space_data.tree_type == BGEBrickTree.bl_idname)
        return ob and ob.name and enabled

    def draw_tree_prop(self, prop, index, box, show_movers):
        col = box.column()
        name = prop.name.split('__')[-1]
        text = 'Logic Tree'
        opts_row = col.row()
        opts_row.label(text=text)
        val_row = col.row()
        val_row.label(text=name)
        val_row.prop(prop, 'value', text='Start')
        if show_movers:
            self.add_movers(index, opts_row)

    def add_movers(self, index, layout):
        movers = layout.row(align=True)
        move_up = movers.operator(
            bge_bricknodes.ops.NLMovePropertyOperator.bl_idname,
            text='',
            icon='TRIA_UP'
        )
        move_up.direction = 'UP'
        move_down = movers.operator(
            bge_bricknodes.ops.NLMovePropertyOperator.bl_idname,
            text='',
            icon='TRIA_DOWN'
        )
        move_down.direction = 'DOWN'
        move_down.index = move_up.index = index

    def draw(self, context):
        layout = self.layout
        column = layout.column()
        obj = bpy.context.object
        column.operator(
            bge_bricknodes.ops.NLAddPropertyOperator.bl_idname,
            text="Add Game Property",
            icon='PLUS'
        )
        options = column.row()
        show_hidden = context.scene.prop_filter.show_hidden
        collapse_trees = context.scene.prop_filter.collapse_trees
        do_filter = context.scene.prop_filter.do_filter
        prop_type = context.scene.prop_filter.filter_by
        prop_name = context.scene.prop_filter.filter_name
        show_trees = context.scene.prop_filter.show_trees

        hide_icon = 'HIDE_OFF' if show_hidden else 'HIDE_ON'
        collapse_icon = 'LOCKED' if collapse_trees else 'UNLOCKED'
        options.prop(
            context.scene.prop_filter,
            'do_filter',
            icon='FILTER',
            text=''
        )
        options.prop(
            context.scene.prop_filter,
            'show_hidden',
            icon=hide_icon,
            text=''
        )
        options.prop(
            context.scene.prop_filter,
            'show_trees',
            icon='OUTLINER',
            text=''
        )
        options.prop(
            context.scene.prop_filter,
            'collapse_trees',
            icon=collapse_icon,
            text=''
        )

        if do_filter:
            column.prop(context.scene.prop_filter, 'filter_by', text='')
        if prop_type == 'NAME' and do_filter:
            column.prop(
                context.scene.prop_filter,
                'filter_name',
                text='',
                icon='VIEWZOOM'
            )
        if not obj:
            return

        show_movers = show_hidden and show_trees and not do_filter

        props = [prop for prop in obj.game.properties]
        for prop in obj.game.properties:
            if not show_hidden and prop.name.startswith('_'):
                continue
            is_tree = prop.name.startswith('NL__')
            if is_tree and not show_trees:
                continue
            has_name = prop_name in prop.name
            if do_filter:
                if prop_type == 'NAME':
                    if not has_name:
                        continue
                elif prop_type == 'TREES':
                    if not is_tree:
                        continue
                elif prop.type != prop_type or is_tree:
                    continue
            index = props.index(prop)
            column.separator()
            box = column.box()
            if is_tree and collapse_trees:
                self.draw_tree_prop(prop, index, box, show_movers)
                continue
            entry = box.column()
            row_title = entry.row()
            row_title.prop(prop, 'name', text='')
            row_title.prop(prop, 'show_debug', text='', icon='INFO')
            if show_movers:
                self.add_movers(index, row_title)
            remove = row_title.operator(
                bge_bricknodes.ops.NLRemovePropertyOperator.bl_idname,
                text='',
                icon='X'
            )
            remove.index = index
            row_info = entry.row()
            row_info.prop(prop, 'type', text='')
            row_info.prop(prop, 'value', text='Value')
        context.region.tag_redraw()


class BGEBN_PT_GameComponentPanel(bpy.types.Panel):
    bl_label = "Components"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Dashboard"
    # module = bpy.StringProperty()

    @classmethod
    def poll(cls, context):
        ob = context.active_object
        enabled = (context.space_data.tree_type == BGEBrickTree.bl_idname)
        return ob and ob.name and enabled

    def draw(self, context):
        layout = self.layout

        ob = context.active_object
        game = ob.game

        row = layout.row()
        row.operator("logic.python_component_register", text="Register", icon="PLUS")
        row.operator("logic.python_component_create", text="Create", icon="PLUS")

        for i, c in enumerate(game.components):
            box = layout.box()
            row = box.row()
            row.prop(c, "show_expanded", text="", emboss=False)
            row.label(text=c.name)
            row.operator("logic.python_component_reload", text="", icon='RECOVER_LAST').index = i
            row.operator("logic.python_component_remove", text="", icon='X').index = i

            if c.show_expanded and len(c.properties) > 0:
                box = box.box()
                for prop in c.properties:
                    row = box.row()
                    row.label(text=prop.name)
                    col = row.column()
                    col.prop(prop, "value", text="")
