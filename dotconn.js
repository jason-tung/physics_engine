var svgns = "http://www.w3.org/2000/svg";
var c = document.getElementById("canvas");
var restart = document.getElementById("restart");
var go = document.getElementById("go");
var bighead = document.getElementById("bighead");
var info = document.getElementById("info");
var instr = document.getElementById("instr");
var pause = document.getElementById("pause");
var spec = document.getElementById("spec_inputs");
var circles = [];
var pointers = [];
var mode = "inelastic collisions";
var requestID;
var animating, xy, pointer;

var intervalId;

function getInfo(mode) {
    if (mode === "inelastic collisions") {
        instr.innerHTML = "Click and drag to create a ball with an initial velocity vector." +
            " The velocity vector is represented with an arrow," +
            " and each ball can have an individual mass determined by the input on the right." +
            " Click go to start/resume the simulation." +
            " The simulation can be paused and restarted at any time. " +
            "A graph on the right will appear after creating your first ball.";
        info.innerHTML = "This simulation is meant to demonstrate the properties of elastic point particles, " +
            "but for the sake of visibility, the points are instead VERY sticky balls!";
        spec.innerHTML = "mass(kg) <input type=\"number\" class=\"form-control\" id=\"mass\" value=\"20\">";

        var mass = document.getElementById("mass");
    }
}

getInfo(mode);
bighead.innerHTML = mode;

function getRandomColor() {
    var letters = '0123456789ABCDEF';
    var color = '#';
    for (var i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}

function updatevar(obj, v, v1, v2, modifier) {
    obj.setAttribute(v, String(Number(obj.getAttribute(v1)) + Number(obj.getAttribute(v2)) * modifier));
}

function getloc(circle) {
    return [circle.getAttribute("cx"), circle.getAttribute("cy")]
}

function getvel(circle) {
    return [circle.getAttribute("vx"), circle.getAttribute("vy")]
}

function circle(x, y) {
    var newcircle = document.createElementNS(svgns, 'circle');
    newcircle.setAttribute('fill', getRandomColor());
    newcircle.setAttribute('cx', x);
    newcircle.setAttribute('cy', y);
    newcircle.setAttribute('r', 20);
    newcircle.setAttribute('stroke', "black");
    // c.appendChild(newcircle);
    if (mode === "inelastic collisions") {
        newcircle.setAttribute('mass', mass.value ? mass.value : "10");
    }
    return newcircle;
}

function line(x1, y1, x2, y2) {
    var line = document.createElementNS(svgns, "line");
    line.setAttribute("x1", x1);
    line.setAttribute("y1", y1);
    line.setAttribute("x2", x2);
    line.setAttribute("y2", y2);
    line.setAttribute("stroke", "black");
    line.setAttribute("marker-end", "url(#triangle)");
    line.setAttribute("stroke-width", "3");
    // piline.appendlinehild(line);
    return line;
}

document.onmousemove = function (e) {
    var event = e || window.event;
    window.mouseX = event.offsetX;
    window.mouseY = event.offsetY;
};

c.addEventListener('mousedown', function (e) {
    // console.log("proc");
    if (mode === "inelastic collisions") {
        collision_mdown(e);
    }
});

c.addEventListener("mouseup", function () {
    clearInterval(intervalId);
});

restart.addEventListener('click', function () {
    collision_restart();
});

pause.addEventListener('click', function () {
    stopIt();
});

var stopIt = function () {
    // console.log("cancled");
    cancelAnimationFrame(requestID);
    animating = false;
};


go.addEventListener('click', function (e) {
    // console.log("go!");
    if (!animating) {
        animating = true;
        updateballs();
    }
});


// COLLISIONS

function collision_mdown(e) {
    if (!animating) {
        var in_circ = false;
        for (var i = 0; i < circles.length; i++) {
            in_circ |= Math.pow(circles[i].getAttribute('cx') - e.offsetX, 2) + Math.pow(circles[i].getAttribute('cy') - e.offsetY, 2) < 40 * 40;
        }
        if (!in_circ) {
            var newcircle = circle(e.offsetX, e.offsetY);
            circles.push(newcircle);
            c.append(newcircle);
            create_pointer(e);
            console.log(circles[circles.length-1]);
            chart_append(circles.length-1);
            if (intervalId) {
                clearInterval(intervalId);
            }
            intervalId = setInterval(update_pointer, 1 / 60 * 1000);
        }

    }
}

function collision_restart() {
    for (var i = 0; i < circles.length; i++) {
        circles[i].remove();
        pointers[i].remove()
    }
    circles = [];
    pointers = [];
    stopIt()
}

function update_pointer() {
    // console.log("procing");
    //  console.log(animating);
    if (!animating) {
        if (intervalId) {
            // console.log("proc");
            pointer = pointers[pointers.length - 1];
            pointer.setAttribute("x2", window.mouseX);
            pointer.setAttribute("y2", window.mouseY);
            var circ = circles[circles.length - 1];
            xy = getloc(circ);
            circ.setAttribute("vx", window.mouseX - xy[0]);
            circ.setAttribute("vy", window.mouseY - xy[1]);
        }
    }
    else {
        for (var i = 0; i < pointers.length; i++) {
            pointer = pointers[i];
            var circle = circles[i];
            xy = getloc(circle);
            pointer.setAttribute("x1", xy[0]);
            pointer.setAttribute("y1", xy[1]);
            pointer.setAttribute("x2", Number(xy[0]) + Number(circle.getAttribute("vx")));
            pointer.setAttribute("y2", Number(xy[1]) + Number(circle.getAttribute("vy")));
        }
    }
}

function create_pointer(e) {
    var circ = circles[circles.length - 1];
    xy = getloc(circ);
    var cx = xy[0];
    var cy = xy[1];
    var pointer = line(cx, cy, e.offsetX, e.offsetY);
    pointers.push(pointer);
    c.append(pointer);
    circ.setAttribute("vx", window.mouseX - xy[0]);
    circ.setAttribute("vy", window.mouseY - xy[1]);
}

function updateballs() {
    for (var i = 0; i < circles.length; i++) {
        var circ = circles[i];
        // console.log(circ);
        updatevar(circ, "cx", "cx", "vx", .02);
        updatevar(circ, "cy", "cy", "vy", .02);
        collision_detect(i);
        chart_update(i);
    }
    update_pointer();
    requestID = window.requestAnimationFrame(updateballs);
}

function collision_detect(j) {
    for (var i = 0; i < circles.length; i++) {
        if (i !== j) {
            // console.log("proc2");
            var xyj = getloc(circles[j]);
            var xyi = getloc(circles[i]);
            var vxyj = getvel(circles[j]);
            var vxyi = getvel(circles[i]);
            if (Math.pow(xyi[0] - xyj[0], 2) + Math.pow(xyi[1] - xyj[1], 2) <= 40 * 40) {
                var new_velcx = (vxyi[0] * Number(circles[i].getAttribute("mass")) + vxyj[0] * Number(circles[j].getAttribute("mass"))) / (Number(circles[i].getAttribute("mass")) + Number(circles[j].getAttribute("mass")));
                // console.log(new_velcx);
                var new_velcy = (vxyi[1] * Number(circles[i].getAttribute("mass")) + vxyj[1] * Number(circles[j].getAttribute("mass"))) / (Number(circles[i].getAttribute("mass")) + Number(circles[j].getAttribute("mass")));
                // console.log(new_velcy);
                circles[i].setAttribute("vx", new_velcx);
                circles[i].setAttribute("vy", new_velcy);
                circles[j].setAttribute("vx", new_velcx);
                circles[j].setAttribute("vy", new_velcy);
                // circles[j].remove();
                // circles.pop(j)
                // console.log(requestID);
            }
        }
    }
}
//
// <table class="table">
//   <thead>
//     <tr>
//       <th scope="col">#</th>
//       <th scope="col">x</th>
//       <th scope="col">y</th>
//       <th scope="col">m</th>
//       <th scope="col">vx</th>
//       <th scope="col">vy</th>
//       <th scope="col">p</th>
//       <th scope="col">KE</th>
//     </tr>
//   </thead>
//   <tbody>
//     <tr>
//       <th scope="row">1</th>
//       <td>Mark</td>
//       <td>Otto</td>
//       <td>@mdo</td>
//     </tr>
//   </tbody>
// </table>
var tbod = document.getElementById("tbod");

function chart_append(i){
    var circle = circles[i];
    var tr = document.createElement("tr");
    var th = document.createElement("th");
    th.innerHTML = i;
    var x = document.createElement("td");
    x.innerHTML = Number(circle.getAttribute("cx")).toFixed(2);
    x.setAttribute("id","cx"+i);
    var y = document.createElement("td");
    y.innerHTML = Number(circle.getAttribute("cy")).toFixed(2);
    y.setAttribute("id","cy"+i);
    var m = document.createElement("td");
    m.innerHTML = Number(circle.getAttribute("mass")).toFixed(2);
    m.setAttribute("id","m"+i);
    var vx = document.createElement("td");
    vx.innerHTML = Number(circle.getAttribute("vx")).toFixed(2);
    vx.setAttribute("id","vx"+i);
    var vy = document.createElement("td");
    vy.innerHTML = Number(circle.getAttribute("vy")).toFixed(2);
    vy.setAttribute("id","vy"+i);
    var p = document.createElement("td");
    p.setAttribute("id","p"+i);
    p.innerHTML = Number(Math.pow(Math.pow(Number(circle.getAttribute("vx")),2) + Math.pow(Number(circle.getAttribute("vy")),2),.5) * Number(circle.getAttribute("mass"))).toFixed(2);
    var KE = document.createElement("td");
    KE.innerHTML = Number(Math.pow(Number(circle.getAttribute("vx")),2) + Math.pow(Number(circle.getAttribute("vy")),2) / Number(circle.getAttribute("mass"))).toFixed(2);
    KE.setAttribute("id","ke"+i);
    tr.appendChild(th);
    tr.appendChild(x);
    tr.appendChild(y);
    tr.appendChild(m);
    tr.appendChild(vx);
    tr.appendChild(vy);
    tr.appendChild(p);
    tr.appendChild(KE);
    tbod.appendChild(tr);
}

function update_helper(i, type ){
    var circle = circles[i];
    // console.log(type+i);
    document.getElementById(type+i).innerHTML=Number(circle.getAttribute(type)).toFixed(2);
}

function chart_update(i){
    var circle = circles[i];
    circle.setAttribute("p",Number(Math.pow(Math.pow(Number(circle.getAttribute("vx")),2) + Math.pow(Number(circle.getAttribute("vy")),2),.5) * Number(circle.getAttribute("mass"))));
    circle.setAttribute("ke",Number(Math.pow(Number(circle.getAttribute("vx")),2) + Math.pow(Number(circle.getAttribute("vy")),2) / Number(circle.getAttribute("mass"))));
    var update_types = ["cx","cy","vx","vy","p","ke"];
    for (var j =0; j < update_types.length; j++){
        update_helper(i,update_types[j]);
    }
}

