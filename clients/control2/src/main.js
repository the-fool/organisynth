const bpmContainer = d3.select('#bpm');
const verbContainer = d3.select('#verb');
const distoContainer = d3.select('#disto');

makeSlider(bpmContainer, 40, 600, console.log, 'y');
makeSlider(verbContainer, 30, 700, console.log, 'x', 'Echo');
makeSlider(distoContainer, 30, 700, console.log, 'x', 'Disto');