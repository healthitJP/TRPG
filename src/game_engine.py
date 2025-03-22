from typing import Dict, List, Optional
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from config.config import config

class GameEngine:
    def __init__(self):
        self.llm = ChatOpenAI(
            model_name=config.model_name,
            temperature=config.temperature,
            openai_api_key=config.openai_api_key
        )
        self.game_state = {
            "players": {},
            "current_scene": None,
            "clues_discovered": [],
            "sanity_events": []
        }
        self.conversation_history: List[Dict] = []

    def initialize_game(self, scenario_name: str) -> str:
        """ゲームの初期化を行います"""
        system_prompt = self._load_keeper_prompt()
        scenario_details = self._load_scenario(scenario_name)
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"シナリオ「{scenario_name}」を開始します。導入部分を説明してください。")
        ]
        
        response = self.llm.invoke(messages)
        self.conversation_history.extend([{"role": "system", "content": system_prompt},
                                       {"role": "assistant", "content": response.content}])
        return response.content

    def process_player_action(self, player_id: str, action: str) -> str:
        """プレイヤーのアクションを処理します"""
        messages = self._build_conversation_context()
        messages.append(HumanMessage(content=f"プレイヤー{player_id}のアクション: {action}"))
        
        response = self.llm.invoke(messages)
        self.conversation_history.append({"role": "human", "content": action})
        self.conversation_history.append({"role": "assistant", "content": response.content})
        
        return response.content

    def perform_skill_check(self, player_id: str, skill: str, difficulty: str = "normal") -> Dict:
        """スキルチェックを実行します"""
        player = self.game_state["players"].get(player_id)
        if not player:
            return {"success": False, "message": "プレイヤーが見つかりません"}
        
        skill_value = player.get("skills", {}).get(skill, 0)
        # スキルチェックのロジックを実装
        return {"success": True, "result": "スキルチェック結果"}

    def update_sanity(self, player_id: str, san_loss: int) -> Dict:
        """正気度の更新を行います"""
        player = self.game_state["players"].get(player_id)
        if not player:
            return {"success": False, "message": "プレイヤーが見つかりません"}
        
        current_san = player.get("san", 0)
        new_san = max(0, current_san - san_loss)
        player["san"] = new_san
        
        if new_san <= 0:
            return {"success": True, "message": "正気度が0になりました", "madness": True}
        return {"success": True, "message": f"正気度が{san_loss}点減少しました"}

    def _load_keeper_prompt(self) -> str:
        """キーパー（GM）のプロンプトを読み込みます"""
        return """あなたはクトゥルフ神話TRPGのキーパー（ゲームマスター）です。
        プレイヤーの行動に対して適切な描写と結果を提供し、
        ゲームの進行を管理してください。
        ホラーと探索の要素のバランスを保ちながら、
        プレイヤーの自由な発想を尊重してください。"""

    def _load_scenario(self, scenario_name: str) -> Dict:
        """シナリオデータを読み込みます"""
        # シナリオデータの読み込みロジックを実装
        return {"name": scenario_name, "details": "シナリオの詳細"}

    def _build_conversation_context(self) -> List:
        """会話コンテキストを構築します"""
        messages = []
        for msg in self.conversation_history[-5:]:  # 直近5つのメッセージのみ使用
            if msg["role"] == "system":
                messages.append(SystemMessage(content=msg["content"]))
            elif msg["role"] == "human":
                messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                messages.append(AIMessage(content=msg["content"]))
        return messages 