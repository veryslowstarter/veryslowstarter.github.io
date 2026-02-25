#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
LR2IR Player Data Fetcher - GitHub Actions用スクリプト
データを JSON ファイルとして出力
"""

import json
import sys
from pathlib import Path
from scraper import LR2IRScraper

def main():
    player_id = 185532
    
    # データ取得
    scraper = LR2IRScraper(player_id)
    data = scraper.fetch_player_data()
    
    if data is None:
        print(f"Failed to fetch player {player_id}")
        sys.exit(1)
    
    # タイムスタンプを追加
    from datetime import datetime
    data['last_updated'] = datetime.now().isoformat()
    
    # JSON ファイルを保存
    output_path = Path(__file__).parent / 'docs' / 'data' / 'player.json'
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"Successfully saved player data to {output_path}")
    print(f"Player: {data.get('player_name', 'Unknown')}")
    print(f"Last Updated: {data.get('last_updated')}")

if __name__ == '__main__':
    main()
