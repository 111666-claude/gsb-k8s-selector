# k8s-selector

解析并求值标签选择器：等值、不等、集合成员与排除、存在与不存在，并按属性建索引。只用 Python 标准库。

```
python3 -m unittest discover -s tests
python3 -m labelsel --sample=neq
python3 -m labelsel --sample=notin
python3 -m labelsel --sample=emptyin
python3 -m labelsel --sample=notexists
python3 -m labelsel --sample=work
```

## 口径

- **等值**：`k=v` 与 `k==v` 都要求标签值相等。
- **不等**：`k!=v` 要求标签存在且值不相等。
- **集合**：`k in (a,b)` 要求标签值在集合里；`k notin (a,b)` 要求不在；空集合 `()` 表示任何值都不满足。
- **存在**：单独写 `k` 表示标签存在；`!k` 表示标签不存在。
- **与**：逗号分隔的多个条件同时满足。
- **查找**：给出等值条件时按标签建索引取候选，不逐条比较。

## 不变量

- `k!=v` 在标签缺失时不成立；`!k` 在标签存在时不成立。
- 空集合的 `in` 恒为假，空集合的 `notin` 恒为真。
- `scanned` 不随对象数乘查询次数放大：八百个对象查八百次的 `scanned` 不超过 6000。

## 输出契约

`parse` 返回条件列表，`matches` 对一组标签求值，`search` 返回命中下标。
场景打印一行 JSON。`--sample=work` 打印 `{"objects": N, "scanned": N}`。
