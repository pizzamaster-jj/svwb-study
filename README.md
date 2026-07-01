# シャドバ ビヨンド 学習ノート

Shadowverse: Worlds Beyond のカードシナジー・相手デッキ対策・ターン別の注意点を
自分で書き溜めて学習するための単一HTMLアプリ。

## 構成
- `index.html` — **これを開く**。カードデータを埋め込んだ単一ファイル（他のファイル不要で動作）
- `template.html` — アプリのソース（`<script src="cards.js">` を参照する編集用。ここを編集してビルドする）
- `cards.js` — カードデータ（日本語・826枚。`window.CARD_DATA`）
- `generate.py` — 公式APIからカードデータ（`cards.js`）を再生成
- `build.py` — `template.html` + `cards.js` を結合して単一の `index.html` を生成

## 機能
| タブ | 内容 |
|---|---|
| カード | 名前/効果テキスト検索、クラス・タイプ・コスト・レア・種族・ローテで絞込。詳細で効果・進化後・公式Q&A・関連カードを表示 |
| デッキ作成 | クラスを選び、そのクラス＋ニュートラルから40枚デッキを構築（同名3枚まで）。マナカーブ・タイプ内訳を表示、複数デッキを保存/読込 |
| プレイング | 保存したデッキを選び「回し方」と現環境ローテ・メタデッキ（Tier1〜2）とのマッチアップを記録。各メタは狙い・キーカード・警戒点が下書き済み。「自動下書き」で自デッキの回答札を提案。連携進化ロイヤルは参考構築(40枚)をワンクリック取込 |
| アドバイザー | 自分のデッキ・先攻/後攻・相手デッキ・ターンを入力→ ①マリガンのキープ推奨度%＋手札診断 ②今ターンの推奨アクション（PP内の最適プレイを候補%で提示）③相手の警戒カードを超幾何分布で確率表示。**%は勝率でなくヒューリスティック/確率推定** |
| コンボ・シナジー | カードを複数選んで「何が起きるか」を登録。下部に同種族カードの自動まとめ |
| マッチアップ | 相手クラス別に ゲームプラン/キツいカード/立ち回り/マリガン を記録（自動保存） |
| ターン別 | Nターン目の相手の動き・自分の準備・注意カードを時系列で登録 |
| データ | 知識のJSON書き出し／読み込み、最新カード取得の案内 |

メタデッキ（プレイングタブ）は `template.html` 内の `META_DECKS` に埋め込み（現行ローテ環境・出典 game8）。環境が変わったら同定数を編集して `python3 build.py` で反映します。

デッキ・知識（プレイング・コンボ・マッチアップ・ターン別）はブラウザの localStorage に保存されます。
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
