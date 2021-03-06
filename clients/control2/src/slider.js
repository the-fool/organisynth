function makeSlider(container, thickness, length, cb, orientation, label = '') {
    if (orientation !== 'x' && orientation !== 'y') {
        throw Error('Orientation must be x or y');
    }

    const isHorizontal = orientation === 'x';

    const width = isHorizontal ? length : thickness;
    const height = isHorizontal ? thickness : length;

    // g is a d3 element
    const g = container.append('svg')
        .attrs({
            height,
            width
        })
        .append('g');

    const scale = d3.scaleLinear()
        .domain([0, 1])
        .range([0, length])
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

    /**
     * Add labels
     */
    const textAttrs = isHorizontal ? {
            x: '10px',
            y: Math.floor(thickness / 2)
        } : {
            x: Math.floor(thickness / 2),
            y: '10px'
        };
        
    const textStyles = isHorizontal ? {
        'alignment-baseline': 'middle'   
    } : {
        'alignment-baseline': 'baseline',
        'writing-mode': 'tb'
    };

    g.insert('text', '.track-overlay')
        .attrs(textAttrs)
        .style('font-size', `${Math.floor(thickness * 0.7)}px`)
        .styles(textStyles)
        .text(label);

    function onDrag() {
        let mostRecentChange = 0;

        function performCb(val) {
            if (val !== mostRecentChange) {
                mostRecentChange = val;
                // do not send a zero
                const percent = isHorizontal ? val / length : (length - val) / length;
                cb(Math.max(percent, 0.01));
            }
        }
        return function () {
            if (isHorizontal) {
                const newVal = scale(scale.invert(d3.event.x));
                handle.attr('width', newVal);
                performCb(newVal);
            } else {
                const newVal = scale(scale.invert(d3.event.y));
                handle.attr('height', height - newVal);
                handle.attr('y', newVal);
                performCb(newVal);
            }
        }
    }
}