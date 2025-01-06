from ray.util.placement_group import (
    placement_group,
    placement_group_table,
    remove_placement_group,
)
from ray.util.scheduling_strategies import PlacementGroupSchedulingStrategy
import ray

ray.init()

print('''Available Resources: {}'''.format(ray.available_resources()))

@ray.remote(num_gpus=2)
def gpu_task():
    print("GPU ids: {}".format(ray.get_runtime_context().get_accelerator_ids()["GPU"]))

# Create Placement Group
pg = placement_group([{"CPU": 16, "GPU": 2}])

# Wait till Placement Group is created
ray.get(pg.ready(), timeout=10)
# Alternatively, we can use ray.wait
ready, unready = ray.wait([pg.ready()], timeout=10)

print('''Placement Group: {}'''.format(placement_group_table(pg)))

# Put this Ray Task into the Placement Group
ray.get(gpu_task.options(
    scheduling_strategy=PlacementGroupSchedulingStrategy(placement_group=pg)
).remote())

# Remove this Placement Group
remove_placement_group(pg)