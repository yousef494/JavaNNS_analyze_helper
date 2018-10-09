# JavaNNS_analyze_helper
## Description
This is a helper python script to simplify multiple run of JavNNS analyze program to only one.
Also, it combines each train result and corresponding test result in a row.
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
## Output
Comma separated output of multiple rows

example:
Run,Learning_rate,Question,#_Hidden_nodes,Part,Epoches,Architecture,id,Momentum,train-wrong0,train-right0,train-unknown0,test-wrong0,test-right0,test-unknown0
test,0.1,6,5,p2,500,A:23-5-1,p2_6_50.1500,0.1,0.00,40.83,59.17,0.00,43.96,56.04
