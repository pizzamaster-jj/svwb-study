# シャドバ ビヨンド 学習ノート

Shadowverse: Worlds Beyond のカードシナジー・相手デッキ対策・ターン別の注意点を
自分で書き溜めて学習するための単一HTMLアプリ。

## 構成
- `index.html` — **これを開く**。カードデータを埋め込んだ単一ファイル（他のファイル不要で動作）
- `template.html` — アプリのソース（`<script src="cards.js">` を参照する編集用。ここを編集してビルドする）
- `cards.js` — カードデータ（日本語・826枚。`window.CARD_DATA`）
- `generate.py` — 公式APIからカードデータ（`cards.js`）を再生成
- `build.py` — `template.html` + `cards.js` を結合して単一の `index.html` を生成

## 機能（シンプル4タブ構成）
| タブ | 内容 |
|---|---|
| デッキ作成 | クラスを選び、そのクラス＋ニュートラルから40枚デッキを構築（同名3枚まで）。マナカーブ・タイプ内訳、複数デッキ保存/読込。参考構築（連携進化ロイヤル/ランプドラゴン/スペルウィッチ）をワンクリック取込 |
| 戦い方 | デッキを選ぶだけで**全自動**：回し方（勝ち筋/マリガン/序盤/中盤/終盤）、マリガンキープ推奨%（カード効果・先後を解析）、現環境メタ9デッキ別の「相手の狙い/警戒点/こちらの立ち回り/マリガン」。実戦ノートの実績も併記 |
| 実戦ノート | 対戦ごとに「実際にどう動いたか」を序盤/中盤/終盤/気付きのフォーマットで記録→マッチアップ別の実測勝率を自動集計し「戦い方」に反映 |
| データ | JSON書き出し／読み込み、最新カード取得の案内 |

※旧タブ（カード検索/プレイング/アドバイザー/コンボ/マッチアップ/ターン別/対戦記録）のコードは温存していますがナビからは非表示。必要になれば復活できます。カード詳細モーダル（画像クリック）は引き続き動作します。

メタデッキ（戦い方タブ）は `template.html` 内の `META_DECKS` に埋め込み（現行ローテ環境・出典 game8）。環境が変わったら同定数を編集して `python3 build.py` で反映します。

デッキ・実戦ノートはブラウザの localStorage に保存されます。
端末移行やGitHubへの保存は「データ」タブから JSON 書き出しを使ってください。

## ローカルで開く
`index.html` をブラウザでダブルクリックして開くだけで動きます（カードデータは埋め込み済み・他ファイル不要）。
表示が古い場合は `Cmd + Shift + R`（ハードリロード）。

## アプリのコードを編集したら（再ビルド）
`template.html` を編集 → `python3 build.py` で `index.html` を再生成。

## GitHub Pages で公開する手順
```bash
cd "svwb-study"
git init
git add index.html cards.js README.md
git commit -m "svwb study tool"
gh repo create svwb-study --public --source=. --push
# GitHubのリポジトリ Settings > Pages > Branch: main / root を選択
# 公開URL: https://<ユーザー名>.github.io/svwb-study/
```

## カードデータの更新（新弾追加時）
公式APIから全カードを取得して `cards.js` を再生成します。

```bash
# 1) 公式APIから全ページ取得して off_all.json を作る
python3 - <<'PY'
import urllib.request, json, time
BASE="https://shadowverse-wb.com/web/CardList/cardList?lang=ja&offset=%d"
details={}; tribe={}; sets={}; seen=set(); off=0
while True:
    req=urllib.request.Request(BASE%off, headers={'User-Agent':'Mozilla/5.0'})
    d=json.load(urllib.request.urlopen(req,timeout=30))['data']
    ids=d['sort_card_id_list']
    if not ids: break
    tribe.update(d.get('tribe_names',{})); sets.update(d.get('card_set_names',{}))
    for cid,det in d['card_details'].items(): details[str(cid)]=det
    newids=[i for i in ids if i not in seen]; seen.update(ids)
    if off>0 and not newids: break
    off+=30
    if off> d['count']+60: break
    time.sleep(0.15)
json.dump({'details':details,'tribe':tribe,'sets':sets}, open('off_all.json','w'), ensure_ascii=False)
print('fetched', len(details))
PY

# 2) off_all.json から cards.js を生成
python3 generate.py   # cards_ja.js を出力 → cards.js に上書き
mv cards_ja.js cards.js
rm off_all.json

# 3) 単一ファイルの index.html に埋め込む
python3 build.py
```

## データ出典
- カード情報: shadowverse-wb.com 公式 CardList API（日本語・`lang=ja`）
- カード画像: static.dotgg.gg（`/shadowverse/cards/<card_id>.webp`）
- カード名・効果・進化・公式Q&Aすべて日本語。カード画像イラスト内の英字名は画像側の仕様。
