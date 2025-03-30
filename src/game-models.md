 ```markdown
# TRPGキーパー用モデル定義

## ゲーム状態モデル

### GameState
```typescript
interface GameState {
  scenario: Scenario;
  currentScene: Scene;
  investigators: Character[];
  npcs: NPC[];
  environment: Environment;
  time: GameTime;
  flags: { [key: string]: boolean };
}
```

### Scene
```typescript
interface Scene {
  id: string;
  description: string;
  npcs: NPC[];
  clues: Clue[];
  events: Event[];
  obstacles: Obstacle[];
  connections: SceneConnection[];
}
```

## キャラクターモデル

### Character
```typescript
interface Character {
  // 基本情報
  id: string;
  name: string;
  occupation: string;
  age: number;
  
  // 能力値
  characteristics: {
    STR: number;  // 筋力
    CON: number;  // 体力
    SIZ: number;  // 体格
    DEX: number;  // 敏捷性
    APP: number;  // 外見
    INT: number;  // 知性
    POW: number;  // 精神力
    EDU: number;  // 教育
  };
  
  // 派生能力値
  derivedStats: {
    HP: number;   // 耐久力
    MP: number;   // マジックポイント
    SAN: number;  // 正気度
    LUCK: number; // 幸運
    DB: number;   // ダメージボーナス
    BUILD: number;// ビルド
    MOV: number;  // 移動力
  };
  
  // 技能
  skills: { [key: string]: number };
  
  // 状態
  status: {
    wounds: Wound[];
    temporaryInsanity: InsanityEffect | null;
    indefiniteInsanity: InsanityEffect | null;
    phobias: Phobia[];
    manias: Mania[];
  };
  
  // 所持品
  inventory: Item[];
  
  // バックストーリー
  background: {
    personalDescription: string;
    ideologyBeliefs: string;
    significantPeople: string[];
    meaningfulLocations: string[];
    treasuredPossessions: string[];
    traits: string[];
    injuries: string[];
    phobiasManias: string[];
    arcaneBooks: string[];
    encounters: string[];
    keyConnection: string;
  };
}
```

### NPC
```typescript
interface NPC extends Character {
  role: string;
  motivation: string;
  knowledge: { [key: string]: string };
  reactions: { [key: string]: string };
  schedule: Schedule[];
}
```

## 戦闘モデル

### CombatState
```typescript
interface CombatState {
  participants: CombatParticipant[];
  round: number;
  currentTurn: number;
  initiativeOrder: string[];
  activeEffects: Effect[];
}
```

### Attack
```typescript
interface Attack {
  type: "melee" | "ranged" | "spell";
  weapon: Weapon | null;
  skill: string;
  damage: string;
  special: string[];
}
```

## 正気度モデル

### Horror
```typescript
interface Horror {
  type: string;
  sanLoss: {
    success: string;   // "1/1D6"のような形式
    failure: string;   // "1D3/1D10"のような形式
  };
  description: string;
}
```

### InsanityEffect
```typescript
interface InsanityEffect {
  type: "temporary" | "indefinite";
  effect: string;
  duration: number;
  symptoms: string[];
}
```

## 魔術モデル

### Spell
```typescript
interface Spell {
  name: string;
  cost: {
    mp: number;
    san: number;
    other?: any;
  };
  castingTime: string;
  effect: string;
  duration: string;
}
```

### MythosBook
```typescript
interface MythosBook {
  title: string;
  author: string;
  language: string;
  studyTime: number;
  sanLoss: number;
  mythosPoints: number;
  spells: Spell[];
  content: string;
}
```

## シナリオモデル

### Scenario
```typescript
interface Scenario {
  title: string;
  introduction: string;
  scenes: Scene[];
  npcs: NPC[];
  clues: Clue[];
  events: Event[];
  horrors: Horror[];
  artifacts: Artifact[];
  endings: Ending[];
}
```

### Clue
```typescript
interface Clue {
  id: string;
  description: string;
  type: "obvious" | "hidden" | "obscure";
  requirements: {
    skills?: { [key: string]: number };
    items?: string[];
    flags?: { [key: string]: boolean };
  };
  reveals: string[];
}
```

## チェイスモデル

### ChaseState
```typescript
interface ChaseState {
  participants: ChaseParticipant[];
  round: number;
  locations: Location[];
  obstacles: Obstacle[];
  distances: { [key: string]: number };
}
```

### Obstacle
```typescript
interface Obstacle {
  type: string;
  difficulty: string;
  skill: string;
  consequences: {
    success: string;
    failure: string;
  };
  damage?: number;
}
```

## 共通型定義

### GameTime
```typescript
interface GameTime {
  year: number;
  month: number;
  day: number;
  hour: number;
  minute: number;
  era: string;
}
```

### Effect
```typescript
interface Effect {
  type: string;
  duration: number;
  modifiers: { [key: string]: number };
  description: string;
}
```

### Item
```typescript
interface Item {
  name: string;
  type: string;
  description: string;
  weight?: number;
  value?: number;
  effects?: Effect[];
}
```

### Weapon extends Item
```typescript
interface Weapon extends Item {
  damage: string;
  range?: string;
  attacks: number;
  ammo?: number;
  malfunction?: number;
}
```
```