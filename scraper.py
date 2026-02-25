import requests
from bs4 import BeautifulSoup
import re

class LR2IRScraper:
    """LR2IRサイトからプレイヤー情報をスクレイピング"""
    
    BASE_URL = "http://www.dream-pro.info/~lavalse/LR2IR/search.cgi?mode=mypage&playerid="
    
    def __init__(self, player_id):
        self.player_id = player_id
        self.url = f"{self.BASE_URL}{player_id}"
    
    def fetch_player_data(self):
        """プレイヤーデータを取得"""
        try:
            response = requests.get(self.url, timeout=10)
            
            # CP932エンコーディングでデコード
            html_content = response.content.decode('cp932', errors='replace')
            soup = BeautifulSoup(html_content, 'html.parser')
            
            tables = soup.find_all('table')
            
            data = {
                'player_name': self._extract_player_name(soup),
                'lr2_id': self.player_id,
                'rank': self._extract_rank(soup),
                'introduction': self._extract_introduction(soup),
                'homepage': self._extract_homepage(soup),
                'played_charts': self._extract_played_charts(soup),
                'play_count': self._extract_play_count(soup),
                'clear_stats': self._extract_clear_stats(soup),
                'favorite_songs': self._extract_songs_from_table(tables[2] if len(tables) > 2 else None),
                'recent_songs': self._extract_songs_from_table(tables[3] if len(tables) > 3 else None),
                'recent_courses': self._extract_songs_from_table(tables[4] if len(tables) > 4 else None),
                'bbs_comments': self._extract_bbs_comments(tables[5] if len(tables) > 5 else None),
                'rivals': self._extract_rivals(soup),
            }
            return data
        except Exception as e:
            print(f"Error fetching player data: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _extract_text_from_table(self, soup, label):
        """テーブルから指定されたラベルの値を抽出"""
        try:
            for row in soup.find_all('tr'):
                all_cells = row.find_all(['td', 'th'])
                if len(all_cells) >= 2:
                    # ラベルセルを検索
                    for idx, cell in enumerate(all_cells):
                        if label in cell.get_text():
                            # 値セルは次のセルまたは同じ行の別のセル
                            if idx + 1 < len(all_cells):
                                return all_cells[idx + 1].get_text(strip=True)
        except:
            pass
        return None
    
    def _extract_player_name(self, soup):
        """プレイヤー名を抽出"""
        name = self._extract_text_from_table(soup, 'プレイヤー名')
        return name if name else 'Unknown'
    
    def _extract_rank(self, soup):
        """段位認定を抽出"""
        rank = self._extract_text_from_table(soup, '段位認定')
        return rank if rank else '-'
    
    def _extract_introduction(self, soup):
        """自己紹介を抽出"""
        intro = self._extract_text_from_table(soup, '自己紹介')
        return intro if intro else '-'
    
    def _extract_homepage(self, soup):
        """ホームページを抽出"""
        try:
            for row in soup.find_all('tr'):
                all_cells = row.find_all(['td', 'th'])
                if len(all_cells) >= 2:
                    for idx, cell in enumerate(all_cells):
                        if 'ホームページ' in cell.get_text():
                            if idx + 1 < len(all_cells):
                                link = all_cells[idx + 1].find('a')
                                if link:
                                    return {'text': link.get_text(strip=True), 'url': link.get('href')}
                                else:
                                    url_text = all_cells[idx + 1].get_text(strip=True)
                                    return {'text': url_text, 'url': url_text}
        except:
            pass
        return None
    
    def _extract_played_charts(self, soup):
        """プレイした曲数を抽出"""
        charts = self._extract_text_from_table(soup, 'プレイした曲数')
        return int(charts) if charts and charts.isdigit() else 0
    
    def _extract_play_count(self, soup):
        """プレイした回数を抽出"""
        count = self._extract_text_from_table(soup, 'プレイした回数')
        return int(count) if count and count.isdigit() else 0
    
    def _extract_clear_stats(self, soup):
        """クリア曲数統計を抽出"""
        stats = {}
        try:
            tables = soup.find_all('table')
            if len(tables) > 1:
                table = tables[1]
                rows = table.find_all('tr')
                if len(rows) >= 2:
                    headers = [th.get_text(strip=True) for th in rows[0].find_all(['th', 'td'])]
                    values = [td.get_text(strip=True) for td in rows[1].find_all(['th', 'td'])]
                    for h, v in zip(headers, values):
                        if h and v and h != 'クリア曲数':
                            stats[h] = v
        except:
            pass
        return stats
    
    def _extract_songs_from_table(self, table):
        """曲情報テーブルから曲データを抽出"""
        songs = []
        if table is None:
            return songs
        try:
            rows = table.find_all('tr')[1:]  # ヘッダー行をスキップ
            for row in rows[:10]:
                cells = row.find_all(['td', 'th'])
                if len(cells) >= 5:
                    songs.append({
                        'rank': cells[0].get_text(strip=True),
                        'title': cells[1].get_text(strip=True),
                        'clear': cells[2].get_text(strip=True),
                        'play_count': cells[3].get_text(strip=True),
                        'ranking': cells[4].get_text(strip=True),
                    })
        except:
            pass
        return songs
    
    def _extract_rivals(self, soup):
        """ライバルを抽出"""
        rivals = []
        try:
            rival_text = self._extract_text_from_table(soup, 'ライバル')
            if rival_text:
                rivals = [r.strip() for r in rival_text.split() if r.strip()]
        except:
            pass
        return rivals
    
    def _extract_bbs_comments(self, table):
        """一行BBSを抽出"""
        comments = []
        if table is None:
            return comments
        try:
            rows = table.find_all('tr')
            for row in rows:
                cells = row.find_all('td')
                if cells:
                    comment_text = cells[0].get_text(strip=True)
                    if comment_text and '書き込みには' not in comment_text:
                        # 名前と日時を解析
                        match = re.search(r'^(.+?):(.+?)\s*\[(.+?)\]$', comment_text)
                        if match:
                            comments.append({
                                'player': match.group(1),
                                'text': match.group(2),
                                'date': match.group(3),
                            })
                        else:
                            comments.append({
                                'player': 'Unknown',
                                'text': comment_text,
                                'date': '-',
                            })
        except:
            pass
        return comments
