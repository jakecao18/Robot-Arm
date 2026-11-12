import math
import socket
import json

ESP_IP = "192.168.4.58"
ESP_PORT = 5000

def final_control(angles):

    theta_1 = float(angles["theta_1"])
    theta_2 = float(angles["theta_2"])
    theta_3 = float(angles["theta_3"])

    upArrow = int(angles["upArrow"])
    downArrow = int(angles["downArrow"])
    leftArrow = int(angles["leftArrow"])
    rightArrow = int(angles["rightArrow"])

    x, y = find_ee(theta_1, theta_2, theta_3)

    phi = theta_1 + theta_2 + theta_3

    result = move_ee(x, y, phi, upArrow, downArrow, leftArrow, rightArrow)

    if result is not None:
        j1, j2, j3 = result

        theta_1gear = 270 - ((j1 + 27 + 10) * 1.5)
        theta_2gear = (j2 + 180) * 1.75
        theta_3gear = j3 + 180

        print(j1, j2, j3)
        
        esp_send(theta_1gear, theta_2gear, theta_3gear, 2)

        return j1, j2, j3

def find_ee(theta1, theta2, theta3):
    l1 = 217.5
    l2 = 180.5
    l3 = 161.5

    x = ((l1 * math.cos(math.radians(theta1))) + (l2 * math.cos(math.radians(theta1 + theta2))) + (l3 * math.cos(math.radians(theta1 + theta2 + theta3))))
    y = ((l1 * math.sin(math.radians(theta1))) + (l2 * math.sin(math.radians(theta1 + theta2))) + (l3 * math.sin(math.radians(theta1 + theta2 + theta3))))

    return x, y


def move_ee(x_old, y_old, phi, upArrow, downArrow, leftArrow, rightArrow):
    try:
        if upArrow == 1:
            x = x_old 
            y = y_old + 10

        elif downArrow == 1:
            x = x_old
            y = y_old - 10  

        elif leftArrow == 1:
            x = x_old - 10
            y = y_old

        elif rightArrow == 1:
            x = x_old + 10
            y = y_old

        l1 = 217.5
        l2 = 180.5
        l3 = 161.5

        # convert phi to radians because the trig functions are set to radians by default
        phi_radians = math.radians(phi)
        a = x - (l3 * math.cos(phi_radians))
        b = y - (l3 * math.sin(phi_radians)) 

        c = (math.sqrt((a * a) + (b * b)))

        if c > l1 + l2:
            print("Target is too far away:", c + l3, "mm")
            return None

        if c < abs(l1 - l2):
            print("Target is too close:", c + l3, "mm")
            return None

        theta_2 = (math.acos(((l1 * l1) + (l2 * l2) - (c * c)) / (2 * l1 * l2)))
        
        alpha = math.degrees(math.atan2(b, a))
        beta = math.degrees(math.acos(((l1 * l1) + (c * c) - (l2 * l2)) / (2 * l1 * c)))
        
        #convert everything to angles since they are in radians by default
        theta_1DEG = alpha + beta
        theta_2DEG = (math.degrees(theta_2)) - 180
        theta_3DEG = phi - (theta_1DEG + theta_2DEG)

        return theta_1DEG, theta_2DEG, theta_3DEG

    except Exception as e:
        print("error", e)


def esp_send(theta_1, theta_2, theta_3, esp_check):

    data = {
        "shoulder": theta_1,
        "elbow": theta_2,
        "wristPitch": theta_3,
        "esp_check": esp_check
    }

    message = json.dumps(data)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sock.sendto(message.encode(), (ESP_IP, ESP_PORT))

    sock.close()