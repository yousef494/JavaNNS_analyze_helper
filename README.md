# JavaNNS_analyze_helper
## Usage
usage: analyze_helper.py [-h] -d DIR

sub-directories naming pa_b a: part number, b: question number. Files naming
c-d-e-f-g.res, c: hidden-units, d: Learning_rate, e: Momentum (optional), f:
cycles, g: "test" (optional). For example: 10-0.2-1000.res,
10-0.2-0.5-1000.res, 10-0.2-1000-test.res, 10-0.2-0.5-1000.res

optional arguments:
  -h, --help         show this help message and exit

Required arguments:
  -d DIR, --dir DIR  Results directory which containes all sub-direcotries
                     which containe .res files
