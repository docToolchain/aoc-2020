#!/bin/bash

wasm-pack build
cargo watch -s 'wasm-pack build'
