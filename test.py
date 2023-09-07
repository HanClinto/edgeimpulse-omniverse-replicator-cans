import omni.replicator.core as rep
import random

local_path = "C:/Users/jplun/Repos/edgeimpulse-omniverse-replicator-cans/"
CONVEYOR_USD = f"http://omniverse-content-production.s3-us-west-2.amazonaws.com/Assets/DigitalTwin/Assets/Warehouse/Equipment/Conveyors/ConveyorBelt_A/ConveyorBelt_A07_PR_NVD_01.usd"
PEPSI_USD = f"{local_path}/assets/Pepsi_Can/Pepsi_Can.usd"
PEPSI_MAX_USD = f"{local_path}/assets/Pepsi_Max_can/Pepsi_Max.usd"
PEPSI_TALLBOY_USD = f"{local_path}/assets/Pepsi_Tallboy/Pepsi_Tallboy.usd"
TOTAL_CANS = 10
CURRENT_CAN = PEPSI_MAX_USD

cans_list = [PEPSI_MAX_USD, PEPSI_TALLBOY_USD]

plane = rep.create.plane(scale=0.85, visible=False)
with plane:
    rep.modify.pose(
        position=(-126, 178.05, 50.56)
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

with rep.trigger.on_frame(num_frames=10, rt_subframes=32):
    with rep.create.group(cans):
        rep.modify.pose(
            rotation=rep.distribution.uniform(
                (-90, -180, 0), (-90, 180, 0))
        )
        rep.randomizer.scatter_2d(plane, check_for_collisions=True)

rep.orchestrator.run()
