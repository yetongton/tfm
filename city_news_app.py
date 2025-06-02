import os
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import sqlite3
import json
from datetime import datetime
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import numpy as np
from translations import get_text, get_city_name

# 创建应用
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['DATABASE'] = 'city_news.db'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max-limit
app.config['MODEL_PATH'] = 'news_sentiment_model'
app.config['DEFAULT_LANGUAGE'] = 'zh'  # 默认语言为中文

# 确保上传文件夹存在
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# 初始化登录管理器
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# 全局变量存储模型和分词器
tokenizer = None
model = None

# 使用模型分析文本情感
def analyze_sentiment(texts):
    try:
        # 加载模型和分词器
        model_path = app.config['MODEL_PATH']
        tokenizer = AutoTokenizer.from_pretrained(model_path)
        model = AutoModelForSequenceClassification.from_pretrained(model_path)
        print("模型和分词器加载成功")
        
        # 批量分析，防止内存溢出
        batch_size = 8
        results = []
        
        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i:i+batch_size]
            # 分词
            inputs = tokenizer(batch_texts, padding=True, truncation=True, max_length=256, return_tensors="pt")
            
            # 推理
            with torch.no_grad():
                outputs = model(**inputs)
                predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
            
            # 处理结果
            for pred in predictions:
                if len(pred) >= 3:
                    negative = pred[0].item()
                    neutral = pred[1].item()
                    positive = pred[2].item()
                elif len(pred) == 2:
                    negative = pred[0].item()
                    positive = pred[1].item()
                    neutral = 0.0
                else:
                    raise ValueError("模型输出标签数量不正确")
                
                # 计算情感分数 (0-100)
                sentiment_score = positive * 100
                
                results.append({
                    'positive': positive,
                    'neutral': neutral,
                    'negative': negative,
                    'sentiment_score': sentiment_score
                })
                
        return results
    except Exception as e:
        print(f"情感分析出错: {str(e)}")
        raise

# 用户类
class User(UserMixin):
    def __init__(self, id, username, password_hash):
        self.id = id
        self.username = username
        self.password_hash = password_hash

# 数据库操作
def get_db_connection():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 创建用户表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # 创建上传记录表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS uploads (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        city TEXT NOT NULL,
        filename TEXT NOT NULL,
        sentiment_score REAL,
        news_count INTEGER,
        positive_pct REAL,
        negative_pct REAL,
        neutral_pct REAL,
        uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')
    
    # 创建用户设置表，用于存储用户的语言偏好
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_settings (
        user_id INTEGER PRIMARY KEY,
        language TEXT NOT NULL DEFAULT 'zh',
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')
    
    conn.commit()
    conn.close()

# 初始化数据库
init_db()

# 获取当前语言
def get_current_language():
    # 首先从会话中获取
    lang = session.get('language')
    if lang:
        return lang
    
    # 如果用户已登录，从用户设置中获取
    if current_user.is_authenticated:
        conn = get_db_connection()
        settings = conn.execute('SELECT language FROM user_settings WHERE user_id = ?', 
                              (current_user.id,)).fetchone()
        conn.close()
        
        if settings:
            # 保存到会话
            session['language'] = settings['language']
            return settings['language']
    
    # 默认使用中文
    return app.config['DEFAULT_LANGUAGE']

# 上下文处理器，为所有模板提供函数
@app.context_processor
def utility_processor():
    def translate(key, *args):
        return get_text(key, get_current_language(), *args)
    
    def translate_city(city):
        return get_city_name(city, get_current_language())
    
    return {
        'translate': translate, 
        'translate_city': translate_city,
        'current_language': get_current_language
    }

# 用户加载函数
@login_manager.user_loader
def load_user(user_id):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    
    if user:
        return User(user['id'], user['username'], user['password_hash'])
    return None

# 加载城市数据
def load_city_data():
    try:
        # 尝试加载CSV文件
        csv_path = os.path.join('jieguo', 'city_sentiment_scores (4).csv')
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            # 确保数据包含所需列
            required_columns = ['city', 'news_count', 'sentiment_score', 'positive_pct', 'negative_pct', 'neutral_pct']
            for col in required_columns:
                if col not in df.columns:
                    print(f"缺少必要的列: {col}")
                    raise ValueError(f"CSV文件缺少必要的列: {col}")
            
            # 数据清洗：过滤掉新闻数量小于5的城市和得分为100的城市
            df = df[df['news_count'] >= 5]  # 过滤掉新闻数量小于5的城市
            df = df[df['sentiment_score'] < 100]  # 过滤掉情感得分为100的城市
            
            # 添加排名列
            df['rank'] = df['sentiment_score'].rank(ascending=False, method='min').astype(int)
            return df
        else:
            print(f"找不到数据文件: {csv_path}")
            raise FileNotFoundError(f"找不到数据文件: {csv_path}")
    except Exception as e:
        print(f"加载数据时出错: {str(e)}")
        # 返回空数据框
        return pd.DataFrame({
            'city': [],
            'news_count': [],
            'sentiment_score': [],
            'positive_pct': [],
            'negative_pct': [],
            'neutral_pct': [],
            'rank': []
        })

# 语言切换
@app.route('/language/<lang>')
def set_language(lang):
    # 检查语言是否有效
    if lang not in ['zh', 'es']:
        lang = app.config['DEFAULT_LANGUAGE']
    
    # 保存到会话
    session['language'] = lang
    
    # 如果用户已登录，保存到用户设置
    if current_user.is_authenticated:
        conn = get_db_connection()
        # 检查是否已有设置
        settings = conn.execute('SELECT * FROM user_settings WHERE user_id = ?', 
                            (current_user.id,)).fetchone()
        
        if settings:
            conn.execute('UPDATE user_settings SET language = ? WHERE user_id = ?',
                      (lang, current_user.id))
        else:
            conn.execute('INSERT INTO user_settings (user_id, language) VALUES (?, ?)',
                      (current_user.id, lang))
        
        conn.commit()
        conn.close()
    
    # 返回上一页，添加时间戳防止缓存
    referrer = request.referrer or url_for('index')
    timestamp = datetime.now().timestamp()
    if '?' in referrer:
        return redirect(f"{referrer}&_={timestamp}")
    else:
        return redirect(f"{referrer}?_={timestamp}")

# 路由：主页
@app.route('/')
def index():
    cities_df = load_city_data()
    if cities_df.empty:
        flash(get_text('no_data', get_current_language()), 'danger')
        return render_template('index.html', top_cities=[], bottom_cities=[])
    
    # 获取前20名城市
    top_cities = cities_df.sort_values(by='sentiment_score', ascending=False).head(20)
    # 获取后20名城市
    bottom_cities = cities_df.sort_values(by='sentiment_score', ascending=True).head(20)
    
    return render_template('index.html', 
                          top_cities=top_cities.to_dict('records'), 
                          bottom_cities=bottom_cities.to_dict('records'))

# 路由：全部城市
@app.route('/cities')
def cities():
    cities_df = load_city_data()
    if cities_df.empty:
        flash(get_text('no_data', get_current_language()), 'danger')
        return render_template('cities.html', cities=[])
    
    # 按情感分数排序
    cities_list = cities_df.sort_values(by='sentiment_score', ascending=False).to_dict('records')
    return render_template('cities.html', cities=cities_list)

# 路由：城市详情
@app.route('/city/<city_name>')
def city_detail(city_name):
    cities_df = load_city_data()
    if cities_df.empty:
        flash(get_text('no_data', get_current_language()), 'danger')
        return redirect(url_for('index'))
    
    # 查找指定城市
    city_data = cities_df[cities_df['city'] == city_name]
    if city_data.empty:
        flash(get_text('city_not_found', get_current_language(), city_name), 'danger')
        return redirect(url_for('cities'))
    
    return render_template('city_detail.html', city=city_data.iloc[0].to_dict())

# 路由：搜索城市
@app.route('/search')
def search():
    query = request.args.get('q', '')
    if not query:
        return redirect(url_for('cities'))
    
    cities_df = load_city_data()
    if cities_df.empty:
        flash(get_text('no_data', get_current_language()), 'danger')
        return render_template('search.html', query=query, results=[])
    
    # 搜索匹配的城市
    results = cities_df[cities_df['city'].str.contains(query)]
    results = results.sort_values(by='sentiment_score', ascending=False)
    
    return render_template('search.html', 
                          query=query, 
                          results=results.to_dict('records'))

# 路由：注册
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if not username or not password:
            flash(get_text('empty_fields', get_current_language()), 'danger')
            return render_template('register.html')
        
        if password != confirm_password:
            flash(get_text('password_mismatch', get_current_language()), 'danger')
            return render_template('register.html')
        
        conn = get_db_connection()
        existing_user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        
        if existing_user:
            flash(get_text('username_exists', get_current_language()), 'danger')
            conn.close()
            return render_template('register.html')
        
        # 创建新用户
        password_hash = generate_password_hash(password)
        conn.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', 
                    (username, password_hash))
        conn.commit()
        conn.close()
        
        flash(get_text('register_success', get_current_language()), 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

# 路由：登录
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        
        if not user or not check_password_hash(user['password_hash'], password):
            flash(get_text('invalid_credentials', get_current_language()), 'danger')
            return render_template('login.html')
        
        # 登录用户
        user_obj = User(user['id'], user['username'], user['password_hash'])
        login_user(user_obj)
        
        # 获取用户语言设置
        conn = get_db_connection()
        settings = conn.execute('SELECT language FROM user_settings WHERE user_id = ?', 
                              (user['id'],)).fetchone()
        
        if settings:
            session['language'] = settings['language']
        else:
            # 创建默认设置
            conn.execute('INSERT INTO user_settings (user_id, language) VALUES (?, ?)',
                        (user['id'], app.config['DEFAULT_LANGUAGE']))
            conn.commit()
        
        conn.close()
        
        return redirect(url_for('index'))
    
    return render_template('login.html')

# 路由：登出
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# 路由：个人中心
@app.route('/profile')
@login_required
def profile():
    conn = get_db_connection()
    uploads = conn.execute('''
        SELECT * FROM uploads 
        WHERE user_id = ? 
        ORDER BY uploaded_at DESC
    ''', (current_user.id,)).fetchall()
    conn.close()
    
    return render_template('profile.html', uploads=uploads)

# 路由：上传数据
@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        # 检查是否有文件
        if 'file' not in request.files:
            flash(get_text('no_file', get_current_language()), 'danger')
            return redirect(request.url)
        
        file = request.files['file']
        city = request.form.get('city', '')
        
        # 检查文件名和城市名
        if file.filename == '' or not city:
            flash(get_text('empty_fields_upload', get_current_language()), 'danger')
            return redirect(request.url)
        
        # 检查文件扩展名
        if not file.filename.endswith('.csv'):
            flash(get_text('csv_only', get_current_language()), 'danger')
            return redirect(request.url)
        
        # 保存文件
        filename = secure_filename(f"{city}_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv")
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        try:
            # 读取CSV文件
            df = pd.read_csv(file_path)
            
            # 提取新闻文本
            texts = []
            if 'title' in df.columns and 'content' in df.columns:
                # 如果同时有标题和内容，合并它们
                for _, row in df.iterrows():
                    text = f"{row['title']} {row['content']}"
                    texts.append(text)
            elif 'content' in df.columns:
                # 如果只有内容
                texts = df['content'].tolist()
            elif 'title' in df.columns:
                # 如果只有标题
                texts = df['title'].tolist()
            else:
                flash(get_text('missing_columns', get_current_language()), 'danger')
                return redirect(request.url)
            
            # 分析情感
            news_count = len(texts)
            if news_count == 0:
                flash(get_text('no_news', get_current_language()), 'danger')
                return redirect(request.url)
            
            sentiment_results = analyze_sentiment(texts)
            
            # 计算整体情感指标
            positives = [result['positive'] for result in sentiment_results]
            neutrals = [result['neutral'] for result in sentiment_results]
            negatives = [result['negative'] for result in sentiment_results]
            
            # 计算平均值
            avg_positive = sum(positives) / len(positives)
            avg_neutral = sum(neutrals) / len(neutrals)
            avg_negative = sum(negatives) / len(negatives)
            
            # 计算百分比
            positive_pct = avg_positive * 100
            neutral_pct = avg_neutral * 100
            negative_pct = avg_negative * 100
            
            # 计算整体情感分数 (0-100)
            sentiment_score = sum([result['sentiment_score'] for result in sentiment_results]) / len(sentiment_results)
            
            # 保存分析结果
            conn = get_db_connection()
            conn.execute('''
                INSERT INTO uploads 
                (user_id, city, filename, sentiment_score, news_count, positive_pct, negative_pct, neutral_pct) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (current_user.id, city, filename, sentiment_score, news_count, positive_pct, negative_pct, neutral_pct))
            conn.commit()
            upload_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]
            conn.close()
            
            flash(get_text('upload_success', get_current_language(), city), 'success')
            return redirect(url_for('upload_detail', upload_id=upload_id))
            
        except Exception as e:
            flash(get_text('analysis_error', get_current_language(), str(e)), 'danger')
            return redirect(request.url)
    
    return render_template('upload.html')

# 路由：上传结果详情
@app.route('/upload/<int:upload_id>')
@login_required
def upload_detail(upload_id):
    conn = get_db_connection()
    upload = conn.execute('SELECT * FROM uploads WHERE id = ? AND user_id = ?', 
                         (upload_id, current_user.id)).fetchone()
    conn.close()
    
    if not upload:
        flash(get_text('upload_not_found', get_current_language()), 'danger')
        return redirect(url_for('profile'))
    
    return render_template('upload_detail.html', upload=upload)

# API：获取全部城市数据
@app.route('/api/cities')
def api_cities():
    cities_df = load_city_data()
    return jsonify(cities_df.to_dict('records'))

# API：获取指定城市数据
@app.route('/api/city/<city_name>')
def api_city(city_name):
    cities_df = load_city_data()
    city_data = cities_df[cities_df['city'] == city_name]
    
    if city_data.empty:
        return jsonify({'error': get_text('city_not_found', get_current_language(), city_name)}), 404
    
    return jsonify(city_data.iloc[0].to_dict())

if __name__ == '__main__':
    app.run(debug=True) 