# TRPGキーパー用関数定義

## ゲーム進行関連

### initializeGame()
- 引数: なし
- 返り値: GameState
- 説明: ゲームの初期状態を設定する。シナリオ、NPCデータ、環境などを初期化

### updateGameState(currentState: GameState, action: Action)
- 引数: 現在のゲーム状態、プレイヤーのアクション
- 返り値: 更新されたGameState
- 説明: プレイヤーのアクションに応じてゲーム状態を更新

### describeScene(scene: Scene)
- 引数: 現在のシーン情報
- 返り値: string
- 説明: 現在のシーンを自然言語で描写

## キャラクター関連

### rollCharacteristic(characteristic: string)
- 引数: 能力値の種類(STR,CON,DEX等)
- 返り値: number
- 説明: 指定された能力値のダイスロールを行う

### calculateDerivedStats(characteristics: CharacterStats)
- 引数: 基本能力値セット
- 返り値: DerivedStats
- 説明: HP,MP,SANなどの派生能力値を計算

### rollSkill(skill: string, difficulty: string)
- 引数: 技能名、難易度(Regular/Hard/Extreme)
- 返り値: {success: boolean, degree: string}
- 説明: 技能判定を行い、成功/失敗と成功度を返す

## 戦闘関連

### initiateCombat(participants: Character[])
- 引数: 戦闘参加者リスト
- 返り値: CombatState
- 説明: 戦闘の初期状態を設定

### resolveCombatRound(state: CombatState)
- 引数: 現在の戦闘状態
- 返り値: 更新されたCombatState
- 説明: 1ラウンドの戦闘を解決

### calculateDamage(attack: Attack, target: Character)
- 引数: 攻撃情報、対象キャラクター
- 返り値: number
- 説明: ダメージを計算

## 正気度関連

### checkSanity(character: Character, horror: Horror)
- 引数: キャラクター、遭遇した恐怖
- 返り値: {sanLoss: number, effect: string}
- 説明: 正気度チェックを行い、正気度喪失と効果を返す

### applyTemporaryInsanity(character: Character)
- 引数: キャラクター
- 返り値: string
- 説明: 一時的狂気の効果を適用

### applyIndefiniteInsanity(character: Character)
- 引数: キャラクター
- 返り値: string
- 説明: 不定の狂気の効果を適用

## 魔術関連

### castSpell(spell: Spell, caster: Character)
- 引数: 呪文情報、詠唱者
- 返り値: {success: boolean, effect: string, cost: {mp: number, san: number}}
- 説明: 呪文の詠唱を解決

### readMythosBook(book: MythosBook, reader: Character)
- 引数: 神話書籍情報、読者
- 返り値: {sanLoss: number, mythosPoints: number, spells: Spell[]}
- 説明: 神話書籍の読書による効果を解決

## シナリオ管理

### provideClue(scene: Scene, investigator: Character)
- 引数: 現在のシーン、探索者
- 返り値: string
- 説明: シーンに応じた手がかりを提供

### triggerEvent(scene: Scene, trigger: string)
- 引数: 現在のシーン、トリガー条件
- 返り値: Event
- 説明: イベントの発生を管理

### manageNPCReaction(npc: NPC, action: Action)
- 引数: NPC情報、プレイヤーのアクション
- 返り値: {reaction: string, action: Action}
- 説明: NPCの反応を決定

## チェイス関連

### initiateChase(participants: Character[])
- 引数: チェイス参加者リスト
- 返り値: ChaseState
- 説明: チェイスの初期状態を設定

### resolveChaseRound(state: ChaseState)
- 引数: 現在のチェイス状態
- 返り値: 更新されたChaseState
- 説明: 1ラウンドのチェイスを解決

### handleChaseObstacle(character: Character, obstacle: Obstacle)
- 引数: キャラクター、障害物情報
- 返り値: {success: boolean, effect: string}
- 説明: チェイス中の障害物への対応を解決 