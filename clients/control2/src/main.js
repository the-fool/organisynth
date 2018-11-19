const bpmContainer = d3.select('#bpm');
const verbContainer = d3.select('#verb');
const distoContainer = d3.select('#disto');


function wsConnect(name) {
  const wsUrl = path => `ws://${window.location.hostname}:7700/${path}`;
  const ws = new WebSocket(wsUrl(name));
  return ws;
}

// const clockWs = wsConnect('clocker');
const bpmWs = wsConnect('metronome_changer');
const drumWs = wsConnect('drummer');
const fxWs = wsConnect('fx_reaper');


const leftWidth = 450;

makeSlider(bpmContainer, 40, 500, throttle(changeBpm, 200), 'y');
makeSlider(verbContainer, 30, leftWidth, throttle(verbify, 200), 'x', 'Flux');
makeSlider(distoContainer, 30, leftWidth, throttle(distort, 200), 'x', 'Force');

const maxSaturate = 15;
const minSaturate = 1;
const maxBlur = 5;
const minBlur = 0;
const ranger = (min, max) => coef => Math.floor((max - min) * coef) + min;
const calcSaturate = ranger(minSaturate, maxSaturate);
const calcBlur = ranger(minBlur, maxBlur);

let blur = '0px';
let saturate = 1;
let canvas = $('canvas');
setTimeout(() => canvas = $('canvas'), 4000);

/**
 * set up power buttons
 */
const powerButtons = {
    'btna': false,
    'btnb': false
};

$('#power-buttons .button').click(function() {
    const el = $(this);
    const key = el.attr('id');
    const oldState = powerButtons[key];
    const newState = !oldState;
    powerButtons[key] = newState;
    el.toggleClass('active', newState);

    const payload = newState ? 1 : 0.01;
    let msg;
    switch (key) {
        case 'btna': {
            msg = {kind: 'special1', payload};
            break;
        }
        case 'btnb': {
            msg = {kind: 'special2', payload};
            break;
        }
    }
    fxWs.send(JSON.stringify(msg));
});

function setFilter() {
    $('canvas').css('filter', `blur(${blur}) saturate(${saturate})`);
    console.log(canvas, blur, saturate);
}

function verbify(val) {
    blur = calcBlur(val) + 'px';
    requestAnimationFrame(setFilter);
    fxChange(val, 'reverb');
}

function distort(val) {
    saturate = calcSaturate(val);
    requestAnimationFrame(setFilter);
    fxChange(val, 'distortion');
}

function fxChange(val, kind) {
    // val [0,1]
    switch (kind) {
        case 'distortion': {
            fxWs.send(JSON.stringify({kind: 'distortion', payload: val}));
            break;
        }
        case 'reverb': {
            fxWs.send(JSON.stringify({kind: 'reverb', payload: val}));
            break;
        }
    }
}

function changeBpm(val) {

}