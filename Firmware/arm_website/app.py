from flask import Flask, render_template, request
import ik
import angle_slider
import arrow_control

app = Flask(__name__)

#actual website page with the controls
@app.route('/')
def home():
    return render_template("website.html")


#this is where the sliders send their data to
@app.route('/command', methods= ["POST"])
def command():

    slider_data = request.json
    angle_slider.control_slider(slider_data)
    return "OK"


#this is where the ik coordinates send their data-
@app.route('/ik', methods= ["POST"])
def ik_route():

    ik_data = request.json
    j1, j2, j3, j4 = ik.control_arm(ik_data)

    return {
        "shoulder": j1,
        "elbow": j2,
        "wristPitch": j3,
        "base": j4
    }

@app.route('/arrow', methods= ["POST"])
def arrow_route():

    angles = request.json
    result = arrow_control.final_control(angles)

    if result is None:
        return {"error": "Arrow movement failed"}, 400

    j1, j2 = result

    return {
        "shoulder": j1,
        "elbow": j2,
    }


app.run(debug = True)