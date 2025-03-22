from typing import Dict, List, Tuple, Any
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import BaseMessage
from .game_engine import GameEngine
from .character import Character
from .scenario import Scenario

class GameFlow:
    def __init__(self):
        self.game_engine = GameEngine()
        self.state = {}

    async def run_game(self, initial_state: Dict) -> Dict:
        """ゲームを実行します"""
        self.state = await self._initialize_game(initial_state)
        
        while True:
            self.state = await self._process_player_action(self.state)
            self.state = await self._handle_skill_check(self.state)
            self.state = await self._update_game_state(self.state)
            state, should_end = await self._check_game_end(self.state)
            self.state = state
            
            if should_end:
                break
                
        return self.state

    async def _initialize_game(self, state: Dict) -> Dict:
        """ゲームの初期化を行います"""
        scenario_name = state.get("scenario_name", "default_scenario")
        players = state.get("players", {})

        # シナリオの読み込み
        scenario = Scenario(scenario_name)
        
        # ゲーム状態の初期化
        game_state = {
            "scenario": scenario,
            "players": players,
            "current_scene": "introduction",
            "messages": []
        }

        # 導入部分の生成
        intro_message = self.game_engine.initialize_game(scenario_name)
        game_state["messages"].append({
            "role": "keeper",
            "content": intro_message
        })

        return game_state

    async def _process_player_action(self, state: Dict) -> Dict:
        """プレイヤーのアクションを処理します"""
        current_player = state.get("current_player")
        action = state.get("current_action")

        if not current_player or not action:
            return state

        # アクションの処理
        response = self.game_engine.process_player_action(current_player, action)
        
        # 結果の保存
        state["messages"].append({
            "role": "player",
            "content": action
        })
        state["messages"].append({
            "role": "keeper",
            "content": response
        })

        return state

    async def _handle_skill_check(self, state: Dict) -> Dict:
        """スキルチェックを処理します"""
        if "skill_check" not in state:
            return state

        player_id = state.get("current_player")
        skill_check = state["skill_check"]
        
        if not player_id:
            return state

        result = self.game_engine.perform_skill_check(
            player_id,
            skill_check["skill"],
            skill_check.get("difficulty", "normal")
        )

        state["skill_check_result"] = result
        state["messages"].append({
            "role": "system",
            "content": f"スキルチェック結果: {result['message']}"
        })

        return state

    async def _update_game_state(self, state: Dict) -> Dict:
        """ゲーム状態を更新します"""
        # SAN値の更新
        if "san_change" in state:
            player_id = state.get("current_player")
            if player_id:
                san_result = self.game_engine.update_sanity(player_id, state["san_change"])
                state["messages"].append({
                    "role": "system",
                    "content": san_result["message"]
                })

        # シナリオの状態更新
        scenario = state.get("scenario")
        if scenario:
            if "discovered_clue" in state:
                scenario.discover_clue(
                    state.get("current_location", ""),
                    state["discovered_clue"]
                )

            if "triggered_event" in state:
                event_result = scenario.trigger_event(state["triggered_event"])
                if event_result:
                    state["messages"].append({
                        "role": "keeper",
                        "content": event_result["description"]
                    })

        return state

    async def _check_game_end(self, state: Dict) -> Tuple[Dict, bool]:
        """ゲーム終了条件をチェックします"""
        scenario = state.get("scenario")
        if not scenario:
            return state, False

        is_complete = scenario.check_completion()
        
        if is_complete:
            state["messages"].append({
                "role": "keeper",
                "content": "シナリオが完了しました。"
            })
            return state, True

        # 全プレイヤーの正気度チェック
        players = state.get("players", {})
        if players:
            all_insane = all(
                player.get("san", 1) <= 0
                for player in players.values()
            )

            if all_insane:
                state["messages"].append({
                    "role": "keeper",
                    "content": "全ての探索者が正気を失いました。ゲームオーバーです。"
                })
                return state, True

        return state, False 