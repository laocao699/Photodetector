#!/usr/bin/env bash
# =============================================================================
# github_publish.sh — 将本项目提交并推送到你的个人 GitHub 仓库
#
# 用法:
#   bash work/tools/github_publish.sh <仓库URL> [remote名] [提交信息]
# 示例:
#   bash work/tools/github_publish.sh https://github.com/<你>/devsim-tcad-research.git
#
# 前置条件（本脚本不会替你修改 git config）:
#   git config user.name  "你的名字"
#   git config user.email "你的邮箱"
#   并已在 GitHub 上创建好一个 **空** 仓库（不要勾选自动生成 README/.gitignore/LICENSE）
#
# 安全措施:
#   - 推送前扫描暂存区，若存在 >50MB 文件则中止（GitHub 告警线；>100MB 会被硬拒）
#   - 不修改任何 git config；不执行 force push
# =============================================================================
set -euo pipefail

URL="${1:-}"
REMOTE="${2:-github}"
MSG="${3:-Add DEVSIM TCAD multi-phase device simulation research (Phase 1-6)

- work/: 研究工作层（二极管 / BJT / 电热 / Si PIN 光电 / beta-Ga2O3 日盲探测器）
- work/tools/: 一键复现、golden 自动对照、打包脚本
- 文档: README、PACKAGE_USAGE、各阶段 REPORT 与 Phase5-6 工作报告
- requirements.txt / .gitignore: 依赖清单与可再生产物忽略规则

上游 DEVSIM 源码版权归 DEVSIM LLC，Apache-2.0（见 LICENSE / NOTICE）。}"

[[ -n "$URL" ]] || { echo "用法: github_publish.sh <仓库URL> [remote名] [提交信息]"; exit 2; }

cd "$(dirname "${BASH_SOURCE[0]}")/../.."

# ---- 前置检查：提交身份 ----
if ! git config user.name >/dev/null 2>&1 || ! git config user.email >/dev/null 2>&1; then
  echo "错误: 未设置 git 提交身份。请先执行（本脚本不代改 git config）:"
  echo '  git config user.name  "你的名字"'
  echo '  git config user.email "你的邮箱"'
  exit 1
fi
echo "提交身份: $(git config user.name) <$(git config user.email)>"

# ---- 暂存 ----
git add -A
echo "已暂存条目: $(git diff --cached --name-only | wc -l)"

# ---- 大文件守卫 ----
BIG=$(git diff --cached --name-only -z \
      | xargs -0 -I{} sh -c 'test -f "{}" && stat -c "%s {}" "{}"' 2>/dev/null \
      | awk '$1>52428800' || true)
if [[ -n "$BIG" ]]; then
  echo "错误: 暂存区存在 >50MB 的文件，GitHub 会告警甚至拒收:"
  echo "$BIG" | awk '{printf "  %.1fMB  %s\n", $1/1048576, substr($0, index($0,$2))}'
  echo "请将其加入 .gitignore 后重试。"
  exit 1
fi
echo "大文件守卫: 通过（无 >50MB 文件）"

# ---- 提交 ----
if git diff --cached --quiet; then
  echo "无变更可提交（工作区已干净）。"
else
  git commit -q -m "$MSG"
  echo "已提交: $(git log --oneline -1)"
fi

# ---- 远端与推送 ----
git remote remove "$REMOTE" 2>/dev/null || true
git remote add "$REMOTE" "$URL"
echo "远端 $REMOTE -> $URL"

BRANCH="$(git symbolic-ref --short HEAD)"
echo "推送分支: $BRANCH"
git push -u "$REMOTE" "$BRANCH"

echo ""
echo "完成 ✓  仓库地址: $URL"
echo "提示: external/ 下 7 个 submodule 默认未初始化，克隆者如需构建 C++ 引擎，"
echo "      执行 git submodule update --init --recursive"
