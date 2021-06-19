const svgns = "http://www.w3.org/2000/svg";
let svg = document.querySelector('svg');
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
window.onload = init;
window.onresize = setSize;

let Setting = {
    mode: 'ai',
    turn: 0,
    player: {'com': 'o', 'player': 'x'},
    difficulty: 5,
    is_player_turn: true,
    ai_first: false,
    board: {
        0: '', 1: '', 2: '', 3: '', 4: '', 5: '', 6: '',
        10: '', 11: '', 12: '', 13: '', 14: '', 15: '', 16: '',
        20: '', 21: '', 22: '', 23: '', 24: '', 25: '', 26: '',
        30: '', 31: '', 32: '', 33: '', 34: '', 35: '', 36: '',
        40: '', 41: '', 42: '', 43: '', 44: '', 45: '', 46: '',
        50: '', 51: '', 52: '', 53: '', 54: '', 55: '', 56: '',
    },
    legal_moves: [0, 1, 2, 3, 4, 5, 6],
}

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
    svg.focus();
}

function cursorPoint(evt) {
    let pt = svg.createSVGPoint();
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
    if (Setting.turn % 2 === 1) {
        color = 'yellow_disc';
    }
    let circle = document.createElementNS(svgns, 'circle');
    circle.setAttributeNS(null, 'id', color);
    circle.setAttributeNS(null, 'cx', get_x_center(x_index));
    circle.setAttributeNS(null, 'cy', 10);
    circle.setAttributeNS(null, 'r', "5");
    svg.appendChild(circle);
    animation(circle, y_index);
    Setting.turn += 1;
}

function get_row(icon, col) {
    for (let i = 50; i >= 0; i -= 10) {
        if (Setting.board[i + col] === '') {
            Setting.board[i + col] = icon;
            return i / 10;
        }
    }
}

function is_legal(col) {
    for (let i = 0; i < Setting.legal_moves.length; i++) {
        if (Setting.legal_moves[i] === col) {
            return true;
        }
    }
    return false;
}

function clear_tmp() {
    if (document.getElementById('tmp_red_disc')) {
        document.getElementById('tmp_red_disc').remove();
    }
    if (document.getElementById('tmp_yellow_disc')) {
        document.getElementById('tmp_yellow_disc').remove();
    }
}

svg.addEventListener('mousemove', function (evt) {
    let loc = cursorPoint(evt);
    if (Setting.is_player_turn) {
        clear_tmp();
        let circle = document.createElementNS(svgns, 'circle');
        let color = 'tmp_red_disc';
        if (Setting.turn % 2 === 1) {
            color = 'tmp_yellow_disc';
        }
        circle.setAttributeNS(null, 'id', color);
        circle.setAttributeNS(null, 'cx', get_x_center(get_x_index(loc)));
        circle.setAttributeNS(null, 'cy', 10);
        circle.setAttributeNS(null, 'r', "5");
        svg.appendChild(circle);
    }
});

svg.addEventListener('click', function (evt) {
    let loc = cursorPoint(evt);
    if (Setting.is_player_turn) {
        let col = get_x_index(loc);
        if (is_legal(col)) {
            clear_tmp();
            let row = get_row(Setting.player['player'], col);
            put_chess(col, row);
            Setting.is_player_turn = false;
            axios({
                method: 'post',
                headers: {"X-CSRFToken": csrftoken},
                url: window.location.protocol + '//' + window.location.host + "/api/connect4/get/move/",
                data: {
                    'chessboard': Setting.board,
                    'ai_mode': true,
                    'depth': Setting.difficulty,
                    'player': Setting.player
                },
            }).then(res => {
                console.log(res.data);
                if (res.data['success']) {
                    let data = res.data['data'];
                    put_chess(data['ai_move'][1], data['ai_move'][0]);
                    Setting.board = data['board'];
                    Setting.legal_moves = data['legal_moves'];
                    if (data['winner'] != null) {
                        console.log(data['winner']);
                        let txt = document.createElementNS(svgns, 'text');
                        txt.setAttributeNS(null, 'x', '50%');
                        txt.setAttributeNS(null, 'y', '10%');
                        txt.setAttributeNS(null, 'dominant-baseline', 'middle');
                        txt.setAttributeNS(null, 'text-anchor', 'middle');
                        txt.setAttributeNS(null, 'style', 'font-size: 8px;');
                        txt.innerHTML = 'Winner is ' + data['winner'];
                        svg.appendChild(txt);
                    } else {
                        Setting.is_player_turn = true;
                    }
                }
            })
        }
    }
});

document.getElementById('newGame').addEventListener('click', function () {
    const CancelToken = axios.CancelToken;
    const source = CancelToken.source();

    axios.post(window.location.protocol + '//' + window.location.host + "/api/connect4/get/move/", {
        cancelToken: source.token
    }).catch(function (thrown) {
        if (axios.isCancel(thrown)) {
            console.log('Request canceled', thrown.message);
        } else {
            console.log(thrown);
        }
    });

    axios.post('/user/12345', {}, {
        headers: {"X-CSRFToken": csrftoken},
        cancelToken: source.token
    })
    source.cancel();

    Setting.board = {
        0: '', 1: '', 2: '', 3: '', 4: '', 5: '', 6: '',
        10: '', 11: '', 12: '', 13: '', 14: '', 15: '', 16: '',
        20: '', 21: '', 22: '', 23: '', 24: '', 25: '', 26: '',
        30: '', 31: '', 32: '', 33: '', 34: '', 35: '', 36: '',
        40: '', 41: '', 42: '', 43: '', 44: '', 45: '', 46: '',
        50: '', 51: '', 52: '', 53: '', 54: '', 55: '', 56: '',
    };
    Setting.legal_moves = [0, 1, 2, 3, 4, 5, 6];
    Setting.turn = 0;
    svg.innerHTML = '';
    Setting.is_player_turn = true;
    draw_chessboard();
    if (Setting.ai_first) {
        Setting.ai_first = false;
        Setting.player = {'com': 'x', 'player': 'o'};
    } else {
        Setting.ai_first = true;
        if (Setting.mode === 'ai') {
            Setting.player = {'com': 'o', 'player': 'x'};
            Setting.board["53"] = Setting.player['com'];
            put_chess(3, 5);
        }
    }
});

document.querySelector('#settingModal').addEventListener('change', function () {
    let radios = document.querySelectorAll('[name=mode]');
    if (radios[0].checked) {
        document.querySelector('#difficulty').removeAttribute('disabled');
        Setting.mode = 'ai';
        Setting.difficulty = parseInt(document.querySelector('#difficulty').value);
    } else if (radios[1].checked) {
        document.querySelector('#difficulty').setAttribute('disabled', 'true');
        Setting.mode = 'player';
        Setting.difficulty = undefined;
    }
})