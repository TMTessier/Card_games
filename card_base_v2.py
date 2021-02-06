# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 14:16:00 2021

@author: tmusetessier

sdlkfjsdkl;ajf;klasdjf;lksadjf;kasjfl;aksdjfkjkdsl;
"""

#design to handle card games
import random
import numpy as np

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
    
    def get_rank_number(self):
        return self.rank +1
    
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



class Poker():
    def rank_counting(self, hand):
        cards=hand.get_cardlist()
        ranks=[card.get_rank() for card in cards]
        ranks,counts=np.unique(ranks,return_counts=True)
        return list(ranks),list(counts)
        
    def is_fullhouse(self,ranks,counts):
        hand_counts=counts.copy()
        hand_counts.sort()
        if hand_counts==[2,3]:
            return True
        else:
            return False
        
    def is_fourkind(self,ranks,counts):
        hand_counts=counts.copy()
        hand_counts.sort()
        if hand_counts==[1,4]:
            return True
        else:
            return False
        
    def is_threekind(self,ranks,counts):
        hand_counts=counts.copy()
        hand_counts.sort()
        if hand_counts==[1,1,3]:
            return True
        else:
            return False      
    
    def is_twopair(self,ranks,counts):
        hand_counts=counts.copy()
        hand_counts.sort()
        if hand_counts==[1,2,2]:
            return True
        else:
            return False        
    
    def is_onepair(self,ranks,counts):
        hand_counts=counts.copy()
        hand_counts.sort()
        if hand_counts==[1,1,1,2]:
            return True
        else:
            return False        
    
    def is_flush(self,hand):
        cards=hand.get_cardlist()
        suits=[card.get_suit() for card in cards]
        if len(set(suits))==1:
            return True
        else:
            return False
    
    def is_straight(self,ranks,counts):
        card_ranks=ranks.copy()
        card_ranks.sort()
        if card_ranks[-1] - card_ranks[0] == 4 and len(set(counts)) == 1:
            return True
        else:
            return False
            
    
    
    def is_straightflush(self,hand,ranks,counts):
        if self.is_flush(hand) and self.is_straight(ranks,counts):
            return True
        else:
            return False
    
    def high_card_value(self,cards):
        print(cards)
        card_values=[card.get_rank_number() for card in cards]
        card_values.sort(reverse=False)
        print(card_values)
        high_card_value=0
        for i in range(len(card_values)):
            high_card_value+=card_values[i] * (10 ** (2*i))
        print(high_card_value)
        return high_card_value
        
    
    
    
    def determine_rank(self,hand):
        """
        0 - high card
        1 - one pair
        2 - two pair
        3 - three of a kind
        4 - straight
        5 - flush
        6 - full house
        7 - four of a kind
        8 - straight flush
        9 - royal flush

        Parameters
        ----------
        hand : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        
        ranks,counts=self.rank_counting(hand)
        if self.is_onepair(ranks,counts):
            hand_value=1
            #high card logic
        elif self.is_twopair(ranks,counts):
            """
            still broken
            """
            hand_value=2
            value_index=counts.index(1)
            high_rank=ranks[value_index]
            high_cards=[card for card in hand.get_cardlist() if card.get_rank()==high_rank]
            key_cards=[card for card in hand.get_cardlist() if card.get_rank()!=high_rank]
            hand_value+=key_cards[0].get_rank_number()/100
            hand_value+=self.high_card_value(high_cards)/10000
        elif self.is_threekind(ranks,counts):
            hand_value=3
            value_index=counts.index(3)
            key_rank=ranks[value_index]
            high_cards=[card for card in hand.get_cardlist() if card.get_rank()!=key_rank]
            key_cards=[card for card in hand.get_cardlist() if card.get_rank()==key_rank]
            print(key_cards)
            hand_value+=key_cards[0].get_rank_number()/100
            hand_value+=self.high_card_value(high_cards)/1000000
        elif self.is_fullhouse(ranks,counts):
            hand_value=6
            value_index=counts.index(3)
            key_rank=ranks[value_index]
            high_cards=[card for card in hand.get_cardlist() if card.get_rank()!=key_rank]
            key_cards=[card for card in hand.get_cardlist() if card.get_rank()==key_rank]
            print(key_cards)
            hand_value+=key_cards[0].get_rank_number()/100
            hand_value+=self.high_card_value(high_cards)/1000000
        elif self.is_fourkind(ranks,counts):
            hand_value=7
            value_index=counts.index(4)
            key_rank=ranks[value_index]
            high_cards=[card for card in hand.get_cardlist() if card.get_rank()!=key_rank]
            key_cards=[card for card in hand.get_cardlist() if card.get_rank()==key_rank]
            hand_value+=key_cards[0].get_rank_number()/100
            hand_value+=self.high_card_value(high_cards)/10000
        elif self.is_straightflush(hand,ranks,counts):
            hand_value=8
            sorted_ranks=ranks.copy()
            sorted_ranks.sort()
            key_card=[card for card in hand.get_cardlist() if card.get_rank()==sorted_ranks[-1]]
            hand_value+=key_card[0].get_rank_number()/100
        elif self.is_straight(ranks,counts):
            hand_value=4
            sorted_ranks=ranks.copy()
            sorted_ranks.sort()
            key_card=[card for card in hand.get_cardlist() if card.get_rank()==sorted_ranks[-1]]
            hand_value+=key_card[0].get_rank_number()/100
        elif self.is_flush(hand):
            hand_value=5
            sorted_ranks=ranks.copy()
            sorted_ranks.sort()
            key_card=[card for card in hand.get_cardlist() if card.get_rank()==sorted_ranks[-1]]
            hand_value+=key_card[0].get_rank_number()/100
        else:
            hand_value=0
            #high card logic
        return hand_value

            




class Player():
    def __init__(self,name):
        self.name=name
        self.hand=Hand(name)
        self.discard=Discard(name)
        
poker=Poker()        
for x in range(1):     
    sample_hand=Hand(x)
#    for i in range(5):
#       sample_hand._add_card(Card(4,random.))
    sample_hand._add_card(Card(2,2))
    sample_hand._add_card(Card(2,1))
    sample_hand._add_card(Card(2,0))
    sample_hand._add_card(Card(5,2))
    sample_hand._add_card(Card(8,3))
    print(sample_hand.get_cardlist())
    print(poker.determine_rank(sample_hand))
    
    
    
    
    
    
"""
sleeve zone, one card in sleeve that can be swapped out with card in hand

mark cards, see if card has been dealt in future hands

house rules (ai cheat)

changing card in hand

forcing a fold, throwaway hand

wild cards

colluding if more than 2 players at table

watcher not at table who cna give info

chip manipulation

trick shuffling
"""