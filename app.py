from flask import Flask, render_template, request, jsonify, redirect
from scraper import LR2IRScraper
import json
from apscheduler.schedulers.background import BackgroundScheduler
import pytz
from datetime import datetime

app = Flask(__name__)

# キャッシュ用の辞書
cache = {}
scheduler = BackgroundScheduler()
last_update_time = None  # 最後の更新時刻

def update_cache():
    """キャッシュを更新する定期タスク"""
    global cache, last_update_time
    cache = {}
    last_update_time = datetime.now(pytz.timezone('Asia/Tokyo'))
    print(f"[{last_update_time}] キャッシュをクリアしました")

@app.route('/')
def index():
    """ホームページ"""
    return render_template('index.html')

@app.route('/player/<int:player_id>')
def player_profile(player_id):
    """プレイヤープロフィール表示"""
    # キャッシュをチェック
    if player_id in cache:
        player_data = cache[player_id]
    else:
        scraper = LR2IRScraper(player_id)
        player_data = scraper.fetch_player_data()
        
        if player_data is None:
            return render_template('error.html', message='プレイヤーデータが取得できませんでした'), 404
        
        cache[player_id] = player_data
    
    return render_template('player_profile.html', player=player_data)

@app.route('/api/player/<int:player_id>')
def api_player_data(player_id):
    """API: プレイヤーデータをJSON形式で返す"""
    # キャッシュをチェック
    if player_id in cache:
        player_data = cache[player_id]
    else:
        scraper = LR2IRScraper(player_id)
        player_data = scraper.fetch_player_data()
        
        if player_data is None:
            return jsonify({'error': 'Player not found'}), 404
        
        cache[player_id] = player_data
    
    return jsonify(player_data)

@app.route('/search', methods=['GET', 'POST'])
def search():
    """検索ページ"""
    if request.method == 'POST':
        player_id = request.form.get('player_id')
        if player_id and player_id.isdigit():
            return redirect(f'/player/{player_id}')
    
    return render_template('search.html')

@app.route('/admin')
def admin():
    """管理ページ - キャッシュ更新時刻を表示"""
    if last_update_time:
        update_time_str = last_update_time.strftime('%Y年%m月%d日 %H:%M:%S')
        next_update = last_update_time.replace(hour=0, minute=0, second=0) + __import__('datetime').timedelta(days=1)
        next_update_str = next_update.strftime('%Y年%m月%d日 %H:%M:%S')
    else:
        update_time_str = '未更新'
        next_update_str = '0時に更新予定'
    
    return f"""
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>管理ページ</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            .info {{ background-color: #f0f0f0; padding: 15px; border-radius: 5px; }}
            h1 {{ color: #333; }}
            .status {{ font-size: 18px; font-weight: bold; color: #006600; }}
        </style>
    </head>
    <body>
        <h1>更新状況確認</h1>
        <div class="info">
            <p><strong>最終更新時刻:</strong> <span class="status">{update_time_str}</span></p>
            <p><strong>次回更新予定:</strong> <span class="status">{next_update_str}</span></p>
        </div>
    </body>
    </html>
    """

@app.route('/api/last-update')
def api_last_update():
    """API: 最終更新時刻をJSON形式で返す"""
    if last_update_time:
        return jsonify({{
            'last_update': last_update_time.isoformat(),
            'timestamp': int(last_update_time.timestamp())
        }})
    else:
        return jsonify({{'last_update': None, 'timestamp': None}})

if __name__ == '__main__':
    # UTC+9 (日本時間) の午前0時にキャッシュを更新
    scheduler.add_job(
        update_cache,
        'cron',
        hour=0,
        minute=0,
        timezone=pytz.timezone('Asia/Tokyo')
    )
    scheduler.start()
    
    app.run(debug=True, host='0.0.0.0', port=5000)
