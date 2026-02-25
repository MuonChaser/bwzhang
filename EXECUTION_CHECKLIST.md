# XGBoost 小鼠行为识别 - 执行检查清单

## 🚀 快速检查列表

### 阶段1: 验证前检查

- [ ] 数据文件已正确下载到指定路径
- [ ] 所有必要的库已安装 (xgboost, lightgbm, optuna, polars等)
- [ ] GPU驱动已安装 (如果使用GPU模式)
- [ ] 磁盘空间充足 (至少10GB)
- [ ] 内存充足 (至少8GB推荐16GB)
- [ ] Notebook已保存

### 阶段2: 配置检查

- [ ] CFG.mode 设置为 "validate"
  ```python
  mode = "validate"  # 不是 "submit"
  ```

- [ ] 数据路径正确
  ```python
  train_path = "/kaggle/input/MABe-mouse-behavior-detection/train.csv"
  test_path = "/kaggle/input/MABe-mouse-behavior-detection/test.csv"
  ```

- [ ] 超参数合理
  ```python
  n_splits = 5  # 或3(快速)/4(中等)
  n_estimators = 250  # 或200/300
  learning_rate = 0.06  # 或0.08/0.05
  max_depth = 6 or 7
  ```

- [ ] 特征工程函数可用
  ```python
  # 检查这些函数是否定义
  add_curvature_features()
  add_multiscale_features()
  add_acceleration_jerk()
  add_spectral_features()
  ```

### 阶段3: 首次执行前

- [ ] Notebook中的所有cell已按顺序准备好
- [ ] 没有依赖关系错误
- [ ] 工作目录设置正确
- [ ] 已备份重要配置

### 阶段4: 执行期间

- [ ] 监控内存使用 (不应持续增长)
- [ ] 监控GPU使用 (如果使用)
- [ ] 检查中间输出没有错误
- [ ] 记录训练时间
- [ ] 保存日志 (如果可能)

### 阶段5: VALIDATE完成后

- [ ] 检查是否成功生成了模型文件
  ```
  xgboost/
  ├── {section}/
  │   ├── {action}/
  │   │   ├── oof_pred_probs.pkl
  │   │   ├── threshold.pkl
  │   │   └── *_trainer_*.pkl
  ```

- [ ] 记录输出指标
  ```python
  - Mean F1: ________
  - Competition metric: ________
  - Execution time: ________
  ```

- [ ] 检查F1分数是否合理
  ```
  F1 >= 0.75 : 好
  F1 >= 0.70 : 可以
  F1 < 0.65 : 需要改进
  ```

- [ ] 分析是否存在问题
  - [ ] 过拟合? (检查fold差异)
  - [ ] 欠拟合? (F1整体很低)
  - [ ] 某些action失败? (检查specific F1)
  - [ ] 内存问题? (是否完整运行)

### 阶段6: 调整迭代

如果需要调整，按以下顺序：

1. **快速调整** (5-10分钟)
   - [ ] 修改超参数
     - max_depth: __ → __
     - learning_rate: __ → __
     - subsample: __ → __
   - [ ] 重新运行VALIDATE

2. **特征调整** (需要重新提取特征)
   - [ ] 启用/禁用特定函数
   - [ ] 调整时间窗口
   - [ ] 重新运行完整pipeline

3. **模型调整** (可能需要额外配置)
   - [ ] 启用集成学习
   - [ ] 调整正则化参数
   - [ ] 重新运行VALIDATE

### 阶段7: 最终确认

在切换到SUBMIT前：

- [ ] VALIDATE至少成功运行一次
- [ ] F1分数记录完整
- [ ] 所有模型文件已保存
- [ ] 超参数配置已记录
- [ ] 性能指标可接受

### 阶段8: 准备SUBMIT

- [ ] 备份VALIDATE的结果和配置
- [ ] 确认所有超参数将保持不变
- [ ] 更改mode为"submit"
  ```python
  # 从这里:
  mode = "validate"
  
  # 改为这里:
  mode = "submit"
  ```

- [ ] 检查其他配置保持一致
  ```python
  n_splits = 5  # 保持与validate相同
  # 所有model参数保持相同
  ```

- [ ] 最后检查一遍配置是否正确
- [ ] 准备好运行时间充足

### 阶段9: SUBMIT执行

- [ ] 完整运行代码
- [ ] 监控是否有错误
- [ ] 检查是否生成 submission.csv
- [ ] 验证submission.csv格式正确

### 阶段10: 提交

- [ ] submission.csv 文件已生成
- [ ] 文件大小合理 (通常100KB-10MB)
- [ ] 包含所有必要的列
  ```python
  row_id, video_id, agent_id, target_id, action, start_frame, stop_frame
  ```

- [ ] 数值范围正确
  - [ ] frame数字有效
  - [ ] 没有NaN或Inf
  - [ ] action名称正确

- [ ] 准备上传到Kaggle

---

## 📝 记录表格

### VALIDATE运行记录

运行1:
- 日期: ____________
- 配置:
  - n_splits: ___
  - max_depth: ___
  - learning_rate: ___
  - n_estimators: ___
- 结果:
  - Mean F1: ___
  - Std: ___
  - Min/Max: ___ / ___
  - Competition metric: ___
- 执行时间: ___小时
- 问题: ________________

运行2 (如果有):
- 日期: ____________
- 改进:
  - [x] 调整: ________________
  - [x] 改进: ________________
- 结果:
  - Mean F1: ___
  - 改进幅度: +__ (从___ 到 ___)
- 执行时间: ___小时

### 最终配置确认

```python
class CFG:
    mode = "submit"  # ✓ 已改为submit
    n_splits = ___
    
    model = XGBClassifier(
        n_estimators = ___,
        learning_rate = ___,
        max_depth = ___,
        min_child_weight = ___,
        subsample = ___,
        colsample_bytree = ___,
        # ... 其他参数
    )
    
    # 签名: ____________
    # 日期: ____________
```

---

## 🎯 常见问题速查

### Q: 我应该立即提交VALIDATE结果吗?
**A:** 否。总是先看VALIDATE的性能，如果不满意就调整参数后重新运行。

### Q: 如何知道VALIDATE完成了?
**A:** 
- 看是否生成了 xgboost/ 文件夹
- 看是否打印了 Mean F1 和 Competition metric
- 看是否生成了 submission.csv

### Q: VALIDATE失败了怎么办?
**A:** 按以下顺序检查:
1. 数据文件是否存在?
2. 内存是否不足? (改n_splits=3)
3. 是否有特征计算错误? (检查NaN)
4. GPU是否可用? (改用CPU)

### Q: VALIDATE很慢怎么办?
**A:** 
```python
# 加快速度 (快50-70%)
CFG.n_splits = 3  # 从5改为3
CFG.model.n_estimators = 150  # 从300改为150
CFG.model.learning_rate = 0.1  # 从0.06改为0.1
```

### Q: 性能还是很低怎么办?
**A:**
```
✓ 尝试不同的特征工程组合
✓ 启用集成学习 (use_ensemble=True)
✓ 调整类别权重
✓ 增加数据增强
✓ 检查输入特征质量
```

### Q: VALIDATE和SUBMIT的结果不一样?
**A:** 这很正常!
```
原因: SUBMIT使用所有数据训练，VALIDATE使用5折验证
      模型容量不同，性能也会不同
      
期望: SUBMIT通常会略低于VALIDATE (过拟合的反面)
      但不应该相差太大 (>10%)
```

---

## 🔐 安全检查

- [ ] 没有硬编码的敏感信息
- [ ] 所有路径都是相对路径或参数化
- [ ] 没有无限循环或递归
- [ ] 内存管理正确 (释放不需要的变量)
- [ ] 没有数据泄露 (验证集不应用于训练)

---

## ✅ 最终准备清单

执行前最后一次检查:

```
VALIDATE:
☐ 模式: validate
☐ 磁盘空间: > 10GB
☐ 内存: > 8GB
☐ 时间: 已分配4-8小时
☐ 数据: 已验证存在
☐ 配置: 已审查

SUBMIT:
☐ 模式: submit
☐ 超参数: 与validate一致
☐ 模型文件: 已保存
☐ 时间: 已分配2-3小时
☐ 网络: 连接良好
☐ Kaggle账户: 已准备

提交前:
☐ submission.csv 已生成
☐ 文件格式: 正确
☐ 数据范围: 合理
☐ 没有错误消息
```

---

**记住**: 仔细准备 → 自信执行 → 成功提交! 🎉

**最后更新**: 2024年11月
