#!/usr/bin/env python3
# Copyright 2026 Abdulrahman S. Al-Batati
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Launch the interception strategy node.

Runs in the interceptor namespace (so it publishes
``/interceptor/intercept_point``, the topic the Behaviour Tree reads) and remaps
its inputs onto the interceptor/target odometry. It consumes the target's
predicted path when one is published; nothing publishes the default
``/target/predicted_path`` in this workspace, so it normally uses its
constant-velocity prediction from the target odometry.
"""
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument('namespace', default_value='interceptor'),
        DeclareLaunchArgument(
            'interceptor_odom',
            default_value='/interceptor/mavros/local_position/odom'),
        DeclareLaunchArgument(
            'target_odom', default_value='/target/mavros/local_position/odom'),
        DeclareLaunchArgument(
            'target_predicted_path', default_value='/target/predicted_path'),
        DeclareLaunchArgument('vmax', default_value='8.0'),
        DeclareLaunchArgument('amax', default_value='4.0'),
        Node(
            package='shaheen_guidance',
            executable='interceptor',
            name='interceptor_node',
            namespace=LaunchConfiguration('namespace'),
            output='screen',
            parameters=[{
                'vmax': LaunchConfiguration('vmax'),
                'amax': LaunchConfiguration('amax'),
                'frame_id': 'map',
                'use_sim_time': True,
            }],
            remappings=[
                ('interceptor_odom', LaunchConfiguration('interceptor_odom')),
                ('target_odom', LaunchConfiguration('target_odom')),
                ('target_predicted_path', LaunchConfiguration('target_predicted_path')),
            ],
        ),
    ])
