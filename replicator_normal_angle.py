import omni.replicator.core as rep
import random
import datetime

local_path = "C:/Users/jplun/Repos/edgeimpulse-omniverse-replicator-cans/"
output_path = local_path + '/rendered/' + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + '/' + "Multi_Cans_Normal_Angle"
ENV_USD = f"http://omniverse-content-production.s3-us-west-2.amazonaws.com/Assets/Scenes/Templates/Interior/ZetCG_ExhibitionHall.usd"
CONVEYOR_USD = f"http://omniverse-content-production.s3-us-west-2.amazonaws.com/Assets/DigitalTwin/Assets/Warehouse/Equipment/Conveyors/ConveyorBelt_A/ConveyorBelt_A07_PR_NVD_01.usd"
PEPSI_USD = f"{local_path}/assets/Pepsi_Can/Pepsi_Can.usd"
PEPSI_MAX_USD = f"{local_path}/assets/Pepsi_Max_can/Pepsi_Max.usd"
PEPSI_TALLBOY_USD = f"{local_path}/assets/Pepsi_Tallboy/Pepsi_Tallboy.usd"
TOTAL_CANS = 6

cans_list = [PEPSI_MAX_USD] # PEPSI_TALLBOY_USD

# Camera parameters
cam_position = (-110, 198, 200) #(46, 200, 78)
cam_position2 = (-100, 198, 280) #(46, 120, 25)
cam_position_random = rep.distribution.uniform((0, 181, 0), (0, 300, 0))
cam_rotation = (0, 0, 0)
focus_distance = 120
focus_distance2 = 90 #39.1
focal_length = 40 #27
focal_length2 = 30 #18.5
f_stop = 20
f_stop2 = 20

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
rep.randomizer.register(rect_lights)

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
rep.randomizer.register(dome_lights)

# Create stage environment
rep.create.from_usd(ENV_USD)

plane1 = rep.create.plane(scale=0.85, visible=False, semantics=[('class', 'plane1')])
with plane1:
    rep.modify.pose(
        position=(-167, 178.05, 50.56)
    )
plane2 = rep.create.plane(scale=0.85, visible=False, semantics=[('class', 'plane2')])
with plane2:
    rep.modify.pose(
        position=(-82, 178.05, 50.56)
    )

conveyor = rep.create.from_usd(CONVEYOR_USD, semantics=[('class', 'conveyor')])
with conveyor:
    rep.modify.pose(
        position=(0, 0, 0),
        rotation=(0, -90, -90),
    )

cans = list()
for i in range(TOTAL_CANS):
    random_can = random.choice(cans_list)
    random_can_name = random_can.split(".")[0].split("/")[-1]
    this_can = rep.create.from_usd(random_can, semantics=[('class', 'can')]) 
    if random_can_name == "Pepsi_Can":
        with this_can:
            rep.modify.pose(
                position=(0, 0, 0),
                rotation=(0, -90, -90),
                scale=(0.001, 0.001, 0.001)
            )
    if random_can_name == "Pepsi_Tallboy":
        with this_can:
            rep.modify.pose(
                position=(0, 0, 0),
                rotation=(0, -90, -90),
                scale=(0.04, 0.04, 0.04)
            )
    else:   
        with this_can:
            rep.modify.pose(
                position=(0, 0, 0),
                rotation=(0, -90, -90)
            )
    cans.append(this_can)

# Multiple setup cameras and attach to render products
camera = rep.create.camera(focus_distance=focus_distance, focal_length=focal_length,
                            position=cam_position, rotation=cam_rotation, f_stop=f_stop)
camera2 = rep.create.camera(focus_distance=focus_distance2, focal_length=focal_length2,
                            position=cam_position2, rotation=cam_rotation, f_stop=f_stop)

# Render images
render_product = rep.create.render_product(camera, (1024, 1024))
render_product2 = rep.create.render_product(camera2, (1024, 1024))

# Initialize and attach writer
writer = rep.WriterRegistry.get("BasicWriter")
writer.initialize(output_dir=f"{output_path}", rgb=True, bounding_box_2d_tight=False)
writer.attach([render_product, render_product2])

with rep.trigger.on_frame(num_frames=50, rt_subframes=55):
    planesList=[('class','plane1'),('class','plane2')]
    with rep.create.group(cans):
        planes=rep.get.prims(semantics=planesList)
        rep.modify.pose(
            rotation=rep.distribution.uniform(
                (-90, -180, 0), (-90, 180, 0)
            )
        )
        rep.randomizer.scatter_2d(planes, check_for_collisions=True)

rep.orchestrator.run()
