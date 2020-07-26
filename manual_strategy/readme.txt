This file explains how the code files in my submission can be run.

All the files have been coded in Python 3.
The file util.py needs to be present in the same folder as these files so that its functions can be imported.

1. indicators.py
To run this file, type
python indicators.py
in the terminal.
This file calculates the technical indicators for the in-sample dates. Runiing this file generates plots of these indicators in the same folder.

2. TheoreticallyOptimalStrategy.py
To run this file, type
python TheoreticallyOptimalStrategy.py
in the terminal.
Running this file applies the theoretically optimal strategy to the in-sample dates, and generates a plot of comparison between the theoretically optimal strategy and the benchmark in the same folder.
It also prints the performance statistics in the terminal.

3. ManualStrategy.py
To run this file, type
python ManualStrategy.py
in the terminal.
This file implements a manual rule-based strategy. Running this file generates plots of comparison between the rule-based strategy and the benchmark for in-sample and out-sample dates in the same folder.
It also prints the performance statistics for both in-sample and out-sample dates in the terminal.

4. marketsimcode.py
This file need not be run. This is being imported in TheoreticallyOptimalStrategy.py and ManualStrategy.py.