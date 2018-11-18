function makeBpmWidget2(node, bpmWs) {
  const sliderG = d3.select(node.find('#bpm-slider svg').get()[0]);
  const flowerG = d3.select(node.find('#flower-clock svg').get()[0]);

  function sendBpmWsMsg(val) {
    bpmWs.send(JSON.stringify({
      kind: 'change',
      payload: val
    }));
  }
  const throttledBpmSend = throttle(sendBpmWsMsg, 200);
  makeSlider(sliderG, 5, 30, 300, throttledBpmSend);

  let i = 1;
  let bpm = 10;

  bpmWs.onmessage = function(d) {
    const data = JSON.parse(d.data);
    bpm = Math.max(1, data.real_bpm);
    console.log(bpm);
  };

  function tick() {
    setTimeout(function() {
      flowerG.select(`#Petal_${i} path`).classed('active', true);
      flowerG.select(`#Petal_${i === 1 ? 16 : i - 1} path`).classed('active', false);
      i = i % 16 + 1;
      tick();
    }, (60 / 4 / bpm) * 1000);
  }

  tick();


  /*
   clockWs.onmessage = function(d) {
   const data = JSON.parse(d.data);
   const tick = data.tick % 16 + 1;
   //console.log(tick, flowerG)
   flowerG.select(`#Petal_${tick} path`).classed('active', true);
   flowerG.select(`#Petal_${tick === 1 ? 16 : tick - 1} path`).classed('active', false);
   };

  */
}