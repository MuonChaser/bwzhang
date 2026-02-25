# XGBoost 小鼠行为识别 - 超参数配置文件

## 配置说明
此文件包含针对不同场景的超参数预设
选择适合您的需求的配置

---

## 配置1: 速度优先 (快速迭代)
用于快速实验和调试

```python
class CFG_FAST:
    n_splits = 3
    
    model = XGBClassifier(
        verbosity=0,
        random_state=42,
        n_estimators=100,
        learning_rate=0.15,
        max_depth=5,
        min_child_weight=5,
        subsample=0.8,
        colsample_bytree=0.8,
        gamma=0,
        reg_alpha=0,
        reg_lambda=0,
    )
    
    # 推荐时间: 1-2小时
    # 预期F1: 0.70-0.72
```

---

## 配置2: 平衡型 (推荐) ⭐
平衡速度和精度，最稳定

```python
class CFG_BALANCED:
    n_splits = 4
    
    model = XGBClassifier(
        verbosity=0,
        random_state=42,
        n_estimators=250,
        learning_rate=0.08,
        max_depth=6,
        min_child_weight=4,
        subsample=0.8,
        colsample_bytree=0.82,
        gamma=0.3,
        reg_alpha=0.2,
        reg_lambda=1.0,
    )
    
    # 推荐时间: 3-4小时
    # 预期F1: 0.74-0.76 (当前配置)
```

---

## 配置3: 精度优先 (高精度)
追求最高精度，计算时间较长

```python
class CFG_PRECISE:
    n_splits = 5
    
    model = XGBClassifier(
        verbosity=0,
        random_state=42,
        n_estimators=400,
        learning_rate=0.05,
        max_depth=7,
        min_child_weight=3,
        subsample=0.75,
        colsample_bytree=0.85,
        gamma=0.5,
        reg_alpha=0.5,
        reg_lambda=1.5,
    )
    
    # 推荐时间: 6-8小时
    # 预期F1: 0.76-0.78 (当前配置)
```

---

## 配置4: 防过拟合 (保守型)
防止模型过度拟合，泛化能力强

```python
class CFG_CONSERVATIVE:
    n_splits = 5
    
    model = XGBClassifier(
        verbosity=0,
        random_state=42,
        n_estimators=200,
        learning_rate=0.1,
        max_depth=5,
        min_child_weight=6,
        subsample=0.7,
        colsample_bytree=0.7,
        gamma=1.0,
        reg_alpha=1.0,
        reg_lambda=2.0,
    )
    
    # 推荐时间: 2-3小时
    # 预期F1: 0.72-0.74
```

---

## 配置5: 轻量级 (资源受限)
内存和计算资源有限时使用

```python
class CFG_LITE:
    n_splits = 3
    
    model = XGBClassifier(
        verbosity=0,
        random_state=42,
        n_estimators=80,
        learning_rate=0.2,
        max_depth=4,
        min_child_weight=10,
        subsample=0.6,
        colsample_bytree=0.6,
        gamma=0,
        reg_alpha=0,
        reg_lambda=0,
        tree_method='hist',  # 更节省内存
    )
    
    # 推荐时间: 30分钟-1小时
    # 预期F1: 0.68-0.70
    # 内存占用: <4GB
```

---

## 配置6: 集成型 (最大精度)
启用多个模型集成，精度最高但计算最重

```python
class CFG_ENSEMBLE:
    n_splits = 5
    use_ensemble = True
    
    # XGBoost 主模型
    model = XGBClassifier(
        verbosity=0,
        random_state=42,
        n_estimators=300,
        learning_rate=0.06,
        max_depth=7,
        min_child_weight=3,
        subsample=0.8,
        colsample_bytree=0.85,
        gamma=0.5,
        reg_alpha=0.5,
        reg_lambda=1.5,
    )
    
    # LightGBM 辅助模型
    lgb_model = LGBMClassifier(
        n_estimators=250,
        learning_rate=0.05,
        max_depth=6,
        num_leaves=31,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        verbose=-1
    )
    
    # CatBoost 备选模型
    catboost_model = CatBoostClassifier(
        iterations=250,
        learning_rate=0.05,
        max_depth=6,
        random_state=42,
        verbose=False,
    )
    
    # 推荐时间: 8-12小时
    # 预期F1: 0.77-0.80
```

---

## 参数详解

### Tree Parameters (树结构)
- `max_depth`: 树的最大深度
  - 5-6: 简单模型,防过拟合
  - 7-8: 标准模型,捕捉复杂性
  - 9+: 复杂模型,易过拟合

- `min_child_weight`: 叶子节点最小权重和
  - 3-5: 允许分裂,捕捉细节
  - 5-10: 保守,防过拟合
  - 10+: 非常保守

### Learning Parameters (学习速率)
- `learning_rate`: 学习速率 (eta)
  - 0.3+: 快速学习,易过拟合
  - 0.05-0.15: 常用范围
  - 0.01-0.05: 精细学习,需更多估计器

- `n_estimators`: 树的数量
  - 随learning_rate增加而减少
  - learning_rate=0.1时: 100-200棵
  - learning_rate=0.05时: 200-400棵

### Regularization (正则化)
- `subsample`: 行采样比例 (0-1)
  - 0.5-0.7: 强正则化,防过拟合
  - 0.8: 标准
  - 0.9-1.0: 弱正则化

- `colsample_bytree`: 树级别列采样 (0-1)
  - 0.5-0.7: 强正则化
  - 0.8: 标准
  - 0.9-1.0: 弱正则化

- `gamma`: 分裂所需最小损失减少
  - 0: 无限制
  - 0.5-1.0: 中等
  - 2.0+: 强正则化

- `reg_alpha`: L1正则化系数
  - 0-0.5: 弱L1
  - 0.5-1.0: 中等L1
  - 1.0+: 强L1

- `reg_lambda`: L2正则化系数
  - 0-1.0: 弱L2
  - 1.0-2.0: 中等L2
  - 2.0+: 强L2

---

## 选择指南

### 我应该选择哪个配置?

**场景1: 快速原型验证**
→ 使用 `CFG_FAST` 或 `CFG_LITE`

**场景2: 生产环境(平衡)**
→ 使用 `CFG_BALANCED` ⭐推荐

**场景3: 追求最高分数**
→ 使用 `CFG_PRECISE` 或 `CFG_ENSEMBLE`

**场景4: 防过拟合,提高泛化**
→ 使用 `CFG_CONSERVATIVE`

**场景5: 资源受限(笔记本电脑)**
→ 使用 `CFG_LITE`

---

## 应用方法

### 方法1: 替换CFG类
```python
# 原始:
class CFG:
    # ... 当前配置

# 改为:
from config import CFG_FAST  # 导入预设配置
class CFG(CFG_FAST):  # 继承
    pass
```

### 方法2: 混合配置
```python
# 合并多个配置的优点
class CFG:
    n_splits = 4
    
    model = XGBClassifier(
        n_estimators=250,       # 从BALANCED
        learning_rate=0.08,     # 从BALANCED
        max_depth=6,            # 从BALANCED
        min_child_weight=4,     # 从BALANCED
        subsample=0.75,         # 从CONSERVATIVE (更保守)
        colsample_bytree=0.8,   # 从BALANCED
        gamma=0.5,              # 从PRECISE (更强)
        reg_alpha=0.5,          # 从PRECISE
        reg_lambda=1.5,         # 从PRECISE
    )
```

### 方法3: 渐进式调整
```python
# 从简单到复杂
# 1. 使用 CFG_FAST 做基线
# 2. 升级到 CFG_BALANCED
# 3. 尝试 CFG_PRECISE
# 4. 最后考虑 CFG_ENSEMBLE
```

---

## 超参数网格搜索

如果想进行系统的超参数搜索:

```python
# 小搜索空间 (快速)
param_grid = {
    'max_depth': [5, 6, 7],
    'learning_rate': [0.05, 0.08, 0.1],
    'n_estimators': [200, 300],
}

# 中等搜索空间 (平衡)
param_grid = {
    'max_depth': [4, 5, 6, 7, 8],
    'learning_rate': [0.03, 0.05, 0.08, 0.1, 0.15],
    'min_child_weight': [1, 3, 5, 7],
    'subsample': [0.7, 0.8, 0.9],
}

# 大搜索空间 (全面)
param_grid = {
    'max_depth': [3, 4, 5, 6, 7, 8, 9],
    'learning_rate': [0.01, 0.03, 0.05, 0.08, 0.1, 0.15, 0.2],
    'min_child_weight': [1, 3, 5, 7, 10],
    'subsample': [0.6, 0.7, 0.8, 0.9],
    'colsample_bytree': [0.6, 0.7, 0.8, 0.9],
    'gamma': [0, 0.1, 0.5, 1.0, 2.0],
}
```

---

## 配置对比表

| 指标 | FAST | BALANCED | PRECISE | CONSERVATIVE | LITE | ENSEMBLE |
|-----|------|----------|---------|--------------|------|----------|
| 速度 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐ |
| 精度 | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| 泛化 | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| 内存 | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐ |
| 推荐场景 | 测试 | 生产⭐ | 竞赛 | 安全 | 受限 | 最优 |

---

## 后续优化步骤

### Step 1: 确定最佳配置 (1小时)
- [ ] 尝试BALANCED配置
- [ ] 验证F1分数提升

### Step 2: 微调超参数 (2-4小时)
- [ ] 调整max_depth
- [ ] 调整learning_rate
- [ ] 监控过拟合

### Step 3: 特征工程 (2-3小时)
- [ ] 启用所有特征模块
- [ ] 验证特征有效性

### Step 4: 集成优化 (2-3小时)
- [ ] 尝试ENSEMBLE配置
- [ ] 投票或平均预测

---

## 常见问题

**Q: 哪个配置能给我最高的F1分数?**
A: `CFG_ENSEMBLE`,但需要8-12小时。快速替代方案: `CFG_PRECISE` (6-8小时)

**Q: 哪个配置最稳定?**
A: `CFG_CONSERVATIVE` 和 `CFG_BALANCED` 都很稳定

**Q: 如何处理过拟合?**
A: 使用 `CFG_CONSERVATIVE` 或降低 `max_depth` 和 `subsample`

**Q: 如何加快训练速度?**
A: 使用 `CFG_FAST` 或 `CFG_LITE`,降低 `n_splits`

---

**最后更新**: 2024年11月
**版本**: 1.0
