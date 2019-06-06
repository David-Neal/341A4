import time
import sympy
import redis

#import antigravity

from flask import Flask

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

@app.route('/isPrime/<number>')
def getPrime(number):
    try:# catches if there is string input
        intNum = int(number)

        for n in cache.keys(): #if the thing is already in the storage, then just return true.
            if n == intNum:
                return '{} is a prime'.format(intNum)

        if sympy.isprime(intNum): #using https://www.sympy.org/en/index.html
            cache.append(intNum, '') #isprime uses Miller-Rabin, and Baillie–PSW, so is reliable, up to numbers larger than the size of an int.
            return '{} is a prime'.format(intNum)
        else:
            return '{} is not a prime'.format(intNum)
    except ValueError:
        return "That's no int! It's a string!"

@app.route('/primesStored')
def stored():
    reVal = ''
    for n in cache.keys():
       reVal = reVal + ' ' + str(int(n))

    return reVal
