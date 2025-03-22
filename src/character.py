from typing import Dict, Optional
import random
from dataclasses import dataclass, field

@dataclass
class Characteristics:
    STR: int = field(default_factory=lambda: sum(random.randint(1, 6) for _ in range(3)) * 5)
    CON: int = field(default_factory=lambda: sum(random.randint(1, 6) for _ in range(3)) * 5)
    SIZ: int = field(default_factory=lambda: (sum(random.randint(1, 6) for _ in range(2)) + 6) * 5)
    DEX: int = field(default_factory=lambda: sum(random.randint(1, 6) for _ in range(3)) * 5)
    APP: int = field(default_factory=lambda: sum(random.randint(1, 6) for _ in range(3)) * 5)
    INT: int = field(default_factory=lambda: (sum(random.randint(1, 6) for _ in range(2)) + 6) * 5)
    POW: int = field(default_factory=lambda: sum(random.randint(1, 6) for _ in range(3)) * 5)
    EDU: int = field(default_factory=lambda: (sum(random.randint(1, 6) for _ in range(2)) + 6) * 5)

class Character:
    def __init__(self, name: str, occupation: str, age: int):
        self.name = name
        self.occupation = occupation
        self.age = age
        self.characteristics = Characteristics()
        self.skills: Dict[str, int] = self._initialize_skills()
        self.derived_attributes = self._calculate_derived_attributes()
        self.inventory: list = []
        self.background: str = ""
        self.mythos_knowledge: int = 0

    def _initialize_skills(self) -> Dict[str, int]:
        """基本的なスキル値を初期化します"""
        return {
            "回避": self.characteristics.DEX * 2,
            "言いくるめ": self.characteristics.APP * 2,
            "応急手当": 30,
            "聞き耳": 20,
            "図書館": self.characteristics.EDU * 2,
            "目星": 25,
            "母国語": self.characteristics.EDU * 5,
            # 他のスキルも同様に初期化
        }

    def _calculate_derived_attributes(self) -> Dict[str, int]:
        """能力値から導出される属性を計算します"""
        return {
            "HP": (self.characteristics.CON + self.characteristics.SIZ) // 10,
            "MP": self.characteristics.POW // 5,
            "SAN": self.characteristics.POW,
            "幸運": sum(random.randint(1, 6) for _ in range(3)) * 5,
            "アイデア": self.characteristics.INT * 5,
            "知識": self.characteristics.EDU * 5
        }

    def modify_skill(self, skill_name: str, new_value: int) -> bool:
        """スキル値を修正します"""
        if skill_name in self.skills:
            self.skills[skill_name] = new_value
            return True
        return False

    def check_skill(self, skill_name: str, difficulty: str = "normal") -> Dict:
        """スキルチェックを実行します"""
        if skill_name not in self.skills:
            return {"success": False, "message": "スキルが見つかりません"}

        skill_value = self.skills[skill_name]
        roll = random.randint(1, 100)

        if difficulty == "hard":
            skill_value //= 2
        elif difficulty == "extreme":
            skill_value //= 5

        result = {
            "roll": roll,
            "skill_value": skill_value,
            "success": roll <= skill_value,
            "critical": roll <= skill_value // 5,
            "fumble": roll > 95
        }

        return result

    def modify_san(self, amount: int) -> Dict:
        """正気度を変更します"""
        current_san = self.derived_attributes["SAN"]
        new_san = max(0, current_san + amount)
        self.derived_attributes["SAN"] = new_san

        if new_san <= 0:
            return {"success": True, "message": "正気度が0になりました", "madness": True}
        return {"success": True, "message": f"正気度が{abs(amount)}点{'減少' if amount < 0 else '回復'}しました"}

    def to_dict(self) -> Dict:
        """キャラクター情報を辞書形式で返します"""
        return {
            "name": self.name,
            "occupation": self.occupation,
            "age": self.age,
            "characteristics": self.characteristics.__dict__,
            "skills": self.skills,
            "derived_attributes": self.derived_attributes,
            "inventory": self.inventory,
            "background": self.background,
            "mythos_knowledge": self.mythos_knowledge
        } 