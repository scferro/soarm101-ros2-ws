#!/usr/bin/env python3

"""
Composite launch file for SO101 robot arm with Gazebo simulation, controllers, and MoveIt.

This launch file combines:
1. Gazebo simulation (so101_gazebo.launch.py)
2. ROS2 Controllers (so101_controller.launch.py with is_sim=True)
3. MoveIt motion planning (so101_moveit.launch.py with is_sim=True)

Usage:
    ros2 launch lerobot_launch so101_single_moveit_gazebo.launch.py
"""

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import PathJoinSubstitution


def generate_launch_description():
    # Find package directories
    lerobot_description_share = FindPackageShare('lerobot_description')
    lerobot_controller_share = FindPackageShare('lerobot_controller')
    lerobot_moveit_share = FindPackageShare('lerobot_moveit')

    # Include Gazebo launch file
    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                lerobot_description_share,
                'launch',
                'so101_gazebo.launch.py'
            ])
        ])
    )

    # Include controller launch file (with is_sim=True)
    controller_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                lerobot_controller_share,
                'launch',
                'so101_controller.launch.py'
            ])
        ]),
        launch_arguments={
            'is_sim': 'True'
        }.items()
    )

    # Include MoveIt launch file (with is_sim=True)
    moveit_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                lerobot_moveit_share,
                'launch',
                'so101_moveit.launch.py'
            ])
        ]),
        launch_arguments={
            'is_sim': 'True'
        }.items()
    )

    return LaunchDescription([
        gazebo_launch,
        controller_launch,
        moveit_launch,
    ])
