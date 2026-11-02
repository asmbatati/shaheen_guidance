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
Launch the Proportional-Navigation interceptor controller.

Flies the interceptor onto the target with PN. Run this OR the BT/FSM/RL
controller (not several at once - they share the FCU).
"""
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument('namespace', default_value='interceptor'),
        DeclareLaunchArgument('law', default_value='pn',
                              description="'pn' (PN on the measured velocity, as in "
                                          "June 2026), 'pn_int' (constant-speed PN "
                                          "integrated on the command) or 'pursuit'"),
        DeclareLaunchArgument('nav_gain', default_value='3.0'),
        DeclareLaunchArgument('closing_speed', default_value='6.0'),
        DeclareLaunchArgument('cbf', default_value='false',
                              description='CBF safety filter on the velocity command'),
        DeclareLaunchArgument('cbf_z_min', default_value='1.5'),
        DeclareLaunchArgument('cbf_alpha', default_value='1.0'),
        DeclareLaunchArgument('vmax', default_value='8.0'),
        DeclareLaunchArgument('target_odom',
                              default_value='/target/mavros/local_position/odom'),
        Node(
            package='shaheen_guidance', executable='guidance',
            name='guidance_node', namespace=LaunchConfiguration('namespace'),
            output='screen',
            parameters=[{
                'law': LaunchConfiguration('law'),
                'nav_gain': LaunchConfiguration('nav_gain'),
                'closing_speed': LaunchConfiguration('closing_speed'),
                'cbf': LaunchConfiguration('cbf'),
                'cbf_z_min': LaunchConfiguration('cbf_z_min'),
                'cbf_alpha': LaunchConfiguration('cbf_alpha'),
                'vmax': LaunchConfiguration('vmax'),
                'use_sim_time': True,
            }],
            remappings=[('target_odom', LaunchConfiguration('target_odom'))],
        ),
    ])
