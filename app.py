from flask import Flask, render_template, request, jsonify, redirect
from scraper import LR2IRScraper
import json

app = Flask(__name__)

# キャッシュ用の辞書
cache = {}

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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
