import dis
import abc
from re import A
import nacl
import discord
import typing as t
import random
import utils
import threading
import datetime


class StockRiser:
    def __init__(self,__max,__min) -> None:
        self.__max = __max
        self.__min = __min
        self.sourceValue = 0
        self.currentValue = 0

    def rise(self):
        return random.randint(0,self.__max)

    def decrease(self):
        return random.randint(0,self.__min)

    def trends(self):
        maxval = self.rise()
        minval = self.decrease()
        returnValue =  [random.randint(minval,maxval),self.sourceValue]
        self.sourceValue  = self.currentValue
        self.currentValue = returnValue[0] 
        return returnValue

class AsynchroneStockRiser:
    def __init__(self,__max,__min) -> None:
        self.__max = __max
        self.__min = __min
        self.sourceValue = 0
        self.currentValue = 0

    async def rise(self):
        return random.randint(0,self.__max)

    async def decrease(self):
        return random.randint(0,self.__min)

    async def trends(self):
        maxval = self.rise()
        minval = self.decrease()
        returnValue =  [random.randint(minval,maxval),self.sourceValue]
        self.sourceValue  = self.currentValue
        self.currentValue = returnValue[0] 
        return returnValue

class stockConsole:
    def __init__(self,__max,__min,**kwargs) -> None:
        self.stocks = StockRiser(__max,__min)

    def riseUpStocks(self,by:int):
        self.stocks.rise(int)

        
    def decreaseStocksValue(self,by:int):
        self.stocks.decrease(int)        

    @property
    def stocksClassLatency(self):
        tstart = datetime.datetime.now()
        stock = StockRiser(1,-1)
        asyncstock = AsynchroneStockRiser(1,-1)
        tend = datetime.datetime.now()

        return tend-tstart

class InvalidDataType(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class MissingData(InvalidDataType):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

def parse(stock):

    if not isinstance(stock, stockConsole):
        console.error(InvalidDataType)
    latency = stock.stocksClassLatency
    async_parser = AsynchroneStockRiser(stock.riseUpStocks(3),stock.decreaseStocksValue(10))
    return (latency, async_parser)

