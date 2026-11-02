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
Frame helpers for MAVROS odometry (no ROS dependency, easy to unit-test).

MAVROS publishes ``local_position/odom`` with the pose in the local ENU frame
but the twist in the BODY frame (``child_frame_id`` base_link; see
``transform_frame_enu_baselink`` in mavros' local_position plugin). Guidance
needs world-frame velocities, so rotate the body twist by the odom orientation
before using it. Skipping this is harmless only while the vehicle holds yaw 0;
a target that yaws along its path otherwise always appears to fly "forward".
"""
import numpy as np


def body_to_world(q_xyzw, v):
    """Rotate body-frame vector ``v`` into the world frame by q = [x, y, z, w]."""
    qvec = np.asarray(q_xyzw[:3], dtype=float)
    qw = float(q_xyzw[3])
    v = np.asarray(v, dtype=float)
    t = 2.0 * np.cross(qvec, v)
    return v + qw * t + np.cross(qvec, t)


def odom_velocity_world(odom):
    """World-frame (ENU) linear velocity of a MAVROS ``local_position/odom``."""
    o = odom.pose.pose.orientation
    v = odom.twist.twist.linear
    return body_to_world([o.x, o.y, o.z, o.w], [v.x, v.y, v.z])
