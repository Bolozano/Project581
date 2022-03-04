'''
 * Copyright (c) 2014, 2015 Entertainment Intelligence Lab, Georgia Institute of Technology.
 * Originally developed by Mark Riedl.
 * Last edited by Mark Riedl 05/2015
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
'''

import sys, pygame, math, numpy, random, time, copy
from pygame.locals import * 

from constants import *
from utils import *
from core import *
from moba import *

class MyMinion(Minion):
    def __init__(self, position, orientation, world, image = NPC, speed = SPEED, viewangle = 360, hitpoints = HITPOINTS, firerate = FIRERATE, bulletclass = SmallBullet):
        Minion.__init__(self, position, orientation, world, image, speed, viewangle, hitpoints, firerate, bulletclass)
        self.states = [Idle,Move,Attack]
		### Add your states to self.states (but don't remove Idle)
        self.world=world
        self.range=bulletclass((0,0),0,None).range
        self.Attackorder=[Tower,Base,Minion]
		### YOUR CODE GOES ABOVE HERE ###

    def start(self):
        Minion.start(self)
        self.changeState(Idle)


############################
### Idle
###
### This is the default state of MyMinion. The main purpose of the Idle state is to figure out what state to change to and do that immediately.

class Idle(State):
	
    def enter(self, oldstate):
        State.enter(self, oldstate)
		# stop moving
        self.agent.stopMoving()
	
    def execute(self, delta = 0):
        State.execute(self, delta)
		### YOUR CODE GOES BELOW HERE ###
        team=self.agent.getTeam()
        aloc=self.agent.getLocation()
        flg=True
        for type in self.agent.Attackorder:
            toattack=[i for i in self.agent.getVisibleType(type) if i.getTeam()!=team and withinRange(i.getLocation(), aloc, self.agent.range)]
            toattack.sort(key=lambda x: x.hitpoints)
            if len(toattack)>0:
                self.agent.changeState(Attack,toattack[0])
                flg=False
                break
        if flg:
            togo=self.agent.world.getEnemyTowers(team)
            if togo==[]:
                togo=self.agent.world.getEnemyBases(team)
            #print(togo[0].getLocation())
            if togo!=[]:
                #print("here")
                self.agent.changeState(Move,togo[0])
		### YOUR CODE GOES ABOVE HERE ###
        return None

##############################
### Taunt
###
### This is a state given as an example of how to pass arbitrary parameters into a State.
### To taunt someome, Agent.changeState(Taunt, enemyagent)

class Taunt(State):

	def parseArgs(self, args):
		self.victim = args[0]

	def execute(self, delta = 0):
		if self.victim is not None:
			print "Hey " + str(self.victim) + ", I don't like you!"
		self.agent.changeState(Idle)

##############################
### YOUR STATES GO HERE:

class Move(State):
    
    def parseArgs(self, args):
        self.target = args[0]
        self.agent.navigateTo(self.target.getLocation())
    
    def execute(self, delta = 0):
        team=self.agent.getTeam()
        #print("move")
        aloc=self.agent.getLocation()
        flg=True
        for type in self.agent.Attackorder:
            toattack=[i for i in self.agent.getVisibleType(type) if i.getTeam()!=team and withinRange(i.getLocation(), aloc, self.agent.range)]
            toattack.sort(key=lambda x: x.hitpoints)
            if len(toattack)>0:
                self.agent.changeState(Attack,toattack[0])
                flg=True
                break
        if flg:
            togo=self.agent.world.getEnemyTowers(team)
            if togo==[]:
                togo=self.agent.world.getEnemyBases(team)
            if togo!=[]:
                if self.target!=togo[0]:
                    self.agent.changeState(Move,togo[0])
            if self.target == None or self.agent.getMoveTarget() == None :
                self.agent.changeState(Idle)
    
class Attack(State):

    def parseArgs(self, args):
        self.victim = args[0]

    def enter(self, oldstate):
        State.enter(self, oldstate)
        # stop moving
        #print("stop")
        self.agent.stopMoving()
        #self.agent.turnToFace(self.victim.getLocation())
        #self.agent.shoot()

    def execute(self, delta = 0):
        #print("shoot")
        aloc=self.agent.getLocation()
        #print(self.agent.getVisible())
        if self.victim is not None and (self.victim in self.agent.getVisible()) and withinRange(aloc, self.victim.getLocation(), self.agent.range):
            self.agent.turnToFace(self.victim.getLocation())
            self.agent.shoot()
        else:
            team=self.agent.getTeam()
            flg=True
            for type in self.agent.Attackorder:
                toattack=[i for i in self.agent.getVisibleType(type) if i.getTeam()!=team and withinRange(i.getLocation(), aloc, self.agent.range)]
                toattack.sort(key=lambda x: x.hitpoints)
                if len(toattack)>0 and toattack[0]!=self.victim:
                    self.agent.changeState(Attack,toattack[0])
                    flg=False
            if flg:
                #print("go again")
                togo=self.agent.world.getEnemyTowers(team)
                if togo==[]:
                    togo=self.agent.world.getEnemyBases(team)
                if togo!=[]:
                    self.agent.changeState(Move,togo[0])
    
    
    
    
    
    
    
    
    
    