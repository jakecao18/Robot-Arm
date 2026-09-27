import math
import socket
import json

ESP_IP = "192.168.4.113"
ESP_PORT = 5000

def final_control(angles):

    theta_1 = float(angles["theta_1"])
    theta_2 = float(angles["theta_2"])

    upArrow = int(angles["upArrow"])
    downArrow = int(angles["downArrow"])
    leftArrow = int(angles["leftArrow"])
    rightArrow = int(angles["rightArrow"])

    x, y = find_ee(theta_1, theta_2)

    result = move_ee(x, y, upArrow, downArrow, leftArrow, rightArrow)

    if result is not None:
        j1, j2 = result

        theta_1gear = 270 - ((j1 + 27 + 10) * 1.5)
        theta_2gear = (j2 + 170) * 1.75

        print(j1, j2)
        
        esp_send(theta_1gear, theta_2gear, 1)

        return j1, j2

def find_ee(theta1, theta2):
    l1 = 217.5
    l2 = 180.5

    x = l1 * math.cos(math.radians(theta1)) + l2 * math.cos(math.radians(theta1 + theta2))
    y = l1 * math.sin(math.radians(theta1)) + l2 * math.sin(math.radians(theta1 + theta2))

    return x, y


def move_ee(a, b, upArrow, downArrow, leftArrow, rightArrow):
    try:
        if upArrow == 1:
            x = a 
            y = b + 10

        elif downArrow == 1:
            x = a 
            y = b - 10  

        elif leftArrow == 1:
            x = a - 10
            y = b  

        elif rightArrow == 1:
            x = a + 10
            y = b   

        l1 = 217.5
        l2 = 180.5

        c = (math.sqrt((x * x) + (y * y)))

        if c > l1 + l2:
            print("Target is too far away:", c, "mm")
            return None

        if c < abs(l1 - l2):
            print("Target is too close:", c, "mm")
            return None

        theta_2 = (math.acos(((l1 * l1) + (l2 * l2) - (c * c)) / (2 * l1 * l2)))
        
        alpha = math.degrees(math.atan2(y, x))
        beta = math.degrees(math.acos(((l1 * l1) + (c * c) - (l2 * l2)) / (2 * l1 * c)))
        
        #convert everything to angles since they are in radians by default
        theta_1DEG = alpha + beta
        theta_2DEG = (math.degrees(theta_2)) - 180

        return theta_1DEG, theta_2DEG

    except Exception as e:
        print("error", e)


def esp_send(theta_1, theta_2, esp_check):

    data = {
        "shoulder": theta_1,
        "elbow": theta_2,
        "esp_check": esp_check
    }

    message = json.dumps(data)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sock.sendto(message.encode(), (ESP_IP, ESP_PORT))

    sock.close()