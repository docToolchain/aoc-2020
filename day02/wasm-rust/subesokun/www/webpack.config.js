const CopyWebpackPlugin = require("copy-webpack-plugin");
const path = require('path');

module.exports = {
    entry: "./bootstrap.js",
    output: {
        path: path.resolve(__dirname, "dist"),
        filename: "bootstrap.js",
        devtoolModuleFilenameTemplate: 'file:///[absolute-resource-path]'
    },
    devServer: {
        transportMode: 'ws'
    },
    devtool: 'source-map',
    mode: "development",
    plugins: [
        new CopyWebpackPlugin(['index.html'])
    ],
    module: {
        rules: [{
                test: /\.txt$/i,
                use: 'raw-loader',
            },
            {
                test: /\.css$/i,
                use: ["style-loader", "css-loader"],
            }
        ],
    }
};