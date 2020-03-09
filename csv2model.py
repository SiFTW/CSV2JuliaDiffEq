#!/usr/bin/python
import sys
import csv
import re

def csv2model(reactionfile,parameterfile,ratelawfile,outputFile):
    ODEDict=dict()
    print('Opening {file} as rate law file'.format(file=ratelawfile))
    ratelaws=dict()
    #let's populate a string array of rate laws
    with open(ratelawfile,'r') as f:
        csvreader=csv.reader(f)
        #skip header row
        next(csvreader)
        for line in csvreader:
            #print('adding key:{key}, val:{val} to ratelaws dict'.format(key=line[0],val=line[0]))
            ratelaws[line[0]]=line[1]

    #let's populate the parameter list
    print('Opening {file} as parameters file'.format(file=parameterfile))
    parametersDict=dict()
    with open(parameterfile,'r') as f:
        csvreader=csv.reader(f)
        #skpip header row
        next(csvreader)
        for line in csvreader:
            parametersDict[line[0]]=float(line[1])


    #let's iterate through the reaction file
    print('Opening {file} as reactions file'.format(file=reactionfile))    
    with open(reactionfile,'r') as f:
        csvreader=csv.reader(f)
        #skip header row
        next(csvreader)
        for line in csvreader:
            #substrate, products, kinetic law, modifiers, parameters
            substrates=line[0]
            products=line[1]
            kineticlaw=line[2]
            modifiers=line[3]
            parameters=line[4]

            #split up substrates, products, modifiers and parameters by space
            substratesInThisRxn=substrates.split(' ')
            substratesInThisRxn=list(filter(None,substratesInThisRxn))
            productsInThisRxn=products.split(' ')
            productsInThisRxn=list(filter(None,productsInThisRxn))
            modifiersInThisRxn=modifiers.split(' ')
            modifiersInThisRxn=list(filter(None,modifiersInThisRxn))            
            parametersInThisRxn=parameters.split(' ')
            parametersInThisRxn=list(filter(None,parametersInThisRxn))
            #print(substratesInThisRxn)

            #print(ratelaws.keys())
            #lookup kinetic law
        
            thisLaw=ratelaws[kineticlaw]
            
            #now we need to go through products substrates modifiers and variable using regular expressions
            # we will substitute in the correct values from each table
            #substrates
            splitLaw=re.split('\[([sS]\d{0,10})\]',thisLaw)
            newLaw=[]
            substrateIndex=0
            #print(splitLaw)
            for part in splitLaw:   
                #print(part)
                if(part and re.search('([sS]\d{0,10})',part)):
                    substrateIndex=int(part[1:])-1
                    newLaw+=substratesInThisRxn[substrateIndex]
                else:
                    newLaw+=list(part)

            thisLaw="".join(newLaw)
            #print(newLaw)

            #products
            splitLaw=re.split('\[([pP]\d{0,10})\]',thisLaw)
            newLaw=[]
            for part in splitLaw:
                if(part and re.search('[pP]\d{0,10}',part)):
                    productIndex=int(part[1:])-1
                    newLaw+=productsInThisRxn[productIndex]
                else:
                    newLaw+=list(part)

            thisLaw="".join(newLaw)
            
            #modifiers
            splitLaw=re.split('\[([mM][Oo][Dd]\d{0,10})\]',thisLaw)
            newLaw=[]
            modifierIndex=0
            for part in splitLaw:
                if(part and re.search('[mM][Oo][Dd]\d{0,10}',part)):
                    modifierIndex=int(part[3:])-1
                    newLaw+=modifiersInThisRxn[modifierIndex]
                else:
                    newLaw+=list(part)

            thisLaw="".join(newLaw)           


            #parameters
            splitLaw=re.split('\{(\w{1,20})\}',thisLaw)
            listLength=len(splitLaw)
            newLaw=[]
            for i in range(listLength):
                if splitLaw[i]:
                    parameterAdded=0
                    for j in range(len(parametersInThisRxn)):
                        thisParameterType=str.split(parametersInThisRxn[j],'_')[0]
                        if splitLaw[i].startswith(thisParameterType):
                            newLaw+=list(str(parametersDict[parametersInThisRxn[j]]))
                            parameterAdded=1
                    else:
                        if not parameterAdded:
                            newLaw+=splitLaw[i]
                                                   
                    

                            thisLaw="".join(newLaw)

            #we need to add this reaction to every product and substrate involved in this reaction
            for i in range(len(substratesInThisRxn)):
                thisSubstrate=substratesInThisRxn[i]
                if thisSubstrate in ODEDict.keys():
                    ODEDict[thisSubstrate]=ODEDict[thisSubstrate]+' - '+thisLaw
                else:
                    ODEDict[thisSubstrate]='du['+str(len(ODEDict))+']= -'+thisLaw
            for i in range(len(productsInThisRxn)):
                thisProduct=productsInThisRxn[i]
                if thisProduct in ODEDict.keys():
                    ODEDict[thisProduct]=ODEDict[thisProduct]+' + '+thisLaw
                else:
                    ODEDict[thisProduct]='du['+str(len(ODEDict))+']= + '+thisLaw

    #print(ODEDict)
    writeODEFile(ODEDict,outputFile)

def writeODEFile(ODEDict,outputFile):
    #this function will write the ODE file ready to be called by Julia
    with open(outputFile,'w') as f:
        f.write('function odeFile(t,y,du)\n')
        for index,line in enumerate(ODEDict.keys()):
            f.write('\t'+line+'=y['+str(index)+']\n')
        for index, line in enumerate(ODEDict.values()):
            f.write('\t#'+ODEDict.keys()[index]+'\n')            
            f.write('\t'+line+'\n')
        f.write('end')
    

csv2model(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
