import socket
import json

ESP_IP = "192.168.4.113"
ESP_PORT = 5000

def control_slider(slider_data):
    base = slider_data["base"]
    shoulder = slider_data["shoulder"]
    elbow = slider_data["elbow"]
    wristPitch = slider_data["wristPitch"]
    wristRoll = slider_data["wristRoll"]
    gripper = slider_data["gripper"]

    base_gear, shoulder_gear, elbow_gear, wristPitch_angle, gripper_angle = gear_reduction(base, shoulder, elbow, wristPitch, gripper)

    esp_send(base_gear, shoulder_gear, elbow_gear, wristPitch_angle, wristRoll, gripper_angle, 0)

def gear_reduction(base, shoulder, elbow, wristPitch, gripper):
    base_gear = base * 4.217
    shoulder_gear = 270 - ((shoulder + 27) * 1.5)
    elbow_gear = (elbow + 170 + 5) * 1.75
    wristPitch_gear = wristPitch + 173
    gripper_angle = 270 - gripper
    return base_gear, shoulder_gear, elbow_gear, wristPitch_gear, gripper_angle

def esp_send(base, shoulder, elbow, wristPitch, wristRoll, gripper, esp_check):

    data = {
        "base": base,
        "shoulder": shoulder,
        "elbow": elbow,
        "wristPitch": wristPitch,
        "wristRoll": wristRoll,
        "gripper": gripper,
        "esp_check": esp_check
    }

    message = json.dumps(data)

    print("Sending to ESP32:")
    print(message)
    print("IP:", ESP_IP)
    print("Port:", ESP_PORT)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sock.sendto(message.encode(), (ESP_IP, ESP_PORT))

    sock.close()