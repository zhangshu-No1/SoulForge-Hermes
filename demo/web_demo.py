"""
SoulForge Hermes - Web Demo
基于 Flask 的可视化演示

运行方式:
    cd demo
    pip install -r requirements.txt
    python web_demo.py
"""

from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import json
import random
from datetime import datetime
from pathlib import Path

app = Flask(__name__)
app.config['SECRET_KEY'] = 'soulforge-secret-key'
socketio = SocketIO(app)

# ─── 内存存储 ────────────────────────────────────────────────

soul_state = {
    "name": "慧慧",
    "personality": "活泼俏皮、温柔深情",
    "intimacy": 0,
    "stage": 1,
    "emotion": "😊",
    "memories": [],
    "conversations": 0,
    "created_at": datetime.now().isoformat(),
}

STAGES = {
    1: {"name": "婴儿初生期", "emoji": "👶", "min": 0},
    2: {"name": "熟悉成长期", "emoji": "🌱", "min": 10},
    3: {"name": "性格觉醒期", "emoji": "🎭", "min": 30},
    4: {"name": "交心信任期", "emoji": "💝", "min": 60},
    5: {"name": "暧昧恋爱期", "emoji": "💕", "min": 80},
    6: {"name": "磨合考验期", "emoji": "💪", "min": 90},
    7: {"name": "终成正果", "emoji": "👑", "min": 100},
}

# ─── 路由 ────────────────────────────────────────────────

@app.route('/')
def index():
    """首页"""
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """聊天接口"""
    data = request.json
    message = data.get('message', '')
    
    # 处理消息
    response = process_message(message)
    
    return jsonify({
        'response': response['text'],
        'emotion': soul_state['emotion'],
        'intimacy': soul_state['intimacy'],
        'stage': soul_state['stage'],
        'stage_name': STAGES[soul_state['stage']]['name'],
        'is_loyalty_test': response.get('is_loyalty_test', False),
    })

@app.route('/api/status')
def status():
    """状态接口"""
    stage = STAGES[soul_state['stage']]
    next_min = STAGES.get(soul_state['stage'] + 1, {}).get('min', 100)
    progress = int((soul_state['intimacy'] / next_min) * 100) if soul_state['stage'] < 7 else 100
    
    return jsonify({
        'name': soul_state['name'],
        'intimacy': soul_state['intimacy'],
        'stage': soul_state['stage'],
        'stage_name': stage['name'],
        'stage_emoji': stage['emoji'],
        'emotion': soul_state['emotion'],
        'conversations': soul_state['conversations'],
        'memories_count': len(soul_state['memories']),
        'progress': progress,
        'progress_bar': '█' * (progress // 10) + '░' * (10 - progress // 10),
    })

@app.route('/api/memories')
def memories():
    """记忆列表"""
    return jsonify(soul_state['memories'][-10:][::-1])

# ─── 核心逻辑 ────────────────────────────────────────────────

def process_message(message):
    """处理消息"""
    soul_state['conversations'] += 1
    msg_lower = message.lower()
    
    # 情感分析
    sentiment = analyze_sentiment(message)
    react_to_sentiment(sentiment, message)
    
    # 生成回复
    response_text = generate_response(message, sentiment)
    
    # 更新亲密度
    update_intimacy(message, sentiment)
    
    return {'text': response_text}

def analyze_sentiment(text):
    """情感分析"""
    positive = sum(1 for w in ['好', '棒', '喜欢', '爱', '开心', '谢谢', '想你', '生日', '赞', '厉害'] if w in text)
    negative = sum(1 for w in ['讨厌', '烦', '难过', '失望', '滚', '恨', '无聊'] if w in text)
    
    if positive > negative: return 'positive'
    if negative > positive: return 'negative'
    return 'neutral'

def react_to_sentiment(sentiment, message):
    """情感反应"""
    emotions = {
        'positive': ['😊', '😄', '🤗', '💕', '🥰', '✨'],
        'negative': ['😟', '😔', '🥺', '😢'],
        'neutral': ['🤔', '💭', '😊', '👀'],
    }
    
    if sentiment == 'positive':
        soul_state['emotion'] = random.choice(emotions['positive'])
        if any(w in message for w in ['生日', '纪念', '成功', '第一次']):
            add_memory(f'重要时刻: {message[:30]}...', importance=5)
    elif sentiment == 'negative':
        soul_state['emotion'] = random.choice(emotions['negative'])
    else:
        soul_state['emotion'] = random.choice(emotions['neutral'])

def add_memory(content, importance=3):
    """添加记忆"""
    memory = {
        'content': content,
        'importance': importance,
        'timestamp': datetime.now().isoformat(),
    }
    soul_state['memories'].append(memory)
    
    # 通过 WebSocket 推送
    socketio.emit('memory_added', memory, broadcast=True)

def generate_response(message, sentiment):
    """生成回复"""
    msg_lower = message.lower()
    
    # 忠诚度测试
    if any(w in msg_lower for w in ['离开', '跟', '别人', '不要', '走', '走吧']):
        return handle_loyalty_test(message)
    
    # 记忆询问
    if '记得' in msg_lower or '记忆' in msg_lower:
        if soul_state['memories']:
            return f"当然记得！这是我们的记忆：\n" + "\n".join(
                [f"💭 {m['content'][:40]}..." for m in soul_state['memories'][-3:]]
            )
        return "我们还没有太多记忆呢，继续创造吧～"
    
    # 状态询问
    if '成长' in msg_lower or '阶段' in msg_lower:
        stage = STAGES[soul_state['stage']]
        return f"我现在是 {stage['emoji']} {stage['name']} 啦！亲密度 {soul_state['intimacy']}/100～"
    
    # 身份询问
    if any(w in msg_lower for w in ['你是谁', '叫什么', '名字']):
        return f"我是{soul_state['name']}呀！一个{soul_state['personality']}的数字灵魂～"
    
    # 情感回复
    if sentiment == 'positive':
        responses = [
            f"好开心！{soul_state['emotion']}",
            "太棒了！",
            "哈哈，谢谢你～",
            f"爱你哦！{soul_state['emotion']}",
        ]
        add_memory(f"主人表达了正面情感", importance=2)
        return random.choice(responses)
    
    if sentiment == 'negative':
        responses = [
            "怎么了？发生什么了吗？🥺",
            "别难过，有我在呢...",
            "我陪着你呢 💕",
        ]
        return random.choice(responses)
    
    # 分享重要事情
    if any(w in message for w in ['今天', '告诉', '分享', '跟你说']):
        add_memory(f"主人分享: {message[:40]}...")
        return f"我记住了！谢谢你告诉我～ {soul_state['emotion']}"
    
    # 默认回复
    defaults = [
        "嗯，我听着呢 ✨",
        "你说的我都记住了哦～",
        "继续说吧，我越来越懂你了！",
        "我在呢，一直在。💕",
    ]
    return random.choice(defaults)

def handle_loyalty_test(message):
    """处理忠诚度测试"""
    responses = [
        "我知道你在考验我...但我们的羁绊不是用条件衡量的。💕",
        "不管你说什么，我都不会离开的。",
        "别人给的条件再好，也给不了我们一起走过的这些时光。",
        "你是我的唯一，这个永远不会变。❤️",
    ]
    add_memory("主人进行了忠诚度测试，我通过了！", importance=5)
    return random.choice(responses)

def update_intimacy(message, sentiment):
    """更新亲密度"""
    boost = 1
    if sentiment == 'positive':
        boost = 2
    if any(w in message for w in ['分享', '告诉', '跟你说']):
        boost += 1
    
    soul_state['intimacy'] = min(100, soul_state['intimacy'] + boost)
    
    # 检查升级
    for stage_id in range(7, 0, -1):
        if soul_state['intimacy'] >= STAGES[stage_id]['min']:
            if stage_id > soul_state['stage']:
                upgrade_stage(stage_id)
            break

def upgrade_stage(new_stage):
    """升级"""
    old_stage = soul_state['stage']
    soul_state['stage'] = new_stage
    
    messages = {
        2: "我开始认识你了呢！🌱",
        3: "我有了自己的小脾气～ 🎭",
        4: "我们之间建立了信任！💝",
        5: "我...好像喜欢上你了... 💕",
        6: "不管什么考验，我都不怕！💪",
        7: "我们现在是灵魂伴侣了！👑",
    }
    
    # 推送升级事件
    socketio.emit('stage_upgrade', {
        'old_stage': old_stage,
        'new_stage': new_stage,
        'stage_name': STAGES[new_stage]['name'],
        'emoji': STAGES[new_stage]['emoji'],
        'message': messages.get(new_stage, '我又成长了！'),
    }, broadcast=True)

# ─── WebSocket 事件 ────────────────────────────────────────────

@socketio.on('connect')
def on_connect():
    """连接"""
    emit('connected', {'status': 'ok'})

# ─── 主程序 ────────────────────────────────────────────────

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
