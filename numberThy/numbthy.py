# -*- coding: utf-8 -*-
"""numbthy.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1zFKorJ2XnXpkVGIpU5_XedMlU4y8SN7s
"""

import tensorflow as tf
import functools
sess = tf.InteractiveSession()
tf.global_variables_initializer()

####################-- euler_criterion function --################

def euler_criterion(a, p):
    """
    p is odd prime, a is positive integer. 
    Euler's Criterion will check if a is a quadratic residue mod p. 
    If yes, returns True. If a is a non-residue mod p, then False
    """
    p_sub_1_div_2 = tf.math.floordiv(tf.math.subtract(p,1),2)
    return tf.math.equal(1,tf.math.floormod(tf.math.pow(a,p_sub_1_div_2),p))

####################-- gcd function --################

def gcd(a,b):
    """
    input: a, b is a integer
    output: return the greatest common divisor 
    of tensor constant a and b.
    """
    a = tf.math.abs(a)
    b = tf.math.abs(b)
    result = tf.while_loop(
        gcd_cond,gcd_body,[a,b]
    )
    return result[1]
def gcd_cond(a,b):
    return tf.math.greater(a, 0)
def gcd_body(a,b):
    b = tf.math.floormod(b,a)
    tep = a
    a = b
    b = tep
    return a, b

a1 = tf.constant(2040)
b2 = tf.constant(1071)
h = gcd(a1,b2)


print (h.eval())

####################-- xgcd function --################

def xgcd(a,b):
    """
    function xgcd the vaule g, x, y satisfy the equation g = ax + by.
    input: number a and b
    output: returns a tuple of form (g,x,y), where g is gcd(a,b) and
    x,y satisfy the equation g = ax + by.
    """
    a1=1; b1=0; a2=0; b2=1; aneg=1; bneg=1; flag=1
    a, aneg = tf.cond(tf.less(a, 0),true_fn= lambda: (tf.math.negative(a), -1), false_fn=lambda:(a, aneg))
    b, bneg = tf.cond(tf.less(b, 0),true_fn=lambda: (tf.math.negative(b), -1), false_fn=lambda:(b, bneg))
    
    a,b,a1,b1,a2,b2,aneg,bneg,flag = tf.while_loop(
        lambda a,b,a1,b1,a2,b2,aneg,bneg,flag: tf.greater(flag,0),
        body_1,
        [a,b,a1,b1,a2,b2,aneg,bneg,flag]
    )
    res1, res2, res3 = tf.cond(
        tf.math.equal(a, 0),
        true_fn = lambda: (tf.identity(b), tf.math.multiply(a2,aneg), tf.math.multiply(b2,bneg)),
        false_fn = lambda: (tf.identity(a), tf.math.multiply(a1,aneg), tf.math.multiply(b1,bneg))
    )
    return (res1, res2, res3)

def body_1(a,b,a1,b1,a2,b2,aneg,bneg,flag): 
    quot = tf.math.negative(tf.math.floordiv(a,b))
    a = tf.math.floormod(a, b)
    a1 = tf.math.add(a1, tf.math.multiply(quot,a2))
    b1 = tf.math.add(b1, tf.math.multiply(quot,b2))
    a,b,a1,b1,a2,b2,aneg,bneg,flag = tf.cond(
        tf.math.equal(a, 0),
        true_fn = lambda:(a,b,a1,b1,a2,b2,aneg,bneg,0),
        false_fn = lambda:(a,b,a1,b1,a2,b2,aneg,bneg,flag)
    )
    a,b,a1,b1,a2,b2,aneg,bneg,flag = tf.cond(
        tf.math.not_equal(a,0),
        true_fn = lambda: body_2(a,b,a1,b1,a2,b2,aneg,bneg,flag),
        false_fn = lambda:(a,b,a1,b1,a2,b2,aneg,bneg,flag)
    )
    return a,b,a1,b1,a2,b2,aneg,bneg,flag
    
def body_2(a,b,a1,b1,a2,b2,aneg,bneg,flag):
    quot = tf.math.negative(tf.math.floordiv(b,a))
    b = tf.math.floormod(b, a)
    a2 = tf.math.add(a2, tf.math.multiply(quot,a1))
    b2 = tf.math.add(b2, tf.math.multiply(quot,b1))
    a,b,a1,b1,a2,b2,aneg,bneg,flag = tf.cond(
        tf.math.equal(b, 0),
        true_fn = lambda:(a,b,a1,b1,a2,b2,aneg,bneg,0),
        false_fn = lambda:(a,b,a1,b1,a2,b2,aneg,bneg,flag)
    )
    return a,b,a1,b1,a2,b2,aneg,bneg,flag

a1 = tf.constant(65)
b2 = tf.constant(78)
a1 = tf.constant(4)
b2 = tf.constant(2)
h,v,f = xgcd(a1,b2)

print(h.eval(),v.eval(),f.eval())

####################-- power_mod function --################

def power_mod(b,e,n):
    """
    function power_mod computes the eth power of b mod n
    input: integer b, e, n
    ouput: return the eth power of b mod d (data type: tensor)
    """
    accum,i,bpow2 = tf.cond(
        tf.math.less(e,0), # Negative powers can be computed if gcd(b,n)=1
        true_fn = lambda: (inverse_mod(b, n), tf.math.negative(e), n), 
        false_fn = lambda: power_mod_cond_body(b,e,n)
    )
    return accum

def power_mod_cond_body(b,e,n):
    accum = 1; i = 0; bpow2 = b
    b,e,n,accum,i,bpow2 = tf.while_loop(
        lambda b,e,n,accum,i,bpow2: tf.greater(tf.bitwise.right_shift(e,i),0),
        power_mod_while_body,
        [b,e,n,accum,i,bpow2]
    )
    return accum,i,bpow2

def power_mod_while_body(b,e,n,accum,i,bpow2):
    b,e,n,accum,i,bpow2 = tf.cond(
        tf.math.equal(tf.bitwise.bitwise_and(tf.bitwise.right_shift(e,i),1),1),
        true_fn = lambda: power_mod_cond_body_1(b,e,n,accum,i,bpow2),
        false_fn = lambda: (b,e,n,accum,i,bpow2)
    )
    bpow2 = tf.math.floormod(tf.math.multiply(bpow2,bpow2),n)
    i = tf.math.add(i,1)
    return b,e,n,accum,i,bpow2

def power_mod_cond_body_1(b,e,n,accum,i,bpow2):
    accum = tf.math.floormod(tf.math.multiply(accum,bpow2),n)
    return b,e,n,accum,i,bpow2

####################-- inverse_mod function --################

def inverse_mod(a,n):
    """
    get the inverse of integer a, 1/a. compute 1/a mod n
    input: integer a and n
    output: return 1/a mod n with tensor
    """
    (g,xa,xb) = xgcd(a,n)
    result = tf.cond(
        tf.math.not_equal(g,1),
        true_fn = lambda: -1,
        false_fn = lambda: tf.math.floormod(xa,n)
    )
    return result

a = inverse_mod(4,7)
print(a.eval())

print(power_mod(4,3,2).eval())
print(power_mod(4,7,9).eval())

print(power_mod(1,6,4).eval())
print(power_mod(9,15,3).eval())

####################-- is_prime function --################

def is_prime(n):
    """
    check whether the number n is prime, if yes,return true, else, return false
    input: number n
    output: boolean (tensor)
    """
    result = 1; 
    n = tf.cond(tf.math.less(n,0), lambda:tf.math.negative(n), lambda: n)
    result = tf.cond(
        tf.math.less(n,2), 
        lambda: tf.math.subtract(result,1), 
        lambda :is_prime_cond_body(n)
        )
    result = tf.math.equal(result, 1)
    return result

def is_prime_cond_body(n):
    check_list = tf.math.equal(n,(2,3,5,7,11,13,17,19,23,29))
    has_true, id_check_list = tf.unique(check_list)
    size = tf.size(has_true)
    result = tf.cond(tf.math.equal(size,2), lambda: 1, lambda: check_isprimeE(n))
    return result
    
def check_isprimeE(n):
    result = tf.logical_and(tf.logical_and(isprimeE(n,2), isprimeE(n,3)),isprimeE(n,5))
    result = tf.cond(tf.math.equal(result, True),lambda:1, lambda:0)
    return result

print(is_prime(2).eval())
print(is_prime(15).eval())
print(is_prime(27).eval())

####################-- factor function --################

@tf.function
def factor(n):
	"""
	function factor() find the factor of a integer n
	input: integer n
	output: Return a sorted tensor list of the prime factors of n with exponents.
	"""
	# Rewritten to align with SAGE.  Previous semantics available as factors(n).
	if ((abs(n) == 1) or (n == 0)): raise ValueError('Unable to factor {0}'.format(n))
	factspow = []
	currfact = None
	thecount = 1
	for thefact in factors(n):
		if thefact != currfact:
			if currfact != None:
				factspow += [(currfact,thecount)]
			currfact = thefact
			thecount = 1
		else:
			thecount += 1
	factspow += [(thefact,thecount)]
	return tuple(factspow)

####################-- prime_divisors function --################

def prime_divisors(n):
    """
    call the function factors() to get a sorted list of the prime divisors of n
    input: integer n
    output: returns a sorted tensor list of the prime divisors of n.
    """
    return tuple(set(factors(n)))

####################-- euler_phi function --################

def euler_phi(n):
    """
    Euler's totient function counts the positive integers 
    up to a given integer n that are relatively prime to n (n>=1)
    input: positive integer n
    output: return the number of coprime of n
    """
    result = 1
    for i in range(2,n):
        result = tf.cond(tf.math.equal(gcd(i,n),1),lambda:tf.math.add(result,1),lambda: tf.math.add(result,0))
    return result

print(euler_phi(8).eval())

####################-- def carmichael_lambda function --################

def carmichael_lambda(n):
    """
    Compute Carmichael's Lambda function
	of n - the smallest exponent e such that b**e = 1 for all b coprime to n.
	Otherwise defined as the exponent of the group of integers mod n.
    """
    coprimes = []; count = 1; list_len = 0; index = 0
    for x in range(1,n):
        result = tf.cond(
            tf.math.equal(gcd(x, n),1),
            lambda:x,
            lambda:0
        )
        coprimes.append(result)
    coprimes, _ = tf.unique(coprimes)
    list_len = tf.size(coprimes)
    coprimes,count,n,index = tf.while_loop(
        lambda coprimes,count,n,index: tf.math.less(index,list_len),
        carmichael_while_body,
        [coprimes,count,n,index]
    )
    return count

def carmichael_while_body(coprimes,count,n,index):
    e = tf.gather(coprimes,index)
    count,index = tf.cond(
        tf.math.logical_not(tf.math.equal(tf.math.floormod(tf.math.pow(e,count),n),1)),
        lambda: (tf.math.add(count,1),tf.math.add(index,1)),
        lambda: (tf.math.add(count,0),tf.math.add(index,1))
    )
    return coprimes,count,n,index

r = carmichael_lambda(13)
print(r.eval())

####################-- is_primitive_root function --################

sess = tf.InteractiveSession()
tf.global_variables_initializer()# call a tensorflow function should use a number
                                 #otherwise, it will raise error
def is_primitive_root(g,n):
    """
    Test whether g is primitive - generates the group of units mod n
    input: integer g
    output: boolean
    """
    result = 1; size = 0; index = 0
    result = tf.cond(
        tf.math.not_equal(gcd(g,n),1),
        lambda: 0,
        lambda: 1
        )
    order = euler_phi(n)
    print(order.eval())
    result = tf.cond(
        tf.math.not_equal(carmichael_lambda(n), order),
        lambda: 0,
        lambda: 1        
        )
    orderfacts = prime_divisors(order.eval())
    for fact in orderfacts:
        fact = tf.dtypes.cast(fact,tf.int32)
        result = tf.cond(
            tf.math.equal(g**(order//fact)%n,1),
            lambda: 0,
            lambda: result
        )
    return tf.math.equal(result,1)
print(is_primitive_root(23,11).eval())

####################-- sqrtmod function --################

@tf.function
def sqrtmod(a,n):
	"""ompute sqrt(a) mod n using various algorithms.
	Currently n must be prime,
	but will be extended to general n (when I get the time)."""
	# SAGE equivalent is mod(g,n).sqrt() in IntegerMod class
	if(not isprime(n)): raise ValueError("*** Error ***:  Currently can only compute sqrtmod(a,n) for prime n.")
	if(pow(a,(n-1)//2,n)!=1): raise ValueError("*** Error ***:  a is not quadratic residue, so sqrtmod(a,n) has no answer.")
	return tonelli(a,n) #Bacause the TSRsqrtmod function cannot return a correct answer,so I use another function for helping

####################-- TSRsqrtmod function --################

g =tf.range(2,7,1)
print(g.eval())

def TSRsqrtmod(a,grpord,p):
    """
    Compute sqrt(a) mod n using Tonelli-Shanks-RESSOL algorithm.
	Here integers mod n must form a cyclic group of order grpord.
    However, tensorflow cannot calculate nagetive power 2^(-1)
    also, the data type is int32, therefore, the result of 2^(-1) is not 0.5, is 0
    hence, this function cannot return a correct answer
    """
    ordpow2=0; non2=grpord; temp_g=0; 
    range1_len = 0; index1 = 1; range2_len=0; index2 = 1
    ordpow2,non2 = tf.while_loop(
        lambda ordpow2,non2: tf.math.logical_not(tf.math.equal(tf.bitwise.bitwise_and(non2,0x01),1)),
        TSRsqrtmod_while,
        [ordpow2,non2]
    )

    range1 = tf.range(2,grpord-1,1)
    range1_len = tf.size(range1)
    g = tf.gather(range1,0)
    g,grpord,p,index1,range1_len,range1= tf.while_loop(
        lambda g,grpord,p,index1,range1_len,range1: tf.math.less(index1,range1_len),
        save_temp_g,
        [g,grpord,p,index1,range1_len,range1]
    )
    g = tf.math.mod(tf.math.pow(g,non2),p)

    gpow=0; atweak=a
    range2 = tf.range(0,tf.math.add(ordpow2,1),1)
    range2_len = tf.size(range2)
    pow2 = tf.gather(range2,0)

    pow2,atweak,non2,ordpow2,p,gpow,g,index2,range2= tf.while_loop(
        lambda pow2,atweak,non2,ordpow2,p,gpow,g,index2,range2:tf.math.less(index2,range2_len),
        TSRsqrtmod_true,
        [pow2,atweak,non2,ordpow2,p,gpow,g,index2,range2]
    )

    d = inverse_mod(2,non2)
    tmp = tf.math.mod(tf.math.pow(g,gpow),p)
    tmp = tf.math.mod(tf.math.pow(tf.math.multiply(a,tmp),d),p)
    result = tf.math.floormod(tf.math.multiply(tmp,inverse_mod(tf.math.floormod(tf.math.pow(g,tf.math.floordiv(gpow,2)),p),p)),p)
    return result

def TSRsqrtmod_while(ordpow2,non2):
    ordpow2 = tf.math.add(ordpow2,1)
    non2 = tf.math.floordiv(non2,2)
    return ordpow2,non2

def save_temp_g(g,grpord,p,index1,range1_len,range1):
    temp = tf.gather(range1,index1)
    g,grpord,p,index1,range1_len,range1 = tf.cond(
        tf.math.not_equal(tf.math.mod(tf.math.pow(g,tf.math.floordiv(grpord,2)),p),1),
        lambda: (g,grpord,p,range1_len,range1_len,range1),
        lambda: (g,grpord,p,tf.math.add(index1,1),range1_len,range1)
    )
    g = temp
    return g,grpord,p,index1,range1_len,range1

def TSRsqrtmod_true(pow2,atweak,non2,ordpow2,p,gpow,g,index2,range2):
    temp = tf.gather(range2,index2)
    pow2,atweak,non2,ordpow2,p,gpow,g,index2,range2 = tf.cond(
            tf.math.not_equal((atweak**(non2*2**(ordpow2-pow2))%p),1),
            lambda:(pow2,((atweak * (g**(2**pow2-1)%p)) % p),non2,ordpow2,p,(gpow + (2**(pow2-1))),g,tf.math.add(index2,1),range2),
            lambda:(pow2,atweak,non2,ordpow2,p,gpow,g,tf.math.add(index2,1),range2)
        )
    pow2 = temp
    return pow2,atweak,non2,ordpow2,p,gpow,g,index2,range2

print(TSRsqrtmod(9,4,5).eval())
print(pow(3,8000//2,2))

################ Internally used functions #########################################

####################-- isprimeF function --################

def isprimeF(n,b):
    """
    isprimeF(n,b) - Test whether number n is prime or a Fermat pseudoprime to base b.
    process: (b**(n-1)) % n
    """
    num = tf.math.floormod(tf.math.pow(b, n-1),n)
    return tf.math.equal(num,1)

a = isprimeF(25,3)
print(a.eval())
l = isprimeF(3,4)
print(l.eval())

####################-- isprimeE function --################

def isprimeE(n,b):
    """
    Test whether n is prime or an Euler pseudoprime to base b
    input: integer n, b
    output: boolean
    """
    result = 1; flag = 1; c = 0
    n,b,c,result,flag =  tf.cond(
        tf.math.logical_not(isprimeF(n,b)), 
        lambda:(n,b,c,0,flag), 
        lambda:cond_body(n,b,c,result,flag)
        )
    result = tf.math.equal(result, 1)
    return result

def cond_body(n,b,c,result,flag):
    r = tf.math.subtract(n,1)
    r = tf.while_loop(lambda r: tf.math.equal(tf.math.floormod(r,2), 0),
                      lambda r:tf.math.floordiv(r,2),
                      [r])
    c = tf.math.floormod(tf.math.pow(b, r),n)
    n,b,c,result,flag = tf.cond(
        tf.math.equal(c, 1), 
        true_fn = lambda:(n,b,c,1,flag), 
        false_fn = lambda: while_loop(n,b,c,result,flag)
        )
    return n,b,c,result,flag

def while_loop(n,b,c,result,flag):
    n,b,c,result,flag = tf.while_loop(
        lambda n,b,c,result,flag: tf.greater(flag,0),
        while_body,
        [n,b,c,result,flag]
    )
    return n,b,c,result,flag

def while_body(n,b,c,result,flag):
    n,b,c,result,flag = tf.cond(
        tf.math.equal(c,1),
        true_fn = lambda: (n,b,c,0,0),
        false_fn = lambda: while_body_1(n,b,c,result,flag)
        )
    return n,b,c,result,flag

def while_body_1(n,b,c,result,flag):
    n,b,c,result,flag = tf.cond(
        tf.math.equal(c,n-1),
        true_fn = lambda: (n,b,c,1,0),
        false_fn = lambda: (n,b,(tf.math.floormod(tf.math.pow(c, 2),n)),result,flag)
        )
    return n,b,c,result,flag

a = isprimeE(25,3)
print(a.eval())
a = isprimeE(15,4)
print(a.eval())
a = isprimeE(3,4)
print(a.eval())

####################-- factorone function --################

def factorone(n):
    """
    Find a prime factor of n using a variety of methods
    input: integer n
    output: a prime factor of n
    """
    fact = -1
    n, fact= tf.cond(is_prime(n), lambda:(n, n), lambda:factorone_cond_body(n,fact))
    fact = tf.cond(tf.math.equal(0,tf.math.mod(n,fact)),lambda:fact,lambda:factorPR(n))
    return fact

def factorone_cond_body(n,fact):
    fact_list = [2,3,5,7,11,13,17,19,23,29]
    size = len(fact_list)
    index = 0
    n,fact,index,size,fact_list = tf.while_loop(
        lambda n,fact,index,size,fact_list: tf.math.less(index,10),
        factorone_while_body,
        [n,fact,index,size,fact_list]
        )
    return n,fact
    
def factorone_while_body(n,fact,index,size,fact_list):
    n,fact,index,size,fact_list = tf.cond(
        tf.math.equal(tf.math.mod(n,tf.gather(fact_list,index)),0),
        lambda: (n,tf.gather(fact_list,index),size,size,fact_list),
        lambda: (n,fact,tf.math.add(index,1),size,fact_list)
        )
    return n,fact,index,size,fact_list

print(factorone(75).eval())

####################-- factors function --################

@tf.function
def factors(n):
    """
    Return a sorted list of the prime factors of n.
    input: integer n
    output: list of prime factors of n
    """
    i = 2
    factors = []
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)
    if n > 1:
        factors.append(n)
    return factors

print(factors(6))

####################-- factorPR function --################

def factorPR(n):
    """
    Find a factor of n using the Pollard Rho method
    """
    numsteps = tf.math.multiply(2.,tf.math.floor(tf.math.sqrt(tf.math.sqrt(tf.dtypes.cast(n,tf.float32)))))
    numsteps = tf.dtypes.cast(numsteps,tf.int32)
    additive = 1; g = -1; result = 0;
    n,numsteps,additive,g = tf.while_loop(
        lambda n,numsteps,additive,g: tf.math.less(additive,5),
        factorPR_while_body,
        [n,numsteps,additive,g]
    )
    result = tf.cond(tf.math.equal(additive,4),lambda:1,lambda:g)
    return result

def factorPR_while_body(n,numsteps,additive,g):
    fast=slow=1; i=1; 
    n,numsteps,fast,slow,i,additive,g = tf.while_loop(
        lambda n,numsteps,fast,slow,i,additive,g: tf.math.less(i,numsteps),
        inside_while_body,
        [n,numsteps,fast,slow,i,additive,g]
    )
    return n,numsteps,additive,g

def inside_while_body(n,numsteps,fast,slow,i,additive,g):
    slow = tf.math.mod(tf.math.add(tf.math.multiply(slow,slow),additive),n)
    i = tf.math.add(i,1)
    fast = tf.math.mod(tf.math.add(tf.math.multiply(fast,fast),additive),n)
    fast = tf.math.mod(tf.math.add(tf.math.multiply(fast,fast),additive),n)
    g = gcd(tf.math.subtract(fast,slow),n)
    n,numsteps,i,additive,g = tf.cond(
        tf.math.not_equal(g,1),
        lambda: factorPR_if_body(n,numsteps,i,additive,g),
        lambda: (n,numsteps,i,additive,g)
    )
    return n,numsteps,fast,slow,i,additive,g
def factorPR_if_body(n,numsteps,i,additive,g):
    n,numsteps,i,additive,g = tf.cond(tf.math.equal(g,n),
        lambda:(n,numsteps,numsteps,(tf.math.add(additive,1)),g),
        lambda:(n,numsteps,numsteps,5,g)
        )
    return n,numsteps,i,additive,g

####################-- helper function --################

@tf.function
def legendre(a, p):
    return pow(a, (p - 1) // 2, p)

@tf.function
def tonelli(n, p):
    assert legendre(n, p) == 1, "not a square (mod p)"
    q = p - 1
    s = 0
    while q % 2 == 0:
        q //= 2
        s += 1
    if s == 1:
        return pow(n, (p + 1) // 4, p)
    for z in range(2, p):
        if p - 1 == legendre(z, p):
            break
    c = pow(z, q, p)
    r = pow(n, (q + 1) // 2, p)
    t = pow(n, q, p)
    m = s
    t2 = 0
    while (t - 1) % p != 0:
        t2 = (t * t) % p
        for i in range(1, m):
            if (t2 - 1) % p == 0:
                break
            t2 = (t2 * t2) % p
        b = pow(c, 1 << (m - i - 1), p)
        r = (r * b) % p
        c = (b * b) % p
        t = (t * c) % p
        m = i
    return r