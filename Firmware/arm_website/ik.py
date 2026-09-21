import math
import socket
import json
import time

ESP_IP = "192.168.4.113"
ESP_PORT = 5000

def control_arm(ik_data):

    x = float(ik_data["x"])
    y = float(ik_data["y"])
    z = float(ik_data["z"])

    result = final_ik(x, y, z)

    if result is not None:
        theta_1, theta_2, theta_3, theta_4 = result
        theta_1gear = 270 - ((theta_1 + 27 + 10) * 1.5)
        theta_2gear = (theta_2 + 170) * 1.75
        theta_3gear = theta_3 + 173
        theta_4gear = theta_4 * 4.217
        esp_send(67.5, 0, 270, 0, 1)

        time.sleep(7)

        esp_send(theta_1gear, theta_2gear, theta_3gear, theta_4gear, 1)

        return theta_1gear, theta_2gear, theta_3gear, theta_4gear

#function that determines wether the joint angles are within limits or not
def joint_limits(theta_1, theta_2, theta_3, theta_4):

    theta_1max = 90.5
    theta_1min = -37.5

    theta_2max = -15
    theta_2min = -180

    theta_3max = 90
    theta_3min = -140

    if theta_1 > theta_1max or theta_1 < theta_1min:
        return False
    elif theta_2 > theta_2max or theta_2 < theta_2min:
        return False
    elif theta_3 > theta_3max or theta_3 < theta_3min:
        return False
    else:
        return True


#finds and adjusts the angles so that joints are within limits
#depending on the x & y (gripper position), a & b are also different 
def final_ik(x, y, z):
    #trying to increase phi 
    for phi in range(-90, -180, -1):
        result = calculate_ik(x, y, z, phi)

        if result is not None and joint_limits(*result):
            print(result, phi)
            return result

    #trying to decrease phi
    for phi in range(-89, 0):
        result = calculate_ik(x, y, z, phi)

        if result is not None and joint_limits(*result):
            print(result, phi)
            return result

    #no valid solution 
    print("coordinate outside reach or invalid angles")
    return None


def calculate_ik(x, y, z, phi):
    try:
        # declare link lengths
        l1 = 217.5
        l2 = 180.5
        l3 = 161.5

        #the arm actually starts at x = 21, y = 124.1 so minus that to make it x = 0, y = 0
        x_2d = x - 21
        y_2d = y - 124.1

        #convert x_2d into correct 3d x
        x_3d = math.sqrt((x_2d * x_2d) + (z * z))
        theta_4 = math.atan2(z, x)

        # convert phi to radians because the trig functions are set to radians by default
        phi_radians = math.radians(phi)
        a = x_3d - (l3 * math.cos(phi_radians))
        b = y_2d - (l3 * math.sin(phi_radians))
        #also finding c for law of cosines
        c = (math.sqrt((a * a) + (b * b)))

        #finding theta 2 internal angle, C in the law of cosines
        #find theta 1, split into 2 angles
        theta_2 = (math.acos(((l1 * l1) + (l2 * l2) - (c * c)) / (2 * l1 * l2)))

        alpha = math.degrees(math.atan2(b, a))
        beta = math.degrees(math.acos(((l1 * l1) + (c * c) - (l2 * l2)) / (2 * l1 * c)))

        #convert everything to angles since they are in radians by default
        theta_1DEG = alpha + beta
        theta_2DEG = (math.degrees(theta_2)) - 180
        theta_3DEG = phi - (theta_1DEG + theta_2DEG)
        theta_4DEG = math.degrees(theta_4)

        print(x_3d, y_2d, a, b)

        return theta_1DEG, theta_2DEG, theta_3DEG, theta_4DEG

    except Exception as e:
            print("IK Error:", e)
            return None




#function that sends data to esp32 via udp socket
def esp_send(theta_1, theta_2, theta_3, theta_4, esp_check):

    data = {
        "base": theta_4,
        "shoulder": theta_1,
        "elbow": theta_2,
        "wristPitch": theta_3,
        "esp_check": esp_check
    }

    message = json.dumps(data)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sock.sendto(message.encode(), (ESP_IP, ESP_PORT))

    sock.close()