import asyncio
import os
from dotenv import load_dotenv
from src.game_flow import GameFlow
from src.character import Character

async def main():
    # 環境変数の読み込み
    load_dotenv()
    
    print("クトゥルフ神話TRPGへようこそ！")
    print("=========================")
    
    # キャラクター作成
    print("\nキャラクター作成を開始します...")
    name = input("探索者の名前を入力してください: ")
    occupation = input("職業を入力してください: ")
    age = int(input("年齢を入力してください（15-90）: "))
    
    character = Character(name, occupation, age)
    print("\n作成されたキャラクター情報:")
    print(f"名前: {character.name}")
    print(f"職業: {character.occupation}")
    print(f"年齢: {character.age}")
    print("\n能力値:")
    for attr, value in character.characteristics.__dict__.items():
        print(f"{attr}: {value}")
    
    # ゲームフローの初期化
    game_flow = GameFlow()
    
    # 初期状態の設定
    initial_state = {
        "scenario_name": "haunted_mansion",
        "players": {
            "player1": character.to_dict()
        },
        "current_player": "player1",
        "current_action": "洋館の正門に到着する"
    }
    
    print("\nゲームを開始します...")
    print("=========================")
    
    # ゲームの実行
    try:
        state = await game_flow.run_game(initial_state)
        
        # メインのゲームループ
        while True:
            # メッセージの表示
            for message in state.get("messages", []):
                if message["role"] == "keeper":
                    print("\nキーパー:", message["content"])
                elif message["role"] == "player":
                    print("\nあなた:", message["content"])
                elif message["role"] == "system":
                    print("\nシステム:", message["content"])
            
            # プレイヤーの行動入力
            print("\n何をしますか？")
            action = input("> ")
            
            if action.lower() in ["quit", "終了"]:
                break
            
            # 状態の更新
            state["current_action"] = action
            state = await game_flow.run_game(state)
            
            # ゲーム終了判定
            if state.get("game_over"):
                print("\nゲームが終了しました。")
                break
    
    except Exception as e:
        print(f"\nエラーが発生しました: {e}")
    
    print("\nゲームを終了します。お疲れ様でした！")

if __name__ == "__main__":
    asyncio.run(main()) 