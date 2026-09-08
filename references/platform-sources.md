# 来源与需要更新的平台信息

迁移核对日期：2026-09-08。以下平台规则与功能会变化，实际发布/投放前核对官方页面和目标账户；脚本创作建议不是审核通过保证。

## 迁移来源

[alchaincyf/huashu-skills：huashu-douyin-script](https://github.com/alchaincyf/huashu-skills/tree/master/huashu-douyin-script)。本适配版参考原版的六步流程、七维分析与审稿方法，重新编写印尼市场说明、示例及辅助代码。作为独立技能安装，不覆盖原版文件。

## 已核对的关键差异

| 官方来源 | 对本 skill 的影响 |
|---|---|
| [TikTok 创意建议](https://ads.tiktok.com/resources/help/article/creative-best-practices) | 采用竖屏、可读字幕、产品/人物演示与 hook→body→CTA；开头尽早交代内容。前 3 秒与节奏长度是创作起点，不是算法保证，不机械套用广告组数量建议。 |
| [印尼站 GMV Max 账户条件](https://ads.tiktok.com/resources/help/article/troubleshoot-account-settings-for-gmv-max-in-tiktok-ads-manager?lang=id) | 印尼属于支持市场，实际商家仍需店铺关联和账户授权；写脚本不等于已具备投放权限。 |
| [TikTok Sales 目标与 Shop Ads](https://ads.tiktok.com/help/article/sales-advertising-objective-tiktok?lang=en) | 官方文档说明 Shop Ads 迁移至 GMV Max；不要给用户套用“千川”操作步骤，区分 TikTok Shop、网站、App 等目的地。 |
| [商业内容披露](https://support.tiktok.com/en/business-and-creator/creator-and-business-accounts/promoting-a-brand-product-or-service?lang=en) | 推广自己品牌或有商业关系的第三方产品都需要相应内容披露；自然流量内容不是豁免。写进发布交接，不假称已替用户开启。 |
| [商业音乐使用](https://support.tiktok.com/en/business-and-creator/creator-and-business-accounts/commercial-use-of-music-on-tiktok?lang=en) | 商业内容优先 CML 可用音乐；其他音乐要有相应权利。参考视频的热门 BGM 不等于本次商用许可，现场原声也需避免混入未授权音乐。 |
| [误导与虚假内容](https://ads.tiktok.com/resources/help/article/tiktok-ads-policy-misleading-and-false-content?lang=en) | 产品承诺与落地页需一致，不用伪造 CTA、销量、体验或效果对比。将无依据功效改成第一人称感受，不会使它变成可靠事实。 |
| [AI 广告披露说明](https://ads.tiktok.com/help/article/add-disclaimers-to-ads?lang=en) | 使用生成/显著修改的图像、视频、音频时核对对应披露方式；仅用 AI 起草文字不自动等于成片含合成媒体。Spark 帖子与非 Spark 广告按各自要求处理。 |

语言样例、时长建议、A/B 测试建议均为本地创作方法，不代表官方流量结论。Rp 价格、包邮、COD、赠品、活动时间、BPOM/halal 等信息以本品可核实资料为准，不从竞品或国别推导。

## 运行参考

- [yt-dlp 官方用法](https://github.com/yt-dlp/yt-dlp#usage-and-options)：使用现有命令行或当前 Python 的模块。下载能力受站点变化影响；本地视频路径是独立入口。
- [Gemini 视频理解](https://ai.google.dev/gemini-api/docs/video-understanding)：小文件内联，大文件使用 Files API；当前模型与视频参数以官方说明为准。
- 辅助分析脚本沿用当前可用的 Interactions 请求方式，支持新旧文本响应布局，不固定过期 preview 别名。默认模型可通过参数或环境变量替换。此次迁移测试不发送真实 Gemini 请求。
