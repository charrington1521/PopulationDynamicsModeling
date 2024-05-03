# Population Dynamics Modeling for CSC 235 at Union College Spr. 2024

## Collin Harrington, Phuc Nguyen

This project contains a module which allows for population modeling.
This modules contains data from the world census as found on wikipedia
and combines that information with world caloric information and 
basic population modeling provide a interesting measurement of suffering.

There are a couple of ways users should use this module.

### System variable 

the `system` variable within the module can be edited to change modeling parameters.
  The system vairable has the following parameters:
  <li> t_0 the initial time (a year) </li>
  <li> t_f the time to simulate until (a year). Must be greater than t_0 </li>
  <li> p_0 the initial population at t_0. If one changes t_0, p_0 should also be changed </li>
  <li> alpha the coefficient used in standard quaratic growth modeling for population </li>
  <li> beta the second coefficient used in standard quadratic growth modeling for population </li>
  <li> cal_per_day the number of calories a person needs to eat in a day to not be considered suffering </li>
  <li> total_calories the total number of calories available in the world. This is presumed to be constant </li>

### Run Simulation and Growth Functions

The `run_simulation` method has two parameters a `system` and a `growth_func`
Included in the module is `growth_func_quad` to model standard qudratic growth, however, 
users may create their own `growth_func`
The expected signature is `def foo(time (year), population (in billions), system)`
And the method should return how much the population grows in the next year. 

`run_simulation` returns two "TimeSeries()" objects, the first containing the simulated population
numbers and the second using our measurement of "suffering" in this model

User should plot these data as they see fit!
