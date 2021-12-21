import bpy
import bge_bricknodes


sensor_types = {
    'ACTUATOR': 'BNSensorActuatorNode',
    'ALWAYS': 'BNSensorAlwaysNode',
    'COLLISION': 'BNSensorCollisionNode',
    'DELAY': 'BNSensorDelayNode',
    'JOYSTICK': 'BNSensorJoystickNode',
    'KEYBOARD': 'BNSensorKeyboardNode',
    'MESSAGE': 'BNSensorMessageNode',
    'MOUSE': 'BNSensorMouseNode',
    'MOVEMENT': 'BNSensorMovementNode',
    'NEAR': 'BNSensorNearNode',
    'PROPERTY': 'BNSensorPropertyNode',
    'RADAR': 'BNSensorRadarNode',
    'RANDOM': 'BNSensorRandomNode',
    'RAY': 'BNSensorRayNode'
}

controller_types = {
    'LOGIC_AND': 'BNControllerAndNode',
    'LOGIC_OR': 'BNControllerOrNode',
    'LOGIC_NAND': 'BNControllerNandNode',
    'LOGIC_NOR': 'BNControllerNorNode',
    'LOGIC_XOR': 'BNControllerXorNode',
    'LOGIC_XNOR': 'BNControllerXnorNode',
    'EXPRESSION': 'BNControllerExpressionNode',
    'PYTHON': 'BNControllerPythonNode'
}

actuator_types = {
    'ACTION': 'BNActuatorActionNode',
    'CAMERA': 'BNActuatorCameraNode',
    'COLLECTION': 'BNActuatorCollectionNode',
    'CONSTRAINT': 'BNActuatorConstraintNode',
    'EDIT_OBJECT': 'BNActuatorEditObjectNode',
    'FILTER_2D': 'BNActuatorFilter2dNode',
    'GAME': 'BNActuatorGameNode',
    'MESSAGE': 'BNActuatorMessageNode',
    'MOTION': 'BNActuatorMotionNode',
    'MOUSE': 'BNActuatorMouseNode',
    'PARENT': 'BNActuatorParentNode',
    'PROPERTY': 'BNActuatorPropertyNode',
    'RANDOM': 'BNActuatorRandomNode',
    'SCENE': 'BNActuatorSceneNode',
    'SOUND': 'BNActuatorSoundNode',
    'STATE': 'BNActuatorStateNode',
    'STEERING': 'BNActuatorSteeringNode',
    'VIBRATION': 'BNActuatorVibrationNode',
    'VISIBILITY': 'BNActuatorVisibilityNode',
}


class BNConvertBricks(bpy.types.Operator):
    """Convert Bricks to Nodes"""
    bl_idname = "bge_bricknodes.convert_bricks"
    bl_label = "Convert"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        available_bricks = {}
        added = 0
        tree = context.space_data.edit_tree
        for n in tree.nodes:
            if isinstance(n, bpy.types.NodeFrame) or isinstance(n, bpy.types.NodeReroute):
                continue
            if n.get_brick() not in available_bricks:
                available_bricks[n.get_brick()] = n
        offstep = 0
        step_min = 0
        offset_y = 0
        mode = 0
        frame = None
        for obj in context.scene.objects:
            frame = None
            if (
                len(obj.game.sensors) == 0 and
                len(obj.game.controllers) == 0 and
                len(obj.game.actuators) == 0
            ):
                continue
            frame = tree.nodes.new('NodeFrame')
            frame.label = obj.name
            s_y = 0
            c_y = 0
            a_y = 0
            for a in obj.game.actuators:
                if a not in available_bricks:
                    added += 1
                    actuator = tree.nodes.new('BNActuatorNode')
                    actuator.parent = frame
                    actuator.show_info = False
                    actuator.target_object = obj
                    actuator.target_brick = a.name
                    actuator.location = (offstep * 1300) + 780, offset_y + a_y
                    a_y -= 40
                    available_bricks[a] = actuator
                    actuator.hide = True
                    actuator.label = a.name
            for c in obj.game.controllers:
                if c not in available_bricks:
                    added += 1
                    controller = tree.nodes.new('BNControllerNode')
                    controller.parent = frame
                    controller.show_info = False
                    controller.target_object = obj
                    controller.target_brick = c.name
                    controller.location = (offstep * 1300) + 440, offset_y + c_y
                    c_y -= 40
                    available_bricks[c] = controller
                    controller.hide = True
                    controller.label = c.name
            for s in obj.game.sensors:
                if s not in available_bricks:
                    added += 1
                    sensor = tree.nodes.new('BNSensorNode')
                    sensor.parent = frame
                    sensor.show_info = False
                    sensor.target_object = obj
                    sensor.target_brick = s.name
                    sensor.location = (offstep * 1300), offset_y + s_y
                    available_bricks[s] = sensor
                    sensor.hide = True
                    sensor.label = s.name
                s_y -= 40
            
            if offstep < 2:
                offstep += 1
                min_y = min([s_y, c_y, a_y])
                if min_y < step_min:
                    step_min = min_y
            else:
                offstep = 0
                offset_y += step_min - 80
                step_min = 0

        if added == 0 and frame:
            tree.nodes.remove(frame)
        
        for obj in context.scene.objects:
            for s in obj.game.sensors:
                for c in s.controllers:
                    if c in available_bricks:
                        tree.links.new(available_bricks[c].inputs[0], available_bricks[s].outputs[0])
            for c in obj.game.controllers:
                for a in c.actuators:
                    if a in available_bricks:
                        tree.links.new(available_bricks[a].inputs[0], available_bricks[c].outputs[0])


        return {'FINISHED'}


class BNDuplicateBrick(bpy.types.Operator):
    """Duplicate this brick"""
    bl_idname = "bge_bricknodes.duplicate_brick"
    bl_label = "Duplicate Brick"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        n = context.node
        old_brick = n.get_brick()
        tree = context.space_data.edit_tree
        active = bpy.context.object
        brick = n.get_brick()
        scene = bpy.context.scene
        if not n.target_object:
            return
        for obj in scene.objects:
            if obj.name != n.target_object.name:
                obj.select_set(False)
            else:
                bpy.context.view_layer.objects.active = obj
                obj.select_set(True)
        if isinstance(brick, bpy.types.Sensor):
            bpy.ops.logic.sensor_add(type=brick.type)
            new_brick = context.object.game.sensors[-1]
        if isinstance(brick, bpy.types.Controller):
            bpy.ops.logic.controller_add(type=brick.type)
            new_brick = context.object.game.controllers[-1]
        if isinstance(brick, bpy.types.Actuator):
            bpy.ops.logic.actuator_add(type=brick.type)
            new_brick = context.object.game.actuators[-1]
        
        
        n.target_brick = new_brick.name
        for attr in dir(old_brick):
            if (
                attr.startswith('__') or
                attr.startswith('rna_') or
                attr.startswith('bl_') or
                callable(attr) or
                attr == 'name'
            ):
                print(f'Skipping {attr}')
                continue
            print(f'Trying {attr}: {getattr(old_brick, attr)} on {old_brick.name} to {new_brick.name}')
            try:
                setattr(new_brick, attr, getattr(old_brick, attr))
            except Exception as e:
                print(f'Failed {attr}: {e}')
                continue
        bpy.context.view_layer.objects.active = active
        active.select_set(True)
        return {'FINISHED'}
    
    def copy_contents(self):
        attrs = [
            'active',
            'use_pulse_true_level',
            'use_pulse_false_level',
            'tick_skip',
            'use_level',
            'use_tap',
            'invert',
            'actuator',
            'use_pulse',
            'use_material',
            'material',
            'property',
            'delay',
            'duration',
            'use_repeat',
            'joystick_index',
            'event_type',
            'use_all_events',
            'axis_number',
            'axis_direction',
            'axis_threshold',
            'single_axis_number',
            'axis_threshold',
            'axis_trigger_number',
            'axis_threshold',
            'button_number',
            'key',
            'modifier_key_1',
            'modifier_key_2',
            'use_all_keys',
            'log',
            'target',
            'subject',
            'mouse_event',
            'axis',
            'use_local',
            'threshold',
            'property',
            'distance',
            'reset_distance',
            'evaluation_type',
            'property',
            'value',
            'angle',
            'distance',
            'seed',
            'ray_type',
            'range',
            'use_x_ray',
            'mask',
            'states',
            'expression',
            'mode',
            'text',
            'mode',
            'module',
            'use_debug',
            'play_mode',
            'use_force',
            'use_additive',
            'use_additive',
            'action',
            'use_continue_last_frame',
            'frame_start',
            'frame_end',
            'apply_to_children',
            'frame_blend_in',
            'priority',
            'layer',
            'layer_weight',
            'blend_mode',
            'frame_property',
            'object',
            'height',
            'min',
            'max',
            'damping'
        ]


class BNRemoveLogicBrickSensor(bpy.types.Operator):
    """Remove the selected sensor from the selected object"""
    bl_idname = "bge_bricknodes.remove_sensor"
    bl_label = "Remove Sensor"
    bl_options = {'REGISTER', 'UNDO'}
    target_brick: bpy.props.StringProperty()

    def execute(self, context):
        if self.target_brick == '':
            n = context.node
            tree = context.space_data.edit_tree
            for link in n.outputs[0].links:
                tree.links.remove(link)
            name = n.target_brick
            n.target_brick = ''
            bpy.ops.logic.sensor_remove(sensor=name, object=n.target_object.name)
        else:
            bpy.ops.logic.sensor_remove(sensor=self.target_brick, object=context.object.name)
        return {'FINISHED'}


class BNRemoveLogicBrickController(bpy.types.Operator):
    """Remove the selected controller from the selected object"""
    bl_idname = "bge_bricknodes.remove_controller"
    bl_label = "Remove Controller"
    bl_options = {'REGISTER', 'UNDO'}
    target_brick: bpy.props.StringProperty()

    def execute(self, context):
        if self.target_brick == '':
            n = context.node
            tree = context.space_data.edit_tree
            for link in n.inputs[0].links:
                tree.links.remove(link)
            for link in n.outputs[0].links:
                tree.links.remove(link)
            name = n.target_brick
            n.target_brick = ''
            bpy.ops.logic.controller_remove(controller=name, object=n.target_object.name)
        else:
            tree = context.space_data.edit_tree
            for n in tree.nodes:
                if n.get_brick().name == self.target_brick and n.target_object == context.object:
                    for link in n.inputs[0].links:
                        tree.links.remove(link)
                    for link in n.outputs[0].links:
                        tree.links.remove(link)
                    tree.nodes.remove(n)
            bpy.ops.logic.controller_remove(controller=self.target_brick, object=context.object.name)
        return {'FINISHED'}


class BNRemoveLogicBrickActuator(bpy.types.Operator):
    """Remove the selected actuator from the selected object"""
    bl_idname = "bge_bricknodes.remove_actuator"
    bl_label = "Remove Actuator"
    bl_options = {'REGISTER', 'UNDO'}
    target_brick: bpy.props.StringProperty()

    def execute(self, context):
        if self.target_brick == '':
            n = context.node
            tree = context.space_data.edit_tree
            for link in n.inputs[0].links:
                tree.links.remove(link)
            name = n.target_brick
            n.target_brick = ''
            bpy.ops.logic.actuator_remove(actuator=name, object=n.target_object.name)
        else:
            bpy.ops.logic.actuator_remove(actuator=self.target_brick, object=context.object.name)
        return {'FINISHED'}


class BNUpdateTree(bpy.types.Operator):
    """Synchronize logic bricks with the node setup. This should normally happen automatically"""
    bl_idname = "bge_bricknodes.update_all"
    bl_label = "Sync"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bge_bricknodes.nodes.update_all_trees(self, context)
        return {'FINISHED'}


class NLAddPropertyOperator(bpy.types.Operator):
    bl_idname = "bricknodes.add_game_prop"
    bl_label = "Add Game Property"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Adds a property available to the UPBGE"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        bpy.ops.object.game_property_new()
        return {'FINISHED'}


class NLMovePropertyOperator(bpy.types.Operator):
    bl_idname = "bricknodes.move_game_prop"
    bl_label = "Move Game Property"
    bl_description = "Move Game Property"
    bl_options = {'REGISTER', 'UNDO'}
    index: bpy.props.IntProperty()
    direction: bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        bpy.ops.object.game_property_move(
            index=self.index,
            direction=self.direction
        )
        return {'FINISHED'}


class NLRemovePropertyOperator(bpy.types.Operator):
    bl_idname = "bricknodes.remove_game_prop"
    bl_label = "Add Game Property"
    bl_description = "Remove this property"
    bl_options = {'REGISTER', 'UNDO'}
    index: bpy.props.IntProperty()

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        bpy.ops.object.game_property_remove(index=self.index)
        return {'FINISHED'}
