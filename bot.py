"""
This is an example for a bot.
"""
from __future__ import division
from penguin_game import *
from math import ceil, floor
import math


siegeMult = 0
siegesMaxTurns = 0
clonebergMult = 0
theCloneberg = None
clonebergMaxTurns = 0
matsavNoash = False
siegeJustArrived = []
siegeConstArrived = []
siegeCounter = 0
siegeConstStarted = []
AlonsBlackList = []
def do_turn(game):
    """
    Makes the bot run a single turn.

    :param game: the current game state.
    :type game: Game
    """
    global siegeMult
    global siegesMaxTurns
    global clonebergMult
    global theCloneberg
    global clonebergMaxTurns
    global matsavNoash
    global siegeJustArrived
    global siegeConstArrived
    global siegeCounter
    global siegeConstStarted
    global AlonsBlackList
    CAEDict = {}
    maxCanSendDICT = {}
    #print "STARTING WITH:",game.get_time_remaining()
    #print "left to timeout1:",game.get_time_remaining()
    myIcebergs = game.get_my_icebergs()
    siegeJustArrived = []
    enemyGroups = game.get_enemy_penguin_groups()
    allIcebergs = game.get_all_icebergs()
    allGroupsMain = game.get_all_penguin_groups()
    
    #allGroupsMain = [i for i in allGroupsMain if i.is_siege_group == False]
    myGroups = game.get_my_penguin_groups()
    if game.get_enemy_icepital_icebergs() == []:
        return
    
    for j in allGroupsMain:
        if j.is_siege_group and j.turns_till_arrival == 0 and j not in siegeConstArrived:
            siegeConstArrived.append(j)
            siegeJustArrived.append(j)
    #siegeJustArrived = [i for i in allGroupsMain if i.is_siege_group and i.turns_till_arrival == 0 and i not in siegeJustArrived]
    
    #print [(i,i.turns_till_arrival) for i in allGroupsMain]
    enemyIcepital = game.get_enemy_icepital_icebergs()[0]
    totalIcepitalSent = 0
    enemyIcebergs = game.get_enemy_icebergs()
    myself = game.get_myself()
    neutralIcebergs = game.get_neutral_icebergs()
    if game.get_my_icepital_icebergs() == []:
        return
    myIcepital = game.get_my_icepital_icebergs()[0]
    enemyIcepitals = game.get_enemy_icepital_icebergs()
    # for i in allGroupsMain:
    #     if i.destination.id == 1:
    #         print "ch",i.destination, myIcepital.get_turns_till_arrival(i.destination)
    timeToDefend = False
    #print "SIEGE:",game.go_through_siege_cost\
    for l in allGroupsMain:
        if l.is_siege_group == False and l.id == 6 and l.destination.id == 2:
            l.turns_till_arrival = l.turns_till_arrival + 1
    if game.turn == 1:
        myIcepital.send_penguins_to_set_siege(enemyIcepital,3)
    #print "TO TAKE SIEGE:",game.go_through_siege_cost
    cloneberg = game.get_cloneberg()
    if game.turn == 1:
        siegeMult = game.go_through_siege_cost
        siegesMaxTurns = game.siege_max_turns
        if cloneberg != None:
            clonebergMult = game.cloneberg_multi_factor
            theCloneberg = game.get_cloneberg()
            clonebergMaxTurns = game.cloneberg_max_pause_turns
            
    
    #print cloneberg
    #print 'SCORE:',myself.score, game.get_enemy().score
    if myIcepital.can_upgrade() and myIcepital.level == 1 and myIcepital.already_acted == False and len(myIcebergs) > 1 and enemyIcepital.level > 1 and sum([i.penguin_amount for i in enemyGroups if i.destination == myIcepital and i.is_siege_group == False]) < myIcepital.penguin_amount - myIcepital.upgrade_cost:
            myIcepital.upgrade()
    closestToCloneberg = []
    sortedNotMine = sorted([i for i in allIcebergs if i != myIcepital], key = lambda x:x.get_turns_till_arrival(myIcepital))[0 : int((len(allIcebergs) - 2) / 2)]
    codeRed = False
    
    if cloneberg != None:

        closestToClonebergList = sorted(allIcebergs, key=lambda x: x.get_turns_till_arrival(cloneberg))
        closestToCloneberg = [i for i in closestToClonebergList[0:int((len(closestToClonebergList)-2)/2)] if i.owner == myself and i != myIcepital]
        #print 'closestToCloneberg[0]', closestToCloneberg
        sendersToCloneberg = []
        diff = len(myIcebergs) - len(enemyIcebergs)
        if diff < 1:
            diff = 1
        sendersToCloneberg = closestToCloneberg[0 : diff]
        
    myHeadedToEnemyIcepital = [j for j in myGroups if j.destination == enemyIcepital]
    enemyHeadedToIcepital = [j for j in enemyGroups if j.destination == myIcepital and j.is_siege_group == False]
    headedToIcepital = [i for i in allGroupsMain if i.destination == myIcepital]
    
    thierHalf = sorted([i for i in allIcebergs if i != myIcepital], key = lambda x:x.get_turns_till_arrival(enemyIcepital))[0 : int((len(allIcebergs) - 2) / 2)]
    sortedNotMine = sorted([i for i in allIcebergs if i != myIcepital], key = lambda x:x.get_turns_till_arrival(myIcepital))[0 : int((len(allIcebergs) - 2) / 2)]

    CAEIcepital = calcAtEndNewInitial(game.acceleration_factor, myIcepital.penguin_amount, myIcepital, allGroupsMain, myIcebergs, enemyIcebergs, ["ME"])
    maxCanSendIcepital = maxCanSend(myIcepital, [j for j in allGroupsMain if j.destination == myIcepital], myIcebergs, enemyIcebergs,1, maxCanSendDICT,CAEDict, game.acceleration_factor)
    
    if CAEIcepital[0] < 0:
        for i in myIcebergs:
            if i != myIcepital:
                if i.is_under_siege == False and myIcepital.is_under_siege == False:
                    i.send_penguins(myIcepital, i.penguin_amount)
                else: 
                    i.send_penguins(myIcepital, int(i.penguin_amount - i.penguin_amount % 3))
                
    #siegeOnOurIcebergs = sum([i.penguin_amount for i in enemyGroups if i.destination in myIcebergs and i.is_siege_group and i.turns_till_arrival == 0])
    icebergsTurnsToEnemyIcepital = list([p.penguin_amount - sum([i.penguin_amount for i in enemyGroups if i.destination == p and i.is_siege_group and i.turns_till_arrival == 0]) * game.go_through_siege_cost - sum([k.penguin_amount for k in enemyGroups if k.destination == p and k.is_siege_group == False]) for p in myIcebergs])
        #print "icebergsTurnsToEnemyIcepital:",icebergsTurnsToEnemyIcepital
    for k in range(len(icebergsTurnsToEnemyIcepital)):
        l = icebergsTurnsToEnemyIcepital[k]
        for i in range(3):
            l /= game.acceleration_cost
            l = int(floor(l))
        icebergsTurnsToEnemyIcepital[k] = l
    sumAcc = sum(icebergsTurnsToEnemyIcepital)
    
    for m in range(len(enemyIcepitals)):
        
        sumWhatNotIcepital = 0
        for i in enemyIcebergs:
            if i == enemyIcepitals[m]: continue
            current = i.penguin_amount - sum([j.penguin_amount for j in myGroups if j.destination == i and j.is_siege_group and j.turns_till_arrival == 0]) * game.go_through_siege_cost
            if current < 0: current = 0
            sumWhatNotIcepital += current
        #print "sumAcc:",sumAcc
        #print "else",ceil((max(myIcebergs, key = lambda x: x.get_turns_till_arrival(enemyIcepital)).get_turns_till_arrival(enemyIcepital) / 8 + 2) * enemyIcepital.penguins_per_turn) + enemyIcepital.penguin_amount + sumWhatNotIcepital / 2.2
        if maxCanSendIcepital == myIcepital.penguin_amount and sumAcc > ceil((max(myIcebergs, key = lambda x: x.get_turns_till_arrival(enemyIcepitals[m])).get_turns_till_arrival(enemyIcepitals[m]) / (game.acceleration_factor ** 3) + 2) * enemyIcepitals[m].penguins_per_turn) + enemyIcepitals[m].penguin_amount + sumWhatNotIcepital / (game.acceleration_cost ** 3):
            #print 'hamas is making it rain rockets*!*!*!*!**!!*!*!*!*!*!*!*!*!*!*!**!*!*!**!*!**!*!*!*!*!*!*!*!*'
            for i in myIcebergs:
                i.send_penguins(enemyIcepitals[m], i.penguin_amount)
            break
    #print "hamasCheck:",hamasCheck
     
    for i in myGroups:
        if (cloneberg != None and i.destination == cloneberg):
            continue
        #print "not continuing",i
        accelerateGroup(i, [m for m in allGroupsMain if m.destination == i.destination] ,myIcebergs, enemyIcebergs,game.acceleration_factor,game.acceleration_cost,CAEDict)
    #print "time:",game.get_time_remaining()
    myIcebergsNew = list(myIcebergs)
    enemyIcepitalRealAmount = enemyIcepital.penguin_amount - sum([i.penguin_amount for i in myGroups if i.destination == enemyIcepital and i.is_siege_group == True and i.turns_till_arrival == 0]) * siegeMult
    
    if (enemyIcepitalRealAmount > myIcepital.penguin_amount * 1.4) or (myIcepital.penguins_per_turn == enemyIcepital.penguins_per_turn and myIcepital.penguin_amount * 1.5 < enemyIcepitalRealAmount) or (len(myIcebergs) > 1 and len(enemyIcebergs) == 1 and enemyGroups == []) or (len(myIcebergs) > len(sortedNotMine) + 1 and myIcepital.penguin_amount < enemyIcepitalRealAmount) or (enemyHeadedToIcepital != [] and sum([i.penguin_amount for i in enemyHeadedToIcepital]) > myIcepital.penguin_amount):
        myIcebergsNew.remove(myIcepital)
    
    specifico = False
    enemySiegerGroups = [i for i in enemyGroups if i.is_siege_group]
    
    for g in enemySiegerGroups:
        if g not in siegeConstStarted:
            siegeConstStarted.append(g)
            siegeCounter += g.penguin_amount
    
    if cloneberg != None:
        starter = False
        toPick = list(set(myIcebergs + sortedNotMine + enemyIcebergs + [i for i in neutralIcebergs if [m for m in enemyGroups if m.destination == i] != []]))
        closestToC = min(sortedNotMine, key = lambda x:x.get_turns_till_arrival(cloneberg) * (x.penguin_amount * x.penguin_amount))
        if game.turn == 3 and closestToC != None:
            myIcepital.send_penguins(closestToC,1)
        if len(myIcebergs) == 1 and [i for i in myGroups if i.destination == closestToC] == []:
            toPick = [closestToC]
        toPick = [i for i in toPick if len([j for j in allGroupsMain if j.destination == i]) <= 20]
        if not(game.turn > 1 and [i for i in enemyGroups if i.is_siege_group == False] != [] and [i for i in enemyGroups if i.is_siege_group == False][0].penguin_amount - [i for i in enemyGroups if i.is_siege_group == False][0].destination.penguin_amount > 4) and len(enemyIcebergs) < 3 and len(myIcebergs) == 1 and [l for l in myGroups if l.is_siege_group] != []:
            #print "SDIDDSD",seigeTurns([l for l in myGroups if l.is_siege_group][0].source.get_turns_till_arrival([l for l in myGroups if l.is_siege_group][0].destination),[l for l in myGroups if l.is_siege_group][0].turns_till_arrival)
            if seigeTurns([l for l in myGroups if l.is_siege_group][0].source.get_turns_till_arrival([l for l in myGroups if l.is_siege_group][0].destination),[l for l in myGroups if l.is_siege_group][0].turns_till_arrival) > 0:
                
                toPick = []
            else:
                toPick = neutralIcebergs
                if cloneberg != None:
                    toPick = [i for i in toPick if i != cloneberg]
            starter = True
            #print "starter: True",[(i.penguin_amount,i) for i in toPick]
        for i in sendersToCloneberg:
            
            CAEDict[(i,i.penguin_amount)] = calcAtEndNewInitial(game.acceleration_factor, i.penguin_amount,i, allGroupsMain, myIcebergs, enemyIcebergs,["ME"])
        toPick = [i for i in toPick if i not in sendersToCloneberg or (i in sendersToCloneberg and CAEDict[(i,i.penguin_amount)][0] < 0)]
        toPick = [i for i in toPick if i != enemyIcepital]
        #print "myIcebergsNew:",myIcebergsNew    
        siegeOnIcepital = sum([i.penguin_amount for i in enemyGroups if i.turns_till_arrival == 0 and i.destination == enemyIcepital])
        if myIcepital.penguin_amount - siegeOnIcepital * game.go_through_siege_cost < 10 and game.turn > 30 and myIcepital in myIcebergsNew:
            myIcebergsNew.remove(myIcepital)
        
        #print 'MYICEEEEEE', myIcebergsNew
        #print "toPick:",toPick
        tupleFunc = automateTask(toPick, allGroupsMain, myself, myIcebergsNew, enemyIcebergs, myIcebergs, allIcebergs, sortedNotMine, enemyHeadedToIcepital, maxCanSendDICT,CAEDict, closestToCloneberg, starter, closestToC, game.acceleration_cost, game.acceleration_factor)
        if myIcepital in myIcebergsNew and len(myIcebergs) == 1 and len(enemyIcebergs) == 1 and tupleFunc[0][2] != [] and myIcepital in tupleFunc[0][2].keys() and len(enemyHeadedToIcepital) == 1 and enemyHeadedToIcepital[0].penguin_amount > myIcepital.penguin_amount - tupleFunc[0][2][myIcepital]:
            tupleFunc = ([],[],[])
            #print "make it good"
        if game.turn == 1: return
        attSuc = False
        if tupleFunc[0] != [] and tupleFunc[0][2] != [] and myIcepital in tupleFunc[0][2] and myIcepital.penguin_amount - tupleFunc[0][2][myIcepital] + 5 < (sum([p.penguin_amount for p in enemyIcebergs]) - sum([i.penguin_amount for i in myGroups if i.turns_till_arrival == 0 and i.is_siege_group and i.destination == enemyIcepital]) * 3) / (game.acceleration_factor ** 3):
            tupleFunc = ([],[],[])
            #print 'make it good 2'
        if tupleFunc[0] != [] and tupleFunc[0][2] != [] and not(tupleFunc[0][0] in neutralIcebergs and len([i for i in enemyIcebergs if i.is_under_siege ]) - len(enemyIcebergs) < -2 and len(myIcebergs) > 1):
            for ice in tupleFunc[0][2].keys():
                if len(myIcebergs) > 1 and min(myIcebergs, key = lambda x : x.get_turns_till_arrival(enemyIcepital)) in tupleFunc[0][2].keys() and abs(min([h for h in allIcebergs if h != enemyIcepital], key = lambda x : x.get_turns_till_arrival(enemyIcepital)).get_turns_till_arrival(enemyIcepital) - min(myIcebergs, key = lambda x : x.get_turns_till_arrival(enemyIcepital)).get_turns_till_arrival(enemyIcepital)) < 2 and (tupleFunc[0][0] in neutralIcebergs or (tupleFunc[0][0] in myIcebergs and [k for k in enemyGroups if k.is_siege_group == False and k.destination == tupleFunc[0][0]] == [])) :
                    break
                print min(myIcebergs, key = lambda x : x.get_turns_till_arrival(enemyIcepital)) in tupleFunc[0][2].keys(),min([h for h in allIcebergs if h != enemyIcepital], key = lambda x : x.get_turns_till_arrival(enemyIcepital)),min([h for h in allIcebergs if h != enemyIcepital], key = lambda x : x.get_turns_till_arrival(enemyIcepital)).get_turns_till_arrival(enemyIcepital),min(myIcebergs, key = lambda x : x.get_turns_till_arrival(enemyIcepital)).get_turns_till_arrival(enemyIcepital),min(myIcebergs, key = lambda x : x.get_turns_till_arrival(enemyIcepital))
                if tupleFunc[0][2][ice] > 0 :
                    print ice.penguin_amount
                    ice.send_penguins(tupleFunc[0][0],tupleFunc[0][2][ice])
                    
        if tupleFunc[1] != [] and tupleFunc[1][2] != []:
            for ice in tupleFunc[1][2].keys():
                if tupleFunc[1][2][ice] > 0:
                    print ice.penguin_amount
                    ice.send_penguins(tupleFunc[1][0],tupleFunc[1][2][ice])
                    attSuc = True

        #print "main:",tupleFunc[0]
        #print "secondary:",tupleFunc[1]
        if specifico == True and myIcepital not in myIcebergsNew:
            myIcebergsNew.append(myIcepital)
        
        for i in enemyGroups:
            if i.destination == cloneberg:
                if i.source not in AlonsBlackList:
                    AlonsBlackList.append(i.source)
        

        for i in AlonsBlackList:
            if i not in enemyIcebergs:
                continue
            enemyHeadedtoTarget = [m for m in enemyGroups if m.destination == i]
            enemyHeadedToClonebergFromTarget = [m for m in enemyGroups if m.source == i and m.destination == cloneberg] #Add case where there is no cloneberg
            amountToSiege = 0
            if [k for k in enemyHeadedtoTarget if k.turns_till_arrival == 7] != []:
                amountToSiege += int(ceil(sum([l.penguin_amount for l in enemyHeadedtoTarget if 7 <= l.turns_till_arrival <= 7 + game.siege_max_turns ]) / game.go_through_siege_cost))
                amountToSiege += int(ceil(sum([l.penguin_amount for l in enemyHeadedToClonebergFromTarget if 7 <= l.turns_till_arrival + game.cloneberg_max_pause_turns + cloneberg.get_turns_till_arrival(l.source) <= 7 + game.siege_max_turns ]) / game.go_through_siege_cost)) * game.cloneberg_multi_factor
            #If they are currently on the cloneberg, add time on cloneberg - maybe add (-1)
            if [k for k in enemyHeadedToClonebergFromTarget if k.turns_till_arrival + game.cloneberg_max_pause_turns + cloneberg.get_turns_till_arrival(k.source) == 7] != []:
                amountToSiege += int(ceil(sum([l.penguin_amount for l in enemyHeadedToClonebergFromTarget if 7 <= l.turns_till_arrival + game.cloneberg_max_pause_turns + cloneberg.get_turns_till_arrival(l.source) <= 7 + game.siege_max_turns ]) / game.go_through_siege_cost)) * game.cloneberg_multi_factor
                amountToSiege += int(ceil(sum([l.penguin_amount for l in enemyHeadedtoTarget if 7 <= l.turns_till_arrival <= 7 + game.siege_max_turns ]) / game.go_through_siege_cost))
            
            
            specialAmountToSiege = 0 
            if amountToSiege ==0:
                p = len([k for k in enemyGroups if k.destination == cloneberg and k.source == i])
                if p!=0:
                    specialAmountToSiege += sum([k.penguin_amount for k in enemyGroups if k.destination == cloneberg])/p *7
            amountToSiege += specialAmountToSiege
            if amountToSiege == 0:
                continue
            if [k for k in myIcebergs if k.is_under_siege == False] != [] and [t for t in myIcebergs if t.is_under_siege == False and [k for k in enemyGroups if k.destination == t and k.is_siege_group == False] == []] != []:
                bestToSendSiege1 = max([p for p in myIcebergs if p.is_under_siege == False and [l for l in enemyGroups if l.destination == p and l.is_siege_group == False] == []], key = lambda x: x.penguin_amount)
                
                maxi = maxCanSend(bestToSendSiege1, [j for j in allGroupsMain if j.destination == bestToSendSiege1], myIcebergs, enemyIcebergs,0, maxCanSendDICT,CAEDict,game.acceleration_factor)
                if bestToSendSiege1.already_acted == False and maxi >= amountToSiege and bestToSendSiege1.can_send_penguins_to_set_siege(i, int(amountToSiege)):
                    bestToSendSiege1.send_penguins_to_set_siege(i, int(amountToSiege))
                    break
                elif bestToSendSiege1.can_send_penguins_to_set_siege(i, int(maxi)):
                    bestToSendSiege1.send_penguins_to_set_siege(i, int(maxi))

                    break
                
        if [i for i in myIcebergs if i.is_under_siege == False] != [] and [i for i in myIcebergs if i.is_under_siege == False and [k for k in enemyGroups if k.destination == i and k.is_siege_group == False] == []] != []:
            bestToSendSiege1 = max([i for i in myIcebergs if i.is_under_siege == False and [k for k in enemyGroups if k.destination == i and k.is_siege_group == False] == []], key = lambda x: x.penguin_amount)
            print bestToSendSiege1
            if len(myIcebergs) > 1 and bestToSendSiege1 != [] and bestToSendSiege1 != None:
                for i in sorted(enemyIcebergs, key = lambda x: x.penguin_amount):
                    if i not in AlonsBlackList:
                        if remainAtEnd(i,1, allGroupsMain, myself,myIcebergs, enemyIcebergs,1, i.unique_id, game.acceleration_factor)[0] != 100000 and game.turn != 16:
                            if bestToSendSiege1.can_send_penguins_to_set_siege(i, 2):
                                bestToSendSiege1.send_penguins_to_set_siege(i, 2)
                                break
    
        if sum([i.penguins_per_turn for i in myIcebergs]) >= sum([i.penguins_per_turn for i in enemyIcebergs]) or sum([i.penguin_amount for i in myIcebergs]) + sum([i.penguin_amount for i in myGroups]) >= sum([i.penguin_amount for i in enemyIcebergs]) + sum([i.penguin_amount for i in enemyGroups]):   
            for i in myIcebergsNew:
                isClosest = False
                if closestToCloneberg != [] and i == closestToCloneberg[0]:
                    isClosest = True
                closestEnemy = min(enemyIcebergs, key = lambda x:x.get_turns_till_arrival(i))
                
                if i.can_upgrade() and i.already_acted == False and calcAtEndNewInitial(game.acceleration_factor, i.penguin_amount - i.upgrade_cost,i, allGroupsMain, myIcebergs, enemyIcebergs,["ME"], forUpgrade = True)[0] > 0 and game.turn > 1 :
                    if i == myIcepital and i.level == 3 and sum([k.penguin_amount for k in myIcebergs]) + sum([k.penguin_amount for k in myGroups]) - i.upgrade_cost < sum([k.penguin_amount for k in enemyIcebergs]) + sum([k.penguin_amount for k in enemyGroups]):
                        continue
                    if (i in closestToCloneberg and i.level > 1) or (i == myIcepital and enemyIcepital.level <= myIcepital.level):
                        continue
                    if abs(min([k for k in allIcebergs if k != enemyIcepital], key = lambda x: x.get_turns_till_arrival(enemyIcepital)).get_turns_till_arrival(enemyIcepital) - i.get_turns_till_arrival(enemyIcepital)) < 2:
                        continue
                    i.upgrade()   
        if closestToCloneberg != [] and closestToCloneberg[0].penguin_amount + sum([i.penguin_amount for i in myGroups if i.destination == closestToCloneberg[0]]) - sum([i.penguin_amount for i in enemyGroups if i.destination == closestToCloneberg[0]]) > sum([i.penguin_amount for i in enemyIcebergs]) + enemyIcepital.penguins_per_turn * closestToCloneberg[0].get_turns_till_arrival(enemyIcepital):
            hamasProtocol = True
            
        elif CAEIcepital[0] > 0 and not(len(enemyIcebergs) == 2 and len(myIcebergs + enemyIcebergs) == len(allIcebergs)):
            
            if len(myIcebergs) > len(enemyIcebergs) and closestToCloneberg != []:
                diff = len(myIcebergs) - len(enemyIcebergs)
                print len(closestToCloneberg)
                
                for i in range(diff):
                    if len(closestToCloneberg) > i:
                        if closestToCloneberg[i] not in sortedNotMine or (closestToCloneberg[i].level == 1):
                            continue
                        CAE = calcAtEndNewInitial(game.acceleration_factor, closestToCloneberg[i].penguins_per_turn,closestToCloneberg[i], allGroupsMain, myIcebergs, enemyIcebergs,["ME"])
                        if CAE[0] > 0 and closestToCloneberg[i].already_acted == False:
                            sumSiege = sum([j.penguin_amount for j in enemyGroups if j.is_siege_group == True and j.destination == closestToCloneberg[i] and seigeTurns(j.source.get_turns_till_arrival(j.destination),j.turns_till_arrival) == 0])
                            #print "i:",i
                            if closestToCloneberg[i].penguin_amount - sumSiege * game.go_through_siege_cost >= 3:
                                print closestToCloneberg[i], 'sends',closestToCloneberg[i].penguin_amount,'0'
                                closestToCloneberg[i].send_penguins(cloneberg,closestToCloneberg[i].penguin_amount)
            else:
                if closestToCloneberg != [] and closestToCloneberg[0] in sortedNotMine and closestToCloneberg[0].level > 1:
                    CAE = calcAtEndNewInitial(game.acceleration_factor, closestToCloneberg[0].penguins_per_turn,closestToCloneberg[0], allGroupsMain, myIcebergs, enemyIcebergs,["ME"])
                    if CAE[0] > 0 and closestToCloneberg[0].already_acted == False:
                        sumSiege = sum([j.penguin_amount for j in enemyGroups if j.is_siege_group == True and j.destination == closestToCloneberg[0] and seigeTurns(j.source.get_turns_till_arrival(j.destination),j.turns_till_arrival) == 0])
                            #print "i:",i
                        if closestToCloneberg[0].penguin_amount - sumSiege * game.go_through_siege_cost >= 3:
                            print closestToCloneberg[0], 'sends',closestToCloneberg[0].penguin_amount,'1'
                            closestToCloneberg[0].send_penguins(cloneberg,closestToCloneberg[0].penguin_amount)
                            #print "sending friend"

                
        print "LAST TIME I SEE ACC:",game.get_time_remaining()
    else:
        starter = False
        toPick = list(set(myIcebergs + sortedNotMine + enemyIcebergs + [i for i in neutralIcebergs if [m for m in enemyGroups if m.destination == i] != []]))
        toPick = [i for i in toPick if len([j for j in allGroupsMain if j.destination == i]) <= 20]
        if not(game.turn > 1 and [i for i in enemyGroups if i.is_siege_group == False] != [] and [i for i in enemyGroups if i.is_siege_group == False][0].penguin_amount - [i for i in enemyGroups if i.is_siege_group == False][0].destination.penguin_amount > 4) and len(enemyIcebergs) < 3 and len(myIcebergs) == 1 and [l for l in myGroups if l.is_siege_group] != []:
            #print "SDIDDSD",seigeTurns([l for l in myGroups if l.is_siege_group][0].source.get_turns_till_arrival([l for l in myGroups if l.is_siege_group][0].destination),[l for l in myGroups if l.is_siege_group][0].turns_till_arrival)
            if seigeTurns([l for l in myGroups if l.is_siege_group][0].source.get_turns_till_arrival([l for l in myGroups if l.is_siege_group][0].destination),[l for l in myGroups if l.is_siege_group][0].turns_till_arrival) > 0:
                
                toPick = []
            else:
                toPick = neutralIcebergs
            starter = True

        toPick = [i for i in toPick if i != enemyIcepital]
        #print "myIcebergsNew:",myIcebergsNew    
        siegeOnIcepital = sum([i.penguin_amount for i in enemyGroups if i.turns_till_arrival == 0 and i.destination == enemyIcepital])
        if myIcepital.penguin_amount - siegeOnIcepital * game.go_through_siege_cost < 10 and game.turn > 30 and myIcepital in myIcebergsNew:
            myIcebergsNew.remove(myIcepital)
        
        tupleFunc = automateTask(toPick, allGroupsMain, myself, myIcebergsNew, enemyIcebergs, myIcebergs, allIcebergs, sortedNotMine, enemyHeadedToIcepital, maxCanSendDICT,CAEDict, closestToCloneberg, starter, None, game.acceleration_cost, game.acceleration_factor)
        if myIcepital in myIcebergsNew and len(myIcebergs) == 1 and len(enemyIcebergs) == 1 and tupleFunc[0][2] != [] and myIcepital in tupleFunc[0][2].keys() and len(enemyHeadedToIcepital) == 1 and enemyHeadedToIcepital[0].penguin_amount > myIcepital.penguin_amount - tupleFunc[0][2][myIcepital]:
            tupleFunc = ([],[],[])
            #print "make it good"
        if game.turn == 1: return
        attSuc = False
        if tupleFunc[0] != [] and tupleFunc[0][2] != [] and myIcepital in tupleFunc[0][2] and myIcepital.penguin_amount - tupleFunc[0][2][myIcepital] + 5 < (sum([p.penguin_amount for p in enemyIcebergs]) - sum([i.penguin_amount for i in myGroups if i.turns_till_arrival == 0 and i.is_siege_group and i.destination == enemyIcepital]) * 3) / 8:
            tupleFunc = ([],[],[])
            #print 'make it good 2'
        if tupleFunc[0] != [] and tupleFunc[0][2] != [] and not(tupleFunc[0][0] in neutralIcebergs and len([i for i in enemyIcebergs if i.is_under_siege ]) - len(enemyIcebergs) < -2 and len(myIcebergs) > 1):
            for ice in tupleFunc[0][2].keys():
                if len(myIcebergs) > 1 and min(myIcebergs, key = lambda x : x.get_turns_till_arrival(enemyIcepital)) in tupleFunc[0][2].keys() and abs(min([h for h in allIcebergs if h != enemyIcepital], key = lambda x : x.get_turns_till_arrival(enemyIcepital)).get_turns_till_arrival(enemyIcepital) - min(myIcebergs, key = lambda x : x.get_turns_till_arrival(enemyIcepital)).get_turns_till_arrival(enemyIcepital)) < 2 and (tupleFunc[0][0] in neutralIcebergs or (tupleFunc[0][0] in myIcebergs and [k for k in enemyGroups if k.is_siege_group == False and k.destination == tupleFunc[0][0]] == [])) :
                    break
                print min(myIcebergs, key = lambda x : x.get_turns_till_arrival(enemyIcepital)) in tupleFunc[0][2].keys(),min([h for h in allIcebergs if h != enemyIcepital], key = lambda x : x.get_turns_till_arrival(enemyIcepital)),min([h for h in allIcebergs if h != enemyIcepital], key = lambda x : x.get_turns_till_arrival(enemyIcepital)).get_turns_till_arrival(enemyIcepital),min(myIcebergs, key = lambda x : x.get_turns_till_arrival(enemyIcepital)).get_turns_till_arrival(enemyIcepital),min(myIcebergs, key = lambda x : x.get_turns_till_arrival(enemyIcepital))
                if tupleFunc[0][2][ice] > 0 :
                    print ice.penguin_amount
                    ice.send_penguins(tupleFunc[0][0],tupleFunc[0][2][ice])
                    
        if tupleFunc[1] != [] and tupleFunc[1][2] != []:
            for ice in tupleFunc[1][2].keys():
                if tupleFunc[1][2][ice] > 0:
                    print ice.penguin_amount
                    ice.send_penguins(tupleFunc[1][0],tupleFunc[1][2][ice])
                    attSuc = True

        #print "main:",tupleFunc[0]
        #print "secondary:",tupleFunc[1]
        if specifico == True and myIcepital not in myIcebergsNew:
            myIcebergsNew.append(myIcepital)
        
        for i in enemyGroups:
            if i.destination == cloneberg:
                if i.source not in AlonsBlackList:
                    AlonsBlackList.append(i.source)
        

        for i in AlonsBlackList:
            if i not in enemyIcebergs:
                continue
            enemyHeadedtoTarget = [m for m in enemyGroups if m.destination == i]
            #enemyHeadedToClonebergFromTarget = [m for m in enemyGroups if m.source == i and m.destination == cloneberg] #Add case where there is no cloneberg
            amountToSiege = 0
            if [k for k in enemyHeadedtoTarget if k.turns_till_arrival == 7] != []:
                amountToSiege += int(ceil(sum([l.penguin_amount for l in enemyHeadedtoTarget if 7 <= l.turns_till_arrival <= 7 + game.siege_max_turns ]) / game.go_through_siege_cost))
                #amountToSiege += int(ceil(sum([l.penguin_amount for l in enemyHeadedToClonebergFromTarget if 7 <= l.turns_till_arrival + game.cloneberg_max_pause_turns + cloneberg.get_turns_till_arrival(l.source) <= 7 + game.siege_max_turns ]) / game.go_through_siege_cost)) * game.cloneberg_multi_factor
            #If they are currently on the cloneberg, add time on cloneberg - maybe add (-1)
            if [k for k in enemyHeadedToClonebergFromTarget if k.turns_till_arrival + game.cloneberg_max_pause_turns + cloneberg.get_turns_till_arrival(k.source) == 7] != []:
                #amountToSiege += int(ceil(sum([l.penguin_amount for l in enemyHeadedToClonebergFromTarget if 7 <= l.turns_till_arrival + game.cloneberg_max_pause_turns + cloneberg.get_turns_till_arrival(l.source) <= 7 + game.siege_max_turns ]) / game.go_through_siege_cost)) * game.cloneberg_multi_factor
                amountToSiege += int(ceil(sum([l.penguin_amount for l in enemyHeadedtoTarget if 7 <= l.turns_till_arrival <= 7 + game.siege_max_turns ]) / game.go_through_siege_cost))
            
            
            if amountToSiege == 0:
                continue
            if [k for k in myIcebergs if k.is_under_siege == False] != [] and [t for t in myIcebergs if t.is_under_siege == False and [k for k in enemyGroups if k.destination == t and k.is_siege_group == False] == []] != []:
                bestToSendSiege1 = max([p for p in myIcebergs if p.is_under_siege == False and [l for l in enemyGroups if l.destination == p and l.is_siege_group == False] == []], key = lambda x: x.penguin_amount)
                
                maxi = maxCanSend(bestToSendSiege1, [j for j in allGroupsMain if j.destination == bestToSendSiege1], myIcebergs, enemyIcebergs,0, maxCanSendDICT,CAEDict,game.acceleration_factor)
                if bestToSendSiege1.already_acted == False and maxi >= amountToSiege and bestToSendSiege1.can_send_penguins_to_set_siege(i, int(amountToSiege)):
                    bestToSendSiege1.send_penguins_to_set_siege(i, int(amountToSiege))
                    break
                elif bestToSendSiege1.can_send_penguins_to_set_siege(i, int(maxi)):
                    bestToSendSiege1.send_penguins_to_set_siege(i, int(maxi))

                    break
                
        if [i for i in myIcebergs if i.is_under_siege == False] != [] and [i for i in myIcebergs if i.is_under_siege == False and [k for k in enemyGroups if k.destination == i and k.is_siege_group == False] == []] != []:
            bestToSendSiege1 = max([i for i in myIcebergs if i.is_under_siege == False and [k for k in enemyGroups if k.destination == i and k.is_siege_group == False] == []], key = lambda x: x.penguin_amount)
            print bestToSendSiege1
            if len(myIcebergs) > 1 and bestToSendSiege1 != [] and bestToSendSiege1 != None:
                for i in sorted(enemyIcebergs, key = lambda x: x.penguin_amount):
                    if i not in AlonsBlackList:
                        if remainAtEnd(i,1, allGroupsMain, myself,myIcebergs, enemyIcebergs,1, i.unique_id,game.acceleration_factor)[0] != 100000 and game.turn != 16:
                            if bestToSendSiege1.can_send_penguins_to_set_siege(i, 2):
                                bestToSendSiege1.send_penguins_to_set_siege(i, 2)
                                break
    
        if sum([i.penguins_per_turn for i in myIcebergs]) >= sum([i.penguins_per_turn for i in enemyIcebergs]) or sum([i.penguin_amount for i in myIcebergs]) + sum([i.penguin_amount for i in myGroups]) >= sum([i.penguin_amount for i in enemyIcebergs]) + sum([i.penguin_amount for i in enemyGroups]):   
            for i in myIcebergsNew:
                closestEnemy = min(enemyIcebergs, key = lambda x:x.get_turns_till_arrival(i))
                
                if i.can_upgrade() and i.already_acted == False and calcAtEndNewInitial(game.acceleration_factor, i.penguin_amount - i.upgrade_cost,i, allGroupsMain, myIcebergs, enemyIcebergs,["ME"], forUpgrade = True)[0] > 0 and game.turn > 1 :
                    if i == myIcepital and i.level == 3 and sum([k.penguin_amount for k in myIcebergs]) + sum([k.penguin_amount for k in myGroups]) - i.upgrade_cost < sum([k.penguin_amount for k in enemyIcebergs]) + sum([k.penguin_amount for k in enemyGroups]):
                        continue
                    if (i == myIcepital and enemyIcepital.level <= myIcepital.level):
                        continue
                    if abs(min([k for k in allIcebergs if k != enemyIcepital], key = lambda x: x.get_turns_till_arrival(enemyIcepital)).get_turns_till_arrival(enemyIcepital) - i.get_turns_till_arrival(enemyIcepital)) < 2:
                        continue
                    i.upgrade()
def automateTask(toPick, allGroupsMain, myself, myIcebergsNew, enemyIcebergs, myIcebergs, allIcebergs, ourHalf, enemyHeadedToIcepital, maxCanSendDICT,CAEDict,closestToCloneberg, starter, closestToC, accCost, accFactor):
    toPick1 = list(toPick)
    #print "time before pickBestTartget:",game1.get_time_remaining()
    
    IcebergTargetList = needConquer(toPick, allGroupsMain, myself, myIcebergsNew, enemyIcebergs,myIcebergs, ourHalf, maxCanSendDICT,CAEDict, closestToCloneberg, accCost, accFactor)
    IcebergTargetList = [i for i in IcebergTargetList if i[0] != {}]
    targets = toPick
    if starter and seigeTurns([l for l in allGroupsMain if l.owner == myself and l.is_siege_group][0].source.get_turns_till_arrival([l for l in allGroupsMain if l.owner == myself and l.is_siege_group][0].destination),[l for l in allGroupsMain if l.owner == myself and l.is_siege_group][0].turns_till_arrival) == 0:
        targets = [i for i in toPick if [m for m in allGroupsMain if m.owner != myself and m.destination == i] != []] + enemyIcebergs
    rocketAtt = rocketAttack(myIcebergs,enemyIcebergs,targets,myself,allGroupsMain, closestToCloneberg, accCost , accFactor)
    if rocketAtt != None:
        if starter and seigeTurns([l for l in allGroupsMain if l.owner == myself and l.is_siege_group][0].source.get_turns_till_arrival([l for l in allGroupsMain if l.owner == myself and l.is_siege_group][0].destination),[l for l in allGroupsMain if l.owner == myself and l.is_siege_group][0].turns_till_arrival) < 2:
            IcebergTargetList = []
        
        IcebergTargetList.append(rocketAtt)
    if starter and rocketAtt == None and closestToC != None:
        toPick = [closestToC]
    #print "IcebergTargetList:",IcebergTargetList
    tupleFuncAttack = pickBestTarget(IcebergTargetList, allIcebergs, allGroupsMain, myself, myIcebergs, enemyIcebergs,CAEDict)
    #print "tupleFuncAttack:",tupleFuncAttack
    secondary = [i for i in IcebergTargetList if i[1] in myIcebergs and set(i[0].keys()).intersection(list(tupleFuncAttack[2].keys())) == set([]) and [j for j in allGroupsMain if j.owner != myself and j.destination == i[1]] != []]
    secondaryProtection = []
    if secondary != []:
        secondaryProtection = pickBestTarget(secondary, allIcebergs, allGroupsMain, myself, myIcebergs, enemyIcebergs,CAEDict)

    if len(myIcebergs) < 2 or sum([i.penguin_amount for i in myIcebergs]) + sum([i.penguin_amount for i in [j for j in allGroupsMain if j.owner == myself]]) < sum([i.penguin_amount for i in enemyIcebergs]) + sum([i.penguin_amount for i in [j for j in allGroupsMain if j.owner != myself]]) or enemyHeadedToIcepital != []:
        return (tupleFuncAttack,secondaryProtection)
    UpgradeTargetList = list(toPick)
    upgradeDictList = []
    listi = getListi(myIcebergsNew, allGroupsMain, myself, enemyIcebergs, maxCanSendDICT,CAEDict)
    
    for i in UpgradeTargetList:
        currentDict = getIcebergsDict(listi, i, myself, myIcebergs, enemyIcebergs, allGroupsMain, i.upgrade_cost, ourHalf, maxCanSendDICT,CAEDict, closestToCloneberg, accCost, accFactor)
        if currentDict != {}:
            upgradeDictList.append((currentDict,i))
    #print "time after MATE:",game1.get_time_remaining()
    tupleFuncUpgrade = pickBestTarget(upgradeDictList, allIcebergs, allGroupsMain, myself, myIcebergs, enemyIcebergs,CAEDict)
    #print "time after automateTask2:",game1.get_time_remaining()
    if tupleFuncAttack[0] == [] and tupleFuncUpgrade[0] == []:
        return ([],[],[])
    elif tupleFuncAttack[0] != [] and tupleFuncUpgrade[0] != []:
        finalList = [(tupleFuncUpgrade[2],tupleFuncUpgrade[0]), (tupleFuncAttack[2],tupleFuncAttack[0])]
        
        tupleFunc = pickBestTarget(finalList,allIcebergs, allGroupsMain, myself, myIcebergs, enemyIcebergs,CAEDict)
        return (tupleFunc,secondaryProtection)
    elif tupleFuncAttack[0] == []:
        return (tupleFuncUpgrade,secondaryProtection)
    else:
        return (tupleFuncAttack,secondaryProtection)
    
    
def maxCanSend(myIci, groupsHeaded, myIcebergs, enemyIcebergs,howMuch, maxCanSendDICT, CAEDict, accFactor):
    global siegeMult
    #print "time remaining before maxCanSend:",game1.get_time_remaining()
    if (myIci,howMuch) in maxCanSendDICT.keys():
        return maxCanSendDICT[(myIci,howMuch)]
    if (myIci,myIci.penguin_amount) in CAEDict.keys():
        CAEMINUS = CAEDict[(myIci,myIci.penguin_amount)]
    else:
        CAEMINUS = calcAtEndNewInitial(accFactor,myIci.penguin_amount,myIci, groupsHeaded, myIcebergs, enemyIcebergs, ["ME"])
        CAEDict[(myIci,myIci.penguin_amount)] = CAEMINUS
        #print 'CAEMINUS',myIci,CAEMINUS,howMuch
    if CAEMINUS[0] <= howMuch + 1:

        maxCanSendDICT[(myIci,howMuch)] = -1
        return -1
    
    if (myIci,0) in CAEDict.keys():
        CAE = CAEDict[(myIci,0)]
    else:
        #print 'calculating for:',myIci
        
        CAE = calcAtEndNewInitial(accFactor, 0,myIci, groupsHeaded, myIcebergs, enemyIcebergs, ["ME"])
        CAEDict[(myIci,0)] = CAE
        #print "maxCAnSEND1:",myIci,howMuch,CAE
    if CAEDict[(myIci,0)][0] > 0:
        maxCanSendDICT[(myIci,howMuch)] = myIci.penguin_amount
    else:
        #print "maxCAnSEND:",myIci,howMuch,CAE[0]
        maxCanSendDICT[(myIci,howMuch)] = CAE[0] + myIci.penguin_amount - howMuch - myIci.penguins_per_turn
    #print "time remaining after maxCanSend:",game1.get_time_remaining()
    
    return maxCanSendDICT[(myIci,howMuch)]
    
    
    
def getIcebergsDict(listi, target, myself, myIcebergs, enemyIcebergs, allPenguinGroups, howMuch, ourHalf, maxCanSendDICT, CAEDict, closestToCloneberg, accCost, accFactor):
    """
    param listi: gets list of all icebergs that belong to our team and send penguins this turn --> list[iceberg]
    param target: gets target iceberg to which we send penguins this turn --> iceberg
    param myself: gets game.get_myself --> player
    param myIcebergs: gets list of all our icebergs --> list[iceberg]
    param enemyIcebergs: gets list of all enemy icebergs --> list[iceberg]
    param allPenguinGroups: gets list of all penguin groups --> list[group]
    :returns dictionary with how many penguins to send from each iceberg --> dict
    """
    global gameEnder
    global siegeMult
    global siegeJustArrived
    if target not in myIcebergs and target not in enemyIcebergs and target.is_icepital == True:
        return {}
    #print "howMuch:",howMuch,target
    isMyIcepital = target.is_icepital and target in myIcebergs
    tieD = None
    owner = [getOwner(target ,myIcebergs,enemyIcebergs)]
    if (target,target.penguin_amount) in CAEDict.keys():
        CAE = CAEDict[(target,target.penguin_amount)]
    else:
        
        #print "CALCULATING FOR",target
        CAE = calcAtEndNewInitial(accFactor, target.penguin_amount,target,allPenguinGroups , myIcebergs, enemyIcebergs, owner)

        CAEDict[(target,target.penguin_amount)] = CAE
       
    

    if CAE[0] > howMuch or (CAE[0] > 0):
        #print 'returning nothing'
        return {}
    maxCanSendList = {}
    listiClone = list(listi)
    if closestToCloneberg != [] and (CAE[0] < 0 and target not in myIcebergs) and closestToCloneberg[0] in listi and [i for i in allPenguinGroups if i.owner == myself and i.destination == target] == []:
        listiClone.remove(closestToCloneberg[0])
        #print 'REMOVING', closestToCloneberg[0], target, listiClone, listi
    sortedByDist = sorted(listiClone, key = lambda x : x.get_turns_till_arrival(target))
    if target in sortedByDist:
        sortedByDist.remove(target)
    
    #print "sortedByDist:",sortedByDist
    sumi = 0
    countsIcebergs = 0
    countsubtractions = 0
    numOfPenguinsInEachIceberg = []
    amountOfPenguinsFromEachIceberg = {}
    RAE = 100000000
    #print "listi for",target,listi,'REAL ONE',sortedByDist
    for iceberg in sortedByDist:
        #print "running through:",iceberg
        turns_till_arrival = int(ceil(iceberg.get_turns_till_arrival(target) / accFactor) + 1)
        if [i for i in allPenguinGroups if i.destination == target and i.owner != myself] != [] and target not in myIcebergs and target not in enemyIcebergs and min([i for i in allPenguinGroups if i.destination == target and i.owner != myself], key = lambda x: x.turns_till_arrival).turns_till_arrival >= turns_till_arrival and [k for k in allPenguinGroups if k.destination == target and k.owner == myself] == []: continue
        if [i for i in allPenguinGroups if i.owner == myself and i.destination == iceberg] != [] and not(target in myIcebergs and CAE < 0):
            #print "for",target,'going herer',iceberg
            maxCanSendCurrent = maxCanSend(iceberg, [j for j in allPenguinGroups if j.destination == iceberg], myIcebergs, enemyIcebergs,iceberg.upgrade_cost, maxCanSendDICT,CAEDict, accFactor)
            #print "maxCanSendCurrent friend: ",maxCanSendCurrent
        else:
            maxCanSendCurrent = maxCanSend(iceberg, [j for j in allPenguinGroups if j.destination == iceberg], myIcebergs, enemyIcebergs,0, maxCanSendDICT,CAEDict, accFactor)
        #print "maxCanSendCurrent2 for:",iceberg,'is:',maxCanSendCurrent,CAEDict[(target,target.penguin_amount)],[i for i in allPenguinGroups if i.owner == myself and i.destination == iceberg],iceberg
        sumCurrentSieges = sum([i.penguin_amount for i in allPenguinGroups if i.owner != myself and seigeTurns(i.source.get_turns_till_arrival(i.destination),i.turns_till_arrival) == 0 and i.destination == iceberg and i.is_siege_group == True])
        
        
        if sumCurrentSieges != 0 and [i for i in allPenguinGroups if i.owner != myself and seigeTurns(i.source.get_turns_till_arrival(i.destination),i.turns_till_arrival) < 2 and i.destination == iceberg and i.is_siege_group][0] in siegeJustArrived:
            sumCurrentSieges = 0
        maxCanSendCurrent -= (sumCurrentSieges * siegeMult)
        #print 'sumCurrentSieges',sumCurrentSieges,maxCanSendCurrent,iceberg,target
        if maxCanSendCurrent > 0:
            #print "calling from",iceberg
            #print "calling RAE:",target,iceberg
            RAE = int(ceil(remainAtEnd(target, turns_till_arrival, allPenguinGroups, myself, myIcebergs, enemyIcebergs,howMuch,iceberg.unique_id, accFactor)[1] * accCost))
            if RAE == 0:
                #print "returninig 0 for",target
                return {}
            
            sumi += maxCanSendCurrent
            maxCanSendList[iceberg] = maxCanSendCurrent
            amountOfPenguinsFromEachIceberg[iceberg] = 0
            
        if sumi >= RAE:
            #print "for",target,'BREAKING FROM LOOP',sumi,RAE
            break
        
        if target.owner != myself and target.owner != enemyIcebergs[0].owner and [i for i in allPenguinGroups if i.owner != myself and i.destination == target] != []:
            sumi = 0
            maxCanSendList = {}
            amountOfPenguinsFromEachIceberg = {}
    
    if sumi >= RAE:
        #print "CHECK1:",sumi,RAE,amountOfPenguinsFromEachIceberg,target
        toBreak = False
        total = 0
        for i in amountOfPenguinsFromEachIceberg.keys():
            #print "maxCanSendList[i]",maxCanSendList[i],i
            while amountOfPenguinsFromEachIceberg[i] < maxCanSendList[i]:
                amountOfPenguinsFromEachIceberg[i] += 1
                total += 1
                if total >= RAE:
                    break
            if total >= RAE:
                break
    
    if sum(amountOfPenguinsFromEachIceberg.values())==0:
        amountOfPenguinsFromEachIceberg = {}
    for j in amountOfPenguinsFromEachIceberg.keys():
        sumCurrentSieges = sum([i.penguin_amount for i in allPenguinGroups if i.owner != myself and seigeTurns(i.source.get_turns_till_arrival(i.destination),i.turns_till_arrival) == 0 and i.destination == j and i.is_siege_group])
        if sumCurrentSieges != 0 and [i for i in allPenguinGroups if i.owner != myself and seigeTurns(i.source.get_turns_till_arrival(i.destination),i.turns_till_arrival) == 0 and i.destination == j and i.is_siege_group][0] in siegeJustArrived:
            sumCurrentSieges = 0
        amountOfPenguinsFromEachIceberg[j] += (sumCurrentSieges * siegeMult)
        
    return amountOfPenguinsFromEachIceberg
    
    
def getListi(myIcebergs, allPenguinsGroups, myself, enemyIcebergs, maxCanSendDICT,CAEDict):
    return [i for i in myIcebergs if i.already_acted == False]# check if statment (i.already_acted == False)

def needConquer(notOurIcebergs, allPenguinsGroups, myself, myIcebergsNew, enemyIcebergs, myIcebergs , ourHalf, maxCanSendDICT,CAEDict, closestToCloneberg, accCost, accFactor):
    targets = []
    #print "before listi:",myIcebergsNew
    listi = getListi(myIcebergsNew, allPenguinsGroups, myself, enemyIcebergs, maxCanSendDICT,CAEDict)
    #print "after listi:",listi
    for i in notOurIcebergs:
        #print "running on:",i
        targets.append((getIcebergsDict(listi, i, myself, myIcebergs, enemyIcebergs, allPenguinsGroups,0, ourHalf, maxCanSendDICT,CAEDict, closestToCloneberg, accCost, accFactor),i))
        #print "after:",game1.get_time_remaining()
    return targets
            
            
    
def getOwner(target,myIcebergs,enemyIcebergs):
    if target in myIcebergs:
        return "ME"
            
    elif target in enemyIcebergs:
        return "ENEMY"
            
    return "NEUTRAL"
    
def remainAtEnd(target,distance, allPenguinsGroups, myself,myIcebergs, enemyIcebergs,howMuch, unId, accFactor):
    """
    :param target: the target iceberg to make the calculations on -> SmartIceberg
    :param distance: the distance of the fake group from the target -> int
    :returns: the amount needed in order to conquer the target iceberg -> int
    """
    global siegeMult
    global theCloneberg
    penguinsGroupsHeaded = [i for i in allPenguinsGroups if i.destination == target]
    if theCloneberg != None:
        penguinsGroupsHeaded += [i for i in allPenguinsGroups if i.source == target and i.destination == theCloneberg]
    owner = getOwner(target,myIcebergs,enemyIcebergs)
    
    if penguinsGroupsHeaded == [] or [i for i in penguinsGroupsHeaded if i.is_siege_group == False] == []:
        sumCurrentSieges = 0
        
        if owner == "ME":
            if howMuch == 0 or (howMuch != 0 and target.penguin_amount + distance * target.penguins_per_turn >= howMuch):
                return 100000,0
            else:
                return 100000, howMuch - (target.penguin_amount + distance * target.penguins_per_turn) 
        elif owner == "ENEMY":
            if target.id == 3:
                print target.penguin_amount,distance,target.level,howMuch
            return target.penguin_amount + (distance + 1) * target.level ,target.penguin_amount + (distance + 1) * target.level
        return target.penguin_amount + 1 ,target.penguin_amount + 1
    fakeGroup = PenguinGroup()
    fakeGroup.owner = myself
    fakeGroup.id = -2
    fakeGroup.destination = target
    fakeGroup.penguin_amount = 0
    fakeGroup.turns_till_arrival = distance
    fakeGroup.unique_id = -5
    fakeGroup.type = "PenguinGroup"
    fakeGroup.is_siege_group = False
    fakeGroup.source = [i for i in myIcebergs + enemyIcebergs if i.unique_id == unId][0]
    penguinsPerTurn = target.penguins_per_turn
    if [i for i in penguinsGroupsHeaded if i.turns_till_arrival == fakeGroup.turns_till_arrival] != []:
        return 100000,0
    penguinsGroupsHeaded.append(fakeGroup)
    
    
    groupsUntilX = [i for i in penguinsGroupsHeaded if i.turns_till_arrival <= fakeGroup.turns_till_arrival + 1]

    groupsFromX = [i for i in penguinsGroupsHeaded if i.turns_till_arrival > fakeGroup.turns_till_arrival + 1]

    currentOwner = [owner]
    CAEUntilX = calcAtEndNewInitial(accFactor, target.penguin_amount, target, groupsUntilX, myIcebergs, enemyIcebergs, currentOwner)
    #print "CAEUntilX:",CAEUntilX,target
    if groupsFromX == [] or (len(groupsFromX) == 1 and groupsFromX[0].penguin_amount == 1):
        CAEAtEnd = CAEUntilX[0]
        
    else:
        #print "GOING HERE",groupsFromX
        newPPT = 0
        original = [i.turns_till_arrival for i in groupsFromX]
        #print "newOwner:",currentOwner,CAEUntilX
        for i in groupsFromX:
            i.turns_till_arrival -= distance
        #print [(i.id, i.penguin_amount, i.turns_till_arrival) for i in groupsFromX],currentOwner
        CAEAtEnd = calcAtEndNewInitial(accFactor, abs(CAEUntilX[0]), target, groupsFromX, myIcebergs, enemyIcebergs, currentOwner, sim = True, siegeOnIcebergP = CAEUntilX[3], siegeHeaededP = CAEUntilX[2], turnsUntillArrivedSiegeP = CAEUntilX[5], turnsRemainingForSeigeP = CAEUntilX[4])[0]
        for i in groupsFromX:
            i.turns_till_arrival += distance
        #print "CAEAtEnd REAL:",CAEAtEnd   
    penguinsGroupsHeaded.remove(fakeGroup)
    fakeGroup = PenguinGroup()
    #print "target",target,"CAEAtEnd:",CAEUntilX,distance,allPenguinsGroups,howMuch
    if CAEAtEnd >= howMuch:
        return 100000, 0

    
    return howMuch - CAEAtEnd + 1, howMuch - CAEAtEnd + 1
    
def calcAtEndNewInitial(accFactor, newInit,target, groupsHeaded1, myIcebergs, enemyIcebergs, owner, sim = False, forUpgrade = False, siegeOnIcebergP = None, siegeHeaededP = None, turnsUntillArrivedSiegeP = None, turnsRemainingForSeigeP = None):
    
    global siegeMult
    global siegesMaxTurns
    global clonebergMult
    global theCloneberg
    global clonebergMaxTurns
    groupsHeaded = [i for i in groupsHeaded1 if i.destination == target]
    if theCloneberg != None and groupsHeaded1 != []:

        groupsHeaded = groupsHeaded + [i for i in groupsHeaded1 if i.source == target and i.destination == theCloneberg]
    groupsHeaded = sorted(groupsHeaded, key = lambda x: x.turns_till_arrival)

    
    if groupsHeaded == [] or [i for i in groupsHeaded if i.is_siege_group == False] == []:
        #print "going here for",target
        siegesGroup = [i for i in groupsHeaded if i.is_siege_group == True and i.destination == target and i.turns_till_arrival == 0]
        sieges = 0 if siegesGroup == [] else sum([i.penguin_amount for i in siegesGroup])
        if owner[0] == "ME":
            return (newInit + target.penguins_per_turn, sieges)
        elif owner[0] == "ENEMY":
            return (newInit * -1 - target.penguins_per_turn, sieges)
        return (newInit * -1, sieges)
    initial, penguinsPerTurn = newInit, target.penguins_per_turn
    totalSieges = [i for i in groupsHeaded if i.destination == target and i.is_siege_group == True]
    siegeHeaeded = siegeHeaededP if siegeHeaededP != None else (None if [i for i in totalSieges if i.turns_till_arrival > 0] == [] else [i for i in totalSieges if i.turns_till_arrival > 0][0])
    siegeOnIceberg = siegeOnIcebergP if siegeOnIcebergP != None else (None if [i for i in totalSieges if i.turns_till_arrival == 0] == [] else [i for i in totalSieges if i.turns_till_arrival == 0][0])
    currentSiegeOnIceberg = 0 if siegeOnIceberg == None else siegeOnIceberg.penguin_amount
    turnsUntillArrivedSiege = turnsUntillArrivedSiegeP if turnsUntillArrivedSiegeP != None else (None if siegeHeaeded == None else seigeTurns(siegeHeaeded.source.get_turns_till_arrival(siegeHeaeded.destination), siegeHeaeded.turns_till_arrival))
    turnsRemainingForSeige = turnsRemainingForSeigeP if turnsRemainingForSeigeP != None else (None if currentSiegeOnIceberg == 0 else siegesMaxTurns - 1 - target.siege_turns)
    

    groupsHeaded = [i for i in groupsHeaded if i.is_siege_group == False]

    if forUpgrade == True and target.level < target.upgrade_level_limit and target in myIcebergs:
        penguinsPerTurn += 1
    if owner[0] == "NEUTRAL":
        penguinsPerTurn = 0
        initial *= -1
    if owner[0] == "ENEMY":
        penguinsPerTurn *= -1
        initial *= -1
    if sim == True:
        penguinsPerTurn = abs(target.penguins_per_turn)

    lastTurns = 0
    tempHeaded = list(groupsHeaded)

    if sim == False:
        initial += penguinsPerTurn
    originalAmount = [i.penguin_amount for i in groupsHeaded]
    for i in tempHeaded:
        if i.owner != myIcebergs[0].owner:
            tempHeaded[tempHeaded.index(i)].penguin_amount *= -1
    
    originalTTA = [i.turns_till_arrival for i in groupsHeaded]
    
    for i in tempHeaded:
        if i.turns_till_arrival > 0 and i.unique_id != -5:
            i.turns_till_arrival = i.turns_till_arrival - 1
    if theCloneberg != None:
        for i in range(len(tempHeaded)):
            if tempHeaded[i].destination == theCloneberg and tempHeaded[i].turns_till_arrival != 0:
                #print tempHeaded[i],"is on its way to the cloneberg"
                tempHeaded[i].turns_till_arrival = tempHeaded[i].turns_till_arrival + clonebergMaxTurns + turnsWithAcc(theCloneberg.get_turns_till_arrival(tempHeaded[i].source) - 1,tempHeaded[i].current_speed,accFactor)
                
            elif tempHeaded[i].destination == theCloneberg and tempHeaded[i].turns_till_arrival == 0:
                #print tempHeaded[i],"is on the cloneberg",tempHeaded[i].cloneberg_pause_turns,theCloneberg.get_turns_till_arrival(tempHeaded[i].source),tempHeaded[i].cloneberg_pause_turns
                tempHeaded[i].turns_till_arrival = tempHeaded[i].cloneberg_pause_turns + turnsWithAcc(theCloneberg.get_turns_till_arrival(tempHeaded[i].source) - 1,tempHeaded[i].current_speed,accFactor)
                #print "NEW IS:",tempHeaded[i].turns_till_arrival
        
        tempHeaded.sort(key = lambda x: x.turns_till_arrival)

    
    if theCloneberg != None:
        for i in tempHeaded:
            if i.destination == theCloneberg:
                i.penguin_amount *= clonebergMult
   
        
    
    #print "original:",listTurns,groupsHeaded
    firstElement = groupsHeaded[0]
    tieBreaker = None


    while len(tempHeaded) > 0:

        x = tempHeaded[0].turns_till_arrival
        if tempHeaded[0] == firstElement:
            initial += (x) * penguinsPerTurn
            d = x
        else:
            initial += penguinsPerTurn * (x - lastTurns)
            d = x - lastTurns

        lastTurns = x
        arrivedSameTime = [i for i in tempHeaded if i.turns_till_arrival == lastTurns]
        currentAmount = tempHeaded[0].penguin_amount
        current = tempHeaded[0]

        if len(arrivedSameTime) > 1 and owner[0] != "NEUTRAL":
            
            totalRemains = reduce(lambda x,y : x + y, [i.penguin_amount for i in arrivedSameTime])
            currentAmount = totalRemains
            tempHeaded = [i for i in tempHeaded if i not in arrivedSameTime]
            
                
            tempHeaded = [current] + tempHeaded
            listTurns = [i.turns_till_arrival for i in tempHeaded if i.turns_till_arrival != lastTurns]

            listTurns = [lastTurns] + listTurns
            
        if siegeOnIceberg != None:    
            turnsRemainingForSeige -= d
            
        if currentSiegeOnIceberg != 0 and turnsRemainingForSeige < 1:
            currentSiegeOnIceberg = 0
            siegeOnIceberg = None
            turnsRemainingForSeige = None

        #if siege is now of the controled group, check that these ifs dont make any problems
        if turnsUntillArrivedSiege != None:
            turnsUntillArrivedSiege -= d
            
        if turnsUntillArrivedSiege != None and turnsUntillArrivedSiege < 1:
            currentSiegeOnIceberg = siegeHeaeded.penguin_amount
            turnsRemainingForSeige = siegesMaxTurns - 1
            turnsUntillArrivedSiege = None
            siegeOnIceberg = siegeHeaeded
        
        if siegeOnIceberg != None and ((owner[0] == "ME" and siegeOnIceberg.owner == myIcebergs[0].owner) or (owner[0] == "ENEMY" and siegeOnIceberg.owner == enemyIcebergs[0].owner)):
            siegeOnIceberg = None
            currentSiegeOnIceberg = 0

        if siegeOnIceberg != None and siegeOnIceberg.owner == enemyIcebergs[0].owner:
            currentSiegeOnIceberg *= -1
        if owner[0] != "NEUTRAL":
            if siegeOnIceberg == None or (currentAmount < 0 and siegeOnIceberg.owner == enemyIcebergs[0].owner) or (currentAmount >= 0 and siegeOnIceberg.owner == myIcebergs[0].owner):
                initial += currentAmount

            else:
                afterSub = currentSiegeOnIceberg
                if currentAmount < 0:
                    toAdd = int(ceil(currentAmount / siegeMult))
                else:
                    toAdd = int(floor(currentAmount / siegeMult))
                afterSub += toAdd
                # if target.id == 1:
                #     print "adding:",currentAmount,siegeMult,toAdd
                if (currentSiegeOnIceberg < 0 and afterSub >= 0) or (currentSiegeOnIceberg > 0 and afterSub <= 0):
                    initial += (currentAmount + currentSiegeOnIceberg * siegeMult)
                    currentSiegeOnIceberg = 0
                    #print "DOING THAT FOR",afterSub,toAdd,currentSiegeOnIceberg,siegeMult
                    siegeOnIceberg = None
                    
                else:
                    currentSiegeOnIceberg = afterSub
                    
        else:
            if len(arrivedSameTime) == 1 or (len(arrivedSameTime) > 1 and ([i for i in arrivedSameTime if i.owner == myIcebergs[0].owner] == arrivedSameTime or [i for i in arrivedSameTime if i.owner == enemyIcebergs[0].owner] == arrivedSameTime)):
                currentAmount = sum([i.penguin_amount for i in arrivedSameTime])
                if sim == True:
                    #print "sim:",sim
                    initial += currentAmount
                else:
                    
                    initial += abs(currentAmount)

                tempHeaded = [i for i in tempHeaded if i not in arrivedSameTime]
            
                tempHeaded = [current] + tempHeaded

            else:
                enemyArrivingToNeutral = sum([i.penguin_amount for i in arrivedSameTime if i.owner == enemyIcebergs[0].owner])
                myArrivingToNeutral = sum([i.penguin_amount for i in arrivedSameTime if i.owner == myIcebergs[0].owner])
                winningEnemy = initial / 2 - enemyArrivingToNeutral
                winningMe = initial / 2 + myArrivingToNeutral
                if winningMe >= 0 and winningEnemy >= 0:
                    initial = winningMe - winningEnemy
                    if initial < 0:
                        currentAmount = -1
                    elif initial > 0:
                        currentAmount = 1
                elif winningMe >= 0 and winningEnemy <= 0:
                    initial = winningMe + winningEnemy
                    if initial > 0:
                        currentAmount = 1
                elif winningEnemy >= 0 and winningMe <= 0:
                    initial = winningEnemy + winningMe
                    if initial > 0:
                        currentAmount = -1

                tempHeaded = [current] + [i for i in tempHeaded if i not in arrivedSameTime]
                initial = int(floor(initial))
                
                # special case for neutral (two groups at the same time)
        
        if sim == False or (sim == True and owner[0] == "NEUTRAL"):
            if initial < 0 and owner[0] == "ME":
                owner[0] = "ENEMY"
                penguinsPerTurn *= -1
            elif initial > 0 and owner[0] == "ENEMY":
                penguinsPerTurn *= -1
                owner[0] = "ME"
            elif owner[0] == "NEUTRAL":
                if initial > 0:
                    if currentAmount >= 0:
                        owner[0] = "ME"
                        penguinsPerTurn = target.penguins_per_turn

                    else:
                        owner[0] = "ENEMY"
                        penguinsPerTurn = target.penguins_per_turn * -1
                        initial *= -1
        #print "popping",tempHeaded[0],initial
        tempHeaded.pop(0)
        #print "after popping",tempHeaded
        
    for i in range(len(groupsHeaded)):
        groupsHeaded[i].penguin_amount = originalAmount[i]
        groupsHeaded[i].turns_till_arrival = originalTTA[i]
        
    return (initial, abs(currentSiegeOnIceberg), siegeHeaeded, siegeOnIceberg, turnsRemainingForSeige, turnsUntillArrivedSiege)
    
    
def accelerateGroup(group, groupsHeaded ,myIcebergs, enemyIcebergs,factor,cost, CAEDict, codeRed = False):#groupsHeaded -> sorted by turns_till_arrival,groupsHeaded must include group
    if group.penguin_amount == 1 or group.is_siege_group == True:
        return
    if group.destination.owner != myIcebergs[0].owner and group.destination.owner != enemyIcebergs[0].owner and min(groupsHeaded, key = lambda x: x.turns_till_arrival) == group and len(groupsHeaded) > 1:
        return
    
    #print "going ",group
    enemyGroupsHeaded = sorted([i for i in groupsHeaded if i.owner == enemyIcebergs[0].owner], key = lambda x: x.turns_till_arrival)
    penguinAmount = group.penguin_amount
    d = group.turns_till_arrival
    newD = int(ceil(d / factor))
    sub = penguinAmount - int(floor(penguinAmount / cost))
    l = group.destination.penguins_per_turn

    owner = [getOwner(group.destination ,myIcebergs,enemyIcebergs)]
    currentCAE = calcAtEndNewInitial(factor, group.destination.penguin_amount,group.destination, groupsHeaded, myIcebergs, enemyIcebergs, owner )

    if newD == 0:
        group.destination.penguin_amount += sub * -1 + penguinAmount
        groupsHeaded.remove(group)
    else:
        group.turns_till_arrival = newD
        group.penguin_amount = sub * -1 + penguinAmount
        groupsHeaded = sorted(groupsHeaded, key = lambda x : x.turns_till_arrival)
    owner = [getOwner(group.destination ,myIcebergs,enemyIcebergs)]
    
    CAE = calcAtEndNewInitial(factor, group.destination.penguin_amount,group.destination, groupsHeaded, myIcebergs, enemyIcebergs, owner)
    #print "CAES",CAE[0],currentCAE[0],group
    if (CAE[0] > currentCAE[0] and group.destination not in [i for i in myIcebergs if i.is_icepital == True]) or ((((group.destination in [i for i in myIcebergs if i.is_icepital == True] and len([m for m in groupsHeaded if m.owner != group.owner and m.is_siege_group == False]) != 0)) or group.destination in [i for i in enemyIcebergs if i.is_icepital == True]) and CAE[0] > 0):
        group.accelerate()
        #print "accelerate2",group
    if group.already_acted == False and CAE[0] > 0 and len(groupsHeaded) == 1 and group.destination.owner != group.owner and group.turns_till_arrival > 1:
        #print "accelerate1",group
        group.accelerate()
    if newD == 0:
        group.destination.penguin_amount -= sub * -1 + penguinAmount
    group.turns_till_arrival = d
    group.penguin_amount = penguinAmount

def pickBestTarget(iterList, allIcebergs, allPenguinsGroups, myself, myIcebergs, enemyIcebergs, CAEDict):
    best_dict = {}
    if iterList == []:
        return ([],[],[])
    bestTarget = None
    if len(iterList) == 1:
        RAEBest = sum(iterList[0][0].values())
        bestTarget = iterList[0][1]
        best_dict = iterList[0][0]
    if iterList == []:
        RAEBest = -1
        bestTarget = None
    for i in range(1,len(iterList)):
        t = 1
        if i == 1:
            dBest = min(list(iterList[0][0].keys()),key = lambda x: x.get_turns_till_arrival(iterList[0][1])).get_turns_till_arrival(iterList[0][1])
            if len(iterList[0]) == 3:
                dBest = iterList[0][2]
            lBest = iterList[0][1].penguins_per_turn
            RAEBest = sum(iterList[0][0].values())
            UCBest = iterList[0][1].upgrade_cost
            CFBest = iterList[0][1].cost_factor
            bestTarget = iterList[0][1]
            best_dict = iterList[0][0]
            
            if (iterList[0][1] in myIcebergs and CAEDict[(iterList[0][1],iterList[0][1].penguin_amount)] < 0) or iterList[0][1] in enemyIcebergs or (iterList[0][1] not in myIcebergs and iterList[0][1] not in enemyIcebergs and [k for k in allPenguinsGroups if k.destination == iterList[0][1] and k.owner != myself] != []):
                t = 2
        d = min(list(iterList[i][0].keys()),key = lambda x: x.get_turns_till_arrival(iterList[i][1])).get_turns_till_arrival(iterList[i][1])
        if len(iterList[i]) == 3:
                dBest = iterList[i][2]
        l = iterList[i][1].penguins_per_turn
        RAE = sum(iterList[i][0].values())
        UC = iterList[i][1].upgrade_cost
        CF = iterList[i][1].cost_factor
        if iterList[i][1].owner != myself and enemyIcebergs != []:
            if iterList[i][1].owner != enemyIcebergs[0].owner and len([k for k in allPenguinsGroups if k.destination == iterList[i][1]]) == 1:
                list1 = [k for k in allPenguinsGroups if k.destination == iterList[i]]
                if len(list1) > 1 and list1[1].turns_till_arrival == attacker.get_turns_till_arrival(iterList[i][1]):
                    break
        if l == lBest:
            CF = UC
            CFBest = UCBest
        if (bestTarget in myIcebergs and CAEDict[(iterList[i][1],iterList[i][1].penguin_amount)] < 0) or bestTarget in enemyIcebergs or (iterList[i][1] not in myIcebergs and iterList[i][1] not in enemyIcebergs and [k for k in allPenguinsGroups if k.destination == iterList[i][1] and k.owner != myself] != []):
            t = 2
        if dBest >= d and lBest >= l:
            if RAE - (dBest - d) * l * t + (UC + CF * (lBest - l - 1)) < RAEBest:
                RAEBest = RAE
                dBest = d
                lBest = l
                UCBest = UC
                CFBest = CF
                bestTarget = iterList[i][1]
                best_dict = iterList[i][0]
        
        elif dBest > d and lBest <= l:
            if RAE - (dBest - d) * l * t - (UCBest + CF * (l - lBest - 1)) < RAEBest:
                RAEBest = RAE
                dBest = d
                lBest = l
                UCBest = UC
                CFBest = CF
                bestTarget = iterList[i][1]
                best_dict = iterList[i][0]
        
        elif dBest <= d and lBest >= l:
            if RAE + (d - dBest) * lBest * t + (UC + CF * (lBest - l - 1)) < RAEBest:
                RAEBest = RAE
                dBest = d
                lBest = l
                UCBest = UC
                CFBest = CF
                bestTarget = iterList[i][1]
                best_dict = iterList[i][0]
            
        elif dBest < d and lBest <= l:
            if RAE + (d - dBest) * lBest * t - (UCBest + CF * (l - lBest - 1)) < RAEBest:
                RAEBest = RAE
                dBest = d
                lBest = l
                UCBest = UC
                CFBest = CF
                bestTarget = iterList[i][1]
                best_dict = iterList[i][0]
    
        else:
            if dBest == d:
                sortedAllies = sorted(myIcebergs,key = lambda x: x.get_turns_till_arrival(iterList[i][1]))
                if iterList[i] in sortedAllies:
                    sortedAllies.remove(iterList[i][1])
                enemiesAllies = sorted(enemyIcebergs,key = lambda x: x.get_turns_till_arrival(iterList[i][1]))
                if iterList[i] in enemiesAllies:
                    enemiesAllies.remove(iterList[i][1])

                if (sortedAllies[0].get_turns_till_arrival(iterList[i][1]) < enemiesAllies[0].get_turns_till_arrival(iterList[i][1])) and (RAE - (dBest - d) * l <= RAEBest):
                    RAEBest = RAE
                    dBest = d
                    lBest = l
                    UCBest = UC
                    CFBest = CF
                    bestTarget = iterList[i][1]
                    best_dict = iterList[i][0]
                
            
    return bestTarget, RAEBest,best_dict
        
def sendWithAccelarate(myIcebergs,enemyIcebergs,target,sender, distance, myself,allPenguinsGroups, accelerationCost,accelerationFactor):
    global siegeJustArrived
    global siegeConstArrived
    m = 1
    for l in [accelerationFactor,accelerationFactor ** 2]:
        distance = int(ceil((distance - 1) / accelerationFactor)) + m

        
        RAE = remainAtEnd(target,distance, allPenguinsGroups, myself, myIcebergs, enemyIcebergs, 1, sender.unique_id, accelerationFactor)
        
        siegeOnIceberg = sum([i.penguin_amount for i in allPenguinsGroups if i.owner != myself and seigeTurns(i.source.get_turns_till_arrival(i.destination),i.turns_till_arrival) < 1 and i.destination == sender and i.is_siege_group == True and i not in siegeJustArrived and i in siegeConstArrived])
        #print "HELLO FRIEND",target,sender,int(ceil(RAE[0] * (1.3 ** m))),RAE[0],distance
        if not(target not in myIcebergs and target not in enemyIcebergs and [i for i in allPenguinsGroups if i.destination == target and i.owner != myself] != [] and min([i for i in allPenguinsGroups if i.destination == target and i.owner != myself], key = lambda x: x.turns_till_arrival).turns_till_arrival >= distance) and RAE[0] != 100000 and int(ceil(RAE[0] * (accelerationCost ** m))) + siegeOnIceberg * 3 < sender.penguin_amount and sum([i.penguin_amount for i in allPenguinsGroups if i.owner != myself and i.is_siege_group == False and i.destination == sender]) - sum([i.penguin_amount for i in allPenguinsGroups if i.owner == myself and i.is_siege_group == False and i.destination == sender]) < sender.penguin_amount - int(ceil(RAE[0] * (accelerationCost ** m))):
            #print "INDEED MY FRIEND"#and RAE <= maxCanSend(myIci, groupsHeaded, myIcebergs, enemyIcebergs,howMuch, maxCanSendDICT, CAEDict)
            return (l ,distance ,int(ceil(RAE[0] * (accelerationCost ** m))) + siegeOnIceberg * 3)
        m += 1

def rocketAttack(myIcebergs,enemyIcebergs,targets,myself,allPenguinsGroups, sendersToCloneberg,accelerationCost,accelerationFactor):
    rocketFinal = None
    f = False
    #print "targets for rocket: ",targets
    for i in targets:
        for j in myIcebergs:
            if f:
                break
            if j != i:
                if (i in myIcebergs and [m for m in allPenguinsGroups if m.destination == i and m.is_siege_group == False] == []) or ([m for m in allPenguinsGroups if m.destination == i and m.is_siege_group == False and m.owner != myself] != [] and (i in myIcebergs or i in enemyIcebergs)) or (j in sendersToCloneberg and i not in myIcebergs and i not in enemyIcebergs and j.level > 1) or (j.penguin_amount < i.penguin_amount + 2):
                    #print "continueing",i,j
                    continue
                distance = j.get_turns_till_arrival(i)
                t = sendWithAccelarate(myIcebergs,enemyIcebergs,i,j, distance, myself, allPenguinsGroups, accelerationCost,accelerationFactor )
                if t != None:
                    accelerate = t[0]
                    distance = t[1]
                    RAE = t[2]
                    rocketFinal = ({j : RAE}, i, distance, t[0],j.get_turns_till_arrival(i))
                    f = True
                    
        if f:
            break
    #print "RETURNING",rocketFinal
    return rocketFinal
    

def seigeTurns(d,currentD):
    if currentD == 1: return 0
    return int(floor(currentD / floor(d / 5)))
    
def turnsWithAcc(d, acc, accFactor):
    if acc == 1: return d
    for i in range(int(math.log(acc,accFactor))):
        d = int(ceil((d - 1) / accFactor))
    #print "for the turnsWithAcc RETURNING",d + int(math.log(acc,2))
    return d + int(math.log(acc,accFactor))
