#!/usr/bin/env python3

"""
Launch file for Isaac Sim ROS2 bridge for bimanual SO-101 robot.

This launch file sets up the ROS2 side of the Isaac Sim integration:
1. robot_state_publisher - publishes TF transforms from URDF
2. controller_manager - manages ros2_control hardware interfaces and controllers
3. Controller spawners - start joint_state_broadcaster and trajectory controllers

Prerequisites:
- Isaac Sim must be running with the bi_so101_world.usd loaded
- Isaac Sim OmniGraph must be configured to publish/subscribe to joint state topics

Topics:
- /isaac_joint_states (sensor_msgs/JointState) - Isaac Sim publishes here
- /isaac_joint_commands (sensor_msgs/JointState) - Isaac Sim subscribes here
- /joint_states (sensor_msgs/JointState) - Unified joint states from broadcaster
- /left_arm_controller/joint_trajectory (trajectory_msgs/JointTrajectory)
- /left_gripper_controller/joint_trajectory (trajectory_msgs/JointTrajectory)
- /right_arm_controller/joint_trajectory (trajectory_msgs/JointTrajectory)
- /right_gripper_controller/joint_trajectory (trajectory_msgs/JointTrajectory)

Usage:
    # Terminal 1: Start Isaac Sim and load USD
    # Open Isaac Sim, load bi_so101_world.usd, click Play

    # Terminal 2: Start ROS2 bridge
    ros2 launch lerobot_launch bi_so101_isaac_bridge.launch.py

    # Terminal 3: Start LeRobot teleoperation
    lerobot-teleoperate --robot.type=bi_so101_ros --teleop.type=bi_so101_keyboard
"""

import os
from launch import LaunchDescription
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch.substitutions import Command
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    # Get URDF via xacro
    robot_description = ParameterValue(
        Command(
            [
                "xacro ",
                os.path.join(
                    get_package_share_directory("lerobot_description"),
                    "urdf",
                    "bi_so101_isaac.urdf.xacro",
                ),
            ]
        ),
        value_type=str,
    )

    # Robot state publisher - publishes TF transforms
    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{"robot_description": robot_description}],
        output="screen",
    )

    # Controller manager - manages hardware interface and controllers
    controller_manager = Node(
        package="controller_manager",
        executable="ros2_control_node",
        parameters=[
            {"robot_description": robot_description},
            os.path.join(
                get_package_share_directory("lerobot_controller"),
                "config",
                "bi_so101_isaac_controllers.yaml",
            ),
        ],
        output="screen",
    )

    # Joint state broadcaster - publishes unified /joint_states topic
    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "joint_state_broadcaster",
            "--controller-manager",
            "/controller_manager",
        ],
        output="screen",
    )

    # Left arm trajectory controller
    left_arm_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "left_arm_controller",
            "--controller-manager",
            "/controller_manager"
        ],
        output="screen",
    )

    # Left gripper trajectory controller
    left_gripper_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "left_gripper_controller",
            "--controller-manager",
            "/controller_manager"
        ],
        output="screen",
    )

    # Right arm trajectory controller
    right_arm_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "right_arm_controller",
            "--controller-manager",
            "/controller_manager"
        ],
        output="screen",
    )

    # Right gripper trajectory controller
    right_gripper_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "right_gripper_controller",
            "--controller-manager",
            "/controller_manager"
        ],
        output="screen",
    )

    return LaunchDescription([
        robot_state_publisher_node,
        controller_manager,
        joint_state_broadcaster_spawner,
        left_arm_controller_spawner,
        left_gripper_controller_spawner,
        right_arm_controller_spawner,
        right_gripper_controller_spawner,
    ])
