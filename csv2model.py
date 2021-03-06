#!/usr/bin/python
import sys
import csv
import re

def csv2model(reactionfile,parameterfile,ratelawfile,outputFile):
    ODEDict=dict()
    print('Opening {file} as rate law file'.format(file=ratelawfile))
    ratelaws=dict()
    delayDict=dict()
    ODEIndexDict=dict()
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
            parametersDict[line[0]]=str(line[1])


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

            splitLaw=re.split('(\[[sS]\d{0,10}\])',thisLaw)
            newLaw=[]
            substrateIndex=0
            try:
                for part in splitLaw:
                    if(part and part.startswith('[') and re.search('([sS]\d{0,10})',part)):
                        substrateIndex=int(part[2:len(part)-1])-1
                        newLaw+=substratesInThisRxn[substrateIndex]
                    else:
                        newLaw+=list(part)

                thisLaw="".join(newLaw)
                #print(newLaw)
            except:
                print('error addding substrates {substrateIndex} to reaction {line}'.format(substrateIndex=substrateIndex, line=line))

            #products
            splitLaw=re.split('(\[[pP]\d{0,10}\])',thisLaw)
            newLaw=[]
            try:
                for part in splitLaw:
                    if(part and part.startswith('[') and re.search('([pP]\d{0,10})',part)):
                        productIndex=int(part[2:len(part)-1])-1
                        newLaw+=productsInThisRxn[productIndex]
                    else:
                        newLaw+=list(part)
            except:
                print('error addding products {productIndex} to reaction {line}'.format(productIndex=productIndex, line=line))
            thisLaw="".join(newLaw)

            #modifiers
            splitLaw=re.split('(\[[mM][Oo][Dd]\d{0,10}\])',thisLaw)
            newLaw=[]
            modifierIndex=0
            try:
                for part in splitLaw:
                    if(part and part.startswith('[') and re.search('[mM][Oo][Dd]\d{0,10}',part)):
                        modifierIndex=int(part[4:len(part)-1])-1
                        thisModifier=modifiersInThisRxn[modifierIndex]
                        if(thisModifier.startswith('delay(')):
                            #cut the word delay and brackets out
                            thisModifier=thisModifier[6:len(thisModifier)-1]
                            thisModDelayProperties=thisModifier.split(',')
                            thisMod=thisModDelayProperties[0]
                            thisModDelay=thisModDelayProperties[1]
                            thisDelayIndex=str(len(delayDict))
                            newLaw+='(h(p,t-tau_'+thisMod+'_'+thisDelayIndex+')[histindex_'+thisMod+'])'
                            delayDict[thisMod+'_'+thisDelayIndex]=thisModDelay
                        else:
                            newLaw+=modifiersInThisRxn[modifierIndex]
                    else:
                        newLaw+=list(part)
            except:
                print('error addding modifiers {modifierIndex} to reaction {line}'.format(modifierIndex=modifierIndex, line=line))
            thisLaw="".join(newLaw)


            #parameters
            splitLaw=re.split('\{(\w{1,20})\}',thisLaw)
            listLength=len(splitLaw)
            newLaw=[]
            try:
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


            except:
                print('error addding parameters {parametersInThisRxn} to reaction {line}'.format(parametersInThisRxn=parametersInThisRxn, line=line))
            thisLaw="".join(newLaw)

            #we need to add this reaction to every product and substrate involved in this reaction

            for thisSubstrate in substratesInThisRxn:
                if thisSubstrate in ODEDict:
                    ODEDict[thisSubstrate]=ODEDict[thisSubstrate]+' - '+thisLaw
                else:
                    ODEDict[thisSubstrate]='dy['+str(len(ODEDict)+1)+']= -'+thisLaw
                    ODEIndexDict[len(ODEDict)]=thisSubstrate
            for thisProduct in productsInThisRxn:
                if thisProduct in ODEDict:
                    ODEDict[thisProduct]=ODEDict[thisProduct]+' + '+thisLaw
                else:
                    ODEDict[thisProduct]='dy['+str(len(ODEDict)+1)+']= + '+thisLaw
                    ODEIndexDict[len(ODEDict)]=thisProduct
            #sometimes a modifier needs an ODE but has no changes other than events
            for thisModifier in modifiersInThisRxn:
                if thisModifier not in ODEDict:
                    ODEDict[thisModifier]='dy['+str(len(ODEDict)+1)+']=0'
                    ODEIndexDict[len(ODEDict)]=thisModifier
    #print(ODEDict)
    writeODEFile(ODEDict,outputFile,delayDict,ODEIndexDict,reactionfile,parameterfile,ratelawfile,len(parametersDict))

def writeODEFile(ODEDict,outputFile,delayDict,ODEIndexDict,reactionfile,parameterfile,ratelawfile,numberOfParameters):
    #this function will write the ODE file ready to be called by Julia

    with open(outputFile,'w') as f:
        f.write('#######################################################\n')
        f.write('# Generated programmatically by CSV2JuliaDiffEq.      #\n')
        f.write('# http://github.com/SiFTW/CSV2JuliaDiffEq             #\n')
        f.write('#######################################################\n')
        f.write('# generated from:\n')
        f.write('#    reactions file: {file}\n'.format(file=reactionfile))
        f.write('#    parameters file file: {file}\n'.format(file=parameterfile))
        f.write('#    rate law file: {file}\n'.format(file=ratelawfile))
        f.write('#\n')
        f.write('# Statistics:\n')
        f.write('#    Equations:{number}\n'.format(number=len(ODEIndexDict)))
        f.write('#    Parameters:{number}\n'.format(number=numberOfParameters))
        f.write('#######################################################\n\n')
        f.write('\n\n')
        odeNameDict=dict()
        if len(delayDict)>0:
            f.write('function ddeFile!(dy,y,h,p,t)\n')
        else:
            f.write('function odeFile!(dy,y,p,t)\n')
        #let's deal with time-dependent params
        for line in ODEIndexDict.keys():
            f.write('\t'+ODEIndexDict[line]+'=y['+str(line)+']\n')
            odeNameDict[ODEIndexDict[line]]=line
        delayOdeNameList=[]
        for delayEntry in delayDict.keys():
            f.write('\ttau_'+delayEntry+'='+delayDict[delayEntry]+'\n')
            odeName=delayEntry.split('_')[0]
            delayOdeNameList.append(odeName)
        for name in delayOdeNameList:
            f.write('\thistindex_'+name+'='+str(odeNameDict[name])+'\n')
        for key in ODEDict.keys():
            f.write('\t#'+key+'\n')
            f.write('\t'+ODEDict[key]+'\n')
        f.write('end')
    with open('variableNames.jl','w') as f:
        f.write('syms=[')
        for line in ODEIndexDict.keys():
            f.write('\"'+ODEIndexDict[line]+'\",')
        f.write(']')


csv2model(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
