# CSV2JuliaDiffEq
Convert reactions and parameters defined in CSV files to DifferentialEquations.jl equations



## Input file formats

Three CSV Files are required as input their format is as follows:

### Reactions

This CSV file should contain a header line followed by 4 fields, seperated by commas:
* Products separated by spaces,
* Products separated by spaces,
* The full title of the rate law,
* Modifiers separated by spaces

`[A]+[B] -> [AB]`

Substrate | Products | Kinetic Law | Modifiers
-|-|-|-
A B|AB|Mass Action|

### Rate Laws

This CSV file contains the name of a ratelaw followed by a regExp-friendly definition of the rate law:
* The rate law name, matching the rate law definition in Reactions.csv,
* The Rate law definition written in julia-compatable format with molecular species in square brakets, parameters in braces.

Rate Law Name | Rate Law Definition
-|-
Mass Action | [S1] * [S2] * {k_on}

###

This CSV file contains parameter names and their values:
* Parameter with name exactly matching the parameter name in the reactions CSV file
* Value. This is the value.

Parameter|Value
-|-
k_on|0.2



