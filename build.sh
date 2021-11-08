#!/bin/bash
set -euo pipefail

export CC=musl-gcc
go build --ldflags '-linkmode external -extldflags "-static"' -o main
