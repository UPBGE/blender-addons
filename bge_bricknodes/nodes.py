import bpy
import bge_bricknodes


_enum_sensor_bricks = [
    ("logic.sensor_add(type='ACTUATOR')", "Actuator", "Add a new sensor"),
    ("logic.sensor_add(type='ALWAYS')", "Always", "Add a new sensor"),
    ("logic.sensor_add(type='COLLISION')", "Collision", "Add a new sensor"),
    ("logic.sensor_add(type='DELAY')", "Delay", "Add a new sensor"),
    ("logic.sensor_add(type='JOYSTICK')", "Joystick", "Add a new sensor"),
    ("logic.sensor_add(type='KEYBOARD')", "Keyboard", "Add a new sensor"),
    ("logic.sensor_add(type='MESSAGE')", "Message", "Add a new sensor"),
    ("logic.sensor_add(type='MOUSE')", "Mouse", "Add a new sensor"),
    ("logic.sensor_add(type='MOVEMENT')", "Movement", "Add a new sensor"),
    ("logic.sensor_add(type='NEAR')", "Near", "Add a new sensor"),
    ("logic.sensor_add(type='PROPERTY')", "Property", "Add a new sensor"),
    ("logic.sensor_add(type='RADAR')", "Radar", "Add a new sensor"),
    ("logic.sensor_add(type='RANDOM')", "Random", "Add a new sensor"),
    ("logic.sensor_add(type='RAY')", "Ray", "Add a new sensor")
]


_enum_controller_bricks = [
    ("logic.controller_add(type='LOGIC_AND')", "And", "Add a new controller"),
    ("logic.controller_add(type='LOGIC_OR')", "Or", "Add a new controller"),
    ("logic.controller_add(type='LOGIC_NAND')", "Nand", "Add a new controller"),
    ("logic.controller_add(type='LOGIC_NOR')", "Nor", "Add a new controller"),
    ("logic.controller_add(type='LOGIC_XOR')", "Xor", "Add a new controller"),
    ("logic.controller_add(type='LOGIC_XNOR')", "Xnor", "Add a new controller"),
    ("logic.controller_add(type='EXPRESSION')", "Expression", "Add a new controller"),
    ("logic.controller_add(type='PYTHON')", "Python", "Add a new controller")
]


_enum_actuator_bricks = [
    ("logic.actuator_add(type='ACTION')", "Action", "Add a new actuator"),
    ("logic.actuator_add(type='CAMERA')", "Camera", "Add a new actuator"),
    ("logic.actuator_add(type='COLLECTION')", "Collection", "Add a new actuator"),
    ("logic.actuator_add(type='CONSTRAINT')", "Constraint", "Add a new actuator"),
    ("logic.actuator_add(type='EDIT_OBJECT')", "Edit Object", "Add a new actuator"),
    ("logic.actuator_add(type='FILTER_2D')", "Filter 2D", "Add a new actuator"),
    ("logic.actuator_add(type='GAME')", "Game", "Add a new actuator"),
    ("logic.actuator_add(type='MESSAGE')", "Message", "Add a new actuator"),
    ("logic.actuator_add(type='MOTION')", "Motion", "Add a new actuator"),
    ("logic.actuator_add(type='MOUSE')", "Mouse", "Add a new actuator"),
    ("logic.actuator_add(type='PARENT')", "Parent", "Add a new actuator"),
    ("logic.actuator_add(type='PROPERTY')", "Property", "Add a new actuator"),
    ("logic.actuator_add(type='RANDOM')", "Random", "Add a new actuator"),
    ("logic.actuator_add(type='SCENE')", "Scene", "Add a new actuator"),
    ("logic.actuator_add(type='SOUND')", "Sound", "Add a new actuator"),
    ("logic.actuator_add(type='STATE')", "State", "Add a new actuator"),
    ("logic.actuator_add(type='STEERING')", "Steering", "Add a new actuator"),
    ("logic.actuator_add(type='VIBRATION')", "Vibration", "Add a new actuator"),
    ("logic.actuator_add(type='VISIBILITY')", "Visibility", "Add a new actuator")
]


def check_logic_brick(self, context):
    self.update_draw()
    tree = getattr(bpy.context.space_data, 'edit_tree', None)
    if not tree:
        return
    if self.brick_name != self.get_brick().name:
        self.brick_name = self.get_brick().name
    tree.update()


def rename_brick(self, context):
    brick = self.get_brick()
    old_name = self.target_brick
    if self.target_brick != self.brick_name:
        brick.name = self.target_brick = self.brick_name
    for t in bpy.data.node_groups:
        if isinstance(t, bge_bricknodes.ui.BGEBrickTree):
            for n in t.nodes:
                if n.target_brick == old_name and n.target_object == self.target_object:
                    n.target_brick = self.brick_name
    tree = getattr(bpy.context.space_data, 'edit_tree', None)
    if not tree:
        return
    tree.update()


def update_tree(self, context):
    tree = getattr(bpy.context.space_data, 'edit_tree', None)
    if not tree:
        return
    tree.update()

def update_all_trees(self, context):
    for tree in bpy.data.node_groups:
        if isinstance(tree, bge_bricknodes.ui.BGEBrickTree):
            tree.update()


def create_sensors(self, context):
    update_tree(self, context)
    select_object(self, context)
    eval('bpy.ops.%s' % self.bricks)
    self.target_brick = bpy.context.object.game.sensors[-1].name


def create_controllers(self, context):
    update_tree(self, context)
    select_object(self, context)
    eval('bpy.ops.%s' % self.bricks)
    self.target_brick = bpy.context.object.game.controllers[-1].name


def create_actuators(self, context):
    update_tree(self, context)
    select_object(self, context)
    eval('bpy.ops.%s' % self.bricks)
    self.target_brick = bpy.context.object.game.actuators[-1].name


def select_object(self, context):
    self.update_draw()
    scene = bpy.context.scene
    if not self.target_object:
        return
    for obj in scene.objects:
        if obj.name != self.target_object.name:
            obj.select_set(False)
        else:
            bpy.context.view_layer.objects.active = obj
            obj.select_set(True)


_sockets = []
_nodes = []
_sen_nodes = []
_act_nodes = []
_con_nodes = []


class BLSocket(bpy.types.NodeSocket):
    bl_idname = "BLSocket"

    def draw_color(self, context, node):
        return [1, 1, 1, 1]

    def draw(self, context, layout, node, text):
        if not self.is_linked:
            layout.label(text=text)


class BLSensorSocket(BLSocket):
    bl_idname = "BLSensorSocket"

    def draw_color(self, context, node):
        return [.8, .2, .2, 1]


_sockets.append(BLSensorSocket)


class BLActuatorSocket(BLSocket):
    bl_idname = "BLActuatorSocket"

    def draw_color(self, context, node):
        return [.4, .8, .4, 1]


_sockets.append(BLActuatorSocket)


class BNBasicNode():
    target_object: bpy.props.PointerProperty(type=bpy.types.Object, update=select_object)
    target_brick: bpy.props.StringProperty(update=check_logic_brick)
    brick_name: bpy.props.StringProperty(update=rename_brick)
    show_info: bpy.props.BoolProperty(
        default=True,
        name='Expand Selector',
        description='Show Object and Brick selection bar',
        update=update_tree
    )

    def init(self, context):
        if bpy.context.object:
            self.target_object = bpy.context.object
        self.use_custom_color = True
        self.color = [.25, .25, .25]

    def update_draw(self):
        pass

    def get_brick(self):
        if isinstance(self, BNSensorNode):
            brick_type = 'sensors'
        elif isinstance(self, BNControllerNode):
            brick_type = 'controllers'
        elif isinstance(self, BNActuatorNode):
            brick_type = 'actuators'
        else:
            return
        game = getattr(self.target_object, 'game', None)
        if not game:
            return None
        bricks = getattr(game, brick_type)
        return bricks.get(self.target_brick, None)


class BNSensorNode(bpy.types.Node, BNBasicNode):
    bl_idname = 'BNSensorNode'
    bl_label = 'Sensor'
    bl_width_default = 360
    bn_type = 'SensorNode'
    bricks: bpy.props.EnumProperty(
        items=_enum_sensor_bricks,
        update=create_sensors,
        name='Add Sensor'
    )

    def init(self, context):
        BNBasicNode.init(self, context)
        self.outputs.new(BLSensorSocket.bl_idname, "Connect to a Controller")
        self.outputs[-1].enabled = False

    def update_draw(self):
        tree = getattr(bpy.context.space_data, 'edit_tree', None)
        if not tree:
            return
        sensor = self.get_brick()
        if not sensor:
            if not self.outputs:
                tree.update()
                return
            self.outputs[0].enabled = False
            for link in self.outputs[0].links:
                tree.links.remove(link)
            tree.update()
            return
        self.outputs[0].enabled = True

    def draw_buttons(self, context, layout):
        sensor = self.get_brick()
        if self.show_info:
            topper = layout.box()
            head = topper.column(align=True)
            header = head.row(align=True)
            if self.target_object:
                header.prop(self, 'show_info', text='', icon='COLLAPSEMENU')
            underline = head.row()
            subheader = underline.row(align=True)
            header.prop(self, 'target_object', text='')
            if self.target_object:
                header.prop_menu_enum(self, 'bricks', text='Add Sensor')
                subheader.prop_search(
                    self,
                    'target_brick',
                    self.target_object.game,
                    'sensors',
                    text='Sensor'
                )
                if sensor:
                    # subheader.operator('bge_bricknodes.rename_brick', text='', icon='GREASEPENCIL')
                    underline.operator('bge_bricknodes.remove_sensor', text='', icon='X')
                    # layout.separator()
                else:
                    return
            else:
                return

        # Custom Draw
        main = layout.column(align=True)
        infobox = main.box()
        info = infobox.row()
        if not self.show_info:
            text = '' if sensor else 'Sensor invalid, choose another'
            info.prop(self, 'show_info', text=text, icon='COLLAPSEMENU')
        if not sensor:
            return
        info.prop(sensor, 'type', text='')
        info.prop(self, 'brick_name', text='')
        info.prop(sensor, 'active', text='')
        info.operator('bge_bricknodes.duplicate_brick', text='', icon='DUPLICATE')
        if not self.show_info:
            info.operator('bge_bricknodes.remove_sensor', text='', icon='X')
        
        optbox = main.box()
        opts = optbox.row()
        trigger = opts.row(align=True)
        trigger.prop(sensor, 'use_pulse_true_level', text='', icon='TRIA_UP')
        trigger.prop(sensor, 'use_pulse_false_level', text='', icon='TRIA_DOWN')
        opts.prop(sensor, 'tick_skip', text='Skip')
        leveltap = opts.row(align=True)
        leveltap.prop(sensor, 'use_level', text='Level', toggle=True)
        leveltap.prop(sensor, 'use_tap', text='Tap', toggle=True)
        opts.prop(sensor, 'invert', text='Invert', toggle=True)
        
        draw_types = {
            'ACTUATOR': self.draw_actuator,
            'COLLISION': self.draw_collision,
            'DELAY': self.draw_delay,
            'JOYSTICK': self.draw_joystick,
            'KEYBOARD': self.draw_keyboard,
            'MESSAGE': self.draw_message,
            'MOUSE': self.draw_mouse,
            'MOVEMENT': self.draw_movement,
            'NEAR': self.draw_near,
            'PROPERTY': self.draw_property,
            'RADAR': self.draw_radar,
            'RANDOM': self.draw_random,
            'RAY': self.draw_ray
        }
        body = main.box()
        if sensor.type != 'ALWAYS':
            draw_types.get(sensor.type)(sensor, body)
        if self.target_object and not self.show_info:
            footer = main.box()
            footer.label(text=f'Applied To: {self.target_object.name}')
    
    def draw_actuator(self, sensor, body):
        row = body.row()
        row.prop_search(sensor, 'actuator', self.target_object.game, 'actuators', text='Actuator', icon='ACTION')

    def draw_collision(self, sensor, body):
        row = body.split(factor=.4)
        pulsemat = row.row(align=True)
        pulsemat.prop(sensor, 'use_pulse', text='Pulse', toggle=True)
        pulsemat.prop(sensor, 'use_material', text='M/P', toggle=True)

        if sensor.use_material:
            row.prop_search(sensor, 'material', bpy.data, 'materials', text='Material')
        else:
            row.prop(sensor, 'property', text='Property')
    
    def draw_delay(self, sensor, body):
        row = body.row()
        row.prop(sensor, 'delay')
        row.prop(sensor, 'duration')
        row.prop(sensor, 'use_repeat')

    def draw_joystick(self, sensor, body):
        header = body.row()
        events = body.row()
        
        header.prop(sensor, 'joystick_index', text='Joystick Index')
        events.prop(sensor, 'event_type', text='Event Type')
        events.prop(sensor, 'use_all_events', text='All Events')
        if sensor.use_all_events:
            return
        elif sensor.event_type == 'STICK_DIRECTIONS':
            content = body.column(align=False)
            content.prop(sensor, 'axis_number', text='Stick')
            content.prop(sensor, 'axis_direction', text='Stick Direction')
            content.prop(sensor, 'axis_threshold', text='Threshold')
        elif sensor.event_type == 'STICK_AXIS':
            content = body.column(align=True)
            content.prop(sensor, 'single_axis_number', text='Stick Axis')
            content.prop(sensor, 'axis_threshold', text='Threshold')
        elif sensor.event_type == 'SHOULDER_TRIGGERS':
            content = body.column(align=True)
            content.prop(sensor, 'axis_trigger_number', text='Triggers')
            content.prop(sensor, 'axis_threshold', text='Threshold')
        elif sensor.event_type == 'BUTTONS':
            content = body.column(align=True)
            content.prop(sensor, 'button_number', text='Button')

    def draw_keyboard(self, sensor, body):
        header = body.row()
        if not sensor.use_all_keys:
            header.label(text='Key:')
            key = header.prop(sensor, 'key', text='', event=True)
            mods = body.column(align=True)
            mod1 = mods.row()
            mod2 = mods.row()
            mod1.label(text='First Modifier:')
            mod1.prop(sensor, 'modifier_key_1', text='', event=True)
            mod2.label(text='Second Modifier:')
            mod2.prop(sensor, 'modifier_key_2', text='', event=True)
        header.prop(sensor, 'use_all_keys', text='All Keys', toggle=True)
        content = body.column()
        content.prop_search(sensor, 'log', self.target_object.game, 'properties', text='Log Toggle')
        content.prop_search(sensor, 'target', self.target_object.game, 'properties', text='Target')

    def draw_message(self, sensor, body):
        body.prop(sensor, 'subject', text='Subject')

    def draw_mouse(self, sensor, body):
        body.prop(sensor, 'mouse_event', text='Mouse Event')

    def draw_movement(self, sensor, body):
        body.prop(sensor, 'axis', text='Axis')
        opts = body.row()
        opts.prop(sensor, 'use_local', text='Local', toggle=True)
        opts.prop(sensor, 'threshold', text='Threshold')

    def draw_near(self, sensor, body):
        body.prop(sensor, 'property', text='Property')
        opts = body.row(align=True)
        opts.prop(sensor, 'distance', text='Distance')
        opts.prop(sensor, 'reset_distance', text='Reset Distance')

    def draw_property(self, sensor, body):
        body.prop(sensor, 'evaluation_type', text='Evaluation Type')
        body.prop_search(sensor, 'property', self.target_object.game, 'properties', text='Property')
        body.prop(sensor, 'value', text='Value')
        print(sensor.evaluation_type)
        if sensor.evaluation_type == 'PROPINTERVAL':
            minmax = body.row()
            minmax.prop(sensor, 'value_min')
            minmax.prop(sensor, 'value_max')

    def draw_radar(self, sensor, body):
        body.prop(sensor, 'property', text='Property')
        body.prop(sensor, 'axis', text='Axis')
        opts = body.row()
        opts.prop(sensor, 'angle', text='Angle')
        opts.prop(sensor, 'distance', text='Distance')

    def draw_random(self, sensor, body):
        body.prop(sensor, 'seed', text='Seed')

    def draw_ray(self, sensor, body):
        main = body.split(factor=.33333)
        main.prop(sensor, 'ray_type', text='')
        if sensor.ray_type == 'PROPERTY':
            main.prop(sensor, 'property', text='')
        else:
            main.prop_search(sensor, 'material', bpy.data, 'materials', text='')
        
        sec = body.row()
        sec.prop(sensor, 'axis', text='')
        sec.prop(sensor, 'range', text='Range')
        sec.prop(sensor, 'use_x_ray', text='X-Ray Mode', toggle=True)
        thi = body.split(factor=.3, align=True)
        thi.label(text='Mask:')
        thi.prop(sensor, 'mask', text='')


class BNControllerNode(bpy.types.Node, BNBasicNode):
    bl_idname = 'BNControllerNode'
    bl_label = 'Controller'
    bl_width_default = 260
    bn_type = 'ControllerNode'
    bricks: bpy.props.EnumProperty(
        items=_enum_controller_bricks,
        update=create_controllers,
        name='Add Controller'
    )

    def init(self, context):
        BNBasicNode.init(self, context)
        self.inputs.new(BLSensorSocket.bl_idname, "Connect to a Sensor")
        self.inputs[-1].link_limit = 100
        self.inputs[-1].enabled = False
        self.outputs.new(BLActuatorSocket.bl_idname, "Connect to an Actuator")
        self.outputs[-1].enabled = False

    def update_draw(self):
        tree = getattr(bpy.context.space_data, 'edit_tree', None)
        if not tree:
            return
        controller = self.get_brick()
        if not controller:
            if not self.inputs or not self.outputs:
                tree.update()
                return
            self.inputs[0].enabled = False
            for link in self.inputs[0].links:
                tree.links.remove(link)
            self.outputs[0].enabled = False
            for link in self.outputs[0].links:
                tree.links.remove(link)
            tree.update()
            return
        self.inputs[0].enabled = True
        self.outputs[0].enabled = True

    def draw_buttons(self, context, layout):
        controller = self.get_brick()
        if self.show_info:
            topper = layout.box()
            head = topper.column(align=True)
            header = head.row(align=True)
            underline = head.row()
            subheader = underline.row(align=True)
            if self.target_object:
                header.prop(self, 'show_info', text='', icon='COLLAPSEMENU')
            header.prop(self, 'target_object', text='')
            if self.target_object:
                header.prop_menu_enum(self, 'bricks', text='Add Controller')
                subheader.prop_search(
                    self,
                    'target_brick',
                    self.target_object.game,
                    'controllers',
                    text='Controller'
                )
                if controller:
                    # subheader.operator('bge_bricknodes.rename_brick', text='', icon='GREASEPENCIL')
                    underline.operator('bge_bricknodes.remove_controller', text='', icon='X')
                    # layout.separator()
                else:
                    return
            else:
                return

        main = layout.column(align=True)
        infobox = main.box()
        info = infobox.row()
        if not self.show_info:
            text = '' if controller else 'Controller invalid, choose another'
            info.prop(self, 'show_info', text=text, icon='COLLAPSEMENU')
        if not controller:
            return
        info.prop(controller, 'type', text='')
        info.prop(self, 'brick_name', text='')
        info.prop(controller, 'use_priority', text='', icon='BOOKMARKS')
        info.prop(controller, 'active', text='')
        info.operator('bge_bricknodes.duplicate_brick', text='', icon='DUPLICATE')
        if not self.show_info:
            info.operator('bge_bricknodes.remove_controller', text='', icon='X')
        infobox.prop(controller, 'states', text='Controller visible at')
        infobox.template_layers(controller, 'states', self.target_object.game, 'used_states', 0)

        body = main.box()
        if controller.type == 'EXPRESSION':
            content = body.row()
            content.prop(controller, 'expression', text='')
        elif controller.type == 'PYTHON':
            if controller.mode == 'SCRIPT':
                content = body.split(factor=.3, align=True)
                content.prop(controller, 'mode', text='')
                content.prop_search(controller, 'text', bpy.data, 'texts', text='')
            else:
                parts = body.split(factor=.9)
                data = parts.split(factor=.3333)
                data.prop(controller, 'mode', text='')
                data.prop(controller, 'module', text='')
                parts.prop(controller, 'use_debug', text='D', toggle=True)
        if self.target_object and not self.show_info:
            footer = main.box()
            footer.label(text=f'Applied To: {self.target_object.name}')


class BNActuatorNode(bpy.types.Node, BNBasicNode):
    bl_idname = 'BNActuatorNode'
    bl_label = 'Actuator'
    bl_width_default = 360
    bn_type = 'ActuatorNode'
    bricks: bpy.props.EnumProperty(
        items=_enum_actuator_bricks,
        update=create_actuators,
        name='Add Actuator'
    )

    def init(self, context):
        BNBasicNode.init(self, context)
        self.inputs.new(BLActuatorSocket.bl_idname, "Connect to a Controller")
        self.inputs[-1].enabled = False
        self.inputs[-1].link_limit = 0
    
    def update_draw(self):
        tree = getattr(bpy.context.space_data, 'edit_tree', None)
        if not tree:
            return
        actuator = self.get_brick()
        if not actuator:
            if not self.outputs:
                tree.update()
                return
            self.inputs[0].enabled = False
            for link in self.inputs[0].links:
                tree.links.remove(link)
            tree.update()
            return
        self.inputs[0].enabled = True

    def draw_buttons(self, context, layout):
        actuator = self.get_brick()
        if self.show_info:
            topper = layout.box()
            head = topper.column(align=True)
            header = head.row(align=True)
            underline = head.row()
            subheader = underline.row(align=True)
            if self.target_object:
                header.prop(self, 'show_info', text='', icon='COLLAPSEMENU')
            header.prop(self, 'target_object', text='')
            if self.target_object:
                header.prop_menu_enum(self, 'bricks', text='Add Actuator')
                subheader.prop_search(
                    self,
                    'target_brick',
                    self.target_object.game,
                    'actuators',
                    text='Actuator'
                )
                if actuator:
                    # subheader.operator('bge_bricknodes.rename_brick', text='', icon='GREASEPENCIL')
                    underline.operator('bge_bricknodes.remove_actuator', text='', icon='X')
                    # layout.separator()
                else:
                    return
            else:
                return

        main = layout.column(align=True)
        infobox = main.box()
        info = infobox.row()
        if not self.show_info:
            text = '' if actuator else 'Actuator invalid, choose another'
            info.prop(self, 'show_info', text=text, icon='COLLAPSEMENU')
        if not actuator:
            return
        info.prop(actuator, 'type', text='')
        info.prop(self, 'brick_name', text='')
        info.prop(actuator, 'active', text='')
        info.operator('bge_bricknodes.duplicate_brick', text='', icon='DUPLICATE')
        if not self.show_info:
            info.operator('bge_bricknodes.remove_actuator', text='', icon='X')

        draw_types = {
            'ACTION': self.draw_action,
            'CAMERA': self.draw_camera,
            'COLLECTION': self.draw_collection,
            'CONSTRAINT': self.draw_constraint,
            'EDIT_OBJECT': self.draw_edit_object,
            'FILTER_2D': self.draw_filter2d,
            'GAME': self.draw_game,
            'MESSAGE': self.draw_message,
            'MOTION': self.draw_motion,
            'MOUSE': self.draw_mouse,
            'PARENT': self.draw_parent,
            'PROPERTY': self.draw_property,
            'RANDOM': self.draw_random,
            'SCENE': self.draw_scene,
            'SOUND': self.draw_sound,
            'STATE': self.draw_state,
            'STEERING': self.draw_steering,
            'VIBRATION': self.draw_vibration,
            'VISIBILITY': self.draw_visibility
        }
        body = main.box()
        draw_types.get(actuator.type)(actuator, body)
        if self.target_object and not self.show_info:
            footer = main.box()
            footer.label(text=f'Applied To: {self.target_object.name}')

    def draw_action(self, act, body):
        main = body.row()
        main.prop(act, 'play_mode', text='')
        forceadd = main.row(align=True)
        forceadd.prop(act, 'use_force', text='Force', toggle=True)
        forceadd.prop(act, 'use_additive', text='Add', toggle=True)
        main.prop(act, 'use_local', text='L', toggle=True)
        action = body.row()
        action.prop_search(act, 'action', bpy.data, 'actions', text='')
        action.prop(act, 'use_continue_last_frame', text='Continue')
        if act.play_mode != 'PROPERTY':
            frames = body.row()
            frames.prop(act, 'frame_start', text='Start Frame')
            frames.prop(act, 'frame_end', text='End Frame')
        else:
            frames = body.split(factor=.6)
            frames.prop_search(act, 'property', self.target_object.game, 'properties', text='Property')
        frames.prop(act, 'apply_to_children', text='Child')
        opts = body.row()
        opts.prop(act, 'frame_blend_in', text='Blendin')
        opts.prop(act, 'priority', text='Priority')
        layers = body.row()
        layers.prop(act, 'layer', text='Layer')
        layers.prop(act, 'layer_weight', text='Layer Weight')
        layers.prop(act, 'blend_mode', text='')
        body.prop_search(act, 'frame_property', self.target_object.game, 'properties', text='Frame Property')

    def draw_camera(self, act, body):
        body.prop(act, 'object', text='Camera Object')
        params = body.row()
        params.prop(act, 'height', text='Height')
        params.prop(act, 'axis', text='Axis')
        minmax = body.row(align=True)
        minmax.prop(act, 'min', text='Min')
        minmax.prop(act, 'max', text='Max')
        body.prop(act, 'damping', text='Damping')

    def draw_collection(self, act, body):
        body.prop_search(act, 'collection', bpy.data, 'collections', text='Collection')
        body.prop(act, 'mode', text='Mode')
        row = body.row()
        if act.mode == 'REMOVE_OVERLAY':
            return
        elif act.mode == 'ADD_OVERLAY':
            row.prop_search(act, 'camera', bpy.data, 'objects', text='Camera')
        else:
            row.prop(act, 'use_logic', text='Logic')
            row.prop(act, 'use_physics', text='Physics')
            row.prop(act, 'use_render', text='Visibility')

    def draw_constraint(self, act, body):
        body.prop(act, 'mode', text='Constraints Mode')
        if act.mode == 'LOC':
            body.prop(act, 'limit', text='Limit')
            minmax = body.row(align=True)
            minmax.prop(act, 'limit_min', text='Min')
            minmax.prop(act, 'limit_max', text='Max')
            body.prop(act, 'damping', text='Damping', slider=True)
        if act.mode == 'DIST':
            header = body.split(factor=.80)
            header.prop(act, 'direction', text='Direction')
            ln = header.row(align=True)
            ln.prop(act, 'use_local', text='L', toggle=True)
            ln.prop(act, 'use_normal', text='N', toggle=True)
            stuff = body.split()
            ran = stuff.column()
            ran.label(text='Range:')
            ran.prop(act, 'range', text='')
            fdist = stuff.column()
            fdist.prop(act, 'use_force_distance', text='Force Distance', toggle=True)
            fdist.prop(act, 'distance', text='')
            body.prop(act, 'damping', text='Damping', toggle=True)
            mp = body.split(factor=.15)
            mp.prop(act, 'use_material_detect', text='M/P', toggle=True)
            if act.use_material_detect:
                mp.prop_search(act, 'material', bpy.data, 'materials', text='Material')
            else:
                mp.prop(act, 'property', text='Property')
            pertiro = body.split(factor=.15)
            pertiro.prop(act, 'use_persistent', text='PER', toggle=True)
            tiro = pertiro.row(align=True)
            tiro.prop(act, 'time', text='Time')
            tiro.prop(act, 'damping_rotation', text='RotDamp', slider=True)
        if act.mode == 'ORI':
            body.prop(act, 'direction', text='Direction')
            dati = body.row(align=True)
            dati.prop(act, 'damping', text='Damping', slider=True)
            dati.prop(act, 'time', text='Time')
            romax = body.row(align=True)
            romax.prop(act, 'rotation_max', text='Reference Direction')
            minmax = body.row(align=True)
            minmax.prop(act, 'angle_min', text='Min')
            minmax.prop(act, 'angle_max', text='Max')
        if act.mode == 'FH':
            header = body.split(factor=.75)
            subhead = header.row()
            subhead.prop(act, 'fh_damping', text='Damping', slider=True)
            subhead.prop(act, 'fh_height', text='Distance')
            header.prop(act, 'use_fh_paralel_axis', text='Rot Fh', toggle=True)
            sub = body.split(factor=.95)
            subsub = sub.row()
            subsub.prop(act, 'direction_axis', text='Direction Axis')
            subsub.prop(act, 'fh_force', text='Force')
            sub.prop(act, 'use_fh_normal', text='N', toggle=True)
            mp = body.split(factor=.15)
            mp.prop(act, 'use_material_detect', text='M/P', toggle=True)
            if act.use_material_detect:
                mp.prop_search(act, 'material', bpy.data, 'materials', text='Material')
            else:
                mp.prop(act, 'property', text='Property')
            pertiro = body.split(factor=.15)
            pertiro.prop(act, 'use_persistent', text='PER', toggle=True)
            tiro = pertiro.row()
            tiro.prop(act, 'time', text='Time')
            tiro.prop(act, 'damping_rotation', text='RotDamp', slider=True)

    def draw_edit_object(self, act, body):
        body.prop(act, 'mode', text='Edit Object')
        if act.mode == 'ADDOBJECT':
            obrow = body.row()
            obrow.prop(act, 'object', text='Object')
            obrow.prop(act, 'time', text='Time')
            velrow = body.split(factor=.85)
            vel = velrow.row(align=True)
            vel.prop(act, 'linear_velocity', text='Linear Velocity')
            velrow.prop(act, 'use_local_linear_velocity', text='L', toggle=True)
            angrow = body.split(factor=.85)
            ang = angrow.row(align=True)
            ang.prop(act, 'angular_velocity', text='Linear Velocity')
            angrow.prop(act, 'use_local_angular_velocity', text='L', toggle=True)
        elif act.mode == 'REPLACEMESH':
            if self.target_object.type != 'MESH':
                body.label(text='Mode only available for mesh objects')
            else:
                content = body.split(factor=.65)
                content.prop_search(act, 'mesh', bpy.data, 'meshes', text='Mesh')
                opts = content.row()
                opts.prop(act, 'use_replace_display_mesh', text='Gfx', toggle=True)
                opts.prop(act, 'use_replace_physics_mesh', text='Phys', toggle=True)
        elif act.mode == 'TRACKTO':
            content = body.split()
            content.prop_search(act, 'track_object', bpy.data, 'objects', text='Object')
            opts = content.row()
            opts.prop(act, 'time', text='Time')
            opts.prop(act, 'use_3d_tracking', text='3D', toggle=True)
            body.prop(act, 'up_axis', text='Up Axis')
            body.prop(act, 'track_axis', text='Track Axis')
        elif act.mode == 'DYNAMICS':
            body.prop(act, 'dynamic_operation', text='Dynamic Operation')
            if act.dynamic_operation == 'SETMASS':
                body.prop(act, 'mass', text='Mass')
            if act.dynamic_operation == 'RESTOREPHY':
                body.prop(act, 'children_recursive_restore', text='Restore Children Dynamics')
            if act.dynamic_operation == 'SUSPENDPHY':
                body.prop(act, 'children_recursive_suspend', text='Suspend Children Dynamics')
                body.prop(act, 'free_constraints', text='Free constraints')
        

    def draw_filter2d(self, act, body):
        body.prop(act, 'mode', text='Filted 2D Type')
        if act.mode == 'MOTIONBLUR':
            content = body.split(factor=.8)
            content.prop(act, 'motion_blur_factor', text='Value')
            content.prop(act, 'use_motion_blur', text='Enable', toggle=True)
        else:
            body.prop(act, 'filter_pass', text='Pass Number')
        if act.mode == 'CUSTOMFILTER':
            body.prop_search(act, 'glsl_shader', bpy.data, 'texts', text='Script')

    def draw_game(self, act, body):
        body.prop(act, 'mode', text='Game')
        if act.mode == 'START' or act.mode == 'SCREENSHOT':
            body.prop(act, 'filename', text='File')

    def draw_message(self, act, body):
        body.prop_search(act, 'to_property', bpy.data, 'objects', text='To')
        body.prop(act, 'subject', text='Subject')
        content = body.split(factor=.6, align=True)
        content.prop(act, 'body_type', text='Body')
        if act.body_type == 'TEXT':
            content.prop(act, 'body_message', text='')
        else:
            content.prop_search(act, 'body_property', self.target_object.game, 'properties', text='')

    def draw_motion(self, act, body):
        body.prop(act, 'mode', text='Motion Type')
        if act.mode == 'OBJECT_NORMAL':
            locrow = body.split(factor=.9)
            loc = locrow.row(align=True)
            loc.prop(act, 'offset_location', text='Loc')
            locrow.prop(act, 'use_local_location', text='L', toggle=True)
            rotrow = body.split(factor=.9)
            rot = rotrow.row(align=True)
            rot.prop(act, 'offset_rotation', text='Rot')
            rotrow.prop(act, 'use_local_rotation', text='L', toggle=True)
            if self.target_object.game.physics_type in ['DYNAMIC', 'RIGID_BODY', 'SOFT_BODY']:
                body.label(text='Dynamic Object Settings:')
                row = body.split(factor=.9)
                rowrow = row.row(align=True)
                rowrow.prop(act, 'force', text='Force')
                row.prop(act, 'use_local_force', text='L', toggle=True)

                row = body.split(factor=.9)
                rowrow = row.row(align=True)
                rowrow.prop(act, 'torque', text='Torque')
                row.prop(act, 'use_local_torque', text='L', toggle=True)

                row = body.split(factor=.9)
                rowrow = row.row(align=True)
                rowrow.prop(act, 'linear_velocity', text='Linear Velocity')
                rowrowrow = row.row(align=True)
                rowrowrow.prop(act, 'use_local_linear_velocity', text='L', toggle=True)
                rowrowrow.prop(act, 'use_add_linear_velocity', text='A', toggle=True)

                row = body.split(factor=.9)
                rowrow = row.row(align=True)
                rowrow.prop(act, 'angular_velocity', text='Angular Velocity')
                row.prop(act, 'use_local_angular_velocity', text='L', toggle=True)

                body.prop(act, 'damping', text='Damping')

        if act.mode == 'OBJECT_SERVO':
            body.prop_search(act, 'reference_object', bpy.data, 'objects', text='Reference Object')
            body.prop(act, 'servo_mode', text='Servo Type')

            row = body.split(factor=.9)
            rowrow = row.row(align=True)
            rowrow.prop(act, 'linear_velocity', text='Linear Velocity')
            row.prop(act, 'use_local_angular_velocity', text='L', toggle=True)

            axis = body.row()
            axis.prop(act, 'use_servo_limit_x', text='X', toggle=True)
            axis.prop(act, 'use_servo_limit_y', text='Y', toggle=True)
            axis.prop(act, 'use_servo_limit_z', text='Z', toggle=True)
            axis_row = body.row()
            x_col = axis_row.column(align=True)
            x_col.prop(act, 'force_max_x', text='Max')
            x_col.prop(act, 'force_min_x', text='Min')
            y_col = axis_row.column(align=True)
            y_col.prop(act, 'force_max_y', text='Max')
            y_col.prop(act, 'force_min_y', text='Min')
            z_col = axis_row.column(align=True)
            z_col.prop(act, 'force_max_z', text='Max')
            z_col.prop(act, 'force_min_z', text='Min')

            opts = body.column(align=True)
            opts.prop(act, 'proportional_coefficient', text='Proportional Coefficient', slider=True)
            opts.prop(act, 'integral_coefficient', text='Integral Coefficient', slider=True)
            opts.prop(act, 'derivate_coefficient', text='Derivate Coefficient', slider=True)

        if act.mode == 'OBJECT_CHARACTER':
            locrow = body.split(factor=.9)
            loc = locrow.row(align=True)
            loc.prop(act, 'offset_location', text='Loc')
            locloc = locrow.row(align=True)
            locloc.prop(act, 'use_local_location', text='L', toggle=True)
            locloc.prop(act, 'use_add_character_location', text='A', toggle=True)
            rotrow = body.split(factor=.9)
            rot = rotrow.row(align=True)
            rot.prop(act, 'offset_rotation', text='Rot')
            rotrow.prop(act, 'use_local_rotation', text='L', toggle=True)
            row = body.split(factor=.6)
            row.label(text='')
            row = row.split(factor=.8)
            row.prop(act, 'use_character_jump', text='Jump', toggle=True)
            row.label(text='')

    def draw_mouse(self, act, body):
        body.prop(act, 'mode', text='Mode')
        if act.mode == 'VISIBILITY':
            body.prop(act, 'visible', text='Visible', toggle=True)
        else:
            data = body.row()
            xdat = data.column(align=True)
            ydat = data.column(align=True)

            xdat.prop(act, 'use_axis_x', text='Use X Axis', toggle=True)
            xdat.prop(act, 'sensitivity_x', text='Sensitivity')
            xdat.prop(act, 'threshold_x', text='Threshold')
            xdat.prop(act, 'min_x', text='Min')
            xdat.prop(act, 'max_x', text='Max')
            xdat.prop(act, 'object_axis_x', text='Object Axis')

            ydat.prop(act, 'use_axis_y', text='Use Y Axis', toggle=True)
            ydat.prop(act, 'sensitivity_y', text='Sensitivity')
            ydat.prop(act, 'threshold_y', text='Threshold')
            ydat.prop(act, 'min_y', text='Min')
            ydat.prop(act, 'max_y', text='Max')
            ydat.prop(act, 'object_axis_y', text='Object Axis')

            subrow = body.row()
            xsub = subrow.row(align=True)
            xsub.prop(act, 'local_x', text='Local', toggle=True)
            xsub.prop(act, 'reset_x', text='Reset', toggle=True)
            ysub = subrow.row(align=True)
            ysub.prop(act, 'local_y', text='Local', toggle=True)
            ysub.prop(act, 'reset_y', text='Reset', toggle=True)

    def draw_parent(self, act, body):
        body.prop(act, 'mode', text='Scene')
        if act.mode == 'SETPARENT':
            body.prop_search(act, 'object', bpy.data, 'objects', text='Parent Object')
            row = body.row()
            row.prop(act, 'use_compound', text='Compound')
            row.prop(act, 'use_ghost', text='Ghost')

    def draw_property(self, act, body):
        body.prop(act, 'mode', text='Mode')
        body.prop_search(act, 'property', self.target_object.game, 'properties', text='Property')
        if act.mode in ['ASSIGN', 'ADD']:
            body.prop(act, 'value', text='Value')
        row = body.split()
        if act.mode == 'COPY':
            row.prop_search(act, 'object', bpy.data, 'objects', text='Object')
            if getattr(act.object, 'game', None):
                row.prop_search(act, 'object_property', act.object.game, 'properties', text='Property')
            else:
                row.label(text='')

    def draw_random(self, act, body):
        header = body.row()
        header.prop(act, 'seed', text='Seed')
        header.prop(act, 'distribution', text='Distribution')
        body.prop_search(act, 'property', self.target_object.game, 'properties', text='Property')
        if act.distribution == 'BOOL_CONSTANT':
            body.prop(act, 'use_always_true', text='Always True', toggle=True)
        elif act.distribution == 'BOOL_UNIFORM':
            body.label(text='Choose between true and false, 50% chance each')
        elif act.distribution == 'BOOL_BERNOUILLI':
            body.prop(act, 'chance', text='Chance', slider=True)
        elif act.distribution == 'INT_CONSTANT':
            body.prop(act, 'int_value', text='Value')
        elif act.distribution == 'INT_UNIFORM':
            row = body.row()
            row.prop(act, 'int_min', text='Min')
            row.prop(act, 'int_max', text='Max')
        elif act.distribution == 'INT_POISSON':
            body.prop(act, 'int_mean', text='Mean')
        elif act.distribution == 'FLOAT_CONSTANT':
            body.prop(act, 'float_value', text='Value')
        elif act.distribution == 'FLOAT_UNIFORM':
            row = body.row()
            row.prop(act, 'float_min', text='Min')
            row.prop(act, 'float_max', text='Max')
        elif act.distribution == 'FLOAT_NORMAL':
            row = body.row()
            row.prop(act, 'float_mean', text='Mean')
            row.prop(act, 'standard_derivation', text='SD')
        elif act.distribution == 'FLOAT_NEGATIVE_EXPONENTIAL':
            body.prop(act, 'half_life_time', text='Half-Life Time')


    def draw_scene(self, act, body):
        body.prop(act, 'mode', text='Mode')
        if act.mode == 'SET':
            body.prop_search(act, 'scene', bpy.data, 'scenes', text='Scene')
        elif act.mode == 'CAMERA':
            body.prop_search(act, 'camera', bpy.data, 'objects', text='Scene')

    def draw_sound(self, act, body):
        body.template_ID(act, 'sound', open='SOUND_OT_open')
        if not act.sound:
            body.label(text='Select a sound from the list or load a new one')
        else:
            body.prop(act, 'mode', text='Play Mode')
            basics = body.row()
            basics.prop(act, 'volume', text='Volume')
            basics.prop(act, 'pitch', text='Pitch')

            body.prop(act, 'use_sound_3d', text='3D Sound')
            if act.use_sound_3d:
                row = body.row()
                c1 = row.column()
                c2 = row.column()

                c1.prop(act, 'gain_3d_min', text='Minimum Gain')
                c1.prop(act, 'distance_3d_reference')
                c1.prop(act, 'rolloff_factor_3d')
                c1.prop(act, 'cone_outer_angle_3d')

                c2.prop(act, 'gain_3d_max')
                c2.prop(act, 'distance_3d_max')
                c2.prop(act, 'cone_outer_gain_3d')
                c2.prop(act, 'cone_inner_angle_3d')

    def draw_state(self, act, body):
        row = body.split(factor=.4)
        row.prop(act, 'operation')
        row.template_layers(act, 'states', self.target_object.game, 'used_states', 0)

    def draw_steering(self, act, body):
        body.prop(act, 'mode')
        body.prop(act, 'target')
        body.prop(act, 'navmesh')
        row = body.row()
        row.prop(act, 'distance')
        row.prop(act, 'velocity')
        row = body.row()
        row.prop(act, 'acceleration')
        row.prop(act, 'turn_speed')
        row = body.row()
        row.prop(act, 'facing')
        row.prop(act, 'facing_axis')
        row.prop(act, 'normal_up')
        row = body.row()
        row.prop(act, 'self_terminated')
        body.prop(act, 'lock_z_velocity')
        if act.mode == 'PATHFOLLOWING':
            body.prop(act, 'show_visualization')
            row.prop(act, 'update_period')


    def draw_vibration(self, act, body):
        body.prop(act, 'joy_index')
        body.prop(act, 'mode')
        if act.mode == 'PLAY':
            row = body.row()
            row.prop(act, 'joy_strength_left')
            row.prop(act, 'joy_strength_right')
            body.prop(act, 'joy_duration')

    def draw_visibility(self, act, body):
        row = body.row()
        row.prop(act, 'use_visible')
        row.prop(act, 'use_occlusion')
        row.prop(act, 'apply_to_children')


class BNSensorPointerNode(BNSensorNode):
    def init(self, context):
        BNSensorNode.init(self, context)


_nodes.append(BNSensorPointerNode)


class BNControllerPointerNode(BNControllerNode):
    def init(self, context):
        BNControllerNode.init(self, context)


_nodes.append(BNControllerPointerNode)


class BNActuatorPointerNode(BNActuatorNode):
    def init(self, context):
        BNActuatorNode.init(self, context)


_nodes.append(BNActuatorPointerNode)


#############################################################################
# Sensors
#############################################################################


class BNSensorActuatorNode(BNSensorNode):
    bl_idname = 'BNSensorActuatorNode'
    bl_label = 'Actuator'

    def init(self, context):
        BNSensorNode.init(self, context)
        if bpy.context.object:
            self.target_object = bpy.context.object
            bpy.ops.logic.sensor_add(type='ACTUATOR')
            self.target_brick = bpy.context.object.game.sensors[-1].name
            self.show_info = False


_sen_nodes.append(BNSensorActuatorNode)


class BNSensorAlwaysNode(BNSensorNode):
    bl_idname = 'BNSensorAlwaysNode'
    bl_label = 'Always'

    def init(self, context):
        BNSensorNode.init(self, context)
        if bpy.context.object:
            self.target_object = bpy.context.object
            bpy.ops.logic.sensor_add(type='ALWAYS')
            self.target_brick = bpy.context.object.game.sensors[-1].name
            self.show_info = False


_sen_nodes.append(BNSensorAlwaysNode)


class BNSensorCollisionNode(BNSensorNode):
    bl_idname = 'BNSensorCollisionNode'
    bl_label = 'Collision'

    def init(self, context):
        BNSensorNode.init(self, context)
        if bpy.context.object:
            self.target_object = bpy.context.object
            bpy.ops.logic.sensor_add(type='COLLISION')
            self.target_brick = bpy.context.object.game.sensors[-1].name
            self.show_info = False


_sen_nodes.append(BNSensorCollisionNode)


class BNSensorDelayNode(BNSensorNode):
    bl_idname = 'BNSensorDelayNode'
    bl_label = 'Delay'

    def init(self, context):
        BNSensorNode.init(self, context)
        if bpy.context.object:
            self.target_object = bpy.context.object
            bpy.ops.logic.sensor_add(type='DELAY')
            self.target_brick = bpy.context.object.game.sensors[-1].name
            self.show_info = False


_sen_nodes.append(BNSensorDelayNode)


class BNSensorJoystickNode(BNSensorNode):
    bl_idname = 'BNSensorJoystickNode'
    bl_label = 'Joystick'

    def init(self, context):
        BNSensorNode.init(self, context)
        if bpy.context.object:
            self.target_object = bpy.context.object
            bpy.ops.logic.sensor_add(type='JOYSTICK')
            self.target_brick = bpy.context.object.game.sensors[-1].name
            self.show_info = False


_sen_nodes.append(BNSensorJoystickNode)


class BNSensorKeyboardNode(BNSensorNode):
    bl_idname = 'BNSensorKeyboardNode'
    bl_label = 'Keyboard'

    def init(self, context):
        BNSensorNode.init(self, context)
        if bpy.context.object:
            self.target_object = bpy.context.object
            bpy.ops.logic.sensor_add(type='KEYBOARD')
            self.target_brick = bpy.context.object.game.sensors[-1].name
            self.show_info = False


_sen_nodes.append(BNSensorKeyboardNode)


class BNSensorMessageNode(BNSensorNode):
    bl_idname = 'BNSensorMessageNode'
    bl_label = 'Message'

    def init(self, context):
        BNSensorNode.init(self, context)
        if bpy.context.object:
            self.target_object = bpy.context.object
            bpy.ops.logic.sensor_add(type='MESSAGE')
            self.target_brick = bpy.context.object.game.sensors[-1].name
            self.show_info = False


_sen_nodes.append(BNSensorMessageNode)


class BNSensorMouseNode(BNSensorNode):
    bl_idname = 'BNSensorMouseNode'
    bl_label = 'Mouse'

    def init(self, context):
        BNSensorNode.init(self, context)
        if bpy.context.object:
            self.target_object = bpy.context.object
            bpy.ops.logic.sensor_add(type='MOUSE')
            self.target_brick = bpy.context.object.game.sensors[-1].name
            self.show_info = False


_sen_nodes.append(BNSensorMouseNode)


class BNSensorMovementNode(BNSensorNode):
    bl_idname = 'BNSensorMovementNode'
    bl_label = 'Movement'

    def init(self, context):
        BNSensorNode.init(self, context)
        if bpy.context.object:
            self.target_object = bpy.context.object
            bpy.ops.logic.sensor_add(type='MOVEMENT')
            self.target_brick = bpy.context.object.game.sensors[-1].name
            self.show_info = False


_sen_nodes.append(BNSensorMovementNode)


class BNSensorNearNode(BNSensorNode):
    bl_idname = 'BNSensorNearNode'
    bl_label = 'Near'

    def init(self, context):
        BNSensorNode.init(self, context)
        if bpy.context.object:
            self.target_object = bpy.context.object
            bpy.ops.logic.sensor_add(type='NEAR')
            self.target_brick = bpy.context.object.game.sensors[-1].name
            self.show_info = False


_sen_nodes.append(BNSensorNearNode)


class BNSensorPropertyNode(BNSensorNode):
    bl_idname = 'BNSensorPropertyNode'
    bl_label = 'Property'

    def init(self, context):
        BNSensorNode.init(self, context)
        if bpy.context.object:
            self.target_object = bpy.context.object
            bpy.ops.logic.sensor_add(type='PROPERTY')
            self.target_brick = bpy.context.object.game.sensors[-1].name
            self.show_info = False


_sen_nodes.append(BNSensorPropertyNode)


class BNSensorRadarNode(BNSensorNode):
    bl_idname = 'BNSensorRadarNode'
    bl_label = 'Radar'

    def init(self, context):
        BNSensorNode.init(self, context)
        if bpy.context.object:
            self.target_object = bpy.context.object
            bpy.ops.logic.sensor_add(type='RADAR')
            self.target_brick = bpy.context.object.game.sensors[-1].name
            self.show_info = False


_sen_nodes.append(BNSensorRadarNode)


class BNSensorRandomNode(BNSensorNode):
    bl_idname = 'BNSensorRandomNode'
    bl_label = 'Random'

    def init(self, context):
        BNSensorNode.init(self, context)
        if bpy.context.object:
            self.target_object = bpy.context.object
            bpy.ops.logic.sensor_add(type='RANDOM')
            self.target_brick = bpy.context.object.game.sensors[-1].name
            self.show_info = False


_sen_nodes.append(BNSensorRandomNode)


class BNSensorRayNode(BNSensorNode):
    bl_idname = 'BNSensorRayNode'
    bl_label = 'Ray'

    def init(self, context):
        BNSensorNode.init(self, context)
        if bpy.context.object:
            self.target_object = bpy.context.object
            bpy.ops.logic.sensor_add(type='RAY')
            self.target_brick = bpy.context.object.game.sensors[-1].name
            self.show_info = False


_sen_nodes.append(BNSensorRayNode)


#############################################################################
# Controllers
#############################################################################

class BNControllerAndNode(BNControllerNode):
    bl_idname = 'BNControllerAndNode'
    bl_label = 'And'

    def init(self, context):
        BNControllerNode.init(self, context)
        if bpy.context.object:
            self.target_object = bpy.context.object
            bpy.ops.logic.controller_add(type='LOGIC_AND')
            self.target_brick = bpy.context.object.game.controllers[-1].name
            self.show_info = False


_con_nodes.append(BNControllerAndNode)


class BNControllerOrNode(BNControllerNode):
    bl_idname = 'BNControllerOrNode'
    bl_label = 'Or'

    def init(self, context):
        BNControllerNode.init(self, context)
        if bpy.context.object:
            self.target_object = bpy.context.object
            bpy.ops.logic.controller_add(type='LOGIC_OR')
            self.target_brick = bpy.context.object.game.controllers[-1].name
            self.show_info = False


_con_nodes.append(BNControllerOrNode)


class BNControllerNandNode(BNControllerNode):
    bl_idname = 'BNControllerNandNode'
    bl_label = 'Nand'

    def init(self, context):
        BNControllerNode.init(self, context)
        if bpy.context.object:
            self.target_object = bpy.context.object
            bpy.ops.logic.controller_add(type='LOGIC_NAND')
            self.target_brick = bpy.context.object.game.controllers[-1].name
            self.show_info = False


_con_nodes.append(BNControllerNandNode)


class BNControllerNorNode(BNControllerNode):
    bl_idname = 'BNControllerNorNode'
    bl_label = 'Nor'

    def init(self, context):
        BNControllerNode.init(self, context)
        if bpy.context.object:
            self.target_object = bpy.context.object
            bpy.ops.logic.controller_add(type='LOGIC_NOR')
            self.target_brick = bpy.context.object.game.controllers[-1].name
            self.show_info = False


_con_nodes.append(BNControllerNorNode)


class BNControllerXorNode(BNControllerNode):
    bl_idname = 'BNControllerXorNode'
    bl_label = 'Xor'

    def init(self, context):
        BNControllerNode.init(self, context)
        if bpy.context.object:
            self.target_object = bpy.context.object
            bpy.ops.logic.controller_add(type='LOGIC_XOR')
            self.target_brick = bpy.context.object.game.controllers[-1].name
            self.show_info = False


_con_nodes.append(BNControllerXorNode)


class BNControllerXnorNode(BNControllerNode):
    bl_idname = 'BNControllerXnorNode'
    bl_label = 'Xnor'

    def init(self, context):
        BNControllerNode.init(self, context)
        if bpy.context.object:
            self.target_object = bpy.context.object
            bpy.ops.logic.controller_add(type='LOGIC_XNOR')
            self.target_brick = bpy.context.object.game.controllers[-1].name
            self.show_info = False


_con_nodes.append(BNControllerXnorNode)


class BNControllerExpressionNode(BNControllerNode):
    bl_idname = 'BNControllerExpressionNode'
    bl_label = 'Expression'

    def init(self, context):
        BNControllerNode.init(self, context)
        if bpy.context.object:
            self.target_object = bpy.context.object
            bpy.ops.logic.controller_add(type='EXPRESSION')
            self.target_brick = bpy.context.object.game.controllers[-1].name
            self.show_info = False


_con_nodes.append(BNControllerExpressionNode)


class BNControllerPythonNode(BNControllerNode):
    bl_idname = 'BNControllerPythonNode'
    bl_label = 'Python'

    def init(self, context):
        BNControllerNode.init(self, context)
        if bpy.context.object:
            self.target_object = bpy.context.object
            bpy.ops.logic.controller_add(type='PYTHON')
            self.target_brick = bpy.context.object.game.controllers[-1].name
            self.show_info = False


_con_nodes.append(BNControllerPythonNode)


#############################################################################
# Actuators
#############################################################################

class BNActuatorActionNode(BNActuatorNode):
    bl_idname = 'BNActuatorActionNode'
    bl_label = 'Action'

    def init(self, context):
        BNActuatorNode.init(self, context)
        if bpy.context.object:
            self.target_object = bpy.context.object
            bpy.ops.logic.actuator_add(type='ACTION')
            self.target_brick = bpy.context.object.game.actuators[-1].name
            self.show_info = False


_act_nodes.append(BNActuatorActionNode)


class BNActuatorCameraNode(BNActuatorNode):
    bl_idname = 'BNActuatorCameraNode'
    bl_label = 'Camera'

    def init(self, context):
        BNActuatorNode.init(self, context)
        if bpy.context.object:
            self.target_object = bpy.context.object
            bpy.ops.logic.actuator_add(type='CAMERA')
            self.target_brick = bpy.context.object.game.actuators[-1].name
            self.show_info = False


_act_nodes.append(BNActuatorCameraNode)


class BNActuatorCollectionNode(BNActuatorNode):
    bl_idname = 'BNActuatorCollectionNode'
    bl_label = 'Collection'

    def init(self, context):
        BNActuatorNode.init(self, context)
        if bpy.context.object:
            self.target_object = bpy.context.object
            bpy.ops.logic.actuator_add(type='COLLECTION')
            self.target_brick = bpy.context.object.game.actuators[-1].name
            self.show_info = False


_act_nodes.append(BNActuatorCollectionNode)


class BNActuatorConstraintNode(BNActuatorNode):
    bl_idname = 'BNActuatorConstraintNode'
    bl_label = 'Constraint'

    def init(self, context):
        BNActuatorNode.init(self, context)
        if bpy.context.object:
            self.target_object = bpy.context.object
            bpy.ops.logic.actuator_add(type='CONSTRAINT')
            self.target_brick = bpy.context.object.game.actuators[-1].name
            self.show_info = False


_act_nodes.append(BNActuatorConstraintNode)


class BNActuatorEditObjectNode(BNActuatorNode):
    bl_idname = 'BNActuatorEditObjectNode'
    bl_label = 'Edit Object'

    def init(self, context):
        BNActuatorNode.init(self, context)
        if bpy.context.object:
            self.target_object = bpy.context.object
            bpy.ops.logic.actuator_add(type='EDIT_OBJECT')
            self.target_brick = bpy.context.object.game.actuators[-1].name
            self.show_info = False


_act_nodes.append(BNActuatorEditObjectNode)


class BNActuatorFilter2dNode(BNActuatorNode):
    bl_idname = 'BNActuatorFilter2dNode'
    bl_label = 'Filter 2D'

    def init(self, context):
        BNActuatorNode.init(self, context)
        if bpy.context.object:
            self.target_object = bpy.context.object
            bpy.ops.logic.actuator_add(type='FILTER_2D')
            self.target_brick = bpy.context.object.game.actuators[-1].name
            self.show_info = False


_act_nodes.append(BNActuatorFilter2dNode)


class BNActuatorGameNode(BNActuatorNode):
    bl_idname = 'BNActuatorGameNode'
    bl_label = 'Game'

    def init(self, context):
        BNActuatorNode.init(self, context)
        if bpy.context.object:
            self.target_object = bpy.context.object
            bpy.ops.logic.actuator_add(type='GAME')
            self.target_brick = bpy.context.object.game.actuators[-1].name
            self.show_info = False


_act_nodes.append(BNActuatorGameNode)


class BNActuatorMessageNode(BNActuatorNode):
    bl_idname = 'BNActuatorMessageNode'
    bl_label = 'Message'

    def init(self, context):
        BNActuatorNode.init(self, context)
        if bpy.context.object:
            self.target_object = bpy.context.object
            bpy.ops.logic.actuator_add(type='MESSAGE')
            self.target_brick = bpy.context.object.game.actuators[-1].name
            self.show_info = False


_act_nodes.append(BNActuatorMessageNode)


class BNActuatorMotionNode(BNActuatorNode):
    bl_idname = 'BNActuatorMotionNode'
    bl_label = 'Motion'

    def init(self, context):
        BNActuatorNode.init(self, context)
        if bpy.context.object:
            self.target_object = bpy.context.object
            bpy.ops.logic.actuator_add(type='MOTION')
            self.target_brick = bpy.context.object.game.actuators[-1].name
            self.show_info = False


_act_nodes.append(BNActuatorMotionNode)


class BNActuatorMouseNode(BNActuatorNode):
    bl_idname = 'BNActuatorMouseNode'
    bl_label = 'Mouse'

    def init(self, context):
        BNActuatorNode.init(self, context)
        if bpy.context.object:
            self.target_object = bpy.context.object
            bpy.ops.logic.actuator_add(type='MOUSE')
            self.target_brick = bpy.context.object.game.actuators[-1].name
            self.show_info = False


_act_nodes.append(BNActuatorMouseNode)


class BNActuatorParentNode(BNActuatorNode):
    bl_idname = 'BNActuatorParentNode'
    bl_label = 'Parent'

    def init(self, context):
        BNActuatorNode.init(self, context)
        if bpy.context.object:
            self.target_object = bpy.context.object
            bpy.ops.logic.actuator_add(type='PARENT')
            self.target_brick = bpy.context.object.game.actuators[-1].name
            self.show_info = False


_act_nodes.append(BNActuatorParentNode)


class BNActuatorPropertyNode(BNActuatorNode):
    bl_idname = 'BNActuatorPropertyNode'
    bl_label = 'Property'

    def init(self, context):
        BNActuatorNode.init(self, context)
        if bpy.context.object:
            self.target_object = bpy.context.object
            bpy.ops.logic.actuator_add(type='PROPERTY')
            self.target_brick = bpy.context.object.game.actuators[-1].name
            self.show_info = False


_act_nodes.append(BNActuatorPropertyNode)


class BNActuatorRandomNode(BNActuatorNode):
    bl_idname = 'BNActuatorRandomNode'
    bl_label = 'Random'

    def init(self, context):
        BNActuatorNode.init(self, context)
        if bpy.context.object:
            self.target_object = bpy.context.object
            bpy.ops.logic.actuator_add(type='RANDOM')
            self.target_brick = bpy.context.object.game.actuators[-1].name
            self.show_info = False


_act_nodes.append(BNActuatorRandomNode)


class BNActuatorSceneNode(BNActuatorNode):
    bl_idname = 'BNActuatorSceneNode'
    bl_label = 'Scene'

    def init(self, context):
        BNActuatorNode.init(self, context)
        if bpy.context.object:
            self.target_object = bpy.context.object
            bpy.ops.logic.actuator_add(type='SCENE')
            self.target_brick = bpy.context.object.game.actuators[-1].name
            self.show_info = False


_act_nodes.append(BNActuatorSceneNode)


class BNActuatorSoundNode(BNActuatorNode):
    bl_idname = 'BNActuatorSoundNode'
    bl_label = 'Sound'

    def init(self, context):
        BNActuatorNode.init(self, context)
        if bpy.context.object:
            self.target_object = bpy.context.object
            bpy.ops.logic.actuator_add(type='SOUND')
            self.target_brick = bpy.context.object.game.actuators[-1].name
            self.show_info = False


_act_nodes.append(BNActuatorSoundNode)


class BNActuatorStateNode(BNActuatorNode):
    bl_idname = 'BNActuatorStateNode'
    bl_label = 'State'

    def init(self, context):
        BNActuatorNode.init(self, context)
        if bpy.context.object:
            self.target_object = bpy.context.object
            bpy.ops.logic.actuator_add(type='STATE')
            self.target_brick = bpy.context.object.game.actuators[-1].name
            self.show_info = False


_act_nodes.append(BNActuatorStateNode)


class BNActuatorSteeringNode(BNActuatorNode):
    bl_idname = 'BNActuatorSteeringNode'
    bl_label = 'Steering'

    def init(self, context):
        BNActuatorNode.init(self, context)
        if bpy.context.object:
            self.target_object = bpy.context.object
            bpy.ops.logic.actuator_add(type='STEERING')
            self.target_brick = bpy.context.object.game.actuators[-1].name
            self.show_info = False


_act_nodes.append(BNActuatorSteeringNode)


class BNActuatorVibrationNode(BNActuatorNode):
    bl_idname = 'BNActuatorVibrationNode'
    bl_label = 'Vibration'

    def init(self, context):
        BNActuatorNode.init(self, context)
        if bpy.context.object:
            self.target_object = bpy.context.object
            bpy.ops.logic.actuator_add(type='VIBRATION')
            self.target_brick = bpy.context.object.game.actuators[-1].name
            self.show_info = False


_act_nodes.append(BNActuatorVibrationNode)


class BNActuatorVisibilityNode(BNActuatorNode):
    bl_idname = 'BNActuatorVisibilityNode'
    bl_label = 'Visibility'

    def init(self, context):
        BNActuatorNode.init(self, context)
        if bpy.context.object:
            self.target_object = bpy.context.object
            bpy.ops.logic.actuator_add(type='VISIBILITY')
            self.target_brick = bpy.context.object.game.actuators[-1].name
            self.show_info = False


_act_nodes.append(BNActuatorVisibilityNode)