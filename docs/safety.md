# Safety and limitations

This repository is an educational simulator, not a production robot stack.

- It does not control motors, actuators, PLCs, or physical robots.
- The grid and range sensors are idealized; they do not model noise, latency, localization error, dynamics, braking distance, or sensor failure.
- The pre-move obstacle check is a software demonstration only and is not safety-rated.
- The ROS 2 node publishes telemetry only and has no motion-command subscriber.
- Do not use this software as a substitute for a risk assessment, emergency-stop design, protective devices, or validated safety functions.
- Before adapting concepts to real equipment, involve qualified robotics and functional-safety engineers and test in a controlled environment.
