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


const leftWidth = 400;

makeSlider(bpmContainer, 40, 540, throttle(changeBpm, 200), 'y', '');
makeSlider(verbContainer, 30, leftWidth, throttle(verbify, 100), 'x', 'Flux');
makeSlider(distoContainer, 30, leftWidth, throttle(distort, 100), 'x', 'Force');

const maxSaturate = 15;
const minSaturate = 1;
const maxBlur = 15;
const minBlur = 0;
const maxBrightness = 5;
const minBrightness = 1

const ranger = (min, max) => coef => Math.floor((max - min) * coef) + min;
const calcSaturate = ranger(minSaturate, maxSaturate);
const calcBlur = ranger(minBlur, maxBlur);
const calcBrightness = ranger(minBrightness, maxBrightness);

let blur = '0px';
let saturate = 1;
let brightness = 1;

/**
 * set up power buttons
 */

const powerButtons = {
    'btna': false,
    'btnb': false,
    'beata': true,
    'beatb': true,
    'beatc': true,
    'beatd': true
};

function handleA(on) {
    const payload = on ? 1 : 0.01;
    const msg = {
        kind: 'special1',
        payload
    };
    $('rect.handle').toggleClass('pulsing', on);
    $('#beat .button').toggleClass('pulsing', on);
    fxWs.send(JSON.stringify(msg));
}

function handleB(on) {
    const payload = on ? 1 : 0.01;
    const msg = {
        kind: 'special2',
        payload
    };
    $('#Petals').toggleClass('pulsing', on);
    fxWs.send(JSON.stringify(msg));
}

function handleBeatElementsChange() {
    const beatElements = [
        powerButtons.beata,
        powerButtons.beatb,
        powerButtons.beatc,
        powerButtons.beatd
    ];

    drumWs.send(JSON.stringify({
        kind: 'change_elements',
        payload: beatElements
    }));
}

$('#beat .button.radio').click(function () {
    const el = $(this);
    const family = el.data('family');
    $('#beat .button.radio').toggleClass('active', false);
    el.toggleClass('active', true);
    drumWs.send(JSON.stringify({
        kind: 'change_family',
        payload: family
    }));
});

$('.button:not(.radio)').click(function () {
    const el = $(this);
    const key = el.attr('id');
    const oldState = powerButtons[key];
    const newState = !oldState;
    powerButtons[key] = newState;
    el.toggleClass('active', newState);

    switch (key) {
        case 'btna':
            {
                handleA(newState);
                break;
            }
        case 'btnb':
            {
                handleB(newState);
                break;
            }
        case 'beata':
        case 'beatb':
        case 'beatc':
        case 'beatd':
            {
                handleBeatElementsChange();
            }
    }
});

function setFilter() {
    $('canvas').css('filter', `blur(${blur}) saturate(${saturate}) brightness(${brightness})`);
}

function verbify(val) {
    blur = calcBlur(val) + 'px';
    requestAnimationFrame(setFilter);
    fxChange(val, 'reverb');
}

function distort(val) {
    saturate = calcSaturate(val);
    brightness = calcBrightness(val);
    requestAnimationFrame(setFilter);
    fxChange(val, 'distortion');
}

function fxChange(val, kind) {
    // val [0,1]
    switch (kind) {
        case 'distortion':
            {
                fxWs.send(JSON.stringify({
                    kind: 'distortion',
                    payload: val
                }));
                break;
            }
        case 'reverb':
            {
                fxWs.send(JSON.stringify({
                    kind: 'reverb',
                    payload: val
                }));
                break;
            }
    }
}

function changeBpm(val) {
    bpmWs.send(JSON.stringify({
        kind: 'change',
        payload: val
    }));
}