const bpmContainer = d3.select('#bpm');
const verbContainer = d3.select('#verb');
const distoContainer = d3.select('#disto');

const leftWidth = 450;

$('#left').css('width', leftWidth + 'px');

makeSlider(bpmContainer, 40, 600, console.log, 'y');
makeSlider(verbContainer, 30, leftWidth, console.log, 'x', 'Flux');
makeSlider(distoContainer, 30, leftWidth, console.log, 'x', 'Force');