colcon build --packages-select exam_robot
source install/setup.bash
ros2 launch exam_robot robot_system.launch.py
