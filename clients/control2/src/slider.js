function makeSlider(container, width, height, cb) {
    // g is a d3 element
    const g = container.append('svg')
        .attrs({
            height,
            width
        })
        .append('g');

    const scale = d3.scaleLinear()
        .domain([0, 1])
        .range([0, height])
        .clamp(true);
    
    // create a closure
    const dragFun = onDrag();

    g.append("rect")
        .attrs({
            'class': 'track',
            x: 0,
            y: 0,
            width,
            height
        })
        .select(function () {
            return this.parentNode.appendChild(this.cloneNode(true));
        })
        .attr("class", "track-inset")
        .select(function () {
            return this.parentNode.appendChild(this.cloneNode(true));
        })
        .attr("class", "track-overlay")
        .call(d3.drag()
            .on("start.interrupt", () => g.interrupt())
            .on("start drag", dragFun));

    const handle = g.insert("rect", ".track-overlay")
        .attr("class", "handle")
        .attrs({
            x: 0,
            y: 0,
            width,
            height
        });

    function onDrag() {
        let mostRecentChange = 0;
        return function () {
            const newVal = scale(scale.invert(d3.event.y));
            handle.attr('height', height - newVal);
            handle.attr('y', newVal);

            if (newVal !== mostRecentChange) {
                mostRecentChange = newVal;
                // do not send a zero
                const percent = (height - newVal) / height;
                cb(Math.max(percent, 0.01));
            }
        }
    }
}