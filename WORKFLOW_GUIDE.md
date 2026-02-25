# XGBoost 小鼠行为识别 - 完整工作流程指南

## 📋 执行流程

### ✅ 推荐工作流程

```
第1步: 设置为 VALIDATE 模式
  ↓
第2步: 运行完整的训练和验证
  ↓
第3步: 分析性能指标和F1分数
  ↓
第4步: 调整超参数和特征
  ↓
第5步: 重复第2-4步直到满意
  ↓
第6步: 设置为 SUBMIT 模式
  ↓
第7步: 运行完整训练（使用相同超参数）
  ↓
第8步: 生成提交文件
```

---

## 🔍 为什么要先使用 VALIDATE 模式？

### VALIDATE 模式的优势

| 优势 | 说明 |
|-----|------|
| **验证效果** | 在hold-out验证集上评估真实性能 |
| **调试快速** | 发现问题和优化空间 |
| **防止过拟合** | 识别模型是否过度拟合 |
| **参数优化** | 找到最优超参数组合 |
| **节省时间** | 避免直接生成不好的提交 |
| **可追溯** | 完整的F1分数和阈值记录 |

### SUBMIT 模式的特点

| 特点 | 说明 |
|-----|------|
| **全数据训练** | 使用所有训练数据，没有hold-out验证集 |
| **使用保存的模型** | 加载已训练的模型权重 |
| **无评估指标** | 没有验证集F1分数，只生成预测 |
| **最终提交** | 用于生成最终的Kaggle提交 |

---

## 📝 详细步骤说明

### 步骤1: 设置 VALIDATE 模式

**修改配置：**
```python
class CFG:
    # ... 其他配置 ...
    
    # mode = "validate"  # 如果已是此行，直接保持
    mode = "validate"
    
    n_splits = 5
    cv = StratifiedGroupKFold(n_splits)
```

**预期输出：**
- 每个action的F1分数
- 阈值.pkl文件
- 分数统计.pkl文件

### 步骤2: 运行验证（第一次执行）

**执行内容：**
```
1. 加载数据
2. 提取特征
3. 5折交叉验证训练
4. 生成验证预测 (OOF predictions)
5. 计算每个action的F1分数
6. 优化和保存阈值
7. 评估竞赛指标
```

**预期时间：** 4-8小时（取决于配置）

**监控指标：**
- 各fold的F1分数是否相近（方差小）
- 平均F1分数的水平
- 具体action分数的分布

### 步骤3: 分析性能

**检查清单：**
```python
# 查看打印输出中的信息：
✓ 各action的F1分数
✓ 平均F1分数
✓ 竞赛指标（competition metric）

# 预期结果示例：
Mean F1: 0.7523
Competition metric: 0.7445
```

**如果性能不满意？**

| 问题 | 解决方案 |
|-----|--------|
| F1分数太低 | 调整超参数、增加特征工程、启用集成 |
| 不同fold差异大 | 数据分布不均、增加fold数、检查数据质量 |
| 某些action F1很低 | 检查该action的样本数、数据不平衡、特征相关性 |
| 过拟合（训练集 >> 验证集） | 增加正则化、降低max_depth、减少特征 |

### 步骤4: 调整并重复

**可调整的参数：**

#### 快速调整（影响大）
- `max_depth`: 5 → 6 → 7
- `learning_rate`: 0.08 → 0.06 → 0.05
- `subsample`: 0.8 → 0.75 → 0.85
- `colsample_bytree`: 0.8 → 0.85 → 0.9

#### 特征调整（影响中等）
- 启用/禁用特定特征工程函数
- 调整时间窗口大小
- 添加新的交互特征

#### 模型调整（影响小但全面）
- 启用集成学习（LightGBM）
- 修改阈值优化方法
- 添加数据增强

**调整建议：**
```python
# 如果要在validate中进行快速迭代
class CFG:
    n_splits = 3  # 从5改为3以加快速度
    model = XGBClassifier(
        n_estimators=200,  # 从300改为200
        learning_rate=0.10,  # 从0.06改为0.10
        max_depth=6,        # 保持或调整
        # ... 其他参数
    )
```

### 步骤5: 确认最优配置

**验收标准：**
```
✓ 平均F1分数 >= 0.75（良好）
✓ 竞赛指标与F1分数相近（无异常）
✓ 各fold分数差异 < 0.05（稳定）
✓ 没有明显的过拟合或欠拟合
✓ 所有action都有合理的F1分数
```

### 步骤6: 切换到 SUBMIT 模式

**修改配置：**
```python
class CFG:
    # ... 其他配置保持不变 ...
    
    mode = "submit"  # 改为submit
    
    n_splits = 5  # 保持验证时的配置
    # 所有超参数保持不变！
```

### 步骤7: 运行提交

**执行内容：**
```
1. 加载保存的模型权重
2. 加载保存的阈值参数
3. 提取测试集特征
4. 生成测试预测
5. 应用阈值和后处理
6. 生成submission.csv
```

**输出文件：**
```
submission.csv
```

---

## 🚨 常见错误和解决方案

### 错误1: "找不到保存的模型文件"

**原因：** 没有运行VALIDATE模式，直接使用SUBMIT模式

**解决：**
1. 改回VALIDATE模式
2. 完整运行一次
3. 等待模型保存完成
4. 再改为SUBMIT模式

### 错误2: "验证阶段F1很低，还要提交吗？"

**判断标准：**
```
F1 >= 0.70 → 可以提交（基本可用）
F1 >= 0.75 → 好的提交（质量不错）
F1 >= 0.80 → 优秀提交（非常好）
F1 < 0.65 → 不推荐提交（需要改进）
```

### 错误3: "VALIDATE和SUBMIT模式的超参数不一致"

**最佳实践：**
```python
# 方案1: 最安全（推荐）
# 1. VALIDATE完整运行
# 2. 记录最优超参数
# 3. 修改model配置为相同参数
# 4. 切换为SUBMIT

# 方案2: 自动化
# 在notebook中定义一个参数类
class BEST_PARAMS:
    n_splits = 5
    max_depth = 7
    learning_rate = 0.06
    # ... 其他
# 然后在CFG中引用这些参数
```

---

## 💾 文件管理

### VALIDATE模式生成的文件

```
xgboost/
├── {section}/
│   ├── {action}/
│   │   ├── oof_pred_probs.pkl      # OOF预测概率
│   │   ├── threshold.pkl           # 最优阈值
│   │   └── *_trainer_*.pkl         # 模型权重
│   └── ...
├── thresholds.pkl                  # 所有阈值总和
└── scores.pkl                       # 所有F1分数
```

### 必须保留的文件（用于SUBMIT）

```
✓ xgboost/{section}/{action}/*_trainer_*.pkl  # 必须！
✓ xgboost/{section}/{action}/threshold.pkl    # 必须！
✓ xgboost/thresholds.pkl                      # 必须！
```

### SUBMIT模式生成的文件

```
submission.csv  # 最终提交文件
```

---

## 🎯 性能指标理解

### F1分数解释

```
F1 = 2 * (precision * recall) / (precision + recall)

在小鼠行为识别中：
- Precision: 预测为真的样本中有多少实际是真的
- Recall: 实际为真的样本中有多少被正确预测

平衡点：precision和recall都很重要
```

### 不同类型的F1

| 类型 | 计算方法 | 用途 |
|-----|--------|------|
| Binary F1 | 单个action的F1 | 评估单个行为 |
| Macro F1 | 所有action的平均 | 平衡所有行为 |
| Weighted F1 | 按样本数加权的平均 | 考虑类别不平衡 |
| 竞赛指标 | 特定的计分方式 | 与Kaggle评估一致 |

---

## 📊 监控建议

### 在VALIDATE阶段应该追踪的指标

```python
# 记录这些值
metrics = {
    'mean_f1': 0.7523,           # 平均F1
    'std_f1': 0.0142,             # F1标准差
    'competition_metric': 0.7445,  # 竞赛指标
    'best_threshold': {},          # 各action的最优阈值
    'n_features': 245,             # 特征数
    'n_samples': 15000,            # 样本数
    'training_time': '6 hours',    # 训练时间
}
```

### 可视化建议

```python
# 绘制这些图表
1. 各fold的F1分数 (检查稳定性)
2. 各action的F1分数分布 (检查均衡性)
3. 超参数敏感性分析 (理解参数影响)
4. 阈值优化曲线 (验证阈值选择)
5. 类别分布 (检查数据平衡)
```

---

## ⏱️ 时间管理

### 推荐时间分配

```
总时间: 8-12小时

1. VALIDATE第一次运行
   - 特征提取: 1-2小时
   - 5折训练: 3-4小时
   - 评估和分析: 0.5-1小时
   小计: 4.5-7小时

2. 分析和调整
   - 性能分析: 0.5小时
   - 超参数调整: 1-2小时
   小计: 1.5-2.5小时

3. VALIDATE第二次运行 (如果需要)
   - 完整流程: 4.5-7小时

4. SUBMIT模式
   - 最终提交: 0.5-1小时
```

### 如果时间有限

```
快速版本 (2-3小时):
1. 使用 CFG_FAST 或 CFG_LITE 配置
2. 设置 n_splits=3
3. 快速验证一次
4. 直接生成提交

完整版本 (8-12小时):
1. 使用 CFG_BALANCED 或 CFG_PRECISE 配置
2. 设置 n_splits=5
3. VALIDATE完整运行和分析
4. 调整参数
5. 可选：第二次VALIDATE验证
6. 生成最终提交
```

---

## ✨ 最佳实践总结

### DO ✅
- ✅ 总是先运行VALIDATE模式
- ✅ 记录最优超参数配置
- ✅ 验证VALIDATE和SUBMIT的配置一致
- ✅ 保存所有中间结果供分析
- ✅ 在VALIDATE中尽量调试和优化
- ✅ 为SUBMIT保留足够的计算资源

### DON'T ❌
- ❌ 不要跳过VALIDATE直接SUBMIT
- ❌ 不要在SUBMIT时改变超参数
- ❌ 不要删除VALIDATE生成的模型文件
- ❌ 不要多次切换VALIDATE/SUBMIT
- ❌ 不要忽视性能指标的异常

---

## 🔄 迭代工作流示例

### 第一轮

```python
# 配置为VALIDATE，快速测试
class CFG:
    n_splits = 3
    model = XGBClassifier(n_estimators=100, learning_rate=0.15, ...)

# 运行：预期F1 ≈ 0.70
# 结果：有改进空间
```

### 第二轮

```python
# 调整超参数
class CFG:
    n_splits = 5
    model = XGBClassifier(n_estimators=250, learning_rate=0.08, ...)
    # 启用特征工程

# 运行：预期F1 ≈ 0.75
# 结果：很好！保持这个配置
```

### 第三步

```python
# 改为SUBMIT，保持相同配置
class CFG:
    mode = "submit"  # 改这里
    n_splits = 5
    model = XGBClassifier(n_estimators=250, learning_rate=0.08, ...)

# 运行：生成submission.csv
# 提交到Kaggle
```

---

## 📞 故障排除

| 问题 | 检查项 | 解决方案 |
|-----|-------|--------|
| VALIDATE无法运行 | 数据路径是否正确？ | 检查train.csv, test.csv路径 |
| VALIDATE内存溢出 | n_splits是否太大？ | 改为n_splits=3 |
| SUBMIT找不到模型 | 是否完整运行VALIDATE？ | 运行VALIDATE并等待完成 |
| F1分数很低 | 特征是否正确计算？ | 检查特征中的NaN/Inf |
| 两个模式结果差异大 | 配置是否一致？ | 对比两个CFG配置 |

---

**关键要点**：
> 🎯 **先VALIDATE后SUBMIT** 是最有效的竞赛策略。
> 
> VALIDATE帮助您验证想法，SUBMIT才是最后的承诺。

**上次更新**: 2024年11月
**版本**: 1.0
