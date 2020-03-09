# CSV2JuliaDiffEq
Convert reactions and parameters defined in CSV files to DifferentialEquations.jl equations



## Input file formats

Three CSV Files are required as input their format is as follows:

### Reactions

This CSV file should contain a header line followed by 4 fields, seperated by commas:
* Products separated by spaces,
* Products separated by spaces,
* The full title of the rate law,
* Modifiers separated by spaces. Modifiers can be delayed and the output will take the format of a DDE. Use the syntax delay(modifier,delayTime) to specify a delayed modifier.
* Parameters separated by spaces, parameter names must include the type of parameter then an underscore and the parameter name. This allows vmax, km etc to be placed in the correct position in the reaction

`[A]+[B] -> [AB]`

Substrate | Products | Kinetic Law | Modifiers | Parameters
-|-|-|-|-
A B|AB|Mass Action||k_ABBinding

### Rate Laws

This CSV file contains the name of a ratelaw followed by a regExp-friendly definition of the rate law:
* The rate law name, matching the rate law definition in Reactions.csv,
* The Rate law definition written in julia-compatable format with molecular species in square brakets, parameters in braces. Substrates should be called S1, S2 etc. Products should be called P1, P2 etc. Modifiers should be called mod1 mod2 etc. Parameters names should match the parameter type from the reactions file (the bit before the underscore) e.g. 'k' or 'vmax'.

Rate Law Name | Rate Law Definition
-|-
Mass Action | [S1] * [S2] * {k}

###

This CSV file contains parameter names and their values:
* Parameter with name exactly matching the parameter name in the reactions CSV file, including the parameter type before the underscore.
* Value. This is the value.

Parameter|Value
-|-
k_ABBinding|0.2



