import anime from '/static/js/anime.es.js';

const svgns = "http://www.w3.org/2000/svg";
let svg = document.querySelector('svg');
let pt = svg.createSVGPoint();
let is_player_turn = true
window.onload = init;
window.onresize = setSize;


let animation = function (target, y_index) {
    anime({
        targets: target,
        translateY: get_y_center(y_index) - 10,
        borderRadius: 50,
        duration: 80 * y_index + 80,
        easing: 'linear',
        direction: 'normal',
    });
};

function setSize() {
    if (svg.clientHeight > window.innerHeight * 0.9) {
        if (window.innerHeight <= window.innerWidth) {
            svg.style.height = window.innerHeight * 0.7 + "px";
            svg.style.width = svg.clientHeight + "px";
        } else {
            svg.style.width = window.innerWidth * 0.7 + "px";
            svg.style.height = svg.clientWidth + "px";
        }
    } else {
        if (window.innerHeight > window.innerWidth) {
            svg.style.width = window.innerWidth * 0.7 + "px";
            svg.style.height = svg.clientWidth + "px";
        } else {
            svg.style.height = window.innerHeight * 0.7 + "px";
            svg.style.width = svg.clientHeight + "px";
        }
    }
}

function init() {
    setSize();
    draw_chessboard();
}

function draw_chessboard() {
    function draw_line(x1, y1, x2, y2) {
        let line = document.createElementNS(svgns, 'line');
        line.setAttributeNS(null, 'id', 'line');
        line.setAttributeNS(null, 'x1', x1);
        line.setAttributeNS(null, 'y1', y1);
        line.setAttributeNS(null, 'x2', x2);
        line.setAttributeNS(null, 'y2', y2);
        svg.appendChild(line);
    }

    let r = 12;
    let x1 = (100 - 7 * r) / 2;
    let y1 = x1 + r;
    for (let i = 0; i < 7; i++) {
        draw_line(x1, y1 + i * r, 100 - x1, y1 + i * r);
    }
    for (let i = 0; i < 8; i++) {
        draw_line(x1 + i * r, y1, x1 + i * r, 100 - x1);
    }
}

function cursorPoint(evt) {
    pt.x = evt.clientX;
    pt.y = evt.clientY;
    return pt.matrixTransform(svg.getScreenCTM().inverse());
}

function get_x_index(loc) {
    let i = Math.floor((loc.x - 8) / 12);
    if (i < 0) i = 0;
    else if (i > 6) i = 6;
    return i;
}

function get_x_center(index) {
    return 8 + index * 12 + 6;
}

function get_y_center(index) {
    return 20 + index * 12 + 6;
}

function put_chess(x_index, y_index) {
    let color = 'red_disc';
    let circle = document.createElementNS(svgns, 'circle');
    circle.setAttributeNS(null, 'id', color);
    circle.setAttributeNS(null, 'cx', get_x_center(x_index));
    circle.setAttributeNS(null, 'cy', 10);
    circle.setAttributeNS(null, 'r', "5");
    svg.appendChild(circle);
    animation(circle, y_index);
}

function clr_tmp() {
    if (document.getElementById('tmp_red_disc')) {
        document.getElementById('tmp_red_disc').remove();
    }
    if (document.getElementById('tmp_yellow_disc')) {
        document.getElementById('tmp_yellow_disc').remove();
    }
}

svg.addEventListener('mousemove', function (evt) {
    let loc = cursorPoint(evt);
    if (is_player_turn) {
        clr_tmp();
        let circle = document.createElementNS(svgns, 'circle');
        circle.setAttributeNS(null, 'id', 'tmp_red_disc');
        circle.setAttributeNS(null, 'cx', get_x_center(get_x_index(loc)));
        circle.setAttributeNS(null, 'cy', 10);
        circle.setAttributeNS(null, 'r', "5");
        svg.appendChild(circle);
    }
}, false);

svg.addEventListener('click', function (evt) {
    let loc = cursorPoint(evt);
    if (is_player_turn) {
        clr_tmp();
        put_chess(get_x_index(loc), 5);
        is_player_turn = false;
    }
}, false);