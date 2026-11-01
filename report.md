Group report 

# Project 4 

A particle starts with positive velocity and after constant time intervalls, the velocity can flip its direction with the probability of $1 - np.exp(-mu *dt)$, dt being the time intervall and mu being the rate. 

## Layout of the algorithm, functions to be created

First all parameters have to get initialized, with the probaility being $1 - np.exp(-mu *dt)$, dt being the time intervall and mu being the rate. Another step is the amount of times $n$, the time intervall should pass through, is initialized.

In the second step, in a for loop with the fixed probability, the velocity changes directions and the current position is noted.

## How to run the code

python3 T4N.py

'numpy' and 'matplotlib.pyplot' are necessary.

v : velocity.   
n : ampunt of steps.   
$mu$ : rate.   
dt = $1/(4*mu)$ : time intervall.   
probability of return : $1 - np.exp(-mu *dt)$.   
revearse : counter for amount of revearses.   
positions : list of positions for the plot.   
pos : starting position is zero.   



## Resulting files

In the end the expected theoretical velocity change probability is compared to the actuall velocity change ratio. Furthermore, a plot of all the positions is shown.

## Successful tests

The actual probability matches witch the theoretical probability

## Problems

No big problems apart from the inexperience with GitHub

## Results (speed tests etc.)

The beautiful part, where you report results, tables, files, or figures, after your code was able to run. 
