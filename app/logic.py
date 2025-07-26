import requests
import os
import json
import streamlit as st # Streamlitのstオブジェクトをインポート（エラー表示のため）

# お気に入りファイルを保存するディレクトリ
DATA_DIR = "data"
FAVORITES_FILE = os.path.join(DATA_DIR, "favorite_pokemon.jsonl") # JSON Lines形式で保存

def ensure_data_directory_exists():
    """データディレクトリが存在しない場合は作成します。"""
    os.makedirs(DATA_DIR, exist_ok=True)

def fetch_pokemon_info(pokemon_id):
    """
    PokeAPIから指定されたIDのポケモンの情報を取得します。
    """
    if not isinstance(pokemon_id, int) or pokemon_id <= 0:
        return None, "無効なポケモンIDです。1以上の数字を入力してください。"

    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}/"
    try:
        response = requests.get(url)
        response.raise_for_status()  # HTTPエラーがあれば例外を発生させる
        pokemon_data = response.json()

        # 必要な情報を抽出
        name = pokemon_data.get("name", "不明").capitalize() # 最初の文字を大文字に
        types = [t["type"]["name"].capitalize() for t in pokemon_data.get("types", [])]
        abilities = [a["ability"]["name"].capitalize() for a in pokemon_data.get("abilities", [])]
        sprite_url = pokemon_data["sprites"]["front_default"] if "sprites" in pokemon_data else None

        return {
            "id": pokemon_id,
            "name": name,
            "types": types,
            "abilities": abilities,
            "sprite_url": sprite_url
        }, None
    except requests.exceptions.RequestException as e:
        if response.status_code == 404:
            return None, f"ポケモンID {pokemon_id} の情報は見つかりませんでした。正しいIDを入力してください。"
        return None, f"ポケモンの取得中にエラーが発生しました: {e}"
    except Exception as e:
        return None, f"予期せぬエラーが発生しました: {e}"

def add_to_favorites(pokemon_data):
    """
    ポケモンの情報をお気に入りファイルに追加します。
    各ポケモンはJSON形式で1行に保存されます (JSON Lines形式)。
    """
    ensure_data_directory_exists() # ディレクトリが存在することを確認
    try:
        # ファイルが存在しない場合は作成し、存在する場合は追記モードで開く
        with open(FAVORITES_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(pokemon_data, ensure_ascii=False) + "\n")
        return "お気に入りに追加しました！"
    except IOError as e:
        return f"ファイルの書き込み中にエラーが発生しました: {e}"

def get_favorites():
    """
    お気に入りファイルからポケモンの情報を読み込みます。
    """
    ensure_data_directory_exists() # ディレクトリが存在することを確認
    favorites = []
    try:
        # ファイルが存在しない場合は空のリストを返す
        if not os.path.exists(FAVORITES_FILE):
            return []
            
        with open(FAVORITES_FILE, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    favorites.append(json.loads(line.strip()))
                except json.JSONDecodeError as e:
                    st.warning(f"お気に入りファイルの破損した行をスキップしました: {line.strip()} - エラー: {e}")
        return favorites
    except IOError as e:
        return [f"ファイルの読み込み中にエラーが発生しました: {e}"]
