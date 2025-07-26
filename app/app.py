import streamlit as st
import logic # logic.py から関数をインポート

# ページ設定
st.set_page_config(page_title="ポケモン図鑑アプリ", layout="centered")

st.title("🔍 ポケモン図鑑アプリ")

st.write("ポケモンの図鑑番号（ID）を入力して、情報をゲットしよう！")

# --- ポケモンのID入力 ---
pokemon_id_input = st.text_input("ポケモンの図鑑番号を入力してください (例: 25)", key="pokemon_id_input")

# 入力されたIDを整数に変換
try:
    pokemon_id = int(pokemon_id_input) if pokemon_id_input else 0
except ValueError:
    pokemon_id = -1 # 無効な入力として扱う

# --- ポケモン情報取得ボタン ---
if st.button("ポケモン情報をゲット！"):
    if pokemon_id <= 0:
        st.error("有効な図鑑番号（1以上の数字）を入力してください。")
    else:
        with st.spinner(f"ポケモンID {pokemon_id} の情報を検索中..."):
            pokemon_info, error_message = logic.fetch_pokemon_info(pokemon_id)
            
            if error_message:
                st.error(error_message)
                st.session_state['current_pokemon'] = None # エラー時は現在のポケモン情報をクリア
            elif pokemon_info:
                st.session_state['current_pokemon'] = pokemon_info # 情報をセッションステートに保存
                st.success(f"{pokemon_info['name']} の情報が見つかりました！")
                
                # ポケモン情報を表示
                st.subheader(f"{pokemon_info['name']} (No. {pokemon_info['id']})")
                
                # --- 画像表示のデバッグ ---
                # 取得した画像URLを一時的に表示して確認
                # st.write(f"画像URL: {pokemon_info['sprite_url']}") 
                # ↑デバッグが終わったらこの行はコメントアウトまたは削除してください。
                # -------------------------

                if pokemon_info['sprite_url']:
                    st.image(pokemon_info['sprite_url'], caption=pokemon_info['name'], width=150)
                else:
                    st.warning("このポケモンの画像は見つかりませんでした。")
                
                st.write(f"**タイプ:** {', '.join(pokemon_info['types'])}")
                st.write(f"**特性:** {', '.join(pokemon_info['abilities'])}")
            else:
                st.error("ポケモンの情報が見つかりませんでした。")
                st.session_state['current_pokemon'] = None

# --- お気に入りに追加ボタン ---
# 現在のポケモン情報がセッションステートに存在する場合のみ表示
if 'current_pokemon' in st.session_state and st.session_state['current_pokemon']:
    if st.button(f"{st.session_state['current_pokemon']['name']} をお気に入りに追加"):
        result_message = logic.add_to_favorites(st.session_state['current_pokemon'])
        st.info(result_message)

st.divider() # 区切り線

# --- お気に入りポケモン一覧 ---
st.subheader("あなたのお気に入りポケモン")
st.info("**注意:** Streamlit Cloudの無料環境では、お気に入りデータはアプリの再起動やセッション終了時に失われます。これは一時的な保存機能です。")

favorite_pokemon_list = logic.get_favorites()

if favorite_pokemon_list:
    # 複数のお気に入りポケモンをグリッド形式で表示
    cols = st.columns(3) # 3列で表示
    for i, pokemon in enumerate(favorite_pokemon_list):
        with cols[i % 3]: # 列を循環させる
            st.markdown(f"**{pokemon['name']}** (No. {pokemon['id']})")
            if pokemon['sprite_url']:
                st.image(pokemon['sprite_url'], width=100)
            else:
                st.caption("画像なし")
            st.caption(f"タイプ: {', '.join(pokemon['types'])}")
            # 必要であれば、さらに詳細情報を表示
else:
    st.info("まだお気に入りのポケモンはいません。ポケモンを検索して追加しましょう！")

