
abspath() {
	echo "$(cd "$(dirname "$1")" && pwd)/$(basename "$1")"
}

export PYTHONPATH=$(abspath ..)

echo "PYTHONPATH: $PYTHONPATH"

python3 -m pytest "$@"

unset PYTHONPATH
