import numpy as np
import matplotlib.pylab as plt


###############################################
# Score skill
################################################

## Equitable threat score 
def skill_ets(h,m,fa,obs_yes,fores_yes,n):
    
    h_random=(1/n)*(obs_yes*fores_yes)
    ets=(h-h_random)/(h+m+fa-h_random)
    
    return ets

## Frequency bias

def Bias (h,m,fa):

    return (h+fa)/(h+m)

## Proportion correct

def Pc(h,cr,n):

    return (h+cr)/n

##Probability of detection

def pod(h,m):
    
    return h/(h+m)

## False alarm ratio

def Far(h,fa):
    
    return fa/(h+fa)

##Success ratio

def Sr(h,fa):
    return 1-Far(h,fa)

## Probability of false detection 

def POFD(fa,cr):
    return fa/(cr+fa)

## Threat score(Critical success index)

def ts(h,m,fa):
    return h/(h+m+fa)


####################################################
#Table_contingency
####################################################


def Table_contingency(threshold,obs,fores):
    print (obs)
    a,b=obs.shape
    
    table=np.empty((len(threshold),7))
    table[:,0]=threshold
    
    for k,index in enumerate(threshold):
    
        hits=[]
        misses=[]
        false_alarms=[]
        correct_reject=[]
        yes_obs=[]
        yes_fore=[]
        for i in range(a):
            for j in range(b):
                if (obs[i,j]>=index and fores[i,j]>=index):
                    var=1
                    hits.append(var)
                if (obs[i,j]>=index and fores[i,j]< index):
                    var=0
                    misses.append(var)
                if (obs[i,j]< index and fores[i,j]>= index):
                    var=0
                    false_alarms.append(var)
                if (obs[i,j]<index and fores[i,j]<index):
                    var=1
                    correct_reject.append(var)
                if (obs[i,j]>=index):
                    var=1
                    yes_obs.append(var)
                if (fores[i,j]>=index):
                    var=1
                    yes_fore.append(var)    
    
        table[k,1]=len(hits)
        table[k,2]=len(misses)
        table[k,3]=len(false_alarms)
        table[k,4]=len(correct_reject)
        table[k,5]=len(yes_obs)
        table[k,6]=len(yes_fore)
        
        print ("***************************************")
    
        print ("threshold",index)
       
        print("Yes_obs:",yes_obs)
        print ("hits:",hits)
        print ("misses:",misses)
        print ("false_alarms:",false_alarms)
        print ("correct_reject:",correct_reject)
        print ("Yes_fore:",yes_fore)     
        
    return table,a*b


##################################################################
# Determination of score for validation
################################################################
def determine_score(threshold,obs,fores):
    
    table,n=Table_contingency(threshold,obs,fores)
    ets_v=[]
    pc_v=[]
    bias_v=[]
    ts_v=[]
    skill_plot=np.empty((len(threshold),5))
    for i in range(len(threshold)):
        ets_v=np.append(ets_v,skill_ets(table[i,1],table[i,2],table[i,3],table[i,5],table[i,6],n))
        bias_v=np.append(bias_v,Bias(table[i,1],table[i,2],table[i,3]))
        pc_v=np.append(pc_v,Pc(table[i,1],table[i,4],n))
        ts_v=np.append(ts_v,ts(table[i,1],table[i,2],table[i,3]))
   # vector_ets=np.append(vector_ets,ets_v)
    skill_plot[:,0]=threshold
    skill_plot[:,1]=ets_v
    skill_plot[:,2]=bias_v
    skill_plot[:,3]=pc_v
    skill_plot[:,4]=ts_v
    
    
    return skill_plot

def plot_result(threshold,obs,fores):
    data=determine_score(threshold,obs,fores)
    
    plt.figure(1)
    plt.xlabel("Threshold of Precipitation")
    plt.ylabel("Equitable threat score")
    plt.plot(data[:,0],data[:,1],label="Index")
    plt.title("Validation of Precipitation")
    plt.legend(loc="best")
    plt.grid()
    
    plt.figure(2)
    plt.xlabel("Threshold of Precipitation")
    plt.ylabel("Threat score")
    plt.plot(data[:,0],data[:,4],label="Index")
    plt.title("Validation of Precipitation")
    plt.legend(loc="best")
    plt.grid()
    plt.show()




if __name__=="__main__":
    obs=np.array([[0,10,3],[0,10,25],[10,0.5,1.]])
    fores=np.array([[0,0.2,0],[2,11,30],[10,0.8,1.]])
    threshold=[0.1,2,3,5,15,20]
    
    print (obs)
    print (fores)
    plot_result(threshold,obs,fores)
   # plot_result(obs,fores,threshold)


    
    
        
