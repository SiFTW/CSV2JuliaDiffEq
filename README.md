# CSV2JuliaDiffEq
Convert reactions and parameters defined in CSV files to DifferentialEquations.jl equations

## Example usage

### We need some packages


```julia
using DifferentialEquations
using Plots 
using CSV
using Distributions
using Random
using DataFrames
using FileIO

plotly(); # if you want pretty graphs
```

# What is the same for all methods

All these methods use three files. 

reactions.csv:

| Substrate | Products | Kinetic Law | Modifiers | Parameters |
| --- | --- | --- | --- | --- |
| --- | A | Constant Exp | --- | k1_Aexp |
| A | B | Mass Action with substrate | --- | k1_AtoB |
| B | C | Mass Action with substrate | --- | k1_BtoC |
| C | --- | Mass Action with substrate | --- | k1_Cdeg |


parameters.csv: 


| Parameter | Value |
| ---| --- |
|k1_Aexp|1|
|k1_AtoB|2|
|k1_BtoC|3|
|k1_Cdeg|p(t)|

and ratelaws.csv:

|Rate Law Name|Rate Law Definition|
| --- | --- |
|Constant Exp|{k1}|
|Mass Action with substrate|[S1] * {k1}|

# The three ways to run a model

There are three ways to create model files with csv2julia. These are specified by the final argument to csv 2 jula.

## inline

This creates models with hardcoded parameters that look like this:

~~~julia 
function toyModel(dy,y,p,t)
        A=maximum([y[1],0])
        B=maximum([y[2],0])
        C=maximum([y[3],0])
        #A
        dy[1]= + 1 - A * 2
        #B
        dy[2]= + A * 2 - B * 3
        #C
        dy[3]= + B * 3 - C * p(t)
    end
~~~

## scan

This creates models where each parameter is a function call, to enable these to by dynamically updated at run time (but at a performance cost):

~~~julia 
function toyModel(dy,y,p,t)
	A=maximum([y[1],0])
	B=maximum([y[2],0])
	C=maximum([y[3],0])
	#A
	dy[1]= + paramFun("k1_Aexp",modify) - A * paramFun("k1_AtoB",modify)
	#B
	dy[2]= + A * paramFun("k1_AtoB",modify) - B * paramFun("k1_BtoC",modify)
	#C
	dy[3]= + B * paramFun("k1_BtoC",modify) - C * p(t)
end

~~~


## params

This creates models where each parameter is passed in through a list. This is the best way to do it if interfacing with JuliaDiffEqs sensitivity analysis functions etc.

~~~julia
    function toyModel(dy,y,p,t)
        A=maximum([y[1],0])
        B=maximum([y[2],0])
        C=maximum([y[3],0])
        #A
        dy[1]= + p[1] - A * p[2]
        #B
        dy[2]= + A * p[2] - B * p[3]
        #C
        dy[3]= + B * p[3] - C * p[4](t)
    end
~~~

# 1. inline: Example with all hardcoded parameters

This method creates models that look like this. All parameters are hardcoded directly as numbers (except any parameters that might be time dependent).

~~~julia 
function toyModel(dy,y,p,t)
        A=maximum([y[1],0])
        B=maximum([y[2],0])
        C=maximum([y[3],0])
        #A
        dy[1]= + 1 - A * 2
        #B
        dy[2]= + A * 2 - B * 3
        #C
        dy[3]= + B * 3 - C * p(t)
    end
~~~


```julia
reactionsFile="reactions.csv"
rateLawsFile="ratelaws.csv"
parametersFile="parameters.csv"
locationOfCSV2Julia="csv2model-multiscale.py"
thisModelName="toyModel.jl"
maxTimeTC=60;
```

First we'll make the time dependent variable just a constant


```julia
p=t->4
```




    #1 (generic function with 1 method)




```julia
arguments=[reactionsFile, parametersFile, rateLawsFile,thisModelName,"inline"]
cmd=`python3 $locationOfCSV2Julia $arguments`

#lets run csv2julia (requires python to be installed)
run(cmd)

#     #if we need to fix species we can do it here
#     #include("variableNames.jl")
#     #indexToFix=findfirst(x->"L"==x,syms)
#     #fixSpecies(modelFile,modelFile,indexToFix)

#pop the outputs in a modelFiles folder
include(thisModelName)
include("variableNames.jl")
```

    inline
    Running CSV2JuliaDiffEq with parameters hard-coded into the CSV file, if this is not correct, re-run with the 5th argument set to 'scan' or 'param'
    Opening ratelaws.csv as rate law file
    Opening parameters.csv as parameters file
    Opening reactions.csv as reactions file





    3-element Vector{String}:
     "A"
     "B"
     "C"




```julia
y0=[1,0,0];
f=ODEFunction(toyModel,syms=Symbol.(syms));
prob=ODEProblem(f,y0,(0.0,maxTimeTC),p);
sol=solve(prob, abstol=1e-5,reltol=1e-3, saveat=1.0);
plot(sol)
```




    <div id="ae249bc1-e8a6-4369-b8d3-a9a5ff60b30f" style="width:600px;height:400px;"></div>
    <script>
        requirejs.config({
        paths: {
            Plotly: 'https://cdn.plot.ly/plotly-1.57.1.min'
        }
    });
    require(['Plotly'], function (Plotly) {

        var PLOT = document.getElementById('ae249bc1-e8a6-4369-b8d3-a9a5ff60b30f');
    Plotly.plot(PLOT, [
    {
        "xaxis": "x",
        "colorbar": {
            "title": ""
        },
        "yaxis": "y",
        "x": [
            0.0,
            1.0,
            2.0,
            3.0,
            4.0,
            5.0,
            6.0,
            7.0,
            8.0,
            9.0,
            10.0,
            11.0,
            12.0,
            13.0,
            14.0,
            15.0,
            16.0,
            17.0,
            18.0,
            19.0,
            20.0,
            21.0,
            22.0,
            23.0,
            24.0,
            25.0,
            26.0,
            27.0,
            28.0,
            29.0,
            30.0,
            31.0,
            32.0,
            33.0,
            34.0,
            35.0,
            36.0,
            37.0,
            38.0,
            39.0,
            40.0,
            41.0,
            42.0,
            43.0,
            44.0,
            45.0,
            46.0,
            47.0,
            48.0,
            49.0,
            50.0,
            51.0,
            52.0,
            53.0,
            54.0,
            55.0,
            56.0,
            57.0,
            58.0,
            59.0,
            60.0
        ],
        "showlegend": true,
        "mode": "lines",
        "name": "A(t)",
        "zmin": null,
        "legendgroup": "A(t)",
        "zmax": null,
        "line": {
            "color": "rgba(0, 154, 250, 1.000)",
            "shape": "linear",
            "dash": "solid",
            "width": 1
        },
        "y": [
            1.0,
            0.5676676903345341,
            0.5091572598472662,
            0.5012377881718262,
            0.5001698762656928,
            0.5000237099188003,
            0.5000038123886293,
            0.5000008974528145,
            0.5000001463031121,
            0.5000000294941155,
            0.5000000046173783,
            0.5000000006444594,
            0.5000000000881726,
            0.5000000000122427,
            0.5000000000017608,
            0.5000000000002617,
            0.5000000000000392,
            0.5000000000000013,
            0.49999999999999706,
            0.5000000000000003,
            0.5000000000000002,
            0.49999999999999994,
            0.49999999999999994,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5
        ],
        "type": "scatter"
    },
    {
        "xaxis": "x",
        "colorbar": {
            "title": ""
        },
        "yaxis": "y",
        "x": [
            0.0,
            1.0,
            2.0,
            3.0,
            4.0,
            5.0,
            6.0,
            7.0,
            8.0,
            9.0,
            10.0,
            11.0,
            12.0,
            13.0,
            14.0,
            15.0,
            16.0,
            17.0,
            18.0,
            19.0,
            20.0,
            21.0,
            22.0,
            23.0,
            24.0,
            25.0,
            26.0,
            27.0,
            28.0,
            29.0,
            30.0,
            31.0,
            32.0,
            33.0,
            34.0,
            35.0,
            36.0,
            37.0,
            38.0,
            39.0,
            40.0,
            41.0,
            42.0,
            43.0,
            44.0,
            45.0,
            46.0,
            47.0,
            48.0,
            49.0,
            50.0,
            51.0,
            52.0,
            53.0,
            54.0,
            55.0,
            56.0,
            57.0,
            58.0,
            59.0,
            60.0
        ],
        "showlegend": true,
        "mode": "lines",
        "name": "B(t)",
        "zmin": null,
        "legendgroup": "B(t)",
        "zmax": null,
        "line": {
            "color": "rgba(227, 111, 71, 1.000)",
            "shape": "linear",
            "dash": "solid",
            "width": 1
        },
        "y": [
            0.0,
            0.4022851497716823,
            0.34834383191099605,
            0.33564689692839894,
            0.33366155457482866,
            0.33337953177702306,
            0.3333404707011917,
            0.33333395939369276,
            0.33333318783132626,
            0.3333332156339718,
            0.33333327373624594,
            0.3333333275862302,
            0.3333333330368691,
            0.3333333333253166,
            0.33333333332927473,
            0.33333333333075577,
            0.33333333333246656,
            0.3333333333334792,
            0.3333333333334423,
            0.3333333333332901,
            0.33333333333331855,
            0.3333333333333433,
            0.3333333333333393,
            0.3333333333333328,
            0.33333333333333026,
            0.33333333333333165,
            0.3333333333333331,
            0.3333333333333338,
            0.33333333333333415,
            0.33333333333333404,
            0.3333333333333336,
            0.33333333333333337,
            0.33333333333333326,
            0.33333333333333315,
            0.33333333333333315,
            0.33333333333333315,
            0.3333333333333332,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333
        ],
        "type": "scatter"
    },
    {
        "xaxis": "x",
        "colorbar": {
            "title": ""
        },
        "yaxis": "y",
        "x": [
            0.0,
            1.0,
            2.0,
            3.0,
            4.0,
            5.0,
            6.0,
            7.0,
            8.0,
            9.0,
            10.0,
            11.0,
            12.0,
            13.0,
            14.0,
            15.0,
            16.0,
            17.0,
            18.0,
            19.0,
            20.0,
            21.0,
            22.0,
            23.0,
            24.0,
            25.0,
            26.0,
            27.0,
            28.0,
            29.0,
            30.0,
            31.0,
            32.0,
            33.0,
            34.0,
            35.0,
            36.0,
            37.0,
            38.0,
            39.0,
            40.0,
            41.0,
            42.0,
            43.0,
            44.0,
            45.0,
            46.0,
            47.0,
            48.0,
            49.0,
            50.0,
            51.0,
            52.0,
            53.0,
            54.0,
            55.0,
            56.0,
            57.0,
            58.0,
            59.0,
            60.0
        ],
        "showlegend": true,
        "mode": "lines",
        "name": "C(t)",
        "zmin": null,
        "legendgroup": "C(t)",
        "zmax": null,
        "line": {
            "color": "rgba(62, 164, 78, 1.000)",
            "shape": "linear",
            "dash": "solid",
            "width": 1
        },
        "y": [
            0.0,
            0.2950667450623204,
            0.2683154974425716,
            0.2532397671781439,
            0.2504774112138527,
            0.2500673347120312,
            0.25000728491625734,
            0.25004228120397476,
            0.25011191149825474,
            0.2501664481758583,
            0.25035103707094675,
            0.2500708849617151,
            0.24993005559709708,
            0.24993196960673403,
            0.2499849751724222,
            0.2500628665748835,
            0.25012846033008257,
            0.24996421614493375,
            0.24998357355498912,
            0.2500097784597622,
            0.25000224547944727,
            0.24999768829325947,
            0.2499989849237035,
            0.2500001870391864,
            0.2500006204141202,
            0.25000028504850474,
            0.2500000254898125,
            0.2499999029571158,
            0.24999985960563154,
            0.2499998954353597,
            0.24999997484557354,
            0.24999999603739734,
            0.250000011604376,
            0.25000002154650963,
            0.25000002586379805,
            0.25000002455624143,
            0.25000001762383967,
            0.2500000050665928,
            0.25000000232848585,
            0.250000000809424,
            0.2499999995204305,
            0.24999999846150547,
            0.24999999763264885,
            0.24999999703386067,
            0.24999999666514092,
            0.24999999652648958,
            0.24999999661790667,
            0.24999999693939218,
            0.24999999749094612,
            0.24999999827256847,
            0.24999999928425926,
            0.2499999998129677,
            0.2499999999648404,
            0.2500000000847711,
            0.2500000001727597,
            0.25000000022880625,
            0.2500000002529108,
            0.25000000024507335,
            0.25000000020529384,
            0.25000000013357226,
            0.25000000002990863
        ],
        "type": "scatter"
    }
]
, {
    "showlegend": true,
    "xaxis": {
        "showticklabels": true,
        "gridwidth": 0.5,
        "tickvals": [
            0.0,
            10.0,
            20.0,
            30.0,
            40.0,
            50.0,
            60.0
        ],
        "range": [
            0.0,
            60.0
        ],
        "domain": [
            0.0658209390492855,
            0.9934383202099738
        ],
        "mirror": false,
        "tickangle": 0,
        "showline": true,
        "ticktext": [
            "0",
            "10",
            "20",
            "30",
            "40",
            "50",
            "60"
        ],
        "zeroline": false,
        "tickfont": {
            "color": "rgba(0, 0, 0, 1.000)",
            "family": "sans-serif",
            "size": 11
        },
        "zerolinecolor": "rgba(0, 0, 0, 1.000)",
        "anchor": "y",
        "visible": true,
        "ticks": "inside",
        "tickmode": "array",
        "linecolor": "rgba(0, 0, 0, 1.000)",
        "showgrid": true,
        "title": "t",
        "gridcolor": "rgba(0, 0, 0, 0.100)",
        "titlefont": {
            "color": "rgba(0, 0, 0, 1.000)",
            "family": "sans-serif",
            "size": 15
        },
        "tickcolor": "rgb(0, 0, 0)",
        "type": "-"
    },
    "paper_bgcolor": "rgba(255, 255, 255, 1.000)",
    "annotations": [],
    "height": 400,
    "margin": {
        "l": 0,
        "b": 20,
        "r": 0,
        "t": 20
    },
    "plot_bgcolor": "rgba(255, 255, 255, 1.000)",
    "yaxis": {
        "showticklabels": true,
        "gridwidth": 0.5,
        "tickvals": [
            0.0,
            0.25,
            0.5,
            0.75,
            1.0
        ],
        "range": [
            -0.03,
            1.03
        ],
        "domain": [
            0.07581474190726165,
            0.9901574803149606
        ],
        "mirror": false,
        "tickangle": 0,
        "showline": true,
        "ticktext": [
            "0.00",
            "0.25",
            "0.50",
            "0.75",
            "1.00"
        ],
        "zeroline": false,
        "tickfont": {
            "color": "rgba(0, 0, 0, 1.000)",
            "family": "sans-serif",
            "size": 11
        },
        "zerolinecolor": "rgba(0, 0, 0, 1.000)",
        "anchor": "x",
        "visible": true,
        "ticks": "inside",
        "tickmode": "array",
        "linecolor": "rgba(0, 0, 0, 1.000)",
        "showgrid": true,
        "title": "",
        "gridcolor": "rgba(0, 0, 0, 0.100)",
        "titlefont": {
            "color": "rgba(0, 0, 0, 1.000)",
            "family": "sans-serif",
            "size": 15
        },
        "tickcolor": "rgb(0, 0, 0)",
        "type": "-"
    },
    "legend_position": {
        "yanchor": "auto",
        "xanchor": "auto",
        "bordercolor": "rgba(0, 0, 0, 1.000)",
        "bgcolor": "rgba(255, 255, 255, 1.000)",
        "borderwidth": 1,
        "tracegroupgap": 0,
        "y": 1.0,
        "font": {
            "color": "rgba(0, 0, 0, 1.000)",
            "family": "sans-serif",
            "size": 11
        },
        "title": {
            "font": {
                "color": "rgba(0, 0, 0, 1.000)",
                "family": "sans-serif",
                "size": 15
            },
            "text": ""
        },
        "traceorder": "normal",
        "x": 1.0
    },
    "width": 600
}
);

    });
    </script>




This is how you can make a variable time depenent:


```julia
p=t->(1/(sin(t)+1))
```




    #3 (generic function with 1 method)




```julia
prob=ODEProblem(f,y0,(0.0,maxTimeTC),p);
timeTaken = @timed sol=solve(prob, abstol=1e-5,reltol=1e-3, saveat=1.0);
println("solved in: "*string(timeTaken.time))
```

    solved in: 4.318221165



```julia
plot(sol)
```




    <div id="a60b907a-a875-49d0-b6c6-78b6d32a920c" style="width:600px;height:400px;"></div>
    <script>
        requirejs.config({
        paths: {
            Plotly: 'https://cdn.plot.ly/plotly-1.57.1.min'
        }
    });
    require(['Plotly'], function (Plotly) {

        var PLOT = document.getElementById('a60b907a-a875-49d0-b6c6-78b6d32a920c');
    Plotly.plot(PLOT, [
    {
        "xaxis": "x",
        "colorbar": {
            "title": ""
        },
        "yaxis": "y",
        "x": [
            0.0,
            1.0,
            2.0,
            3.0,
            4.0,
            5.0,
            6.0,
            7.0,
            8.0,
            9.0,
            10.0,
            11.0,
            12.0,
            13.0,
            14.0,
            15.0,
            16.0,
            17.0,
            18.0,
            19.0,
            20.0,
            21.0,
            22.0,
            23.0,
            24.0,
            25.0,
            26.0,
            27.0,
            28.0,
            29.0,
            30.0,
            31.0,
            32.0,
            33.0,
            34.0,
            35.0,
            36.0,
            37.0,
            38.0,
            39.0,
            40.0,
            41.0,
            42.0,
            43.0,
            44.0,
            45.0,
            46.0,
            47.0,
            48.0,
            49.0,
            50.0,
            51.0,
            52.0,
            53.0,
            54.0,
            55.0,
            56.0,
            57.0,
            58.0,
            59.0,
            60.0
        ],
        "showlegend": true,
        "mode": "lines",
        "name": "A(t)",
        "zmin": null,
        "legendgroup": "A(t)",
        "zmax": null,
        "line": {
            "color": "rgba(0, 154, 250, 1.000)",
            "shape": "linear",
            "dash": "solid",
            "width": 1
        },
        "y": [
            1.0,
            0.5676671607638394,
            0.5091569824481709,
            0.5012376155725479,
            0.5001686729636938,
            0.5000228279478443,
            0.5000030892292263,
            0.5000004145985629,
            0.5000000533708883,
            0.5000000087774074,
            0.5000000013770078,
            0.5000000001871151,
            0.5000000000253233,
            0.5000000000034178,
            0.5000000000004324,
            0.5000000000000668,
            0.5000000000000105,
            0.5000000000000016,
            0.5000000000000003,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5
        ],
        "type": "scatter"
    },
    {
        "xaxis": "x",
        "colorbar": {
            "title": ""
        },
        "yaxis": "y",
        "x": [
            0.0,
            1.0,
            2.0,
            3.0,
            4.0,
            5.0,
            6.0,
            7.0,
            8.0,
            9.0,
            10.0,
            11.0,
            12.0,
            13.0,
            14.0,
            15.0,
            16.0,
            17.0,
            18.0,
            19.0,
            20.0,
            21.0,
            22.0,
            23.0,
            24.0,
            25.0,
            26.0,
            27.0,
            28.0,
            29.0,
            30.0,
            31.0,
            32.0,
            33.0,
            34.0,
            35.0,
            36.0,
            37.0,
            38.0,
            39.0,
            40.0,
            41.0,
            42.0,
            43.0,
            44.0,
            45.0,
            46.0,
            47.0,
            48.0,
            49.0,
            50.0,
            51.0,
            52.0,
            53.0,
            54.0,
            55.0,
            56.0,
            57.0,
            58.0,
            59.0,
            60.0
        ],
        "showlegend": true,
        "mode": "lines",
        "name": "B(t)",
        "zmin": null,
        "legendgroup": "B(t)",
        "zmax": null,
        "line": {
            "color": "rgba(227, 111, 71, 1.000)",
            "shape": "linear",
            "dash": "solid",
            "width": 1
        },
        "y": [
            0.0,
            0.4022895569866244,
            0.34834578011852496,
            0.33564702812997205,
            0.3336611711878937,
            0.3333785156732723,
            0.3333394882343248,
            0.3333341615189801,
            0.33333344009786076,
            0.3333333508742868,
            0.3333333360759182,
            0.3333333337069441,
            0.3333333333839492,
            0.33333333334016746,
            0.333333333334198,
            0.3333333333334669,
            0.3333333333333545,
            0.33333333333333653,
            0.33333333333333387,
            0.33333333333333337,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333
        ],
        "type": "scatter"
    },
    {
        "xaxis": "x",
        "colorbar": {
            "title": ""
        },
        "yaxis": "y",
        "x": [
            0.0,
            1.0,
            2.0,
            3.0,
            4.0,
            5.0,
            6.0,
            7.0,
            8.0,
            9.0,
            10.0,
            11.0,
            12.0,
            13.0,
            14.0,
            15.0,
            16.0,
            17.0,
            18.0,
            19.0,
            20.0,
            21.0,
            22.0,
            23.0,
            24.0,
            25.0,
            26.0,
            27.0,
            28.0,
            29.0,
            30.0,
            31.0,
            32.0,
            33.0,
            34.0,
            35.0,
            36.0,
            37.0,
            38.0,
            39.0,
            40.0,
            41.0,
            42.0,
            43.0,
            44.0,
            45.0,
            46.0,
            47.0,
            48.0,
            49.0,
            50.0,
            51.0,
            52.0,
            53.0,
            54.0,
            55.0,
            56.0,
            57.0,
            58.0,
            59.0,
            60.0
        ],
        "showlegend": true,
        "mode": "lines",
        "name": "C(t)",
        "zmin": null,
        "legendgroup": "C(t)",
        "zmax": null,
        "line": {
            "color": "rgba(62, 164, 78, 1.000)",
            "shape": "linear",
            "dash": "solid",
            "width": 1
        },
        "y": [
            0.0,
            0.8024469597292148,
            1.3479290597831097,
            1.432317976589997,
            0.5976336148596422,
            0.03267699378269493,
            0.393733877358387,
            0.8699673619978687,
            1.2960755499165333,
            1.4804801921934945,
            0.9677920554497718,
            1.6059665102947496e-5,
            0.2699772396204259,
            0.7340425241153498,
            1.18929488057771,
            1.4708004856545513,
            1.231224587104982,
            0.06183370065318904,
            0.15924103214163504,
            0.5973404373422602,
            1.0695235959910006,
            1.4225264343745883,
            1.3889618581592522,
            0.3762188494142472,
            0.06874530174209935,
            0.4629753890065269,
            0.9407972808412058,
            1.3458404764701748,
            1.4654830447268699,
            0.7830623583775712,
            0.010452597372125293,
            0.33445084767882677,
            0.806539157947923,
            1.2479273109678706,
            1.4814652847819647,
            1.1044176710743074,
            0.009571157244621346,
            0.21608000219494342,
            0.6698776546093198,
            1.1345041465109702,
            1.4522255996590465,
            1.3159707624463761,
            0.1777936592348958,
            0.1137294907230219,
            0.5338654194517105,
            1.0100800938334287,
            1.3896230854612082,
            1.4339716003552405,
            0.5704336868375967,
            0.036373307104964725,
            0.40176538568318676,
            0.878355953943193,
            1.3022053946772087,
            1.4796238907139816,
            0.9479809943072517,
            0.0002357864916681245,
            0.27739163177017645,
            0.742595638027126,
            1.196382777668441,
            1.4725587112856058,
            1.217354313179665
        ],
        "type": "scatter"
    }
]
, {
    "showlegend": true,
    "xaxis": {
        "showticklabels": true,
        "gridwidth": 0.5,
        "tickvals": [
            0.0,
            10.0,
            20.0,
            30.0,
            40.0,
            50.0,
            60.0
        ],
        "range": [
            0.0,
            60.0
        ],
        "domain": [
            0.05100612423447069,
            0.9934383202099737
        ],
        "mirror": false,
        "tickangle": 0,
        "showline": true,
        "ticktext": [
            "0",
            "10",
            "20",
            "30",
            "40",
            "50",
            "60"
        ],
        "zeroline": false,
        "tickfont": {
            "color": "rgba(0, 0, 0, 1.000)",
            "family": "sans-serif",
            "size": 11
        },
        "zerolinecolor": "rgba(0, 0, 0, 1.000)",
        "anchor": "y",
        "visible": true,
        "ticks": "inside",
        "tickmode": "array",
        "linecolor": "rgba(0, 0, 0, 1.000)",
        "showgrid": true,
        "title": "t",
        "gridcolor": "rgba(0, 0, 0, 0.100)",
        "titlefont": {
            "color": "rgba(0, 0, 0, 1.000)",
            "family": "sans-serif",
            "size": 15
        },
        "tickcolor": "rgb(0, 0, 0)",
        "type": "-"
    },
    "paper_bgcolor": "rgba(255, 255, 255, 1.000)",
    "annotations": [],
    "height": 400,
    "margin": {
        "l": 0,
        "b": 20,
        "r": 0,
        "t": 20
    },
    "plot_bgcolor": "rgba(255, 255, 255, 1.000)",
    "yaxis": {
        "showticklabels": true,
        "gridwidth": 0.5,
        "tickvals": [
            0.0,
            0.5,
            1.0,
            1.5
        ],
        "range": [
            -0.044443958543458936,
            1.5259092433254235
        ],
        "domain": [
            0.07581474190726165,
            0.9901574803149606
        ],
        "mirror": false,
        "tickangle": 0,
        "showline": true,
        "ticktext": [
            "0.0",
            "0.5",
            "1.0",
            "1.5"
        ],
        "zeroline": false,
        "tickfont": {
            "color": "rgba(0, 0, 0, 1.000)",
            "family": "sans-serif",
            "size": 11
        },
        "zerolinecolor": "rgba(0, 0, 0, 1.000)",
        "anchor": "x",
        "visible": true,
        "ticks": "inside",
        "tickmode": "array",
        "linecolor": "rgba(0, 0, 0, 1.000)",
        "showgrid": true,
        "title": "",
        "gridcolor": "rgba(0, 0, 0, 0.100)",
        "titlefont": {
            "color": "rgba(0, 0, 0, 1.000)",
            "family": "sans-serif",
            "size": 15
        },
        "tickcolor": "rgb(0, 0, 0)",
        "type": "-"
    },
    "legend_position": {
        "yanchor": "auto",
        "xanchor": "auto",
        "bordercolor": "rgba(0, 0, 0, 1.000)",
        "bgcolor": "rgba(255, 255, 255, 1.000)",
        "borderwidth": 1,
        "tracegroupgap": 0,
        "y": 1.0,
        "font": {
            "color": "rgba(0, 0, 0, 1.000)",
            "family": "sans-serif",
            "size": 11
        },
        "title": {
            "font": {
                "color": "rgba(0, 0, 0, 1.000)",
                "family": "sans-serif",
                "size": 15
            },
            "text": ""
        },
        "traceorder": "normal",
        "x": 1.0
    },
    "width": 600
}
);

    });
    </script>




# 2. scan: Example with parameters defined by a function

This model will be formatted as shown:
~~~julia 
function toyModel(dy,y,p,t)
	A=maximum([y[1],0])
	B=maximum([y[2],0])
	C=maximum([y[3],0])
	#A
	dy[1]= + paramFun("k1_Aexp",modify) - A * paramFun("k1_AtoB",modify)
	#B
	dy[2]= + A * paramFun("k1_AtoB",modify) - B * paramFun("k1_BtoC",modify)
	#C
	dy[3]= + B * paramFun("k1_BtoC",modify) - C * p(t)
end

~~~
An include file (scanIncludes.jl) will be created that looks like this:
~~~julia
    modify=Dict("k1_Aexp"=>1.0, "k1_AtoB"=>1.0, "k1_BtoC"=>1.0, )

    parameterList=Dict("k1_Aexp"=>1, "k1_AtoB"=>2, "k1_BtoC"=>3, )

    function paramFun(paramName,modify)
       return parameterList[paramName]*modify[paramName]
    end
~~~  
With this format parameters can be updated using the modify dictionary at run time:
~~~julia
    modify["k_binding"]=1.5
~~~


```julia
arguments=[reactionsFile, parametersFile, rateLawsFile,thisModelName,"scan"]
cmd=`python3 $locationOfCSV2Julia $arguments`

#lets run csv2julia (requires python to be installed)
run(cmd)

#     #if we need to fix species we can do it here
#     #include("variableNames.jl")
#     #indexToFix=findfirst(x->"L"==x,syms)
#     #fixSpecies(modelFile,modelFile,indexToFix)

#pop the outputs in a modelFiles folder
include(thisModelName)
include("variableNames.jl")
include("scanIncludes.jl")
```

    scan
    Running CSV2JuliaDiffEq with parameters left as a function call to paramFun(n), for all params. We will also create a paramFun.jl file that should be included and defines all parameters. If this is incorrect, please re-run with 5th argument set to 'inline' or 'param'
    Opening ratelaws.csv as rate law file
    Opening parameters.csv as parameters file
    Opening reactions.csv as reactions file
    parameters can now be modified by name.
    example to modify k_binding 1.5 fold higher:
    modify["k_binding"]=1.5



```julia
p=t->4
```




    #5 (generic function with 1 method)




```julia
y0=[1,0,0];
f=ODEFunction(toyModel,syms=Symbol.(syms));
prob=ODEProblem(f,y0,(0.0,maxTimeTC),p);
sol=solve(prob, abstol=1e-5,reltol=1e-3, saveat=1.0);
```


```julia
plot(sol)
```




    <div id="f3fffbe7-4c7e-4e73-8845-bb8820981d45" style="width:600px;height:400px;"></div>
    <script>
        requirejs.config({
        paths: {
            Plotly: 'https://cdn.plot.ly/plotly-1.57.1.min'
        }
    });
    require(['Plotly'], function (Plotly) {

        var PLOT = document.getElementById('f3fffbe7-4c7e-4e73-8845-bb8820981d45');
    Plotly.plot(PLOT, [
    {
        "xaxis": "x",
        "colorbar": {
            "title": ""
        },
        "yaxis": "y",
        "x": [
            0.0,
            1.0,
            2.0,
            3.0,
            4.0,
            5.0,
            6.0,
            7.0,
            8.0,
            9.0,
            10.0,
            11.0,
            12.0,
            13.0,
            14.0,
            15.0,
            16.0,
            17.0,
            18.0,
            19.0,
            20.0,
            21.0,
            22.0,
            23.0,
            24.0,
            25.0,
            26.0,
            27.0,
            28.0,
            29.0,
            30.0,
            31.0,
            32.0,
            33.0,
            34.0,
            35.0,
            36.0,
            37.0,
            38.0,
            39.0,
            40.0,
            41.0,
            42.0,
            43.0,
            44.0,
            45.0,
            46.0,
            47.0,
            48.0,
            49.0,
            50.0,
            51.0,
            52.0,
            53.0,
            54.0,
            55.0,
            56.0,
            57.0,
            58.0,
            59.0,
            60.0
        ],
        "showlegend": true,
        "mode": "lines",
        "name": "A(t)",
        "zmin": null,
        "legendgroup": "A(t)",
        "zmax": null,
        "line": {
            "color": "rgba(0, 154, 250, 1.000)",
            "shape": "linear",
            "dash": "solid",
            "width": 1
        },
        "y": [
            1.0,
            0.5676676903345341,
            0.5091572598472662,
            0.5012377881718262,
            0.5001698762656928,
            0.5000237099188003,
            0.5000038123886293,
            0.5000008974528145,
            0.5000001463031121,
            0.5000000294941155,
            0.5000000046173783,
            0.5000000006444594,
            0.5000000000881726,
            0.5000000000122427,
            0.5000000000017608,
            0.5000000000002617,
            0.5000000000000392,
            0.5000000000000013,
            0.49999999999999706,
            0.5000000000000003,
            0.5000000000000002,
            0.49999999999999994,
            0.49999999999999994,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5
        ],
        "type": "scatter"
    },
    {
        "xaxis": "x",
        "colorbar": {
            "title": ""
        },
        "yaxis": "y",
        "x": [
            0.0,
            1.0,
            2.0,
            3.0,
            4.0,
            5.0,
            6.0,
            7.0,
            8.0,
            9.0,
            10.0,
            11.0,
            12.0,
            13.0,
            14.0,
            15.0,
            16.0,
            17.0,
            18.0,
            19.0,
            20.0,
            21.0,
            22.0,
            23.0,
            24.0,
            25.0,
            26.0,
            27.0,
            28.0,
            29.0,
            30.0,
            31.0,
            32.0,
            33.0,
            34.0,
            35.0,
            36.0,
            37.0,
            38.0,
            39.0,
            40.0,
            41.0,
            42.0,
            43.0,
            44.0,
            45.0,
            46.0,
            47.0,
            48.0,
            49.0,
            50.0,
            51.0,
            52.0,
            53.0,
            54.0,
            55.0,
            56.0,
            57.0,
            58.0,
            59.0,
            60.0
        ],
        "showlegend": true,
        "mode": "lines",
        "name": "B(t)",
        "zmin": null,
        "legendgroup": "B(t)",
        "zmax": null,
        "line": {
            "color": "rgba(227, 111, 71, 1.000)",
            "shape": "linear",
            "dash": "solid",
            "width": 1
        },
        "y": [
            0.0,
            0.4022851497716823,
            0.34834383191099605,
            0.33564689692839894,
            0.33366155457482866,
            0.33337953177702306,
            0.3333404707011917,
            0.33333395939369276,
            0.33333318783132626,
            0.3333332156339718,
            0.33333327373624594,
            0.3333333275862302,
            0.3333333330368691,
            0.3333333333253166,
            0.33333333332927473,
            0.33333333333075577,
            0.33333333333246656,
            0.3333333333334792,
            0.3333333333334423,
            0.3333333333332901,
            0.33333333333331855,
            0.3333333333333433,
            0.3333333333333393,
            0.3333333333333328,
            0.33333333333333026,
            0.33333333333333165,
            0.3333333333333331,
            0.3333333333333338,
            0.33333333333333415,
            0.33333333333333404,
            0.3333333333333336,
            0.33333333333333337,
            0.33333333333333326,
            0.33333333333333315,
            0.33333333333333315,
            0.33333333333333315,
            0.3333333333333332,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333
        ],
        "type": "scatter"
    },
    {
        "xaxis": "x",
        "colorbar": {
            "title": ""
        },
        "yaxis": "y",
        "x": [
            0.0,
            1.0,
            2.0,
            3.0,
            4.0,
            5.0,
            6.0,
            7.0,
            8.0,
            9.0,
            10.0,
            11.0,
            12.0,
            13.0,
            14.0,
            15.0,
            16.0,
            17.0,
            18.0,
            19.0,
            20.0,
            21.0,
            22.0,
            23.0,
            24.0,
            25.0,
            26.0,
            27.0,
            28.0,
            29.0,
            30.0,
            31.0,
            32.0,
            33.0,
            34.0,
            35.0,
            36.0,
            37.0,
            38.0,
            39.0,
            40.0,
            41.0,
            42.0,
            43.0,
            44.0,
            45.0,
            46.0,
            47.0,
            48.0,
            49.0,
            50.0,
            51.0,
            52.0,
            53.0,
            54.0,
            55.0,
            56.0,
            57.0,
            58.0,
            59.0,
            60.0
        ],
        "showlegend": true,
        "mode": "lines",
        "name": "C(t)",
        "zmin": null,
        "legendgroup": "C(t)",
        "zmax": null,
        "line": {
            "color": "rgba(62, 164, 78, 1.000)",
            "shape": "linear",
            "dash": "solid",
            "width": 1
        },
        "y": [
            0.0,
            0.2950667450623204,
            0.2683154974425716,
            0.2532397671781439,
            0.2504774112138527,
            0.2500673347120312,
            0.25000728491625734,
            0.25004228120397476,
            0.25011191149825474,
            0.2501664481758583,
            0.25035103707094675,
            0.2500708849617151,
            0.24993005559709708,
            0.24993196960673403,
            0.2499849751724222,
            0.2500628665748835,
            0.25012846033008257,
            0.24996421614493375,
            0.24998357355498912,
            0.2500097784597622,
            0.25000224547944727,
            0.24999768829325947,
            0.2499989849237035,
            0.2500001870391864,
            0.2500006204141202,
            0.25000028504850474,
            0.2500000254898125,
            0.2499999029571158,
            0.24999985960563154,
            0.2499998954353597,
            0.24999997484557354,
            0.24999999603739734,
            0.250000011604376,
            0.25000002154650963,
            0.25000002586379805,
            0.25000002455624143,
            0.25000001762383967,
            0.2500000050665928,
            0.25000000232848585,
            0.250000000809424,
            0.2499999995204305,
            0.24999999846150547,
            0.24999999763264885,
            0.24999999703386067,
            0.24999999666514092,
            0.24999999652648958,
            0.24999999661790667,
            0.24999999693939218,
            0.24999999749094612,
            0.24999999827256847,
            0.24999999928425926,
            0.2499999998129677,
            0.2499999999648404,
            0.2500000000847711,
            0.2500000001727597,
            0.25000000022880625,
            0.2500000002529108,
            0.25000000024507335,
            0.25000000020529384,
            0.25000000013357226,
            0.25000000002990863
        ],
        "type": "scatter"
    }
]
, {
    "showlegend": true,
    "xaxis": {
        "showticklabels": true,
        "gridwidth": 0.5,
        "tickvals": [
            0.0,
            10.0,
            20.0,
            30.0,
            40.0,
            50.0,
            60.0
        ],
        "range": [
            0.0,
            60.0
        ],
        "domain": [
            0.0658209390492855,
            0.9934383202099738
        ],
        "mirror": false,
        "tickangle": 0,
        "showline": true,
        "ticktext": [
            "0",
            "10",
            "20",
            "30",
            "40",
            "50",
            "60"
        ],
        "zeroline": false,
        "tickfont": {
            "color": "rgba(0, 0, 0, 1.000)",
            "family": "sans-serif",
            "size": 11
        },
        "zerolinecolor": "rgba(0, 0, 0, 1.000)",
        "anchor": "y",
        "visible": true,
        "ticks": "inside",
        "tickmode": "array",
        "linecolor": "rgba(0, 0, 0, 1.000)",
        "showgrid": true,
        "title": "t",
        "gridcolor": "rgba(0, 0, 0, 0.100)",
        "titlefont": {
            "color": "rgba(0, 0, 0, 1.000)",
            "family": "sans-serif",
            "size": 15
        },
        "tickcolor": "rgb(0, 0, 0)",
        "type": "-"
    },
    "paper_bgcolor": "rgba(255, 255, 255, 1.000)",
    "annotations": [],
    "height": 400,
    "margin": {
        "l": 0,
        "b": 20,
        "r": 0,
        "t": 20
    },
    "plot_bgcolor": "rgba(255, 255, 255, 1.000)",
    "yaxis": {
        "showticklabels": true,
        "gridwidth": 0.5,
        "tickvals": [
            0.0,
            0.25,
            0.5,
            0.75,
            1.0
        ],
        "range": [
            -0.03,
            1.03
        ],
        "domain": [
            0.07581474190726165,
            0.9901574803149606
        ],
        "mirror": false,
        "tickangle": 0,
        "showline": true,
        "ticktext": [
            "0.00",
            "0.25",
            "0.50",
            "0.75",
            "1.00"
        ],
        "zeroline": false,
        "tickfont": {
            "color": "rgba(0, 0, 0, 1.000)",
            "family": "sans-serif",
            "size": 11
        },
        "zerolinecolor": "rgba(0, 0, 0, 1.000)",
        "anchor": "x",
        "visible": true,
        "ticks": "inside",
        "tickmode": "array",
        "linecolor": "rgba(0, 0, 0, 1.000)",
        "showgrid": true,
        "title": "",
        "gridcolor": "rgba(0, 0, 0, 0.100)",
        "titlefont": {
            "color": "rgba(0, 0, 0, 1.000)",
            "family": "sans-serif",
            "size": 15
        },
        "tickcolor": "rgb(0, 0, 0)",
        "type": "-"
    },
    "legend_position": {
        "yanchor": "auto",
        "xanchor": "auto",
        "bordercolor": "rgba(0, 0, 0, 1.000)",
        "bgcolor": "rgba(255, 255, 255, 1.000)",
        "borderwidth": 1,
        "tracegroupgap": 0,
        "y": 1.0,
        "font": {
            "color": "rgba(0, 0, 0, 1.000)",
            "family": "sans-serif",
            "size": 11
        },
        "title": {
            "font": {
                "color": "rgba(0, 0, 0, 1.000)",
                "family": "sans-serif",
                "size": 15
            },
            "text": ""
        },
        "traceorder": "normal",
        "x": 1.0
    },
    "width": 600
}
);

    });
    </script>





```julia
p=t->(1/(sin(t)+1))
```




    #7 (generic function with 1 method)




```julia
prob=ODEProblem(f,y0,(0.0,maxTimeTC),p);
timeTaken = @timed sol=solve(prob, abstol=1e-5,reltol=1e-3, saveat=1.0);
println("solved in: "*string(timeTaken.time))
```

    solved in: 4.28871762



```julia
plot(sol)
```




    <div id="0bd63b1e-0068-4e11-b03a-6fa1e79bf782" style="width:600px;height:400px;"></div>
    <script>
        requirejs.config({
        paths: {
            Plotly: 'https://cdn.plot.ly/plotly-1.57.1.min'
        }
    });
    require(['Plotly'], function (Plotly) {

        var PLOT = document.getElementById('0bd63b1e-0068-4e11-b03a-6fa1e79bf782');
    Plotly.plot(PLOT, [
    {
        "xaxis": "x",
        "colorbar": {
            "title": ""
        },
        "yaxis": "y",
        "x": [
            0.0,
            1.0,
            2.0,
            3.0,
            4.0,
            5.0,
            6.0,
            7.0,
            8.0,
            9.0,
            10.0,
            11.0,
            12.0,
            13.0,
            14.0,
            15.0,
            16.0,
            17.0,
            18.0,
            19.0,
            20.0,
            21.0,
            22.0,
            23.0,
            24.0,
            25.0,
            26.0,
            27.0,
            28.0,
            29.0,
            30.0,
            31.0,
            32.0,
            33.0,
            34.0,
            35.0,
            36.0,
            37.0,
            38.0,
            39.0,
            40.0,
            41.0,
            42.0,
            43.0,
            44.0,
            45.0,
            46.0,
            47.0,
            48.0,
            49.0,
            50.0,
            51.0,
            52.0,
            53.0,
            54.0,
            55.0,
            56.0,
            57.0,
            58.0,
            59.0,
            60.0
        ],
        "showlegend": true,
        "mode": "lines",
        "name": "A(t)",
        "zmin": null,
        "legendgroup": "A(t)",
        "zmax": null,
        "line": {
            "color": "rgba(0, 154, 250, 1.000)",
            "shape": "linear",
            "dash": "solid",
            "width": 1
        },
        "y": [
            1.0,
            0.5676671607638394,
            0.5091569824481709,
            0.5012376155725479,
            0.5001686729636938,
            0.5000228279478443,
            0.5000030892292263,
            0.5000004145985629,
            0.5000000533708883,
            0.5000000087774074,
            0.5000000013770078,
            0.5000000001871151,
            0.5000000000253233,
            0.5000000000034178,
            0.5000000000004324,
            0.5000000000000668,
            0.5000000000000105,
            0.5000000000000016,
            0.5000000000000003,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5
        ],
        "type": "scatter"
    },
    {
        "xaxis": "x",
        "colorbar": {
            "title": ""
        },
        "yaxis": "y",
        "x": [
            0.0,
            1.0,
            2.0,
            3.0,
            4.0,
            5.0,
            6.0,
            7.0,
            8.0,
            9.0,
            10.0,
            11.0,
            12.0,
            13.0,
            14.0,
            15.0,
            16.0,
            17.0,
            18.0,
            19.0,
            20.0,
            21.0,
            22.0,
            23.0,
            24.0,
            25.0,
            26.0,
            27.0,
            28.0,
            29.0,
            30.0,
            31.0,
            32.0,
            33.0,
            34.0,
            35.0,
            36.0,
            37.0,
            38.0,
            39.0,
            40.0,
            41.0,
            42.0,
            43.0,
            44.0,
            45.0,
            46.0,
            47.0,
            48.0,
            49.0,
            50.0,
            51.0,
            52.0,
            53.0,
            54.0,
            55.0,
            56.0,
            57.0,
            58.0,
            59.0,
            60.0
        ],
        "showlegend": true,
        "mode": "lines",
        "name": "B(t)",
        "zmin": null,
        "legendgroup": "B(t)",
        "zmax": null,
        "line": {
            "color": "rgba(227, 111, 71, 1.000)",
            "shape": "linear",
            "dash": "solid",
            "width": 1
        },
        "y": [
            0.0,
            0.4022895569866244,
            0.34834578011852496,
            0.33564702812997205,
            0.3336611711878937,
            0.3333785156732723,
            0.3333394882343248,
            0.3333341615189801,
            0.33333344009786076,
            0.3333333508742868,
            0.3333333360759182,
            0.3333333337069441,
            0.3333333333839492,
            0.33333333334016746,
            0.333333333334198,
            0.3333333333334669,
            0.3333333333333545,
            0.33333333333333653,
            0.33333333333333387,
            0.33333333333333337,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333
        ],
        "type": "scatter"
    },
    {
        "xaxis": "x",
        "colorbar": {
            "title": ""
        },
        "yaxis": "y",
        "x": [
            0.0,
            1.0,
            2.0,
            3.0,
            4.0,
            5.0,
            6.0,
            7.0,
            8.0,
            9.0,
            10.0,
            11.0,
            12.0,
            13.0,
            14.0,
            15.0,
            16.0,
            17.0,
            18.0,
            19.0,
            20.0,
            21.0,
            22.0,
            23.0,
            24.0,
            25.0,
            26.0,
            27.0,
            28.0,
            29.0,
            30.0,
            31.0,
            32.0,
            33.0,
            34.0,
            35.0,
            36.0,
            37.0,
            38.0,
            39.0,
            40.0,
            41.0,
            42.0,
            43.0,
            44.0,
            45.0,
            46.0,
            47.0,
            48.0,
            49.0,
            50.0,
            51.0,
            52.0,
            53.0,
            54.0,
            55.0,
            56.0,
            57.0,
            58.0,
            59.0,
            60.0
        ],
        "showlegend": true,
        "mode": "lines",
        "name": "C(t)",
        "zmin": null,
        "legendgroup": "C(t)",
        "zmax": null,
        "line": {
            "color": "rgba(62, 164, 78, 1.000)",
            "shape": "linear",
            "dash": "solid",
            "width": 1
        },
        "y": [
            0.0,
            0.8024469597292148,
            1.3479290597831097,
            1.432317976589997,
            0.5976336148596422,
            0.03267699378269493,
            0.393733877358387,
            0.8699673619978687,
            1.2960755499165333,
            1.4804801921934945,
            0.9677920554497718,
            1.6059665102947496e-5,
            0.2699772396204259,
            0.7340425241153498,
            1.18929488057771,
            1.4708004856545513,
            1.231224587104982,
            0.06183370065318904,
            0.15924103214163504,
            0.5973404373422602,
            1.0695235959910006,
            1.4225264343745883,
            1.3889618581592522,
            0.3762188494142472,
            0.06874530174209935,
            0.4629753890065269,
            0.9407972808412058,
            1.3458404764701748,
            1.4654830447268699,
            0.7830623583775712,
            0.010452597372125293,
            0.33445084767882677,
            0.806539157947923,
            1.2479273109678706,
            1.4814652847819647,
            1.1044176710743074,
            0.009571157244621346,
            0.21608000219494342,
            0.6698776546093198,
            1.1345041465109702,
            1.4522255996590465,
            1.3159707624463761,
            0.1777936592348958,
            0.1137294907230219,
            0.5338654194517105,
            1.0100800938334287,
            1.3896230854612082,
            1.4339716003552405,
            0.5704336868375967,
            0.036373307104964725,
            0.40176538568318676,
            0.878355953943193,
            1.3022053946772087,
            1.4796238907139816,
            0.9479809943072517,
            0.0002357864916681245,
            0.27739163177017645,
            0.742595638027126,
            1.196382777668441,
            1.4725587112856058,
            1.217354313179665
        ],
        "type": "scatter"
    }
]
, {
    "showlegend": true,
    "xaxis": {
        "showticklabels": true,
        "gridwidth": 0.5,
        "tickvals": [
            0.0,
            10.0,
            20.0,
            30.0,
            40.0,
            50.0,
            60.0
        ],
        "range": [
            0.0,
            60.0
        ],
        "domain": [
            0.05100612423447069,
            0.9934383202099737
        ],
        "mirror": false,
        "tickangle": 0,
        "showline": true,
        "ticktext": [
            "0",
            "10",
            "20",
            "30",
            "40",
            "50",
            "60"
        ],
        "zeroline": false,
        "tickfont": {
            "color": "rgba(0, 0, 0, 1.000)",
            "family": "sans-serif",
            "size": 11
        },
        "zerolinecolor": "rgba(0, 0, 0, 1.000)",
        "anchor": "y",
        "visible": true,
        "ticks": "inside",
        "tickmode": "array",
        "linecolor": "rgba(0, 0, 0, 1.000)",
        "showgrid": true,
        "title": "t",
        "gridcolor": "rgba(0, 0, 0, 0.100)",
        "titlefont": {
            "color": "rgba(0, 0, 0, 1.000)",
            "family": "sans-serif",
            "size": 15
        },
        "tickcolor": "rgb(0, 0, 0)",
        "type": "-"
    },
    "paper_bgcolor": "rgba(255, 255, 255, 1.000)",
    "annotations": [],
    "height": 400,
    "margin": {
        "l": 0,
        "b": 20,
        "r": 0,
        "t": 20
    },
    "plot_bgcolor": "rgba(255, 255, 255, 1.000)",
    "yaxis": {
        "showticklabels": true,
        "gridwidth": 0.5,
        "tickvals": [
            0.0,
            0.5,
            1.0,
            1.5
        ],
        "range": [
            -0.044443958543458936,
            1.5259092433254235
        ],
        "domain": [
            0.07581474190726165,
            0.9901574803149606
        ],
        "mirror": false,
        "tickangle": 0,
        "showline": true,
        "ticktext": [
            "0.0",
            "0.5",
            "1.0",
            "1.5"
        ],
        "zeroline": false,
        "tickfont": {
            "color": "rgba(0, 0, 0, 1.000)",
            "family": "sans-serif",
            "size": 11
        },
        "zerolinecolor": "rgba(0, 0, 0, 1.000)",
        "anchor": "x",
        "visible": true,
        "ticks": "inside",
        "tickmode": "array",
        "linecolor": "rgba(0, 0, 0, 1.000)",
        "showgrid": true,
        "title": "",
        "gridcolor": "rgba(0, 0, 0, 0.100)",
        "titlefont": {
            "color": "rgba(0, 0, 0, 1.000)",
            "family": "sans-serif",
            "size": 15
        },
        "tickcolor": "rgb(0, 0, 0)",
        "type": "-"
    },
    "legend_position": {
        "yanchor": "auto",
        "xanchor": "auto",
        "bordercolor": "rgba(0, 0, 0, 1.000)",
        "bgcolor": "rgba(255, 255, 255, 1.000)",
        "borderwidth": 1,
        "tracegroupgap": 0,
        "y": 1.0,
        "font": {
            "color": "rgba(0, 0, 0, 1.000)",
            "family": "sans-serif",
            "size": 11
        },
        "title": {
            "font": {
                "color": "rgba(0, 0, 0, 1.000)",
                "family": "sans-serif",
                "size": 15
            },
            "text": ""
        },
        "traceorder": "normal",
        "x": 1.0
    },
    "width": 600
}
);

    });
    </script>




# 3. params: Example with parameters defined by a list

For this version we need to slightly tweak the reactions file so that time dependent variables are defined in line. The file will look like this:


| Parameter | Value |
| ---| --- |
|k1_Aexp|1|
|k1_AtoB|2|
|k1_BtoC|3|
|k1_Cdeg|**t->tdfunc(t)**|


(see parametersTD.csv)

This model will be formatted as shown:
~~~julia
    function toyModel(dy,y,p,t)
        A=maximum([y[1],0])
        B=maximum([y[2],0])
        C=maximum([y[3],0])
        #A
        dy[1]= + p[1] - A * p[2]
        #B
        dy[2]= + A * p[2] - B * p[3]
        #C
        dy[3]= + B * p[3] - C * p[4](t)
    end
~~~

An include file (scanIncludes.jl) will be created that looks like this:
~~~julia
    paramVals=[
    1 #p[0] is k1_Aexp
    2 #p[1] is k1_AtoB
    3 #p[2] is k1_BtoC
    t->tdfunc(t) #p[3] is k1_Cdeg
    ]

    parameterNameList=["k1_Aexp" #parameterNameList[0]=1
    "k1_AtoB" #parameterNameList[1]=2
    "k1_BtoC" #parameterNameList[2]=3
    "k1_Cdeg" #parameterNameList[3]=t->tdfunc(t)
    ]
~~~  
With this format parameters can be updated using the above two variables at run time:
~~~julia
    indexOfParam=findfirst(x->"k_binding"==x,parameterNameList)
    paramVals[indexOfParam]=paramVals[indexOfParam]*1.5
~~~


```julia
parametersFile="parametersTD.csv"
```




    "parametersTD.csv"



This is an example of how to defined a time dependent variable. Please note that this *cannot* be called 'p' because that is used for the entire parameters variable inside the ODE file. The first example is just a constant variable, below we'll give an example that is time dependent. 


```julia
tdfunc=t->4
```




    #9 (generic function with 1 method)




```julia
arguments=[reactionsFile, parametersFile, rateLawsFile,thisModelName,"param"]
cmd=`python3 $locationOfCSV2Julia $arguments`

#lets run csv2julia (requires python to be installed)
run(cmd)

#     #if we need to fix species we can do it here
#     #include("variableNames.jl")
#     #indexToFix=findfirst(x->"L"==x,syms)
#     #fixSpecies(modelFile,modelFile,indexToFix)

#pop the outputs in a modelFiles folder
include(thisModelName)
include("variableNames.jl")
include("scanIncludes.jl")
```

    param
    Running CSV2JuliaDiffEq with parameters dynamically determined by a variable, re-run with the 5th argument set to 'scan' or 'inline'
    Opening ratelaws.csv as rate law file
    Opening parametersTD.csv as parameters file
    Opening reactions.csv as reactions file
    parameters can now be searched in parameterNameList by name.
    example to modify k_binding 1.5 fold higher:
    indexOfParam=findfirst(x->"k_binding"==x,parameterNameList)
    paramVals[indexOfParam]=paramVals[indexOfParam]*1.5



```julia
y0=[1,0,0];
f=ODEFunction(toyModel,syms=Symbol.(syms));
prob=ODEProblem(f,y0,(0.0,maxTimeTC),paramVals);
sol=solve(prob, abstol=1e-5,reltol=1e-3, saveat=1.0);
```


```julia
plot(sol)
```




    <div id="8bf28c82-e6e8-413f-99e6-8e7755c31b6d" style="width:600px;height:400px;"></div>
    <script>
        requirejs.config({
        paths: {
            Plotly: 'https://cdn.plot.ly/plotly-1.57.1.min'
        }
    });
    require(['Plotly'], function (Plotly) {

        var PLOT = document.getElementById('8bf28c82-e6e8-413f-99e6-8e7755c31b6d');
    Plotly.plot(PLOT, [
    {
        "xaxis": "x",
        "colorbar": {
            "title": ""
        },
        "yaxis": "y",
        "x": [
            0.0,
            1.0,
            2.0,
            3.0,
            4.0,
            5.0,
            6.0,
            7.0,
            8.0,
            9.0,
            10.0,
            11.0,
            12.0,
            13.0,
            14.0,
            15.0,
            16.0,
            17.0,
            18.0,
            19.0,
            20.0,
            21.0,
            22.0,
            23.0,
            24.0,
            25.0,
            26.0,
            27.0,
            28.0,
            29.0,
            30.0,
            31.0,
            32.0,
            33.0,
            34.0,
            35.0,
            36.0,
            37.0,
            38.0,
            39.0,
            40.0,
            41.0,
            42.0,
            43.0,
            44.0,
            45.0,
            46.0,
            47.0,
            48.0,
            49.0,
            50.0,
            51.0,
            52.0,
            53.0,
            54.0,
            55.0,
            56.0,
            57.0,
            58.0,
            59.0,
            60.0
        ],
        "showlegend": true,
        "mode": "lines",
        "name": "A(t)",
        "zmin": null,
        "legendgroup": "A(t)",
        "zmax": null,
        "line": {
            "color": "rgba(0, 154, 250, 1.000)",
            "shape": "linear",
            "dash": "solid",
            "width": 1
        },
        "y": [
            1.0,
            0.5676676903345341,
            0.5091572598472662,
            0.5012377881718262,
            0.5001698762656928,
            0.5000237099188003,
            0.5000038123886293,
            0.5000008974528145,
            0.5000001463031121,
            0.5000000294941155,
            0.5000000046173783,
            0.5000000006444594,
            0.5000000000881726,
            0.5000000000122427,
            0.5000000000017608,
            0.5000000000002617,
            0.5000000000000392,
            0.5000000000000013,
            0.49999999999999706,
            0.5000000000000003,
            0.5000000000000002,
            0.49999999999999994,
            0.49999999999999994,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5
        ],
        "type": "scatter"
    },
    {
        "xaxis": "x",
        "colorbar": {
            "title": ""
        },
        "yaxis": "y",
        "x": [
            0.0,
            1.0,
            2.0,
            3.0,
            4.0,
            5.0,
            6.0,
            7.0,
            8.0,
            9.0,
            10.0,
            11.0,
            12.0,
            13.0,
            14.0,
            15.0,
            16.0,
            17.0,
            18.0,
            19.0,
            20.0,
            21.0,
            22.0,
            23.0,
            24.0,
            25.0,
            26.0,
            27.0,
            28.0,
            29.0,
            30.0,
            31.0,
            32.0,
            33.0,
            34.0,
            35.0,
            36.0,
            37.0,
            38.0,
            39.0,
            40.0,
            41.0,
            42.0,
            43.0,
            44.0,
            45.0,
            46.0,
            47.0,
            48.0,
            49.0,
            50.0,
            51.0,
            52.0,
            53.0,
            54.0,
            55.0,
            56.0,
            57.0,
            58.0,
            59.0,
            60.0
        ],
        "showlegend": true,
        "mode": "lines",
        "name": "B(t)",
        "zmin": null,
        "legendgroup": "B(t)",
        "zmax": null,
        "line": {
            "color": "rgba(227, 111, 71, 1.000)",
            "shape": "linear",
            "dash": "solid",
            "width": 1
        },
        "y": [
            0.0,
            0.4022851497716823,
            0.34834383191099605,
            0.33564689692839894,
            0.33366155457482866,
            0.33337953177702306,
            0.3333404707011917,
            0.33333395939369276,
            0.33333318783132626,
            0.3333332156339718,
            0.33333327373624594,
            0.3333333275862302,
            0.3333333330368691,
            0.3333333333253166,
            0.33333333332927473,
            0.33333333333075577,
            0.33333333333246656,
            0.3333333333334792,
            0.3333333333334423,
            0.3333333333332901,
            0.33333333333331855,
            0.3333333333333433,
            0.3333333333333393,
            0.3333333333333328,
            0.33333333333333026,
            0.33333333333333165,
            0.3333333333333331,
            0.3333333333333338,
            0.33333333333333415,
            0.33333333333333404,
            0.3333333333333336,
            0.33333333333333337,
            0.33333333333333326,
            0.33333333333333315,
            0.33333333333333315,
            0.33333333333333315,
            0.3333333333333332,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333
        ],
        "type": "scatter"
    },
    {
        "xaxis": "x",
        "colorbar": {
            "title": ""
        },
        "yaxis": "y",
        "x": [
            0.0,
            1.0,
            2.0,
            3.0,
            4.0,
            5.0,
            6.0,
            7.0,
            8.0,
            9.0,
            10.0,
            11.0,
            12.0,
            13.0,
            14.0,
            15.0,
            16.0,
            17.0,
            18.0,
            19.0,
            20.0,
            21.0,
            22.0,
            23.0,
            24.0,
            25.0,
            26.0,
            27.0,
            28.0,
            29.0,
            30.0,
            31.0,
            32.0,
            33.0,
            34.0,
            35.0,
            36.0,
            37.0,
            38.0,
            39.0,
            40.0,
            41.0,
            42.0,
            43.0,
            44.0,
            45.0,
            46.0,
            47.0,
            48.0,
            49.0,
            50.0,
            51.0,
            52.0,
            53.0,
            54.0,
            55.0,
            56.0,
            57.0,
            58.0,
            59.0,
            60.0
        ],
        "showlegend": true,
        "mode": "lines",
        "name": "C(t)",
        "zmin": null,
        "legendgroup": "C(t)",
        "zmax": null,
        "line": {
            "color": "rgba(62, 164, 78, 1.000)",
            "shape": "linear",
            "dash": "solid",
            "width": 1
        },
        "y": [
            0.0,
            0.2950667450623204,
            0.2683154974425716,
            0.2532397671781439,
            0.2504774112138527,
            0.2500673347120312,
            0.25000728491625734,
            0.25004228120397476,
            0.25011191149825474,
            0.2501664481758583,
            0.25035103707094675,
            0.2500708849617151,
            0.24993005559709708,
            0.24993196960673403,
            0.2499849751724222,
            0.2500628665748835,
            0.25012846033008257,
            0.24996421614493375,
            0.24998357355498912,
            0.2500097784597622,
            0.25000224547944727,
            0.24999768829325947,
            0.2499989849237035,
            0.2500001870391864,
            0.2500006204141202,
            0.25000028504850474,
            0.2500000254898125,
            0.2499999029571158,
            0.24999985960563154,
            0.2499998954353597,
            0.24999997484557354,
            0.24999999603739734,
            0.250000011604376,
            0.25000002154650963,
            0.25000002586379805,
            0.25000002455624143,
            0.25000001762383967,
            0.2500000050665928,
            0.25000000232848585,
            0.250000000809424,
            0.2499999995204305,
            0.24999999846150547,
            0.24999999763264885,
            0.24999999703386067,
            0.24999999666514092,
            0.24999999652648958,
            0.24999999661790667,
            0.24999999693939218,
            0.24999999749094612,
            0.24999999827256847,
            0.24999999928425926,
            0.2499999998129677,
            0.2499999999648404,
            0.2500000000847711,
            0.2500000001727597,
            0.25000000022880625,
            0.2500000002529108,
            0.25000000024507335,
            0.25000000020529384,
            0.25000000013357226,
            0.25000000002990863
        ],
        "type": "scatter"
    }
]
, {
    "showlegend": true,
    "xaxis": {
        "showticklabels": true,
        "gridwidth": 0.5,
        "tickvals": [
            0.0,
            10.0,
            20.0,
            30.0,
            40.0,
            50.0,
            60.0
        ],
        "range": [
            0.0,
            60.0
        ],
        "domain": [
            0.0658209390492855,
            0.9934383202099738
        ],
        "mirror": false,
        "tickangle": 0,
        "showline": true,
        "ticktext": [
            "0",
            "10",
            "20",
            "30",
            "40",
            "50",
            "60"
        ],
        "zeroline": false,
        "tickfont": {
            "color": "rgba(0, 0, 0, 1.000)",
            "family": "sans-serif",
            "size": 11
        },
        "zerolinecolor": "rgba(0, 0, 0, 1.000)",
        "anchor": "y",
        "visible": true,
        "ticks": "inside",
        "tickmode": "array",
        "linecolor": "rgba(0, 0, 0, 1.000)",
        "showgrid": true,
        "title": "t",
        "gridcolor": "rgba(0, 0, 0, 0.100)",
        "titlefont": {
            "color": "rgba(0, 0, 0, 1.000)",
            "family": "sans-serif",
            "size": 15
        },
        "tickcolor": "rgb(0, 0, 0)",
        "type": "-"
    },
    "paper_bgcolor": "rgba(255, 255, 255, 1.000)",
    "annotations": [],
    "height": 400,
    "margin": {
        "l": 0,
        "b": 20,
        "r": 0,
        "t": 20
    },
    "plot_bgcolor": "rgba(255, 255, 255, 1.000)",
    "yaxis": {
        "showticklabels": true,
        "gridwidth": 0.5,
        "tickvals": [
            0.0,
            0.25,
            0.5,
            0.75,
            1.0
        ],
        "range": [
            -0.03,
            1.03
        ],
        "domain": [
            0.07581474190726165,
            0.9901574803149606
        ],
        "mirror": false,
        "tickangle": 0,
        "showline": true,
        "ticktext": [
            "0.00",
            "0.25",
            "0.50",
            "0.75",
            "1.00"
        ],
        "zeroline": false,
        "tickfont": {
            "color": "rgba(0, 0, 0, 1.000)",
            "family": "sans-serif",
            "size": 11
        },
        "zerolinecolor": "rgba(0, 0, 0, 1.000)",
        "anchor": "x",
        "visible": true,
        "ticks": "inside",
        "tickmode": "array",
        "linecolor": "rgba(0, 0, 0, 1.000)",
        "showgrid": true,
        "title": "",
        "gridcolor": "rgba(0, 0, 0, 0.100)",
        "titlefont": {
            "color": "rgba(0, 0, 0, 1.000)",
            "family": "sans-serif",
            "size": 15
        },
        "tickcolor": "rgb(0, 0, 0)",
        "type": "-"
    },
    "legend_position": {
        "yanchor": "auto",
        "xanchor": "auto",
        "bordercolor": "rgba(0, 0, 0, 1.000)",
        "bgcolor": "rgba(255, 255, 255, 1.000)",
        "borderwidth": 1,
        "tracegroupgap": 0,
        "y": 1.0,
        "font": {
            "color": "rgba(0, 0, 0, 1.000)",
            "family": "sans-serif",
            "size": 11
        },
        "title": {
            "font": {
                "color": "rgba(0, 0, 0, 1.000)",
                "family": "sans-serif",
                "size": 15
            },
            "text": ""
        },
        "traceorder": "normal",
        "x": 1.0
    },
    "width": 600
}
);

    });
    </script>




This is an example of re-solving with a time dependent variable:


```julia
tdfunc=t->(1/(sin(t)+1))
```




    #13 (generic function with 1 method)




```julia
prob=ODEProblem(f,y0,(0.0,maxTimeTC),paramVals);
timeTaken = @timed sol=solve(prob, abstol=1e-5,reltol=1e-3, saveat=1.0);
println("solved in: "*string(timeTaken.time))
```

    solved in: 0.022777966



```julia
plot(sol)
```




    <div id="e0bb73a9-729a-477a-b0a5-81d61c604cc9" style="width:600px;height:400px;"></div>
    <script>
        requirejs.config({
        paths: {
            Plotly: 'https://cdn.plot.ly/plotly-1.57.1.min'
        }
    });
    require(['Plotly'], function (Plotly) {

        var PLOT = document.getElementById('e0bb73a9-729a-477a-b0a5-81d61c604cc9');
    Plotly.plot(PLOT, [
    {
        "xaxis": "x",
        "colorbar": {
            "title": ""
        },
        "yaxis": "y",
        "x": [
            0.0,
            1.0,
            2.0,
            3.0,
            4.0,
            5.0,
            6.0,
            7.0,
            8.0,
            9.0,
            10.0,
            11.0,
            12.0,
            13.0,
            14.0,
            15.0,
            16.0,
            17.0,
            18.0,
            19.0,
            20.0,
            21.0,
            22.0,
            23.0,
            24.0,
            25.0,
            26.0,
            27.0,
            28.0,
            29.0,
            30.0,
            31.0,
            32.0,
            33.0,
            34.0,
            35.0,
            36.0,
            37.0,
            38.0,
            39.0,
            40.0,
            41.0,
            42.0,
            43.0,
            44.0,
            45.0,
            46.0,
            47.0,
            48.0,
            49.0,
            50.0,
            51.0,
            52.0,
            53.0,
            54.0,
            55.0,
            56.0,
            57.0,
            58.0,
            59.0,
            60.0
        ],
        "showlegend": true,
        "mode": "lines",
        "name": "A(t)",
        "zmin": null,
        "legendgroup": "A(t)",
        "zmax": null,
        "line": {
            "color": "rgba(0, 154, 250, 1.000)",
            "shape": "linear",
            "dash": "solid",
            "width": 1
        },
        "y": [
            1.0,
            0.5676671607638394,
            0.5091569824481709,
            0.5012376155725479,
            0.5001686729636938,
            0.5000228279478443,
            0.5000030892292263,
            0.5000004145985629,
            0.5000000533708883,
            0.5000000087774074,
            0.5000000013770078,
            0.5000000001871151,
            0.5000000000253233,
            0.5000000000034178,
            0.5000000000004324,
            0.5000000000000668,
            0.5000000000000105,
            0.5000000000000016,
            0.5000000000000003,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5
        ],
        "type": "scatter"
    },
    {
        "xaxis": "x",
        "colorbar": {
            "title": ""
        },
        "yaxis": "y",
        "x": [
            0.0,
            1.0,
            2.0,
            3.0,
            4.0,
            5.0,
            6.0,
            7.0,
            8.0,
            9.0,
            10.0,
            11.0,
            12.0,
            13.0,
            14.0,
            15.0,
            16.0,
            17.0,
            18.0,
            19.0,
            20.0,
            21.0,
            22.0,
            23.0,
            24.0,
            25.0,
            26.0,
            27.0,
            28.0,
            29.0,
            30.0,
            31.0,
            32.0,
            33.0,
            34.0,
            35.0,
            36.0,
            37.0,
            38.0,
            39.0,
            40.0,
            41.0,
            42.0,
            43.0,
            44.0,
            45.0,
            46.0,
            47.0,
            48.0,
            49.0,
            50.0,
            51.0,
            52.0,
            53.0,
            54.0,
            55.0,
            56.0,
            57.0,
            58.0,
            59.0,
            60.0
        ],
        "showlegend": true,
        "mode": "lines",
        "name": "B(t)",
        "zmin": null,
        "legendgroup": "B(t)",
        "zmax": null,
        "line": {
            "color": "rgba(227, 111, 71, 1.000)",
            "shape": "linear",
            "dash": "solid",
            "width": 1
        },
        "y": [
            0.0,
            0.4022895569866244,
            0.34834578011852496,
            0.33564702812997205,
            0.3336611711878937,
            0.3333785156732723,
            0.3333394882343248,
            0.3333341615189801,
            0.33333344009786076,
            0.3333333508742868,
            0.3333333360759182,
            0.3333333337069441,
            0.3333333333839492,
            0.33333333334016746,
            0.333333333334198,
            0.3333333333334669,
            0.3333333333333545,
            0.33333333333333653,
            0.33333333333333387,
            0.33333333333333337,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333,
            0.3333333333333333
        ],
        "type": "scatter"
    },
    {
        "xaxis": "x",
        "colorbar": {
            "title": ""
        },
        "yaxis": "y",
        "x": [
            0.0,
            1.0,
            2.0,
            3.0,
            4.0,
            5.0,
            6.0,
            7.0,
            8.0,
            9.0,
            10.0,
            11.0,
            12.0,
            13.0,
            14.0,
            15.0,
            16.0,
            17.0,
            18.0,
            19.0,
            20.0,
            21.0,
            22.0,
            23.0,
            24.0,
            25.0,
            26.0,
            27.0,
            28.0,
            29.0,
            30.0,
            31.0,
            32.0,
            33.0,
            34.0,
            35.0,
            36.0,
            37.0,
            38.0,
            39.0,
            40.0,
            41.0,
            42.0,
            43.0,
            44.0,
            45.0,
            46.0,
            47.0,
            48.0,
            49.0,
            50.0,
            51.0,
            52.0,
            53.0,
            54.0,
            55.0,
            56.0,
            57.0,
            58.0,
            59.0,
            60.0
        ],
        "showlegend": true,
        "mode": "lines",
        "name": "C(t)",
        "zmin": null,
        "legendgroup": "C(t)",
        "zmax": null,
        "line": {
            "color": "rgba(62, 164, 78, 1.000)",
            "shape": "linear",
            "dash": "solid",
            "width": 1
        },
        "y": [
            0.0,
            0.8024469597292148,
            1.3479290597831097,
            1.432317976589997,
            0.5976336148596422,
            0.03267699378269493,
            0.393733877358387,
            0.8699673619978687,
            1.2960755499165333,
            1.4804801921934945,
            0.9677920554497718,
            1.6059665102947496e-5,
            0.2699772396204259,
            0.7340425241153498,
            1.18929488057771,
            1.4708004856545513,
            1.231224587104982,
            0.06183370065318904,
            0.15924103214163504,
            0.5973404373422602,
            1.0695235959910006,
            1.4225264343745883,
            1.3889618581592522,
            0.3762188494142472,
            0.06874530174209935,
            0.4629753890065269,
            0.9407972808412058,
            1.3458404764701748,
            1.4654830447268699,
            0.7830623583775712,
            0.010452597372125293,
            0.33445084767882677,
            0.806539157947923,
            1.2479273109678706,
            1.4814652847819647,
            1.1044176710743074,
            0.009571157244621346,
            0.21608000219494342,
            0.6698776546093198,
            1.1345041465109702,
            1.4522255996590465,
            1.3159707624463761,
            0.1777936592348958,
            0.1137294907230219,
            0.5338654194517105,
            1.0100800938334287,
            1.3896230854612082,
            1.4339716003552405,
            0.5704336868375967,
            0.036373307104964725,
            0.40176538568318676,
            0.878355953943193,
            1.3022053946772087,
            1.4796238907139816,
            0.9479809943072517,
            0.0002357864916681245,
            0.27739163177017645,
            0.742595638027126,
            1.196382777668441,
            1.4725587112856058,
            1.217354313179665
        ],
        "type": "scatter"
    }
]
, {
    "showlegend": true,
    "xaxis": {
        "showticklabels": true,
        "gridwidth": 0.5,
        "tickvals": [
            0.0,
            10.0,
            20.0,
            30.0,
            40.0,
            50.0,
            60.0
        ],
        "range": [
            0.0,
            60.0
        ],
        "domain": [
            0.05100612423447069,
            0.9934383202099737
        ],
        "mirror": false,
        "tickangle": 0,
        "showline": true,
        "ticktext": [
            "0",
            "10",
            "20",
            "30",
            "40",
            "50",
            "60"
        ],
        "zeroline": false,
        "tickfont": {
            "color": "rgba(0, 0, 0, 1.000)",
            "family": "sans-serif",
            "size": 11
        },
        "zerolinecolor": "rgba(0, 0, 0, 1.000)",
        "anchor": "y",
        "visible": true,
        "ticks": "inside",
        "tickmode": "array",
        "linecolor": "rgba(0, 0, 0, 1.000)",
        "showgrid": true,
        "title": "t",
        "gridcolor": "rgba(0, 0, 0, 0.100)",
        "titlefont": {
            "color": "rgba(0, 0, 0, 1.000)",
            "family": "sans-serif",
            "size": 15
        },
        "tickcolor": "rgb(0, 0, 0)",
        "type": "-"
    },
    "paper_bgcolor": "rgba(255, 255, 255, 1.000)",
    "annotations": [],
    "height": 400,
    "margin": {
        "l": 0,
        "b": 20,
        "r": 0,
        "t": 20
    },
    "plot_bgcolor": "rgba(255, 255, 255, 1.000)",
    "yaxis": {
        "showticklabels": true,
        "gridwidth": 0.5,
        "tickvals": [
            0.0,
            0.5,
            1.0,
            1.5
        ],
        "range": [
            -0.044443958543458936,
            1.5259092433254235
        ],
        "domain": [
            0.07581474190726165,
            0.9901574803149606
        ],
        "mirror": false,
        "tickangle": 0,
        "showline": true,
        "ticktext": [
            "0.0",
            "0.5",
            "1.0",
            "1.5"
        ],
        "zeroline": false,
        "tickfont": {
            "color": "rgba(0, 0, 0, 1.000)",
            "family": "sans-serif",
            "size": 11
        },
        "zerolinecolor": "rgba(0, 0, 0, 1.000)",
        "anchor": "x",
        "visible": true,
        "ticks": "inside",
        "tickmode": "array",
        "linecolor": "rgba(0, 0, 0, 1.000)",
        "showgrid": true,
        "title": "",
        "gridcolor": "rgba(0, 0, 0, 0.100)",
        "titlefont": {
            "color": "rgba(0, 0, 0, 1.000)",
            "family": "sans-serif",
            "size": 15
        },
        "tickcolor": "rgb(0, 0, 0)",
        "type": "-"
    },
    "legend_position": {
        "yanchor": "auto",
        "xanchor": "auto",
        "bordercolor": "rgba(0, 0, 0, 1.000)",
        "bgcolor": "rgba(255, 255, 255, 1.000)",
        "borderwidth": 1,
        "tracegroupgap": 0,
        "y": 1.0,
        "font": {
            "color": "rgba(0, 0, 0, 1.000)",
            "family": "sans-serif",
            "size": 11
        },
        "title": {
            "font": {
                "color": "rgba(0, 0, 0, 1.000)",
                "family": "sans-serif",
                "size": 15
            },
            "text": ""
        },
        "traceorder": "normal",
        "x": 1.0
    },
    "width": 600
}
);

    });
    </script>





```julia

```
