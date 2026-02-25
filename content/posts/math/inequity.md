+++
date = '2025-11-21T11:55:17+08:00'
draft = false
title = '概率论中的常见不等式'
toc = false
categories = ['学习笔记']

+++

## Jenson 不等式

对于凸函数 $f$，有如下不等式成立：
$$ E[f(X)] \geq f(E[X]) $$

算术-几何均值不等式是 Jenson 不等式取 $X$ 服从两点分布的特例。取 $f(x) = x^2$, 得方差的非负性。

## Young 不等式

设 $a, b \geq 0$，$p, q > 1$ 且 $\frac{1}{p} + \frac{1}{q} = 1$，则有
$$ ab \leq \frac{a^p}{p} + \frac{b^q}{q} $$

证明可由 Jenson 不等式导出。取 $f(x) = e^x$，$X$ 服从两点分布，取 $ln(a^{p})$ 和 $ln(b^{q})$ 两点的概率分别为 $\frac{1}{p}$ 和 $\frac{1}{q}$。

## Hölder 不等式

设 $X, Y$ 为随机变量，则有
$$ E[|XY|] \leq (E[|X|^p])^{1/p} (E[|Y|^q])^{1/q} $$
设 $p, q > 1$ 且 $\frac{1}{p} + \frac{1}{q} = 1$，则对于任意实数列 $(a_i), (b_i)$ 有
$$ \sum_{i} |a_i b_i| \leq \left( \sum_{i} |a_i|^p \right)^{1/p} \left( \sum_{i} |b_i|^q \right)^{1/q} $$


证明可由 Young 不等式导出。对每一项应用 Young 不等式，然后对所有项求和。

首先，设 $u_i = \frac{|a_i|}{(\sum_{j} |a_j|^p)^{1/p}}$，$v_i = \frac{|b_i|}{(\sum_{j} |b_j|^q)^{1/q}}$，则有
$$ |a_i b_i| = (\sum_{j} |a_j|^p)^{1/p} (\sum_{j} |b_j|^q)^{1/q} |u_i v_i| $$

只需证明 $\sum_{i} |u_i v_i| \leq 1$。应用 Young 不等式，有
$$ |u_i v_i| \leq \frac{|u_i|^p}{p} + \frac{|v_i|^q}{q} $$
由于 $\sum_{i} |u_i|^p = 1$ 和 $\sum_{i} |v_i|^q = 1$，所以
$$ \sum_{i} |u_i v_i| \leq \frac{1}{p} + \frac{1}{q} = 1 $$


Hölder 用于控制两个随机变量乘积的期望，其不大于各自某个 $L_p$ 范数的乘积。在机器学习中，Hölder 不等式常用于分析模型的泛化误差、正则化项以及优化算法的收敛性。   


### Cauthy-Schwarz 不等式
Cauthy-Schwarz 不等式是 Hölder 不等式取 $p = q = 2$ 后，两侧平方的特例。

设 $X, Y$ 为随机变量，则有
$$ (E[XY])^2 \leq E[X^2] E[Y^2] $$

设 $(a_i), (b_i)$ 为任意实数列，则有
$$ \left( \sum_{i} a_i b_i \right)^2 \leq \left( \sum_{i} a_i^2 \right) \left( \sum_{i} b_i^2 \right) $$

或连续形式：
$$ \left( \int_a^b f(x) g(x) dx \right)^2 \leq \left( \int_a^b f(x)^2 dx \right) \left( \int_a^b g(x)^2 dx \right) $$
其中， $f(x), g(x)$ 为区间 $[a, b]$ 上的可积函数。

## Minkowski 不等式
设 $X, Y$ 为随机变量，则有
$$ (E[|X + Y|^p])^{1/p} \leq (E[|X|^p])^{1/p} + (E[|Y|^p])^{1/p} $$
设 $p \geq 1$，则对于任意实数列 $(a_i), (b_i)$ 有
$$ \left( \sum_{i} |a_i + b_i|^p \right)^{1/p} \leq \left( \sum_{i} |a_i|^p \right)^{1/p} + \left( \sum_{i} |b_i|^p \right)^{1/p} $$

证明可由 Hölder 不等式导出。设 $S = \left( \sum_{i} |a_i + b_i|^p \right)^{1/p}$，则有
$$ S^p = \sum_{i} |a_i + b_i|^p = \sum_{i} |a_i + b_i|^{p-1} |a_i| + \sum_{i} |a_i + b_i|^{p-1} |b_i| $$
应用 Hölder 不等式，有
$$ \sum_{i} |a_i + b_i|^{p-1} |a_i| \leq \left( \sum_{i} |a_i + b_i|^p \right)^{(p-1)/p} \left( \sum_{i} |a_i|^p \right)^{1/p} = S^{p-1} \left( \sum_{i} |a_i|^p \right)^{1/p} $$
类似地，
$$ \sum_{i} |a_i + b_i|^{p-1} |b_i| \leq S^{p-1} \left( \sum_{i} |b_i|^p \right)^{1/p} $$
将两式相加，得到
$$ S^p \leq S^{p-1} \left( \sum_{i} |a_i|^p \right)^{1/p} + S^{p-1} \left( \sum_{i} |b_i|^p \right)^{1/p} $$
两边除以 $S^{p-1}$（$S > 0$），得到 Minkowski 不等式。  

Minkowski 不等式是 $L_p$ 空间中范数的三角不等式。