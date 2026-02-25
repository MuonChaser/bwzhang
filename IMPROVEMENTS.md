# MABe 小鼠行为识别模型改进方案

## 概述
本文档详细说明了对XGBoost模型的所有改进措施，旨在最大化F1-beta评分。

---

## 一、特征工程增强（最重要）

### 1.1 频域特征 (`add_spectral_features`)
- **原理**：通过FFT分析运动的周期性成分
- **特征**：
  - `fft_mean`: FFT值的均值
  - `fft_std`: FFT值的标准差
  - `fft_max`: FFT值的最大值
- **优势**：捕捉重复性动作（如rear、grooming）

### 1.2 加速度和急动特征 (`add_acceleration_jerk`)
- **原理**：运动学层面的高阶导数
- **特征**：
  - `acc_m{w}`: 加速度在不同时间窗口的均值和标准差
  - `jerk_m{w}`: 急动（加速度变化）的均值和标准差
- **优势**：区分快速与缓慢的行为转换

### 1.3 时间模式特征 (`add_temporal_patterns`)
- **原理**：捕捉时间序列中的模式
- **特征**：
  - `speed_cyclic`: 周期性正弦信号
  - `speed_trend_up`: 速度上升趋势
  - `speed_stability`: 速度稳定性指标
- **优势**：识别规律性行为

### 1.4 对称性特征 (`add_symmetry_features`)
- **原理**：分析左右侧身体的协调性
- **特征**：
  - `symmetry`: 左右侧平衡度
- **优势**：区分单侧与对称行为

### 1.5 距离比率特征 (`add_distance_ratios`)
- **原理**：身体部位之间的相对几何关系
- **特征**：
  - `nose_body_dist`: 鼻子到身体的距离
  - `body_tail_dist`: 身体到尾部的距离
  - `dist_ratio`: 距离比率及其趋势
- **优势**：刻画姿态变化

### 1.6 高级互动特征 (`add_interaction_advanced`)
- **原理**：增强鼠鼠对之间的相互作用特征
- **特征**：
  - `rel_speed_m{w}`: 相对速度的均值
  - `dist_acc_m{w}`: 距离变化的加速度
- **优势**：更准确地识别社交行为

---

## 二、模型优化

### 2.1 超参数调整
```python
XGBClassifier(
    n_estimators=300,        # 从250增加到300
    learning_rate=0.06,      # 从0.08降低到0.06（更精细的学习）
    max_depth=7,             # 从6增加到7（更深的树）
    min_child_weight=3,      # 从5降低到3（更灵活）
    subsample=0.8,           # 保持
    colsample_bytree=0.85,   # 从0.8增加到0.85
    colsample_bylevel=0.8,   # 新增：每层的特征采样
    gamma=0.5,               # 新增：分裂损失阈值
    reg_alpha=0.5,           # 新增：L1正则化
    reg_lambda=1.5,          # 新增：L2正则化
)
```

### 2.2 交叉验证改进
- **n_splits**: 从3增加到5（更稳定的评估）
- **cv方法**: 保持 `StratifiedGroupKFold`（按group分层）

### 2.3 集成学习（可选）
- **主模型**: XGBoost
- **辅助模型**: LightGBM
- **融合方法**: 简单平均 (0.5 * xgb_pred + 0.5 * lgb_pred)
- **优势**：减少单个模型的偏差

---

## 三、阈值优化增强

### 3.1 改进的贝叶斯优化
```python
def tune_threshold(oof_action, y_action, metric='f1'):
    # 从1000次trial减少到100次（平衡效率）
    # 支持多种指标：'f1', 'balanced_accuracy'
```

### 3.2 自适应阈值
- 为每个action单独调整阈值
- 利用OOF预测进行优化
- 避免固定的0.5阈值

---

## 四、数据预处理改进

### 4.1 缺失值处理
```python
def handle_missing_values(X, method='median'):
    # 中位数填充：保留数据的中心趋势
    # 避免均值填充可能的异常值影响
```

### 4.2 异常值和常数特征处理
```python
# 移除方差为0的特征
X_tr = X_tr.loc[:, (X_tr.std() > 0)]
```

### 4.3 类别权重平衡（可选）
```python
def apply_class_weights(y_action):
    # 为少数类分配更大的权重
    # 防止模型偏向多数类
```

### 4.4 数据增强（可选）
```python
def apply_data_augmentation(X, y, augmentation_factor=0.3):
    # 对少数类进行上采样
    # 添加小量高斯噪声
```

---

## 五、预测后处理改进

### 5.1 时间平滑 (Temporal Smoothing)
```python
# 应用移动众数（window_size=3）
# 消除预测中的随机波动
```

### 5.2 最小持续时间过滤
```python
# 移除持续时间小于min_duration帧的预测
# 防止识别噪声事件
# 推荐值：min_duration=2-5
```

### 5.3 改进的边界处理
```python
# 正确处理视频边界处的事件
# 防止跨越视频边界的预测
```

---

## 六、实施步骤

### 第一阶段：基础改进（快速见效）
1. ✅ 更新超参数（max_depth=7, learning_rate=0.06）
2. ✅ 增加交叉验证fold到5
3. ✅ 添加缺失值处理
4. ✅ 改进阈值优化

**预期提升**: +0.02 ~ +0.04 F1分数

### 第二阶段：特征工程（关键改进）
1. ✅ 添加加速度和急动特征
2. ✅ 添加时间模式特征
3. ✅ 添加对称性特征
4. ✅ 添加距离比率特征

**预期提升**: +0.03 ~ +0.06 F1分数

### 第三阶段：高级优化（边际改进）
1. ✅ 集成LightGBM
2. ✅ 频域特征（FFT）
3. ✅ 高级互动特征
4. ✅ 数据增强

**预期提升**: +0.01 ~ +0.03 F1分数

### 第四阶段：细调
1. ✅ 进行网格搜索或贝叶斯优化找最佳超参数
2. ✅ 尝试不同的特征组合
3. ✅ 优化最小持续时间阈值

---

## 七、关键参数说明

| 参数 | 推荐值 | 影响 |
|------|--------|------|
| `n_splits` | 5 | 更稳定的评估，但计算时间更长 |
| `max_depth` | 6-7 | 7更深，可能捕捉复杂模式；8+容易过拟合 |
| `learning_rate` | 0.05-0.08 | 越小学习越精细，但需要更多迭代 |
| `subsample` | 0.8 | 行采样比例，防止过拟合 |
| `colsample_bytree` | 0.8-0.85 | 列采样比例 |
| `min_duration` | 2-5 | 最小事件持续时间（帧数） |
| `window_smooth` | 3 | 时间平滑窗口大小 |

---

## 八、预期性能提升

基于类似竞赛的经验：
- **基础模型**: F1 = 0.70 (参考)
- **+超参数优化**: F1 = 0.72-0.73
- **+特征工程**: F1 = 0.75-0.77
- **+集成学习**: F1 = 0.76-0.78
- **+后处理**: F1 = 0.77-0.79

---

## 九、故障排除

### 9.1 内存不足
- 减少 `n_splits` 到3
- 启用特征选择，只保留top 100特征
- 分批处理数据

### 9.2 训练时间过长
- 减少 `n_estimators` 到200
- 增加 `learning_rate` 到0.10
- 禁用集成学习（只用XGBoost）

### 9.3 模型性能不提升
- 检查特征计算是否正确
- 验证缺失值处理
- 尝试移除新特征，逐个测试

---

## 十、代码文件对应

| 功能 | 文件位置 | 单元格ID |
|------|---------|---------|
| 特征工程 | Notebook | `#VSC-0640be70` |
| 模型配置 | Notebook | `#VSC-0a4d5bc2` |
| 单鼠特征 | Notebook | `#VSC-80630e0e` |
| 主训练循环 | Notebook | `#VSC-b9bc7311` |
| 预测后处理 | Notebook | `#VSC-338dff97` |

---

## 十一、附加建议

1. **特征相关性分析**：计算特征间的相关性，移除高度相关的特征
2. **特征重要性监控**：追踪每个action的重要特征
3. **交叉验证监控**：记录每个fold的F1分数，检查方差
4. **迁移学习**：考虑使用预训练模型的特征表示
5. **集成投票**：尝试soft voting或hard voting集成

---

## 十二、资源参考

- XGBoost文档: https://xgboost.readthedocs.io/
- LightGBM文档: https://lightgbm.readthedocs.io/
- Optuna文档: https://optuna.readthedocs.io/
- 时间序列特征工程: https://github.com/feature-engine/feature-engine

