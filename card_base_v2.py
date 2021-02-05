# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 14:16:00 2021

@author: tmusetessier
"""

#design to handle card games
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
    #A zone is an area where cards can exist
    #deck, hand, playfield, river, monster zone, etc
    #zone can have cards in it in provided order
    #cards in zone can be visible to all players, one player, or no players
    #All zones need to add cards, remove cards, be viewed by valid players
    #cards move between zones
    def __init__(self,owner=None):
        self.cardlist=[]
        self.owner = owner
        
    def _add_card(self,card):
        self.cardlist.insert(0,card)
        
    def _remove_card(self,card):
        if card in self.cardlist:
            self.cardlist.remove(card)
        else:
            print('Card not in Zone')

    def move_card(self,card,to_zone):
        self._remove_card(card)
        to_zone._add_card(card)
        
    def reveal(self,viewer):
        if viewer in self.viewers:
            print (self.cardlist)
        else:
            print('Not allowed to view zone')
    
    def get_card(self,index):
        return self.cardlist[index]
    
    def get_cardlist(self):
        return self.cardlist
    
    def define_cards(self,cards):
        self.cardlist=cards    
    
    
    
class Deck(Zone):
    #a deck is a zone that is not visible to any players
    #deck needs to be shuffled
    def __init__(self):
        super().__init__('Game')
        
    
    def build_standard(self):
        for rank in range(0,13):
            for suit in range(0,4):
                self._add_card(Card(rank,suit))
                
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
            
    
    def deal(self,number,players):
        for i in range(number):
            for player in players:
                self.move_card(self.get_card(0),player.hand)
    
    
    
class Hand(Zone):
    #a hand is a zone visible to a single player
    def __init__(self,name):
        super().__init__(name)
    
    
class Discard(Zone):
    #a discard is visible to all players
    def __init__(self,name):
        super().__init__(name)

class InPlay(Zone):
    #cards in play are visible to all players
    pass



class Player():
    def __init__(self,name):
        self.name=name
        self.hand=Hand(name)
        self.discard=Discard(name)
        