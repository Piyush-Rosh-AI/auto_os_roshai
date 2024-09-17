# DWB Controller

The DWB controller is the successor to the base local planner and DWA controllers in ROS 1. It was created in ROS 1 by David Lu!! at Locus Robotics as part of the `robot_navigation` project. It was then ported to ROS 2 for use in Nav2 as its critic-based controller algorithm.

DWB improves on DWA in a few major ways:

- It implements plugin-based critics to allow users to specify new critic functions to use in the system. They can be dynamically reconfigured, reweighted, and tuned to gain very particular behavior in your robot system.
- It implements plugin-based trajectory generation techniques, so that users can generate trajectories any number of ways and for any number of types of vehicles
- Includes a number of plugin implementations for common use

It is possible to tune DWB to gain both DWA and base local planner behaviors, as well as expansions using new plugins for totally use-case specific behaviors. The current trajectory generator plugins work for omnidirectional and differential drive robots, though an ackermann generator would be trivial to add. The current critic plugins work for both circular and non-circular robots and include many of the cost functions needed to build a path tracking system with various attributes.

See its [Configuration Guide Page](https://docs.nav2.org/configuration/packages/configuring-dwb-controller.html) for additional parameter descriptions.

## DWB Plugins

DWB is highly configurable through the use of plugins. There are three types of
plugins used. For each of them, a few implementations are available but you can
create custom ones if you need to.

### Trajectory Generator Plugins

These plugins generate the set of possible trajectories that should be evaluated
by the critics. The trajectory with the best score determines the output command
velocity.

There are two trajectory generators provided with Navigation 2. Only one can be
loaded at a time.

* **StandardTrajectoryGenerator** - This is similar to the trajectory rollout
  algorithm used in base_local_planner in ROS 1.
* **LimitedAccelGenerator** - This is similar to DWA used in ROS 1.

### Critic Plugins

These plugins score the trajectories generated by the trajectory generator.
Multiple plugins can be loaded and the sum of their scores determines the chosen
command velocity.

* **BaseObstacle** - Scores a trajectory based on where the path passes over the
  costmap. To use this properly, you must use the inflation layer in costmap to
  expand obstacles by the robot's radius.
* **ObstacleFootprint** - Scores a trajectory based on verifying all points along
  the robot's footprint don't touch an obstacle marked in the costmap.
* **GoalAlign** - Scores a trajectory based on how well aligned the trajectory is
  with the goal pose.
* **GoalDist** - Scores a trajectory based on how close the trajectory gets the robot
  to the goal pose.
* **PathAlign** - Scores a trajectory based on how well it is aligned to the path
  provided by the global planner.
* **PathDist** - Scores a trajectory based on how far it ends up from the path
  provided by the global planner.
* **PreferForward** - Scores trajectories that move the robot forwards more highly
* **RotateToGoal** - Only allows the robot to rotate to the goal orientation when it
  is sufficiently close to the goal location
* **Oscillation** - Prevents the robot from just moving backwards and forwards.
* **Twirling** - Prevents holonomic robots from spinning as they make their way to
  the goal.