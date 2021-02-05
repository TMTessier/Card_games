# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 08:32:57 2021

@author: tmusetessier
"""

import random


class Card():
    
    def __init__(self, rank, suit):
        self.rank=rank
        self.suit=suit
       
    def __repr__(self):
        card_rank_names=['Ace','Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten','Jack','Queen','King']
        card_suit_names=['Clubs','Diamonds','Hearts','Spades']
        return card_rank_names[self.rank] + ' of ' + card_suit_names[self.suit]    
        
    def get_rank(self):
        return self.rank
    
    def get_suit(self):
        return self.suit
    
    def set_rank(self,new_rank):
        self.rank=new_rank
        pass    
    
    def set_suit(self,new_suit):
        self.suit=new_suit
        




class Zone():
    def __init__(self,visible,owner):
        self.visible=visible
        self.owner=owner
        self.cards=[]
        
        
    def add_card(self,card):
        self.cards.append(card)
        
    
    def get_cards(self):
        return self.cards
    
    def define_cards(self,cards):
        self.cards=cards
        


    
    
class Deck(Zone):
    def __init__(self):
        super().__init__(visible='visible',owner='game')
        
    def build_standard(self):
        for rank in range(0,13):
            for suit in range(0,4):
                self.add_card(Card(rank,suit))
                
    def shuffle(self):
        decklist=self.get_cards()
        size=len(decklist)
        cut_point=int(size/2)
        for i in range(0,7):
            top_half=decklist[0:cut_point]
            bottom_half=decklist[cut_point:]
            shuffled=[]
            while len(top_half) > 0 and len(bottom_half) > 0:
                halves=(top_half,bottom_half)
                half=random.randint(0,1)
                shuffled.insert(0,halves[half][-1])
                del(halves[half][-1])
            if len(top_half) > 0:
                shuffled=top_half+shuffled
            elif len(bottom_half) > 0:
                shuffled=bottom_half+shuffled
            decklist=shuffled
        self.define_cards(decklist)
        
    def draw(self,number,target_zone):
        for i in range(0,number):
            









class             
