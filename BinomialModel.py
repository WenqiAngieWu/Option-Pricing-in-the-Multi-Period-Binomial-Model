# -*- coding: utf-8 -*-
"""

@author: WenqiAngieWu

@para:

T: maturity
n: # option periods
N: # futures period
S: initial stock price
r: continuously-compunded interest rate
c: dividend yield
sigma: annualized volatility 
K: strike price
cp: +1/-1 with regards to call/put
"""


from math import exp, sqrt
import numpy as np



def Parameter(T,n,sigma,r,c):
    """Parameter calculation"""    
    dt = T/n
    u = exp(sigma * sqrt(dt))
    d = 1/u
    
    q1 = (exp((r-c)*dt)-d)/(u-d)
    q2 = 1-q1
    R = exp(r*dt)
    
    return (u, d, q1, q2, R)

# =============================================================================

def GenerateTree(T,n,S,sigma,r,c):
    """generate stock tree"""    
    u, d, q1, q2, R = Parameter(T,n,sigma,r,c)
    
    stockTree = np.zeros((n+1, n+1))  
    
    # compute the stock tree
    stockTree[0,0] = S
    for i in range(1,n+1):
        stockTree[0,i] = stockTree[0, i-1]*u
        for j in range(1,n+1):
            stockTree[j,i] = stockTree[j-1, i-1]*d
    
    return stockTree

# =============================================================================

def StockOptionAM(T,n,S,r,c,sigma,K,cp):
    """first return: American Stock Option Pricing"""
    """second return: when is the earliest time to exercise""" 
    """Though it's never optimal to early exercise AM call"""
    """It matters for AM put"""
          
    u, d, q1, q2, R = Parameter(T,n,sigma,r,c)
    
    stockTree = GenerateTree(T,n,S,sigma,r,c)
    optionTree = np.zeros((n+1,n+1))

    
    # compute the option tree
    for j in range(n+1):
        optionTree[j, n] = max(0, cp * (stockTree[j, n]-K))
        
    flag = 0 
    list = []
    for i in range(n-1,-1,-1):
        for j in range(i+1):
            optionTree[j, i] = max((q1 * optionTree[j, i+1] + q2 * optionTree[j+1, i+1])/R,   
                               cp * (stockTree[j, i] - K))                        
            if (optionTree[j, i] - cp * (stockTree[j, i] - K)) < 1e-10:
                flag += 1
                list.append(i)
    
    when = n
    if(flag):  when = list[-1]
    
                
    return (optionTree[0,0], when)

# =============================================================================

def StockOptioneEU(T,n,S,r,c,sigma,K,cp):
    """European Stock Option Pricing"""        
    u, d, q1, q2, R = Parameter(T,n,sigma,r,c)
    
    stockTree = GenerateTree(T,n,S,sigma,r,c)
    optionTree = np.zeros((n+1,n+1))
    
    
    # compute the option tree
    for j in range(n+1):
        optionTree[j, n] = max(0, cp * (stockTree[j, n]-K))
        
   
    for i in range(n-1,-1,-1):
        for j in range(i+1):
            optionTree[j, i] = (q1 * optionTree[j, i+1] + q2 * optionTree[j+1, i+1])/R
   
                
    return optionTree[0,0]

# =============================================================================
  
def FuturesOptionAM(T,n,N,S,r,c,sigma,K,cp):
    """first return: American Futures Option Pricing"""
    """second return: when is the earliest time to exercise"""   
    u, d, q1, q2, R = Parameter(T,N,sigma,r,c)
    
    stockTree = GenerateTree(T,N,S,sigma,r,c)
    futuresTree = np.zeros((N+1, N+1))
    optionTree = np.zeros((n+1,n+1))           
            
    # compute the futures tree
    for j in range(N+1):
        futuresTree[j, N] = stockTree[j, N]
    
    for i in range(N-1, -1,-1): 
        for j in range(i+1):
            futuresTree[j,i] = q1 * futuresTree[j, i+1] + q2 * futuresTree[j+1, i+1]
    
    
    # compute the option tree
    for j in range(n+1):
        optionTree[j, n] = max(0, cp * (futuresTree[j, n]-K))
    
    flag = 0
    list = []
    for i in range(n-1,-1,-1):
        for j in range(i+1):
            optionTree[j, i] = max((q1 * optionTree[j, i+1] + q2 * optionTree[j+1, i+1])/R,   
                               cp * (futuresTree[j, i] - K))                        
            if  (optionTree[j, i] - cp * (futuresTree[j, i] - K)) < 1e-10:
                flag += 1
                list.append(i)
                
    when = n
    if(flag):  when = list[-1]
            
    return (optionTree[0,0], when)
# =============================================================================

def FuturesOptionEU(T,n,N,S,r,c,sigma,K,cp):
    """European Futures Option Pricing"""
    u, d, q1, q2, R = Parameter(T,N,sigma,r,c)
    
    stockTree = GenerateTree(T,N,S,sigma,r,c)
    futuresTree = np.zeros((N+1, N+1))
    optionTree = np.zeros((n+1,n+1))           
            
    # compute the futures tree
    for j in range(N+1):
        futuresTree[j, N] = stockTree[j, N]
    
    for i in range(N-1, -1,-1): 
        for j in range(i+1):
            futuresTree[j,i] = q1 * futuresTree[j, i+1] + q2 * futuresTree[j+1, i+1]
    
    
    # compute the option tree
    for j in range(n+1):
        optionTree[j, n] = max(0, cp * (futuresTree[j, n]-K))
    
    for i in range(n-1,-1,-1):
        for j in range(i+1):
            optionTree[j, i] = (q1 * optionTree[j, i+1] + q2 * optionTree[j+1, i+1])/R                 
            
    return optionTree[0,0]

# =============================================================================



    


