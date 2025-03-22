from typing import Dict, List, Optional
from pathlib import Path
import yaml
from dataclasses import dataclass
from config.config import config

@dataclass
class Location:
    name: str
    description: str
    clues: List[str]
    events: List[Dict]
    npcs: List[str]

@dataclass
class NPC:
    name: str
    description: str
    motivation: str
    stats: Optional[Dict] = None
    dialogue: Optional[Dict] = None

@dataclass
class Event:
    name: str
    description: str
    triggers: List[str]
    consequences: List[str]
    san_loss: Optional[int] = None

class Scenario:
    def __init__(self, scenario_name: str):
        self.name = scenario_name
        self.data = self._load_scenario_data()
        self.locations: Dict[str, Location] = self._initialize_locations()
        self.npcs: Dict[str, NPC] = self._initialize_npcs()
        self.events: Dict[str, Event] = self._initialize_events()
        self.current_state = {
            "discovered_clues": set(),
            "triggered_events": set(),
            "completed_objectives": set()
        }

    def _load_scenario_data(self) -> Dict:
        """シナリオデータをYAMLファイルから読み込みます"""
        scenario_path = Path(__file__).parent.parent / "data" / "scenarios" / f"{self.name}.yaml"
        try:
            with open(scenario_path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            raise ValueError(f"シナリオ '{self.name}' が見つかりません")

    def _initialize_locations(self) -> Dict[str, Location]:
        """場所データを初期化します"""
        locations = {}
        for loc_data in self.data.get("locations", []):
            locations[loc_data["name"]] = Location(
                name=loc_data["name"],
                description=loc_data["description"],
                clues=loc_data.get("clues", []),
                events=loc_data.get("events", []),
                npcs=loc_data.get("npcs", [])
            )
        return locations

    def _initialize_npcs(self) -> Dict[str, NPC]:
        """NPCデータを初期化します"""
        npcs = {}
        for npc_data in self.data.get("npcs", []):
            npcs[npc_data["name"]] = NPC(
                name=npc_data["name"],
                description=npc_data["description"],
                motivation=npc_data["motivation"],
                stats=npc_data.get("stats"),
                dialogue=npc_data.get("dialogue")
            )
        return npcs

    def _initialize_events(self) -> Dict[str, Event]:
        """イベントデータを初期化します"""
        events = {}
        for event_data in self.data.get("events", []):
            events[event_data["name"]] = Event(
                name=event_data["name"],
                description=event_data["description"],
                triggers=event_data["triggers"],
                consequences=event_data["consequences"],
                san_loss=event_data.get("san_loss")
            )
        return events

    def get_location_description(self, location_name: str) -> Optional[str]:
        """指定された場所の説明を取得します"""
        location = self.locations.get(location_name)
        return location.description if location else None

    def discover_clue(self, location_name: str, clue_index: int) -> Optional[str]:
        """手がかりを発見します"""
        location = self.locations.get(location_name)
        if not location or clue_index >= len(location.clues):
            return None
        
        clue = location.clues[clue_index]
        self.current_state["discovered_clues"].add(clue)
        return clue

    def trigger_event(self, event_name: str) -> Optional[Dict]:
        """イベントを発生させます"""
        event = self.events.get(event_name)
        if not event:
            return None

        self.current_state["triggered_events"].add(event_name)
        return {
            "description": event.description,
            "consequences": event.consequences,
            "san_loss": event.san_loss
        }

    def get_npc_dialogue(self, npc_name: str, topic: str) -> Optional[str]:
        """NPCの会話内容を取得します"""
        npc = self.npcs.get(npc_name)
        if not npc or not npc.dialogue:
            return None
        return npc.dialogue.get(topic, "その話題については何も知りません。")

    def check_completion(self) -> bool:
        """シナリオの完了条件を確認します"""
        required_objectives = set(self.data.get("completion_objectives", []))
        return required_objectives.issubset(self.current_state["completed_objectives"])

    def get_current_state(self) -> Dict:
        """現在のシナリオ状態を取得します"""
        return {
            "discovered_clues": list(self.current_state["discovered_clues"]),
            "triggered_events": list(self.current_state["triggered_events"]),
            "completed_objectives": list(self.current_state["completed_objectives"]),
            "completion_status": self.check_completion()
        } 