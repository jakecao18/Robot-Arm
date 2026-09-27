//puts slider and input values into a variable
const base = document.getElementById("baseSlider");
const baseInput = document.getElementById("baseInput");

const shoulder = document.getElementById("shoulderSlider");
const shoulderInput = document.getElementById("shoulderInput");

const elbow = document.getElementById("elbowSlider");
const elbowInput = document.getElementById("elbowInput");

const wristPitch = document.getElementById("wristPitchSlider");
const wristPitchInput = document.getElementById("wristPitchInput");

const wristRoll = document.getElementById("wristRollSlider");
const wristRollInput = document.getElementById("wristRollInput");

const gripper = document.getElementById("gripperSlider");
const gripperInput = document.getElementById("gripperInput");

const xInput = document.getElementById("xInput");
const yInput = document.getElementById("yInput");
const zInput = document.getElementById("zInput");
const moveButton = document.getElementById("moveButton");

const upArrow = document.getElementById("upButton");
const downArrow = document.getElementById("downButton");
const rightArrow = document.getElementById("rightButton");
const leftArrow = document.getElementById("leftButton");

upArrow.addEventListener("click", function(){
    sendArrow(1, 0, 0, 0);
});

downArrow.addEventListener("click", function(){
    sendArrow(0, 1, 0, 0);
});

rightArrow.addEventListener("click", function(){
    sendArrow(0, 0, 0, 1);
});

leftArrow.addEventListener("click", function(){
    sendArrow(0, 0, 1, 0);
});

//sends the ik coordinates to /ik in app.py
moveButton.addEventListener("click", function(){

    const ik = {
        x: Number(xInput.value), 
        y: Number(yInput.value),
        z: Number(zInput.value)
    };

    fetch("/ik", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify(ik)

    })
    .then(response => response.json())
    .then(data => {

        // Update sliders
        base.value = data.base / 4.217;
        shoulder.value = ((data.shoulder - 270) / -1.5) - 27;
        elbow.value = (data.elbow / 1.75) - 170 - 5;
        wristPitch.value = data.wristPitch - 173;

        // Update input boxes
        baseInput.value = data.base / 4.217;
        shoulderInput.value = ((data.shoulder - 270) / -1.5) - 27;
        elbowInput.value = (data.elbow / 1.75) - 170 - 5;
        wristPitchInput.value = data.wristPitch - 173;

        // Update displayed values
        baseValue.textContent = data.base / 4.217 + "°";
        shoulderValue.textContent = ((data.shoulder - 270) / -1.5) - 27 + "°";
        elbowValue.textContent = (data.elbow / 1.75) - 170 - 5 + "°";
        wristPitchValue.textContent = data.wristPitch - 173 + "°";

    });

    xInput.value = 0;
    yInput.value = 0;
    zInput.value = 0;
    
});

//update base slider & input and sends data to /command in app.py
base.addEventListener("input", function() {
    baseInput.value = base.value
    baseValue.textContent = base.value + "°";
    sendCommand()
});
baseInput.addEventListener("input", function() {
    base.value = baseInput.value
    baseValue.textContent = baseInput.value + "°";
    sendCommand()
});

//update shoulder slider & input and sends data to /command in app.py
shoulder.addEventListener("input", function() {
    shoulderInput.value = shoulder.value
    shoulderValue.textContent = shoulder.value + "°";
    sendCommand()
});
shoulderInput.addEventListener("input", function() {
    shoulder.value = shoulderInput.value
    shoulderValue.textContent = shoulderInput.value + "°";
    sendCommand()
});

//update elbow slider & input and sends data to /command in app.py
elbow.addEventListener("input", function() {
    elbowInput.value = elbow.value
    elbowValue.textContent = elbow.value + "°";
    sendCommand()
});
elbowInput.addEventListener("input", function() {
    elbow.value = elbowInput.value
    elbowValue.textContent = elbowInput.value + "°";
    sendCommand()
});

//update wristPitch slider & input and sends data to /command in app.py
wristPitch.addEventListener("input", function() {
    wristPitchInput.value = wristPitch.value
    wristPitchValue.textContent = wristPitch.value + "°";
    sendCommand()
});
wristPitchInput.addEventListener("input", function() {
    wristPitch.value = wristPitchInput.value
    wristPitchValue.textContent = wristPitchInput.value + "°";
    sendCommand()
});

//update wristRoll slider & input and sends data to /command in app.py
wristRoll.addEventListener("input", function() {
    wristRollInput.value = wristRoll.value
    wristRollValue.textContent = wristRoll.value + "°";
    sendCommand()
});
wristRollInput.addEventListener("input", function() {
    wristRoll.value = wristRollInput.value
    wristRollValue.textContent = wristRollInput.value + "°";
    sendCommand()
});

//update gripper slider & input and sends data to /command in app.py
gripper.addEventListener("input", function() {
    gripperInput.value = gripper.value
    gripperValue.textContent = gripper.value + "°";
    sendCommand()
});
gripperInput.addEventListener("input", function() {
    gripper.value = gripperInput.value
    gripperValue.textContent = gripperInput.value + "°";
    sendCommand()
});


//function that sends data to /arrow in app.py
function sendArrow(up, down, left, right){

    const command = {
        theta_1: Number(shoulder.value),
        theta_2: Number(elbow.value),
        upArrow: up,
        downArrow: down,
        leftArrow: left,
        rightArrow: right
    };

    fetch("/arrow", {
        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify(command)
    })
    .then(response => response.json())
    .then(data => {

        // Convert Python IK angles back to your slider angles
        const newShoulder = data.shoulder;
        const newElbow = data.elbow;

        // Update sliders
        shoulder.value = newShoulder;
        elbow.value = newElbow;

        // Update number inputs
        shoulderInput.value = newShoulder;
        elbowInput.value = newElbow;

        // Update displayed values
        shoulderValue.textContent = newShoulder + "°";
        elbowValue.textContent = newElbow + "°";
    });
}


//function that sends data to /command in app.py
function sendCommand(){

    const command = {

        base: Number(base.value),
        shoulder: Number(shoulder.value),
        elbow: Number(elbow.value),
        wristPitch: Number(wristPitch.value),
        wristRoll: Number(wristRoll.value),
        gripper: Number(gripper.value)
        
    };

    fetch("/command", {

        method:"POST",

        headers:{
            "Content-Type":"application/json"
        },

        body:JSON.stringify(command)

    });

}
