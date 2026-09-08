# TikTok 印尼站脚本 Skill · Codex 优先

为 TikTok / TikTok Shop 印尼站创作 **印尼语台词＋中文执行说明**，交付「时间＋画面＋字幕＋台词＋声音」制作表，并从节奏、口语感、新鲜感、结构四个角度审稿改写。

Codex-first skill for TikTok Indonesia: Bahasa Indonesia scripts, storyboards and editorial review. Gemini is optional and only supplements essential video evidence that Codex cannot reliably obtain.

## 什么时候用 Codex，什么时候用 Gemini？

| 输入与任务 | 执行方式 |
|---|---|
| 没有视频，只有产品资料 | Codex 直接写作、分镜、翻译和审稿；不需要 Gemini 密钥 |
| 有视频，但只需改写、翻译或整理已有报告 | 仍由 Codex 完成 |
| 需要视频事实，现有报告、时间戳画面或转写足够 | Codex 综合分析，并说明观察精度 |
| 必要的连续动作、声音或声画同步证据仍缺失 | 才用 Gemini 补充指定问题或片段，随后回到 Codex 写作 |

附件里有视频，并不自动触发 Gemini。用户禁止 Gemini 时，保留无法确认项。抽样画面与转写的综合分析不等于原生完整音视频理解。

## 安装

把本仓库作为 `huashu-tiktok-id-script` 文件夹放入 Codex 的技能目录。默认是 `~/.codex/skills`；设置了 `CODEX_HOME` 时使用其中的 `skills` 目录。

**Windows PowerShell（已安装 Git）：**

```powershell
$skillHome = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $env:USERPROFILE '.codex' }
$skillTarget = Join-Path $skillHome 'skills/huashu-tiktok-id-script'
if (Test-Path -LiteralPath $skillTarget) { throw '技能目录已存在，请先检查现有版本。' }
New-Item -ItemType Directory -Path (Split-Path -Parent $skillTarget) -Force | Out-Null
git clone https://github.com/878872221kl-a11y/huashu-tiktok-id-script.git $skillTarget
```

**macOS / Linux（已安装 Git）：**

```bash
skill_target="${CODEX_HOME:-$HOME/.codex}/skills/huashu-tiktok-id-script"
mkdir -p "$(dirname "$skill_target")"
git clone https://github.com/878872221kl-a11y/huashu-tiktok-id-script.git "$skill_target"
```

也可通过仓库的 **Code → Download ZIP** 下载，解压后将文件夹改名为 `huashu-tiktok-id-script`，放入上述目录。确认 `SKILL.md` 直接位于该文件夹内，然后重启 Codex 以加载技能。安装不会修改原版 `huashu-douyin-script`。

## 直接使用

```text
使用 $huashu-tiktok-id-script。
面向 TikTok 印尼站，品牌：[品牌]，产品资料：[材质、尺寸、功能等已确认事实]。
受众：[目标人群]，目标：[种草/商品转化/达人合作/引流直播]，时长：30 秒。
目前没有视频，请直接由 Codex 完成，不调用 Gemini。
输出两个开头钩子、印尼语台词与中文对照，以及时间、画面、字幕、台词、声音制作表。
最后从节奏、口语感、新鲜感和结构审稿，并将修改应用到完整脚本。
```

有参考视频时，在同一任务附上本地视频、TikTok 链接或已有拆解报告。提供品牌、产品实测信息与真实转化入口；未知价格、折扣、销量和使用经历会省略，不编造。ONEBEAR 制作表示例见 [印尼语写法与样例](references/id-writing-and-examples.md)。

需要团队脚本库时，可以另行要求增加编号、版本、状态、负责人、计划日期、素材链接和复盘字段。写入飞书需要当前 Codex 环境中可用的飞书工具及目标表权限；本仓库不附带私人表格或账号配置。

## 可选的视频工具

纯脚本创作只需可用的 Codex，不要求安装以下依赖。辅助脚本使用 Python 3.9+；具体第三方依赖可能要求更新的 Python。

| 工具 | 何时需要 |
|---|---|
| `yt-dlp` | 下载可访问的 TikTok 视频；已有本地视频可跳过 |
| FFmpeg | 需要在本地截帧、截取片段时 |
| Gemini API 密钥 | 仅在必要视频证据无法由 Codex 可靠取得时 |
| `google-genai` | Gemini 辅助脚本上传较大视频时 |

密钥通过环境变量 `GEMINI_API_KEY` 或 `GOOGLE_API_KEY` 提供；模型用 `--model` 或 `GEMINI_MODEL` 指定为账号实际可用的型号。不要将真实密钥或 Cookie 提交到仓库。执行方式与完整流程见 [SKILL.md](SKILL.md)；辅助脚本可用 `--help` 查看参数。

`analyze_video.py --dry-run` 不上传视频、不读取密钥。`--start/--end` 仅限定模型处理时段，**不会缩小上传文件范围**；只允许发送片段时，应先在本地截取。接口失败会停止，不自动重试生成或切换付费模型。

## 检查

在仓库目录运行：

```bash
python scripts/test_helpers.py
```

离线检查覆盖链接边界、时间参数、无密钥 dry-run、响应解析、输出保护及配额错误处理，不下载视频、不发送真实 API 请求。实际下载和 Gemini 服务可用性取决于网络、目标站点及账户；离线通过不代表这些服务已完成联调。

## 来源

参考 [花叔 alchaincyf/huashu-skills 的 huashu-douyin-script](https://github.com/alchaincyf/huashu-skills/tree/master/huashu-douyin-script) 六步工作流、七维拆解与审稿方法，重新编写印尼市场说明、样例及辅助代码。本仓库是独立适配版，不代表原作者、OpenAI、Google 或 TikTok 官方发布。

平台核对链接与更新时间见 [来源与平台信息](references/platform-sources.md)。脚本与结构样例是待实拍、试读和数据验证的创作起点，不承诺爆款或转化成绩。
