# trace.cli

板端脚本：一次抓取 **IPP + EPP** 的流水线 trace dump（MAU + parser）。

- IPP：`mau0` … `mau8` + `iparser`
- EPP：`mau9` … `mau10` + `eparser` + `pedt`

在板端解释器中执行，输出带 `---- xxx start/end ----` 标记的 `reg read` 日志，可供 `trace_viewer.html` 解析。

## 用法

```text
trace.cli ipp <die> <pp0|pp1> epp <die> <pp0|pp1>
```

六个参数均为**位置参数**，顺序固定。IPP 与 EPP 的 die / 管道可不同。

```text
trace.cli ipp xdie pp0 epp sdie8 pp1
```

## 参数

| 位置 | 名称 | 取值 | 说明 |
|------|------|------|------|
| `$1` | 关键字 | `ipp` | 必须为 `ipp`，否则跳过整个 IPP 段 |
| `$2` | IPP die | `xdie` 或 `sdie0` … `sdie8` | IPP 侧芯片实例，决定 `reg read` 的 uniq |
| `$3` | IPP 管道 | `pp0` 或 `pp1` | IPP 的 packet pipe；sdie 上还会参与 uniq |
| `$4` | 关键字 | `epp` | 必须为 `epp`，否则跳过整个 EPP 段 |
| `$5` | EPP die | `xdie` 或 `sdie0` … `sdie8` | EPP 侧芯片实例，可与 IPP 不同 |
| `$6` | EPP 管道 | `pp0` 或 `pp1` | EPP 的 packet pipe |

### die

| 取值 | 含义 |
|------|------|
| `xdie` | 主 die，uniq 固定 `0x90`（与 pp 无关） |
| `sdie0` … `sdie8` | 从 die；uniq = `0xN0`（pp0）或 `0xN1`（pp1），N 为 die 号 |

非法 die 会 abort 对应的 IPP 或 EPP 段。

### 管道（pp）

| 取值 | 含义 |
|------|------|
| `pp0` | pipe 0 |
| `pp1` | pipe 1 |

只影响该侧（IPP 或 EPP）的 uniq 与抓取对象，不改变 MAU 编号范围。

## 抓取内容

每个合法的 MAU 会依次 dump：

`cls` → `keygen` → `vme0`…`vme4` → `lrr` → `egr` → `statistics`

IPP 额外 dump `iparser`；EPP 额外 dump `eparser`、`pedt`。

## 生成 trace_viewer.html 并展示 dump

`trace.cli` 只负责在板端读寄存器；字段级展示在离线页 `view/trace_viewer.html`。改 yaml 后必须重新生成该 HTML，否则页面仍用旧格式表。

### 生成

在 `tools/trace` 下执行：

```text
python view/build_viewer.py
```

脚本把 `viewer_template.html` 与三份 yaml（`mau_trace.yaml`、`iparser_trace.yaml`、`eparser_pedt_fields.yaml`）嵌进一个可双击打开的 HTML，默认写出 `view/trace_viewer.html`。

| 参数 | 说明 |
|------|------|
| `-y` / `--yaml` | MAU 格式表，默认 `mau_trace.yaml` |
| `--iparser-yaml` | iparser 格式表 |
| `--eparser-yaml` | eparser / pedt 格式表 |
| `-o` / `--output` | 输出 HTML 路径 |
| `-i` / `--input` | 可选：预解析好的 `result.json`，打开页面即带数据 |

也可 `python view/mau/app.py`：先 build，再在 `http://127.0.0.1:8765/` 打开同一份 HTML。

### 把 trace.cli 日志放进页面

1. 板端跑 `trace.cli …`，把完整输出存成 `.log` / `.txt`（需保留 `---- mau0 start ----` 这类标记）。
2. 用浏览器打开 `view/trace_viewer.html`（纯本地，不上传文件）。
3. 左侧「选择日志文件」选该文件，或把日志粘贴进文本框。
4. 点 **解析**。按标记切成 mau / iparser / eparser / pedt，再按 yaml 解字段。
5. 顶栏切模块；左侧树选 `mauN` 的 `cls` / `keygen` / `vme*` / `lrr` / `egr` 或 parser 块。`keygen` 会附带 `lpm_mpl_req_data`，`egr` 会附带 `lpm_mpl_rsp_data`。

## 相关文件

| 文件 | 作用 |
|------|------|
| `mau_trace.cli` | 仅 MAU（参数：`<die> <ipp\|epp> <pp0\|pp1>`） |
| `iparser_trace.cli` | 仅 iparser |
| `eparser_pe_trace.cli` | 仅 eparser + pedt |
| `_gen_trace_cli.py` | 将上面三个脚本拼成 `trace.cli` |
| `view/build_viewer.py` | 生成 `view/trace_viewer.html` |
| `view/trace_viewer.html` | 将本脚本的日志解析为字段视图 |
