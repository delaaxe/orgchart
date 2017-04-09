module.exports = {
    entry: {
        'bundle': './app/main.js'
        //'js/vendor/orgchart-webcomponents': './node_modules/orgchart-webcomponents/src/orgchart-webcomponents.js'
    },
    output: {
        path: './app/',
        filename: '[name].js'
    },
    devtool: 'source-map',
    module: {
        loaders: [
            {
                loader: 'babel',
                query: {
                    presets: ['es2015']
                }
            }
        ]
    }
};
