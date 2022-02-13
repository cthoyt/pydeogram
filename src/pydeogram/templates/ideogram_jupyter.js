require.config({
    paths: {
        Ideogram: 'https://unpkg.com/ideogram@1.5.0/dist/js/ideogram.min'
    }
});

require(['Ideogram'], function (Ideogram) {
    window.Ideogram = Ideogram.default;
});

var ideogram = new Ideogram({
    container: '#{{ container }}',
    organism: 'human',
    annotationsLayout: 'histogram',
    barWidth: 3,
    annotations: {{ annotations|safe }}
});
