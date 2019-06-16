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
var apointers = [];
var mode = "inelastic collisions";
var requestID;
var mass;
var g;

var animating, xy, pointer;

var intervalId;

function getInfo(mode) {
    var thead = document.getElementById("thead");
    if (mode === "inelastic collisions") {
        instr.innerHTML = "Click and drag to create a ball with an initial velocity vector." +
            " The velocity vector is represented with an arrow," +
            " and each ball can have an individual mass determined by the input on the right." +
            " Click go to start/resume the simulation." +
            " The simulation can be paused and restarted at any time. " +
            "A table on the right will appear after creating your first ball.";
        info.innerHTML = "This simulation is meant to demonstrate the properties of perfectly inelastic point particles, " +
            "but for the sake of visibility, the points are instead VERY sticky balls!";
        spec.innerHTML = "";
        thead.innerHTML = "<th scope=\"col\">#</th>\n" +
            "                    <th scope=\"col\">x</th>\n" +
            "                    <th scope=\"col\">y</th>\n" +
            "                    <th scope=\"col\">m</th>\n" +
            "                    <th scope=\"col\">vx</th>\n" +
            "                    <th scope=\"col\">vy</th>\n" +
            "                    <th scope=\"col\">p</th>\n" +
            "                    <th scope=\"col\">KE</th>"
    }
    else if (mode === "gravity") {
        instr.innerHTML = "Click and drag to create a ball with an initial velocity vector." +
            " The velocity vector is represented with an arrow," +
            " and each ball can have an individual mass determined by the input on the right." +
            " There is also an input that will affect the gravitational constant" +
            " Click go to start/resume the simulation." +
            " The simulation can be paused and restarted at any time. " +
            "A table on the right will appear after creating your first ball. Note that the objects have to be pretty close to demonstrate visible gravity, as this is how gravity works...";
        info.innerHTML = "This simulation demonstrates gravity between two strange... objects. After two objects collide, they become immovable";
        spec.innerHTML = "G(10^13 Nm^2/kg^2) <input type=\"number\" class=\"form-control mt-2\" id=\"g\" value=\"5\">";
        g = document.getElementById("g");
        thead.innerHTML = "<th scope=\"col\">#</th>\n" +
            "                    <th scope=\"col\">x</th>\n" +
            "                    <th scope=\"col\">y</th>\n" +
            "                    <th scope=\"col\">m</th>\n" +
            "                    <th scope=\"col\">vx</th>\n" +
            "                    <th scope=\"col\">vy</th>\n" +
            "                    <th scope=\"col\">ax</th>\n" +
            "                    <th scope=\"col\">ay</th>"
    }
    mass = document.getElementById("mass");
}


var dropdown = document.getElementById("dropdown");
dropdown.addEventListener('change', function () {
    mode = dropdown.options[dropdown.selectedIndex].value;
    collision_restart();
    getInfo(mode);
    bighead.innerHTML = mode;
});


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
    return [Number(circle.getAttribute("cx")), Number(circle.getAttribute("cy"))]
}

function getvel(circle) {
    return [Number(circle.getAttribute("vx")), Number(circle.getAttribute("vy"))]
}

function getaccel(circle) {
    return [Number(circle.getAttribute("ax")), Number(circle.getAttribute("ay"))]
}

function circle(x, y) {
    var newcircle = document.createElementNS(svgns, 'circle');
    newcircle.setAttribute('fill', getRandomColor());
    newcircle.setAttribute('cx', x);
    newcircle.setAttribute('cy', y);
    newcircle.setAttribute('ax', "0");
    newcircle.setAttribute('ay', "0");
    newcircle.setAttribute('r', "20");
    newcircle.setAttribute('stroke', "black");
    // c.appendChild(newcircle);
    newcircle.setAttribute('mass', mass.value ? mass.value : "10");
    return newcircle;
}

function collision_restart() {
    for (var i = 0; i < circles.length; i++) {
        circles[i].remove();
        pointers[i].remove();
    }
    for (i = 0; i < apointers.length; i++) {
        apointers[i].remove();
    }
    circles = [];
    pointers = [];
    apointers = [];
    tbod.innerHTML = "";
    stopIt();
}

function line(x1, y1, x2, y2, c) {
    var line = document.createElementNS(svgns, "line");
    line.setAttribute("x1", x1);
    line.setAttribute("y1", y1);
    line.setAttribute("x2", x2);
    line.setAttribute("y2", y2);
    line.setAttribute("stroke", c);
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
    collision_mdown(e);
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


go.addEventListener('click', function () {
    // console.log("go!");
    if (!animating) {
        animating = true;
        // console.log(mode);
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
            if (mode === "gravity") {
                create_apointer();
                for (i = 0; i < circles.length; i++) {
                    update_gravity(i);
                }
                update_apointers();
            }
            // console.log(circles[circles.length - 1]);
            chart_append(circles.length - 1);
            if (intervalId) {
                clearInterval(intervalId);
            }
            intervalId = setInterval(update_pointer, 1 / 60 * 1000);
        }

    }
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

function update_apointers() {
    for (var i = 0; i < apointers.length; i++) {
        pointer = apointers[i];
        var circle = circles[i];
        var xy = getloc(circle);
        pointer.setAttribute("x1", xy[0]);
        pointer.setAttribute("y1", xy[1]);
        pointer.setAttribute("x2", Number(xy[0]) + 5 * Number(circle.getAttribute("ax")));
        pointer.setAttribute("y2", Number(xy[1]) + 5 * Number(circle.getAttribute("ay")));
    }
}

function create_pointer(e) {
    var circ = circles[circles.length - 1];
    xy = getloc(circ);
    var cx = xy[0];
    var cy = xy[1];
    var pointer = line(cx, cy, e.offsetX, e.offsetY, "black");
    pointers.push(pointer);
    c.append(pointer);
    circ.setAttribute("vx", window.mouseX - xy[0]);
    circ.setAttribute("vy", window.mouseY - xy[1]);
}

function create_apointer() {
    var circ = circles[circles.length - 1];
    xy = getloc(circ);
    var a = getaccel(circ);
    // console.log(a);
    var cx = xy[0];
    var cy = xy[1];
    var apointer = line(cx, cy, cx + a[0], cy + a[1], "red");
    // console.log(apointer);
    apointers.push(apointer);
    c.append(apointer);
}

function updateballs() {
    for (var i = 0; i < circles.length; i++) {
        var circ = circles[i];
        // console.log(circ);
        updatevar(circ, "cx", "cx", "vx", .02);
        updatevar(circ, "cy", "cy", "vy", .02);
        updatevar(circ, "vx", "vx", "ax", 1);
        updatevar(circ, "vy", "vy", "ay", 1);
        var gravcol = false;
        if (mode === "gravity") {
            update_gravity(i);
            gravcol = gravity_collision(i);
        }
        else {
            collision_detect(i);
        }
        chart_update(i);
    }
    update_pointer();
    update_apointers();
    requestID = window.requestAnimationFrame(updateballs);
}

function collision_detect(j) {
    for (var i = 0; i < circles.length; i++) {
        if (i !== j) {
            // console.log("proc2");
            var xyj = getloc(circles[j]);
            var xyi = getloc(circles[i]);
            if (Math.pow(xyi[0] - xyj[0], 2) + Math.pow(xyi[1] - xyj[1], 2) <= 40 * 40) {
                var vxyj = getvel(circles[j]);
                var vxyi = getvel(circles[i]);
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

function rm(i) {
    // circles[i].setAttribute("cx", 0);
    // circles[i].setAttribute("cy", 0);
    circles[i].setAttribute("vx", 0);
    circles[i].setAttribute("vy", 0);
    // circles[i].setAttribute("mass", 0);
    circles[i].setAttribute("ax", 0);
    circles[i].setAttribute("ay", 0);
    // circles[i].setAttribute("fill", "white");
    // circles[i].setAttribute("display", "none");
    // pointers[i].setAttribute("display", "none");
    // apointers[i].setAttribute("display", "none");

}


function gravity_collision(i) {
    for (var j = 0; j < circles.length; j++) {
        if (i !== j) {
            // console.log("proc2");
            var xyj = getloc(circles[j]);
            var xyi = getloc(circles[i]);
            if (Math.pow(xyi[0] - xyj[0], 2) + Math.pow(xyi[1] - xyj[1], 2) <= 40 * 40) {
                rm(i);
                rm(j);
                return true;
            }
        }
    }
    return false;
}

function getg() {
    return g.value * Math.pow(10, 13)
}

function update_gravity(i) {
    var net_ax = 0;
    var net_ay = 0;
    for (var j = 0; j < circles.length; j++) {
        if (i !== j) {
            var xyj = getloc(circles[j]);
            var xyi = getloc(circles[i]);
            var dx = xyi[0] - xyj[0];
            var dy = xyi[1] - xyj[1];
            var theta = Math.atan(dy / dx) + (dx < 0 ? 0 : Math.PI);
            var d = Math.pow(dx * dx + dy * dy, 2);
            var magnitude = getg() * circles[i].getAttribute('mass') * circles[j].getAttribute('mass') / (d * d);
            // console.log(magnitude);
            var this_ax = magnitude * Math.cos(theta);
            var this_ay = magnitude * Math.sin(theta);
            net_ax += this_ax;
            net_ay += this_ay;
        }
    }
    // console.log(net_ax);
    // console.log(net_ay);
    circles[i].setAttribute("ax", net_ax);
    circles[i].setAttribute("ay", net_ay);
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

function chart_append(i) {
    var circle = circles[i];
    var tr = document.createElement("tr");
    var th = document.createElement("th");
    th.innerHTML = i;
    var x = document.createElement("td");
    x.innerHTML = Number(circle.getAttribute("cx")).toFixed(2);
    x.setAttribute("id", "cx" + i);
    var y = document.createElement("td");
    y.innerHTML = Number(circle.getAttribute("cy")).toFixed(2);
    y.setAttribute("id", "cy" + i);
    var m = document.createElement("td");
    m.innerHTML = Number(circle.getAttribute("mass")).toFixed(2);
    m.setAttribute("id", "m" + i);
    var vx = document.createElement("td");
    vx.innerHTML = Number(circle.getAttribute("vx")).toFixed(2);
    vx.setAttribute("id", "vx" + i);
    var vy = document.createElement("td");
    vy.innerHTML = Number(circle.getAttribute("vy")).toFixed(2);
    vy.setAttribute("id", "vy" + i);
    tr.appendChild(th);
    tr.appendChild(x);
    tr.appendChild(y);
    tr.appendChild(m);
    tr.appendChild(vx);
    tr.appendChild(vy);
    if (mode === "inelastic collisions") {
        var p = document.createElement("td");
        p.setAttribute("id", "p" + i);
        p.innerHTML = Number(Math.pow(Math.pow(Number(circle.getAttribute("vx")), 2) + Math.pow(Number(circle.getAttribute("vy")), 2), .5) * Number(circle.getAttribute("mass"))).toFixed(2);
        var KE = document.createElement("td");
        KE.innerHTML = Number(Math.pow(Number(circle.getAttribute("vx")), 2) + Math.pow(Number(circle.getAttribute("vy")), 2) / Number(circle.getAttribute("mass"))).toFixed(2);
        KE.setAttribute("id", "ke" + i);
        tr.appendChild(p);
        tr.appendChild(KE);
    }
    else {
        var ax = document.createElement("td");
        ax.innerHTML = Number(circle.getAttribute("ax")).toFixed(2);
        ax.setAttribute("id", "ax" + i);
        var ay = document.createElement("td");
        ay.innerHTML = Number(circle.getAttribute("ay")).toFixed(2);
        ay.setAttribute("id", "ay" + i);
        tr.appendChild(ax);
        tr.appendChild(ay);
    }
    tbod.appendChild(tr);
}

function update_helper(i, type) {
    var circle = circles[i];
    // console.log(type + i);
    document.getElementById(type + i).innerHTML = Number(circle.getAttribute(type)).toFixed(2);
}

function chart_update(i) {
    var circle = circles[i];
    circle.setAttribute("p", Number(Math.pow(Math.pow(Number(circle.getAttribute("vx")), 2) + Math.pow(Number(circle.getAttribute("vy")), 2), .5) * Number(circle.getAttribute("mass"))));
    circle.setAttribute("ke", Number(Math.pow(Number(circle.getAttribute("vx")), 2) + Math.pow(Number(circle.getAttribute("vy")), 2) / Number(circle.getAttribute("mass"))));
    var update_types;
    if (mode === "inelastic collisions") {
        update_types = ["cx", "cy", "vx", "vy", "p", "ke"];
    }
    else {
        update_types = ["cx", "cy", "vx", "vy", "ax", "ay"];
    }
    for (var j = 0; j < update_types.length; j++) {
        update_helper(i, update_types[j]);
    }
}

