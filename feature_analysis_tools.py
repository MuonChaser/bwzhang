"""
Feature Engineering Analysis and Visualization Tools

This module contains utility functions for analyzing features 
and optimizing model performance.

Usage:
    from feature_analysis_tools import analyze_feature_importance
    analyze_feature_importance(X_tr, y_action)
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import f1_score


def analyze_feature_importance(X, y, top_n=20, model='xgboost'):
    """
    分析特征重要性,识别关键特征
    
    参数:
    - X: 特征矩阵
    - y: 标签
    - top_n: 显示top N个特征
    - model: 'xgboost' 或 'random_forest'
    """
    from xgboost import XGBClassifier
    from sklearn.ensemble import RandomForestClassifier
    import matplotlib.pyplot as plt
    
    if model == 'xgboost':
        clf = XGBClassifier(n_estimators=100, random_state=42, verbosity=0)
    else:
        clf = RandomForestClassifier(n_estimators=100, random_state=42)
    
    clf.fit(X, y)
    
    importance = pd.DataFrame({
        'feature': X.columns,
        'importance': clf.feature_importances_
    }).sort_values('importance', ascending=False)
    
    # 绘图
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(importance['feature'][:top_n], importance['importance'][:top_n])
    ax.set_xlabel('Importance')
    ax.set_title(f'Top {top_n} Feature Importance')
    plt.tight_layout()
    plt.show()
    
    print(importance.head(top_n))
    return importance
```

---

## 工具2: 数据质量检查

```python
def check_feature_quality(X, y=None, verbose=True):
    """
    检查特征数据质量
    
    检查项:
    - 缺失值
    - 无穷大
    - 常数特征
    - 重复特征
    - 类别不平衡
    """
    issues = []
    
    # 1. 缺失值
    missing = X.isnull().sum()
    if missing.sum() > 0:
        issues.append(f"⚠️ 缺失值: {missing[missing > 0].to_dict()}")
    
    # 2. 无穷大
    inf_mask = np.isinf(X).any()
    if inf_mask.any():
        issues.append(f"⚠️ 包含无穷大的列: {X.columns[inf_mask].tolist()}")
    
    # 3. 常数特征
    constant = X.std() == 0
    if constant.any():
        issues.append(f"⚠️ 常数特征 (方差=0): {X.columns[constant].tolist()}")
    
    # 4. 方差很小的特征
    low_variance = X.std() < X.std().median() * 0.1
    if low_variance.any():
        issues.append(f"ℹ️ 低方差特征: {X.columns[low_variance].tolist()[:5]}")
    
    # 5. 重复特征
    duplicates = []
    for i, col1 in enumerate(X.columns):
        for col2 in X.columns[i+1:]:
            if (X[col1] == X[col2]).all():
                duplicates.append((col1, col2))
    if duplicates:
        issues.append(f"⚠️ 重复特征: {duplicates}")
    
    # 6. 强相关特征
    corr_matrix = X.corr().abs()
    high_corr = []
    for i in range(len(corr_matrix.columns)):
        for j in range(i+1, len(corr_matrix.columns)):
            if corr_matrix.iloc[i, j] > 0.95:
                high_corr.append((corr_matrix.columns[i], corr_matrix.columns[j], corr_matrix.iloc[i, j]))
    if high_corr:
        issues.append(f"ℹ️ 强相关特征对(>0.95): {len(high_corr)}对")
    
    # 7. 类别不平衡 (如果提供y)
    if y is not None:
        ratio = y.value_counts(normalize=True)
        imbalance = ratio.max() / ratio.min()
        if imbalance > 10:
            issues.append(f"⚠️ 严重不平衡: {imbalance:.1f}x")
        elif imbalance > 5:
            issues.append(f"ℹ️ 不平衡: {imbalance:.1f}x")
    
    if verbose:
        print("\n=== 数据质量检查 ===")
        if not issues:
            print("✅ 所有检查通过!")
        else:
            for issue in issues:
                print(issue)
        print(f"\n总特征数: {X.shape[1]}")
        print(f"总样本数: {X.shape[0]}")
    
    return {
        'n_features': X.shape[1],
        'n_samples': X.shape[0],
        'n_missing': missing.sum(),
        'n_inf': np.isinf(X).sum().sum(),
        'n_constant': constant.sum(),
        'issues': issues
    }
```

---

## 工具3: 类别分布可视化

```python
def visualize_class_distribution(y, title='Class Distribution'):
    """
    可视化类别分布
    """
    import matplotlib.pyplot as plt
    
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    
    # 条形图
    counts = y.value_counts()
    axes[0].bar(counts.index, counts.values, color=['#1f77b4', '#ff7f0e'][:len(counts)])
    axes[0].set_ylabel('Count')
    axes[0].set_title(title)
    axes[0].set_xticklabels(['Negative', 'Positive'])
    
    # 饼图
    axes[1].pie(counts.values, labels=['Negative', 'Positive'][:len(counts)], 
                autopct='%1.1f%%', colors=['#1f77b4', '#ff7f0e'][:len(counts)])
    axes[1].set_title('Proportion')
    
    plt.tight_layout()
    plt.show()
    
    # 统计信息
    print(f"\n类别分布:")
    print(f"  0 (Negative): {counts[0]} ({counts[0]/len(y)*100:.1f}%)")
    print(f"  1 (Positive): {counts[1]} ({counts[1]/len(y)*100:.1f}%)")
    print(f"  不平衡比: {counts.max() / counts.min():.2f}x")
```

---

## 工具4: 特征相关性热力图

```python
def plot_correlation_matrix(X, top_n=50):
    """
    绘制特征相关性热力图
    
    参数:
    - X: 特征矩阵
    - top_n: 只显示与目标最相关的top N个特征
    """
    import matplotlib.pyplot as plt
    import seaborn as sns
    
    # 只取方差最大的特征
    std_cols = X.std().nlargest(top_n).index
    X_subset = X[std_cols]
    
    # 计算相关性
    corr = X_subset.corr()
    
    # 绘图
    fig, ax = plt.subplots(figsize=(12, 10))
    sns.heatmap(corr, cmap='coolwarm', center=0, ax=ax, 
                square=True, linewidths=0.5, cbar_kws={"shrink": 0.8})
    ax.set_title(f'Correlation Matrix (Top {top_n} Features)')
    plt.tight_layout()
    plt.show()
```

---

## 工具5: 特征分布分析

```python
def analyze_feature_distributions(X, columns=None, n_cols=3):
    """
    绘制特征分布直方图
    """
    import matplotlib.pyplot as plt
    
    if columns is None:
        # 选择方差最大的特征
        columns = X.std().nlargest(12).index
    
    n_features = len(columns)
    n_rows = (n_features + n_cols - 1) // n_cols
    
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, n_rows*3))
    axes = axes.flatten()
    
    for idx, col in enumerate(columns):
        axes[idx].hist(X[col].dropna(), bins=50, edgecolor='black', alpha=0.7)
        axes[idx].set_title(col)
        axes[idx].set_ylabel('Frequency')
    
    # 隐藏空白子图
    for idx in range(len(columns), len(axes)):
        axes[idx].set_visible(False)
    
    plt.tight_layout()
    plt.show()
```

---

## 工具6: 交叉验证性能分析

```python
def analyze_cv_performance(f1_scores, action_names=None):
    """
    分析交叉验证性能
    
    参数:
    - f1_scores: list of F1 scores
    - action_names: list of action names
    """
    import matplotlib.pyplot as plt
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # 箱线图
    axes[0].boxplot(f1_scores, labels=['F1 Scores'])
    axes[0].set_ylabel('F1 Score')
    axes[0].set_title('CV F1 Score Distribution')
    axes[0].grid(True, alpha=0.3)
    
    # 分布直方图
    axes[1].hist(f1_scores, bins=20, edgecolor='black', alpha=0.7)
    axes[1].axvline(np.mean(f1_scores), color='r', linestyle='--', label=f'Mean: {np.mean(f1_scores):.3f}')
    axes[1].axvline(np.median(f1_scores), color='g', linestyle='--', label=f'Median: {np.median(f1_scores):.3f}')
    axes[1].set_xlabel('F1 Score')
    axes[1].set_ylabel('Frequency')
    axes[1].set_title('F1 Score Distribution')
    axes[1].legend()
    
    plt.tight_layout()
    plt.show()
    
    # 统计信息
    print("\n=== CV 性能统计 ===")
    print(f"平均F1: {np.mean(f1_scores):.4f}")
    print(f"中位数F1: {np.median(f1_scores):.4f}")
    print(f"标准差: {np.std(f1_scores):.4f}")
    print(f"最小值: {np.min(f1_scores):.4f}")
    print(f"最大值: {np.max(f1_scores):.4f}")
    print(f"方差系数: {np.std(f1_scores) / np.mean(f1_scores):.4f}")
```

---

## 工具7: 超参数敏感性分析

```python
def analyze_parameter_sensitivity():
    """
    分析超参数对性能的敏感性
    """
    import matplotlib.pyplot as plt
    
    # 示例数据
    params_effects = {
        'max_depth': [0.70, 0.72, 0.74, 0.76, 0.75, 0.73],
        'learning_rate': [0.75, 0.75, 0.76, 0.76, 0.74, 0.72],
        'subsample': [0.70, 0.73, 0.76, 0.77, 0.75, 0.72],
        'colsample': [0.71, 0.74, 0.76, 0.77, 0.75, 0.73],
    }
    
    param_values = {
        'max_depth': [4, 5, 6, 7, 8, 9],
        'learning_rate': [0.01, 0.05, 0.08, 0.1, 0.15, 0.2],
        'subsample': [0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
        'colsample': [0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
    }
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    axes = axes.flatten()
    
    for idx, (param, f1_scores) in enumerate(params_effects.items()):
        axes[idx].plot(param_values[param], f1_scores, marker='o', markersize=8, linewidth=2)
        axes[idx].set_xlabel(param)
        axes[idx].set_ylabel('F1 Score')
        axes[idx].set_title(f'{param} Sensitivity')
        axes[idx].grid(True, alpha=0.3)
        
        # 标记最优点
        best_idx = np.argmax(f1_scores)
        axes[idx].plot(param_values[param][best_idx], f1_scores[best_idx], 'r*', markersize=15)
    
    plt.tight_layout()
    plt.show()
```

---

## 工具8: 模型性能比较

```python
def compare_models(results_dict):
    """
    比较多个模型的性能
    
    参数:
    - results_dict: {'model_name': f1_scores_list}
    """
    import matplotlib.pyplot as plt
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # 箱线图
    f1_lists = list(results_dict.values())
    labels = list(results_dict.keys())
    
    axes[0].boxplot(f1_lists, labels=labels)
    axes[0].set_ylabel('F1 Score')
    axes[0].set_title('Model Performance Comparison')
    axes[0].grid(True, alpha=0.3)
    
    # 均值条形图
    means = [np.mean(scores) for scores in f1_lists]
    stds = [np.std(scores) for scores in f1_lists]
    
    axes[1].bar(labels, means, yerr=stds, capsize=5, alpha=0.7)
    axes[1].set_ylabel('Mean F1 Score')
    axes[1].set_title('Mean F1 Score ± Std')
    axes[1].grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.show()
    
    # 打印统计信息
    print("\n=== 模型性能比较 ===")
    for model_name, scores in results_dict.items():
        print(f"{model_name}:")
        print(f"  平均: {np.mean(scores):.4f}")
        print(f"  标准差: {np.std(scores):.4f}")
        print(f"  最小/最大: {np.min(scores):.4f} / {np.max(scores):.4f}")
```

---

## 工具9: 阈值优化可视化

```python
def visualize_threshold_optimization(oof_preds, y_true):
    """
    可视化阈值优化过程
    """
    import matplotlib.pyplot as plt
    
    thresholds = np.linspace(0, 1, 100)
    f1_scores = []
    
    for threshold in thresholds:
        y_pred = (oof_preds >= threshold).astype(int)
        f1 = f1_score(y_true, y_pred, zero_division=0)
        f1_scores.append(f1)
    
    best_threshold = thresholds[np.argmax(f1_scores)]
    best_f1 = np.max(f1_scores)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(thresholds, f1_scores, linewidth=2)
    ax.axvline(best_threshold, color='r', linestyle='--', label=f'Best: {best_threshold:.3f}')
    ax.scatter([best_threshold], [best_f1], color='r', s=100, zorder=5)
    ax.set_xlabel('Threshold')
    ax.set_ylabel('F1 Score')
    ax.set_title('Threshold Optimization')
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()
    
    print(f"\n最优阈值: {best_threshold:.4f}")
    print(f"对应F1分数: {best_f1:.4f}")
    
    return best_threshold
```

---

## 使用示例

```python
# 在notebook的最后添加:

# 1. 检查数据质量
quality_report = check_feature_quality(X_tr, y_action)

# 2. 分析特征重要性
importance = analyze_feature_importance(X_tr, y_action, top_n=20)

# 3. 可视化类别分布
visualize_class_distribution(y_action)

# 4. 查看特征分布
analyze_feature_distributions(X_tr, n_cols=3)

# 5. 分析相关性
plot_correlation_matrix(X_tr, top_n=30)

# 6. 分析CV性能
analyze_cv_performance(f1_list, action_names=pred.columns)

# 7. 优化阈值
best_threshold = visualize_threshold_optimization(oof_action, y_action)
```

---

## 输出示例

```
=== 数据质量检查 ===
✅ 所有检查通过!

总特征数: 245
总样本数: 15000

=== CV 性能统计 ===
平均F1: 0.7523
中位数F1: 0.7531
标准差: 0.0142
最小值: 0.7312
最大值: 0.7721
方差系数: 0.0189
```

