from distutils.log import debug
from flask import Flask, render_template, session, request, \
    copy_current_request_context
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect
from game.player import Player
from game.play_field import Field
import random

app = Flask(__name__)
socketio = SocketIO(app,async_mode = 'threading')
player1 = Player('player1')
player2 = Player('player2')
field = Field()
player1_sit = False
player2_sit = False

@app.route('/')
def index():
    field_name = []
    archivement1 = []
    hand1 = []
    target1 = []
    archivement2 = []
    hand2 = []
    target2 = []
    for i in field.archivement:
        field_name.append(i.name)
    for i in player1.archivement:
        archivement1.append(i.name)
    for i in player1.hand:
        hand1.append(i.name)
    for i in player2.archivement:
        archivement2.append(i.name)
    for i in player2.hand:
        hand2.append(i.name)
    for i in field.archivement:
        if i.target == 'player1':
            target1.append(i.name)
        elif i.target == 'player2':
            target2.append(i.name)
    info = {'field':field_name,
            'player1_sit':player1_sit,
            'player1_deck':len(player1.deck),
            'player1_archivement':archivement1,
            'player1_hand':hand1,
            'player1_resource':player1.resource,
            'player1_target':target1,
            'player2_sit':player2_sit,
            'player2_deck':len(player2.deck),
            'player2_archivement':archivement2,
            'player2_hand':hand2,
            'player2_resource':player2.resource,
            'player2_target':target2}
    return render_template('index.html',info = info)

@socketio.event
def game_start():
    emit('chat','ゲーム開始',broadcast = True)
    for i in range(5):
        player1.draw()
        player2.draw()
    target = random.sample(field.archivement,10)
    target[0].target = 'player1'
    target[1].target = 'player1'
    target[2].target = 'player1'
    target[3].target = 'player1'
    target[4].target = 'player1'
    target[5].target = 'player2'
    target[6].target = 'player2'
    target[7].target = 'player2'
    target[8].target = 'player2'
    target[9].target = 'player2'
    update()
    turn_player = 'player1' if random.randint(0,1) == 0 else 'player2'
    emit('turn_change',turn_player,broadcast =True)
    turn_start(turn_player)

def turn_start(player):
    emit('chat',player+':ターン開始',broadcast = True)
    player1.start_turn() if player == 'player1' else player2.start_turn()
    emit('chat',player+':イベントの使用',broadcast = True)
    update()
    emit('mode_change','event',broadcast = True)    

@socketio.event
def event(player):
    field.event[0].play(player1) if player == 'player1' else field.event[0].play(player2)
    emit('chat',field.event[0].name + '発動',broadcast = True)
    update()
    use(player)

@socketio.event
def use(player):
    emit('chat',player+':リソースの使用',broadcast = True)
    emit('chat',player+':目標の獲得',broadcast = True)
    player1.play_resource() if player == 'player1' else player2.play_resource()
    update()
    goal_buy(player)
    emit('mode_change','buy',broadcast = True)  

@socketio.event
def goal_buy(player):
    player = player1 if player == 'player1' else player2
    for goal in player.archivement:
        if(goal.phase == 'buy'):
            emit('exchange',goal.name)

@socketio.event
def exchange(player,name,resource):
    player = player1 if player == 'player1' else player2
    for goal in player.archivement:
        if(goal.name == name):
            goal.play(player,resource)
    update()

@socketio.event
def buy(player,num):
    num = int(num)
    player = player1 if player == 'player1' else player2
    goal = field.archivement[num]
    if goal.target == 'player1':
        cost = 5
    elif goal.target == 'player2':
        cost = 6
    else:
        cost = 4

    if player.resource[goal.cost] >= cost:
        player.buy(field,num,cost)
        update()
    else:
        emit('chat','コストが足りません')

@socketio.event
def add(player):
    emit('chat',player+':リソースの追加',broadcast = True)
    emit('mode_change','add',broadcast = True)

@socketio.event
def end(player,resource):
    emit('chat',player+':ターン終了',broadcast = True)
    player1.end_turn(resource) if player == 'player1' else player2.end_turn(resource)
    turn_player = 'player2' if player == 'player1' else 'player1'
    update()
    target_num = 0
    for goal in field.archivement:
        if goal.target == 'player1':
            target_num += 1
        elif goal.target == 'player2':
            target_num += 1
    if target_num > 0:
        emit('turn_change',turn_player,broadcast =True)
        turn_start(turn_player)
    else :
        game_end()

def game_end():
    player1_score = len(player1.archivement)
    player2_score = len(player2.archivement)
    if player1_score > player2_score:
        emit('chat','player1WIN')
    elif player2_score > player1_score:
        emit('chat','player2WIN')
    else:
        emit('chat','DRAW')

@socketio.event
def sitdown(player):
    if player == 'player1':
        global player1_sit
        player1_sit = True
    if player == 'player2':
        global player2_sit
        player2_sit = True
    update()
    
def update():
    field_name = []
    archivement1 = []
    hand1 = []
    target1 = []
    archivement2 = []
    hand2 = []
    target2 = []
    for i in field.archivement:
        field_name.append(i.name)
    for i in player1.archivement:
        archivement1.append(i.name)
    for i in player1.hand:
        hand1.append(i.name)
    for i in player2.archivement:
        archivement2.append(i.name)
    for i in player2.hand:
        hand2.append(i.name)
    for i in field.archivement:
        if i.target == 'player1':
            target1.append(i.name)
        elif i.target == 'player2':
            target2.append(i.name)
    info = {'field':field_name,
            'player1_sit':player1_sit,
            'player1_deck':len(player1.deck),
            'player1_archivement':archivement1,
            'player1_hand':hand1,
            'player1_resource':player1.resource,
            'player1_target':target1,
            'player2_sit':player2_sit,
            'player2_deck':len(player2.deck),
            'player2_archivement':archivement2,
            'player2_hand':hand2,
            'player2_resource':player2.resource,
            'player2_target':target2}
    emit('update',info,broadcast = True)    

if __name__ == '__main__':
    socketio.run(app, debug = True)