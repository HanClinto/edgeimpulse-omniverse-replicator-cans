import omni.replicator.core as rep
import carb.settings
import datetime

with rep.new_layer():

    # Load in asset
    local_path = "C:/Users/jplun/Repos/edgeimpulse-omniverse-replicator-cans/"
    CONVEYOR_USD = f"http://omniverse-content-production.s3-us-west-2.amazonaws.com/Assets/DigitalTwin/Assets/Warehouse/Equipment/Conveyors/ConveyorBelt_A/ConveyorBelt_A07_PR_NVD_01.usd"
    #PEPSI_USD = f"{local_path}/assets/Pepsi_Max_can/Pepsi_Can.usd"
    PEPSI_MAX_USD = f"{local_path}/assets/Pepsi_Max_can/Pepsi_Max.usd"

    # Camera paramters
    cam_position = (-110, 425, 200) #(46, 200, 78)
    cam_position2 = (-100, 425, 240) #(46, 120, 25)
    cam_position_random = rep.distribution.uniform((0, 181, 0), (0, 300, 0))
    cam_rotation = (-60, 0, 0)
    focus_distance = 120
    focus_distance2 = 90 #39.1
    focal_length = 40 #27
    focal_length2 = 30 #18.5
    f_stop = 20
    f_stop2 = 20
    #focus_distance_random = rep.distribution.normal(500.0, 100)

    # Cans path
    current_can = PEPSI_MAX_USD  # Change the item here e.g KNIFE_USD
    current_can_name = current_can.split(".")[0].split("/")[-1]
    output_path = local_path + '/rendered/' + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + '/' + current_can_name

    def rect_lights(num=1):
        lights = rep.create.light(
            light_type="rect",
            temperature=rep.distribution.normal(6500, 500),
            intensity=rep.distribution.normal(0, 5000),
            position=(45, 110, 0),
            rotation=(-90, 0, 0),
            scale=rep.distribution.uniform(50, 100),
            count=num
        )
        return lights.node

    def dome_lights(num=3):
        lights = rep.create.light(
            light_type="dome",
            temperature=rep.distribution.normal(6500, 500),
            intensity=rep.distribution.normal(0, 1000),
            position=(45, 120, 18),
            rotation=(225, 0, 0),
            count=num
        )
        return lights.node

    def conveyor():
        conveyor = rep.create.from_usd(CONVEYOR_USD, semantics=[('class', 'conveyor')])

        with conveyor:
            rep.modify.pose(
                position=(0, 0, 0),
                rotation=(0, -90, -90),
            )
        return conveyor
    

    # Define randomizer function for CULTERY assets. This randomization includes placement and rotation of the assets on the surface.
    def cans(size=15):
        instances = rep.randomizer.instantiate(rep.utils.get_usd_files(
            current_can), size=size, mode='point_instance')

        with instances:
            #rep.randomizer.scatter_2d(conveyor, check_for_collisions=True)
            rep.modify.pose(
                
                """position=rep.distribution.uniform(
                    (-150, 178.05, 10), (0, 178.05, 70)), #(0, 76.3651, 0), (90, 76.3651, 100)),
                rotation=rep.distribution.uniform(
                    (-90, -180, 0), (-90, 180, 0)),"""
            )
        return instances.node

    # Register randomization
    rep.randomizer.register(conveyor)
    rep.randomizer.register(cans)
    rep.randomizer.register(rect_lights)
    rep.randomizer.register(dome_lights)

    # Multiple setup cameras and attach it to render products
    camera = rep.create.camera(focus_distance=focus_distance, focal_length=focal_length,
                               position=cam_position, rotation=cam_rotation, f_stop=f_stop)
    camera2 = rep.create.camera(focus_distance=focus_distance2, focal_length=focal_length2,
                                position=cam_position2, rotation=cam_rotation, f_stop=f_stop)

    # Will render 1024x1024 images and 512x512 images
    render_product = rep.create.render_product(camera, (1024, 1024))
    render_product2 = rep.create.render_product(camera2, (512, 512))

    # Initialize and attach writer
    writer = rep.WriterRegistry.get("BasicWriter")
    writer.initialize(output_dir=f"{output_path}", # output_dir=f"{local_path}/data/angled_60/{output_path}"
                      rgb=True, bounding_box_2d_tight=False, semantic_segmentation=False)
    writer.attach([render_product, render_product2])

    with rep.trigger.on_frame(num_frames=25, rt_subframes=32):
        rep.randomizer.conveyor()
        rep.randomizer.rect_lights(1)
        rep.randomizer.dome_lights(1)
        rep.randomizer.cans(5)

    #carb.settings.get_settings().set(5)

    # Run the simulation graph
    rep.orchestrator.run()
