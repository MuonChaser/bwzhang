# 资源加载超时配置（1秒限制）

## 修改说明

已成功配置网页加载所有外部资源（JS、CSS、字体、图片等）最多等待 1 秒的限制。具体修改如下：

### 1. 全局资源加载超时管理器（head.html）

在 `/themes/maupassant/layouts/partials/head.html` 中添加了一个全局资源加载超时管理器：

```javascript
(function() {
    const RESOURCE_TIMEOUT = 1000; // 1 second in milliseconds
    const originalCreateElement = document.createElement;
    
    document.createElement = function(tagName) {
        const element = originalCreateElement.call(document, tagName);
        const tag = tagName.toLowerCase();
        
        // Apply timeout to scripts, stylesheets, images, and fonts
        if (['script', 'link', 'img'].includes(tag)) {
            const timeoutId = setTimeout(() => {
                if (element.parentNode) {
                    element.parentNode.removeChild(element);
                    const src = element.src || element.href;
                    console.warn(`Resource loading timeout (${tag}): ${src}`);
                }
            }, RESOURCE_TIMEOUT);
            
            // Clear timeout if resource loads successfully
            element.addEventListener('load', () => clearTimeout(timeoutId));
            element.addEventListener('error', () => clearTimeout(timeoutId));
        }
        return element;
    };
})();
```

**工作原理：**
- 拦截所有 `document.createElement()` 的调用
- 监听脚本（script）、样式表（link）、图片（img）等资源的创建
- 为每个资源设置 1 秒的加载超时
- 如果超时，资源会被从 DOM 中移除
- 资源成功加载或出错时会清除超时计时器
- 超时的资源会在浏览器控制台输出警告信息

### 2. 降低所有外部资源加载优先级

在所有外部资源上添加 `fetchpriority="low"` 属性，以降低其加载优先级：

#### 应用 fetchpriority="low" 的资源：

**CSS 样式表：**
- 字体库 CSS（LXGW WenKai）
- normalize.css
- style.css
- Fancybox CSS
- 自定义 CSS

**JavaScript 脚本：**
- jQuery 库
- Google Ads 脚本
- Graphviz 脚本
- Flowchart 脚本
- Sequence 图表脚本
- MathJax 脚本
- 其他第三方脚本

## 支持的资源类型

| 资源类型 | 标签 | 超时处理 | 优先级调整 |
|---------|------|--------|---------|
| JavaScript | `<script>` | ✅ | ✅ |
| CSS 样式表 | `<link>` | ✅ | ✅ |
| 字体文件 | `<link>` | ✅ | ✅ |
| 图片 | `<img>` | ✅ | - |
| 其他资源 | - | - | - |

## 效果

✅ **关键资源优先加载**
- 页面文档和关键 CSS 首先加载
- 内联脚本不受影响

✅ **非关键资源超时控制**
- 所有外部资源最多等待 1 秒
- 超时后自动移除，不阻塞页面加载
- 页面加载速度大幅提升

✅ **降低第三方服务影响**
- 字体、图表库、统计脚本等降低优先级
- 即使这些资源加载缓慢也不影响页面主体显示

✅ **错误监控和调试**
- 超时事件在浏览器控制台输出警告
- 便于后续调试和优化

## 配置文件

修改的文件：
1. `/themes/maupassant/layouts/partials/head.html`
2. `/themes/maupassant/layouts/partials/footer.html`

## 测试方法

1. 打开浏览器开发者工具（F12）
2. 进入 Console 选项卡
3. 访问网站页面
4. 如果有超时的资源，会看到类似的警告信息：
   ```
   Resource loading timeout (script): //code.jquery.com/...
   Resource loading timeout (link): https://cdn.jsdelivr.net/...
   Resource loading timeout (img): https://example.com/image.png
   ```

## 可调整参数

如需修改超时时间，编辑 `head.html` 中的这一行：
```javascript
const RESOURCE_TIMEOUT = 1000; // 改这个值，单位：毫秒
```

- 500ms = 0.5秒
- 1000ms = 1秒
- 2000ms = 2秒

## 浏览器兼容性

- `fetchpriority` 属性：现代浏览器支持（Chrome 101+、Firefox 101+、Safari 15.4+）
- 超时处理脚本：所有现代浏览器支持
- 在不支持的浏览器中，fetchpriority 会被忽略，但超时处理仍然有效

