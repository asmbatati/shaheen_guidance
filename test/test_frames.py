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

"""Unit tests for the MAVROS odometry frame helpers."""
import math

import numpy as np

from shaheen_guidance.frames import body_to_world


def _yaw_quat(yaw):
    return [0.0, 0.0, math.sin(yaw / 2.0), math.cos(yaw / 2.0)]


def test_identity_rotation_keeps_vector():
    v = [1.0, -2.0, 0.5]
    assert np.allclose(body_to_world([0.0, 0.0, 0.0, 1.0], v), v)


def test_yaw_90_maps_body_forward_to_world_north():
    # nose pointing north (ENU yaw +90 deg): body +x is world +y
    assert np.allclose(body_to_world(_yaw_quat(math.pi / 2), [2.0, 0.0, 0.0]),
                       [0.0, 2.0, 0.0], atol=1e-9)


def test_rotation_preserves_speed():
    q = _yaw_quat(1.234)
    v = np.array([3.0, -1.0, 0.7])
    assert math.isclose(np.linalg.norm(body_to_world(q, v)), np.linalg.norm(v))
