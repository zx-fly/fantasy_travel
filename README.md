# Fantasy Travel

面向 Minecraft Java 26.2 的模块化数据包项目。当前版本为 `0.1.0`，只包含开发骨架，不包含完整玩法。

## 项目布局

数据包根目录为 `main/fantasy_travel/`，可选资源包位于 `optional/fantasy_travel_resources/`。

所有自定义资源统一使用 `fantasy_travel` 命名空间：

```text
data/fantasy_travel/
├─ function/
│  ├─ core/          生命周期、分频调度、迁移和玩家初始化
│  ├─ combat/        战斗系统
│  ├─ trade/         交易系统
│  ├─ achievement/   成就同步与奖励
│  ├─ world/         地形、建筑、生物刷新、天气与气候
│  ├─ event/         通常事件和特殊事件
│  ├─ admin/         管理与调试入口
│  └─ util/          无业务依赖的通用工具
├─ tags/function/    模块加载和 fast/normal/slow/maintenance 调度
├─ advancement/      内部触发器与玩家可见成就
├─ predicate/        可复用条件
├─ loot_table/       战斗、交易和事件奖励
├─ recipe/           玩法配方
├─ item_modifier/    物品状态修改
├─ damage_type/      自定义伤害类型
├─ enchantment/      自定义附魔
├─ dialog/           对话定义
├─ structure/        NBT 建筑模板
├─ tags/             方块、物品、实体等资源标签
├─ dimension/        自定义维度
├─ dimension_type/   自定义维度类型
└─ worldgen/         原生新区块生成配置
```

尚未使用的资源目录不提前创建，在对应功能落地时再加入。

## 生命周期

- `#minecraft:load` → `fantasy_travel:core/load`
- `#minecraft:tick` → `fantasy_travel:core/tick`
- `#fantasy_travel:load`：模块幂等初始化
- `#fantasy_travel:tick/fast`：每 tick，仅允许处理已登记的活跃对象
- `#fantasy_travel:tick/normal`：每 5 tick
- `#fantasy_travel:tick/slow`：每 20 tick
- `#fantasy_travel:tick/maintenance`：每 100 tick

攻击、交互和成就优先使用 advancement reward 触发。阶段式事件使用 `schedule function` 推进，禁止通过每 tick 全量扫描维持。

## 状态约定

- 高频玩家数字：`scoreboard`，目标名称以 `ft.` 开头
- 玩家布尔状态：`tag` 或 advancement
- 全局配置、事件和队列：`storage fantasy_travel:runtime`
- storage 结构版本：`meta.schema_version`
- 数据包版本：`meta.pack_version`

模块初始化必须可重复执行。存档升级通过 `function/core/migrate/` 中的有序、幂等迁移完成，不允许在普通 `/reload` 时清空玩家数据。

## 模块边界

模块只暴露 `init`、`start`、`stop`、`trigger` 等稳定入口。跨模块代码只能调用这些入口或公开函数标签，不得依赖其他模块的内部函数路径。

通常事件和特殊事件统一使用以下状态：

```text
idle -> prepare -> active -> cleanup -> cooldown
```

原生世界生成与运行时改造相互独立：

- `worldgen/` 只影响新生成区块。
- `function/world/` 使用队列和固定预算进行运行时建筑或地形改造。

## 新增模块

1. 在 `function/<module>/init.mcfunction` 创建幂等入口。
2. 将入口注册到 `tags/function/load.json`。
3. 仅在确有周期任务时加入对应频率标签。
4. 将玩家可见内容、条件和奖励分别放入 advancement、predicate、loot_table 等资源目录。
5. 在 `storage fantasy_travel:runtime modules` 中增加默认开关。

## 可选资源包

资源包使用同一个 `fantasy_travel` 命名空间，负责纹理、物品模型、翻译、声音和字体。数据包必须在未安装资源包时仍可游玩，并为所有自定义表现提供原版回退。

## 验证

提交前先运行静态检查：

```text
python tools/validate_pack.py
```

将 `main/fantasy_travel/` 放入测试世界的 `datapacks/` 后执行：

```text
/reload
/datapack list
/function fantasy_travel:core/load
```

目标版本：

- 数据包格式：`107.1`
- 可选资源包格式：`88.0`
