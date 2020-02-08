import math
import pandas as pd
from matplotlib import pyplot as plt
"""
    File:   HW02_Verdesi_Jacob_Mentor.py
    Author: Jacob Verdesi
    Email:  jxv3386@rit.edu
    Description:
    This is a Mentor program for Classifying Abominable Data

"""

def comment(str):
    return "\"\"\"{"+str+"}\"\"\";"
def indent(train):
    tab=0
    out=""
    for c in train:
        if(c=='{'or c=='}'or c==';'):
            if(c=='{'):
                tab+=1
            if(c=='}'):
                tab-=1
            out += "\n" + (tab * '\t')
        else:
            out+=c
    return out
def header(file):
    return "import pandas as pd;"\
           +comment("File:"+file.name+";Author: Jacob Verdesi;Email:jxv3386@rit.edu;"
            "Description:This is a Trained program for Classifying Abominable Data")

def body():
    return "def printClassified(data,bestAttribute,bestThreshold):{" \
           "for i in data[bestAttribute]:{" \
           "if (bestAttribute==\"Height\" and i>bestThreshold) or (bestAttribute==\"Age\" and i<bestThreshold):{" \
           "print(-1);}else:{print(1);}}}"

def print_trailer(bestAttribute,bestThreshold):
    return "def main():{"+\
           comment("Main function")\
           +"fileName=\"the_validation_file.csv\";"\
           +"data=(pd.read_csv(fileName,sep=','));"\
           +"printClassified(data,\""+str(bestAttribute)+"\","+str(bestThreshold)+");"\
           +"}if __name__ == '__main__':{main()}"


def quantize(data):
    data['Age'] = data['Age'].apply(lambda x: 2 * (round(x / 2)))
    data['Height'] = data['Height'].apply(lambda x: 5 * (round(x / 5)))
    return data
def get_quantized_bin_size(data,attribute):
    """
    This function looks for the bin_size by sorting the values and then calculating
    the diffrence of 2 values that are next to eachother and are not the same
    :param data: DataFrame
    :param attribute: attribute to find bin_size
    :return: bin_size
    """
    for index in range(0, len(data[attribute])):
        list = sorted(data[attribute])
        if (list[index] != list[index + 1]):
            return list[index + 1] - list[index]

def binary(data):
    minMiss=math.inf
    bestThresh=0
    bst=tn=tp=fn=fp=pd.DataFrame()

    minDistance = math.inf
    minDistThresh = 0
    bestAttribute=""
    bestAttributeIndex=0
    bestTpr=[]
    bestFpr=[]
    bestMisses=[]
    for attribute in data:
        if attribute=="Class" :
            pass
        else:
            index=get_quantized_bin_size(data,attribute)
            tprList = []
            fprList = []
            misses=[]
            for threshold in range(min(data[attribute]),max(data[attribute]),index):
                out = data.copy()
                if (attribute=='Age'):
                    out['left']=(data[attribute]>threshold)
                else:
                    out['left']=(data[attribute]<=threshold)

                out['sum']=out['left']+out['Class']
                miss=((out['sum'])==1).sum()+((out['sum'])==0).sum()
                misses.append(miss)
                tpr=(out['sum']==1).sum()/((out['sum']==1).sum()+(out['sum']==2).sum())
                fpr=((out['sum']==-1).sum()/((out['sum']==0).sum()+(out['sum']==-1).sum()))
                tprList.append(tpr)
                fprList.append(fpr)
                distance=math.sqrt(pow(1-fpr,2)+pow(tpr,2))
                if(distance<minDistance):
                    minDistance=distance
                    minDistThresh=threshold
                if(miss<minMiss):
                    minMiss=miss
                    bestThresh=threshold
                    bestAttribute=attribute
                    bestAttributeIndex=index
                    bestTpr=tprList
                    bestFpr=fprList
                    bst=out
                    bestMisses=misses
                    tp=out.loc[(out['sum']==2)]
                    fp=out.loc[(out['sum']==0)]
                    tn=out.loc[(out['sum']==-1)]
                    fn=out.loc[(out['sum']==1)]
    print(minMiss,bestThresh)
    print(bestAttribute)
    print(minDistance,minDistThresh)
    bins=[x for x in range(min(data[bestAttribute]),max(data[bestAttribute]),bestAttributeIndex)]
    plt.scatter(bins,bestMisses)
    # plt.hist(data[bestAttribute],bins=bins,label="total",color='purple',alpha=.5,histtype='stepfilled')
    # plt.hist(tp[bestAttribute],bins=bins,label="tp",color='b',alpha=.5,histtype='stepfilled')
    # plt.hist(fp[bestAttribute],bins=bins, label="fp", color='y', alpha=.5, histtype='stepfilled')
    # plt.hist(tn[bestAttribute],bins=bins,label="tn",color='g',alpha=.5,histtype='stepfilled')
    # plt.hist(fn[bestAttribute],bins=bins,label="fn",color='r',alpha=.5,histtype='stepfilled')
    # plt.legend(prop={'size': 10})

    #plt.scatter(bestTpr,bestFpr)
    #rocIndex=(minDistThresh - min(data[bestAttribute])) // bestAttributeIndex
    #plt.annotate(minDistThresh,(bestTpr[rocIndex],bestFpr[rocIndex]))
    plt.show()
    return bestAttribute,bestThresh
def main():
    fileName="Abominable_Data_For_1D_Classification__v92_HW3_720_final.csv"
    writeFile="HW02_Verdesi_Jacob_Trainer.py"
    file=open(writeFile,"w")

    data=quantize(pd.read_csv(fileName,sep=','))
    bestAttribute,bestThreshold=binary(data)


    trainer=indent(header(file)+body()+print_trailer(bestAttribute,bestThreshold))
    file.write(trainer)
    file.close()

if __name__ == '__main__':
    main()