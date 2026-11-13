# Portfolio copy

## LinkedIn project description (English)

**ROS 2 Warehouse Robot Simulator | Python, ROS 2, Robotics Simulation**

Built a small warehouse-robot simulation to explore autonomous navigation and task execution. The Python simulator uses a grid-based world, simulated range sensors, and breadth-first search to plan paths to pickup and drop-off waypoints. It replans as the map changes and emits timestamped JSON telemetry. I also added an optional ROS 2 (`rclpy`) node that publishes simulation state on `/warehouse/telemetry`, plus unit tests and architecture/safety documentation.

This is an educational simulation; it does not control physical robot hardware or provide safety-rated functions.

**Technologies:** Python, ROS 2, `rclpy`, BFS, JSON Lines, `unittest`.

Project: https://github.com/jiji456/ros2-warehouse-robot-simulator

## Résumé bullet (English)

- Developed a Python warehouse-robot simulator with BFS navigation, pickup/drop-off task execution, simulated range sensing, dynamic obstacle replanning, JSON telemetry, and an optional ROS 2 publisher; added unit tests and safety-focused documentation.

## คำอธิบายสำหรับ LinkedIn (ภาษาไทย)

**ROS 2 Warehouse Robot Simulator | Python, ROS 2, Robotics Simulation**

พัฒนาโปรแกรมจำลองหุ่นยนต์ขนส่งสินค้าในคลังสินค้า เพื่อสาธิตแนวคิดการนำทางอัตโนมัติและการทำงานตามภารกิจ ใช้ Python จำลองแผนที่แบบ grid และเซนเซอร์ระยะอย่างง่าย พร้อมอัลกอริทึม BFS สำหรับหาเส้นทางไปยังจุดรับและจุดส่งสินค้า ระบบคำนวณเส้นทางใหม่เมื่อแผนที่เปลี่ยน และสร้าง telemetry ในรูปแบบ JSON นอกจากนี้ยังมี ROS 2 (`rclpy`) node สำหรับเผยแพร่สถานะจำลองผ่าน topic `/warehouse/telemetry` พร้อม unit tests และเอกสารด้านสถาปัตยกรรมและข้อจำกัดด้านความปลอดภัย

เป็นโปรเจกต์เพื่อการเรียนรู้และสาธิตเท่านั้น ไม่ได้ควบคุมหุ่นยนต์จริงหรือทำหน้าที่ด้านความปลอดภัยที่ผ่านการรับรอง

**เทคโนโลยี:** Python, ROS 2, `rclpy`, BFS, JSON Lines, `unittest`

โปรเจกต์: https://github.com/jiji456/ros2-warehouse-robot-simulator

## Résumé bullet (ภาษาไทย)

- พัฒนาโปรแกรมจำลองหุ่นยนต์คลังสินค้าด้วย Python รองรับการหาเส้นทางด้วย BFS การทำงานตามจุดรับ–ส่ง การจำลองเซนเซอร์ การคำนวณเส้นทางใหม่เมื่อมีสิ่งกีดขวาง และ telemetry แบบ JSON พร้อม ROS 2 publisher, unit tests และเอกสารด้านความปลอดภัย
