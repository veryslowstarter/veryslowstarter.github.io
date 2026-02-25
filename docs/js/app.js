// LR2IR Player Profile Viewer - Client-side JavaScript
// GitHub Pages で動作

document.addEventListener('DOMContentLoaded', function() {
    loadPlayerData();
});

async function loadPlayerData() {
    const contentDiv = document.getElementById('player-content');
    
    try {
        // JSON データを読み込む
        const response = await fetch('./data/player.json');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        renderPlayerProfile(data, contentDiv);
        
    } catch (error) {
        console.error('Error loading player data:', error);
        contentDiv.innerHTML = `<div class="error-message">
            <p>申し訳ございません。プレイヤーデータの読み込みに失敗しました。</p>
            <p>Error: ${error.message}</p>
        </div>`;
    }
}

function renderPlayerProfile(data, container) {
    const html = `
        <!-- プレイヤー基本情報 -->
        <section class="player-info">
            <h2>${escapeHtml(data.player_name)}</h2>
            <div class="info-grid">
                <div class="info-item">
                    <span class="label">LR2ID:</span>
                    <span class="value">${data.lr2_id}</span>
                </div>
                <div class="info-item">
                    <span class="label">段位認定:</span>
                    <span class="value">${escapeHtml(data.rank)}</span>
                </div>
            </div>

            <div class="section">
                <h3>自己紹介</h3>
                <p class="introduction">
                    ${data.introduction && data.introduction !== '-' 
                        ? escapeHtml(data.introduction) 
                        : '紹介文がまだ設定されていません'}
                </p>
            </div>

            ${data.homepage ? `
            <div class="section">
                <h3>ホームページ</h3>
                <a href="${escapeHtml(data.homepage.url)}" target="_blank" class="homepage-link">
                    ${escapeHtml(data.homepage.text)}
                </a>
            </div>
            ` : ''}
        </section>

        <!-- プレイ統計 -->
        <section class="statistics">
            <h2>プレイ統計</h2>
            <div class="stat-grid">
                <div class="stat-item">
                    <span class="stat-label">プレイした曲数</span>
                    <span class="stat-value">${data.played_charts}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">プレイした回数</span>
                    <span class="stat-value">${data.play_count}</span>
                </div>
            </div>

            ${Object.keys(data.clear_stats).length > 0 ? `
            <div class="section">
                <h3>クリア曲数</h3>
                <table class="clear-stats-table">
                    <thead>
                        <tr>
                            <th>FULLCOMBO</th>
                            <th>HARD</th>
                            <th>NORMAL</th>
                            <th>EASY</th>
                            <th>FAILED</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>${data.clear_stats['FULLCOMBO'] || '-'}</td>
                            <td>${data.clear_stats['HARD'] || '-'}</td>
                            <td>${data.clear_stats['NORMAL'] || '-'}</td>
                            <td>${data.clear_stats['EASY'] || '-'}</td>
                            <td>${data.clear_stats['FAILED'] || '-'}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
            ` : ''}
        </section>

        <!-- ライバル -->
        ${data.rivals && data.rivals.length > 0 ? `
        <section class="rivals">
            <h2>ライバル (${data.rivals.length}人)</h2>
            <div class="rival-list">
                ${data.rivals.map(rival => `<span class="rival-tag">${escapeHtml(rival)}</span>`).join('')}
            </div>
        </section>
        ` : ''}

        <!-- よくプレイする曲 -->
        ${data.favorite_songs && data.favorite_songs.length > 0 ? `
        <section class="songs">
            <h2>よくプレイする曲 Top 10</h2>
            <table class="songs-table">
                <thead>
                    <tr>
                        <th>#</th>
                        <th>タイトル</th>
                        <th>クリア</th>
                        <th>プレイ回数</th>
                        <th>ランキング</th>
                    </tr>
                </thead>
                <tbody>
                    ${data.favorite_songs.map(song => `
                    <tr class="clear-${song.clear.replace(/\\s+/g, '').toLowerCase()}">
                        <td class="rank">${escapeHtml(song.rank)}</td>
                        <td class="title">${escapeHtml(song.title)}</td>
                        <td class="clear">${escapeHtml(song.clear)}</td>
                        <td class="play-count">${escapeHtml(song.play_count)}</td>
                        <td class="ranking">${escapeHtml(song.ranking)}</td>
                    </tr>
                    `).join('')}
                </tbody>
            </table>
        </section>
        ` : ''}

        <!-- 最近プレイした曲 -->
        ${data.recent_songs && data.recent_songs.length > 0 ? `
        <section class="songs">
            <h2>最近プレイした曲</h2>
            <table class="songs-table">
                <thead>
                    <tr>
                        <th>#</th>
                        <th>タイトル</th>
                        <th>クリア</th>
                        <th>プレイ回数</th>
                        <th>ランキング</th>
                    </tr>
                </thead>
                <tbody>
                    ${data.recent_songs.map(song => `
                    <tr class="clear-${song.clear.replace(/\\s+/g, '').toLowerCase()}">
                        <td class="rank">${escapeHtml(song.rank)}</td>
                        <td class="title">${escapeHtml(song.title)}</td>
                        <td class="clear">${escapeHtml(song.clear)}</td>
                        <td class="play-count">${escapeHtml(song.play_count)}</td>
                        <td class="ranking">${escapeHtml(song.ranking)}</td>
                    </tr>
                    `).join('')}
                </tbody>
            </table>
        </section>
        ` : ''}

        <!-- 最近プレイしたコース -->
        ${data.recent_courses && data.recent_courses.length > 0 ? `
        <section class="courses">
            <h2>最近プレイしたコース</h2>
            <table class="songs-table">
                <thead>
                    <tr>
                        <th>#</th>
                        <th>タイトル</th>
                        <th>クリア</th>
                        <th>プレイ回数</th>
                        <th>ランキング</th>
                    </tr>
                </thead>
                <tbody>
                    ${data.recent_courses.map(course => `
                    <tr class="clear-${course.clear.replace(/\\s+/g, '').toLowerCase()}">
                        <td class="rank">${escapeHtml(course.rank)}</td>
                        <td class="title">${escapeHtml(course.title)}</td>
                        <td class="clear">${escapeHtml(course.clear)}</td>
                        <td class="play-count">${escapeHtml(course.play_count)}</td>
                        <td class="ranking">${escapeHtml(course.ranking)}</td>
                    </tr>
                    `).join('')}
                </tbody>
            </table>
        </section>
        ` : ''}

        <!-- 一行BBS -->
        ${data.bbs_comments && data.bbs_comments.length > 0 ? `
        <section class="bbs">
            <h2>一行BBS</h2>
            <div class="bbs-comments">
                ${data.bbs_comments.map(comment => `
                <div class="bbs-comment">
                    <span class="comment-player"><strong>${escapeHtml(comment.player)}</strong></span>
                    <span class="comment-date">[${escapeHtml(comment.date)}]</span>
                    <p class="comment-text">${escapeHtml(comment.text)}</p>
                </div>
                `).join('')}
            </div>
        </section>
        ` : ''}
    `;
    
    container.innerHTML = html;
    
    // 最後の更新時刻を表示
    if (data.last_updated) {
        const footerDiv = document.querySelector('footer');
        if (footerDiv) {
            const updateDate = new Date(data.last_updated);
            const formattedDate = updateDate.toLocaleString('ja-JP', {
                year: 'numeric',
                month: '2-digit',
                day: '2-digit',
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit'
            });
            
            const updateSpan = document.createElement('p');
            updateSpan.className = 'last-updated';
            updateSpan.textContent = `最終更新: ${formattedDate} JST`;
            footerDiv.appendChild(updateSpan);
        }
    }
}

function escapeHtml(text) {
    if (!text) return '';
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}
