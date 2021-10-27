using DifferentialEquations, DataFrames
using Plots
using CSV
include("odeFileExample.jl")
include("variableNames.jl")
include("scanIncludes.jl")

f=DDEFunction(ddeFile,syms=Symbol.(syms))
#f=ODEFunction(odeFile,syms=Symbol.(syms))
y0=ones(length(syms))
p=1
h(p,t)=ones(length(syms))
params=1
prob=DDEProblem(f,ones(length(syms)),h,(0.0,10.0),syms=Symbol.(syms))
#prob=ODEProblem(f,ones(length(syms)),(0.0,10.0))
print("Solving Equations \n")
@timev sol=solve(prob)
plot(sol)

modify["k_ABBinding"]=1.5

prob=DDEProblem(f,ones(length(syms)),h,(0.0,10.0),syms=Symbol.(syms))
print("Solving Equations \n")
@timev sol=solve(prob)
plot!(sol)
png("testOutScan.png")
