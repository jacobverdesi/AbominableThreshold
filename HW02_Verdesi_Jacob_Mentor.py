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
    return "import pandas as pd;" \
           "import sys;"\
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
           +"fileName=sys.argv[1];"\
           +"data=(pd.read_csv(fileName,sep=','));"\
           +"printClassified(data,\""+str(bestAttribute)+"\","+str(bestThreshold)+");"\
           +"}if __name__ == '__main__':{main()}"


def quantize(data):
    """
    Takes the columns of a DataFrame and rounds to nearest value given
    :param data: DataFrame of unQuantized data
    :return: Quantized Data
    """
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
def shortestDistance(yAxis,xAxis):
    shortest=math.inf
    pointIndex=0
    if len(yAxis)==len(xAxis):
        for i in range(0,len(yAxis)):
            distance=math.sqrt(pow(1-yAxis[i],2)+pow(xAxis[i],2))
            if distance<shortest:
                shortest=distance
                pointIndex=i
    return shortest,pointIndex
def binary(data):
    minMiss=math.inf
    bestThresh=0
    tn=tp=fn=fp=pd.DataFrame()
    bestAttribute=""
    bestAttributeIndex=0
    bestTpr=[]
    bestFpr=[]
    bestMisses=[]
    for attribute in data:
        tprList = []
        fprList = []
        if attribute=="Class" :
            pass
        else:
            index=get_quantized_bin_size(data,attribute)
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

                if(miss<minMiss):
                    minMiss=miss
                    bestThresh=threshold
                    bestAttribute=attribute
                    bestAttributeIndex=index
                    bestMisses=misses
                    tp=out.loc[(out['sum']==2)]
                    fp=out.loc[(out['sum']==0)]
                    tn=out.loc[(out['sum']==-1)]
                    fn=out.loc[(out['sum']==1)]
        bestTpr.append(tprList)
        bestFpr.append(fprList)

    bins=[x for x in range(min(data[bestAttribute]),max(data[bestAttribute]),bestAttributeIndex)]

    fig,((ax0,ax1),(ax2,ax3))=plt.subplots(2,2)

    ax0.hist(tp[bestAttribute],bins=bins,label="true positive",color='b',alpha=.5,histtype='stepfilled')
    ax0.hist(fp[bestAttribute],bins=bins, label="false positive", color='y', alpha=.5, histtype='stepfilled')
    ax0.hist(tn[bestAttribute],bins=bins,label="true negative",color='g',alpha=.5,histtype='stepfilled')
    ax0.hist(fn[bestAttribute],bins=bins,label="false negative",color='r',alpha=.5,histtype='stepfilled')
    ax0.set_title('Confusion Histogram of Height')
    ax0.set_xlabel('Height Thresholds')
    ax0.set_ylabel('# of Values in Dataset')

    ax0.legend(loc=2,prop={'size': 6})
    ax1.scatter(bins, bestMisses)
    ax1.set_title('Cost function vs Height threshold')
    ax1.set_ylabel('# of Datapoint Misses')
    ax1.set_xlabel('Height Thresholds')

    ageRocDistance,ageRocThresh=shortestDistance(bestFpr[0],bestTpr[0])
    ax2.plot(bestTpr[0],bestFpr[0],'-gD',markevery=[ageRocThresh])
    ax2.plot((0,1),(0,1),linestyle='--',color='b')
    ax2.set_title('ROC of Age')
    ax2.set_xlabel('False Positive Rate (%)')
    ax2.set_ylabel('True Positive Rate (%)')
    ax2.set(adjustable='box', aspect='equal')
    heightRocDistance,heightRocThresh=shortestDistance(bestFpr[1],bestTpr[1])
    ax3.plot(bestTpr[1],bestFpr[1],'-gD',markevery=[heightRocThresh])
    ax3.plot((0,1),(0,1),linestyle='--',color='b')
    ax3.set_title('ROC of Height')
    ax3.set_xlabel('False Positive Rate (%)')
    ax3.set_ylabel('True Positive Rate (%)')
    ax3.set(adjustable='box', aspect='equal')


    #ax2.annotate(minDistThresh,(bestTpr[rocIndex],bestFpr[rocIndex]))
    plt.tight_layout()
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