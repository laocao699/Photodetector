# Copyright 2016 Devsim LLC
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

import sys
Vb=float(sys.argv[1])
# 可选第 2 参数: Vc 扫描的相对误差容差(默认 1e-3, 行为与原脚本完全一致)。
# Vb=0.1 处于近截止离态, 电流为纯数值噪声(~1e-12 A), 用默认 1e-3 会触发
# "Min step size too small"; 需放宽到 1e-2 才能扫完(见 REPORT_phase1_3.md §3.3)。
rel_error=float(sys.argv[2]) if len(sys.argv) > 2 else 1e-3

import bjt_common
bjt_common.run()

from physics.ramp2 import *
rampvoltage("bjt", "Vb", 0.0, Vb, 0.1, 0.001, 40, 1e-2, 1e6, bjt_common.make_bias("base"))
rampvoltage("bjt", "Vc", 0.0, 1.5, 0.1, 0.0001, 10, rel_error, 1e6, bjt_common.make_sweep(("base", "collector", "emitter"), ("Vb", "Vc", "Ve")))

