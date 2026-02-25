+++
date = '2025-11-23T19:36:43+08:00'
draft = false
title = 'KL散度与MLE、MAP'
categories = ['学习笔记']
tags = ['概率论']
+++

KL 散度（KL Divergence），是衡量两个概率分布之间差异的一种非对称度量。对分布 $P(x)$ 和 $Q(x)$，KL 散度可以被理解为按照 $P(x)$ 或 $Q(x)$ 加权的对数似然比的期望值：
$$ D_{KL}(P || Q) = \mathbb{E}_{x \sim P} \left[ \log \frac{P(x)}{Q(x)} \right] $$
对于离散分布，KL 散度定义为：
$$ \sum_{x} P(x) \log \frac{P(x)}{Q(x)} $$
对于连续分布，KL 散度定义为：
$$ \int P(x) \log \frac{P(x)}{Q(x)} dx $$

## 性质

### 非负性

从Jenson不等式可以导出KL散度的非负性：
$$
D_{KL}(P || Q) = \mathbb{E}_{x \sim P} \left[ -\log \frac{Q(x)}{P(x)} \right] \geq -\log \mathbb{E}_{x \sim P} \left[ \frac{Q(x)}{P(x)} \right] = -\log 1 = 0
$$

也可直接用基本不等式：
$$
D_{KL}(P || Q) = \sum_{x} P(x) \log \frac{P(x)}{Q(x)} \geq \sum_{x} P(x) (1 - \frac{Q(x)}{P(x)}) = \sum_{x} P(x) - \sum_x Q(x) = 0
$$

### 非对称性    
这是显然的，$D_{KL}(P || Q)$，可以理解为$P$ 是真实分布，故用 $P$ 加权。

## KL 散度与交叉熵

交叉熵定义为：
$$ H(P, Q) = - \mathbb{E}_{x \sim P} [\log Q(x)] $$

因此，KL 散度可以表示为交叉熵与熵的差值：
$$ D_{KL}(P || Q) = H(P, Q) - H(P) $$

其中，$H(P)$ 是分布 $P$ 的熵，定义为：
$$ H(P) = - \mathbb{E}_{x \sim P} [\log P(x)] $$

由于在给定一组数据的情况下，$H(P)$ 是常数，因此最小化 KL 散度等价于最小化交叉熵。

### 分类问题中的交叉熵

在分类问题中，真实标签通常使用独热编码（one-hot encoding）表示。对某样本，其为 One-hot 编码 $\mathbf{y}$，预测概率分布为 $\hat{\mathbf{y}}$，则交叉熵损失函数为：
$$ L = - \sum_{i} y_i \log \hat{y}_i $$
但由于 $\mathbf{y}$ 是独热编码，只有一个元素为1，其余为0，因此损失函数简化为：
$$ L = - \log \hat{y}_k $$
其中，$k$ 是真实类别的索引。
