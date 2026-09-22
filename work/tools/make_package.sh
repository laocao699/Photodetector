#!/usr/bin/env bash
# =============================================================================
# make_package.sh — 将本项目打包为可分发压缩包
#
# 用法:
#   bash work/tools/make_package.sh [输出路径]
#     默认输出: <仓库根>/devsim_tcad_research_package.tar.gz
#
# 行为:
#   - 按 work/tools/package_exclude.txt 排除「可再生大产物 + 版本控制/缓存元数据」
#   - 生成 SHA256 校验和（<归档>.sha256）
#   - 打印体积、条目数与校验和，便于分发时核对完整性
#
# 说明: 排除后体积约 40MB（未排除时 work/ 单目录即 944MB）。被排除的场数据
#       (.vtu/.tec) 与日志均可由 work/tools/run_phase.sh 重跑再生。
# =============================================================================
set -uo pipefail

TOOLS="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$TOOLS/../.." && pwd)"
EXCLUDE="$TOOLS/package_exclude.txt"
OUT="${1:-$ROOT/devsim_tcad_research_package.tar.gz}"

[[ -f "$EXCLUDE" ]] || { echo "错误: 找不到排除清单 $EXCLUDE"; exit 1; }

cd "$ROOT" || exit 1
echo "打包根目录 : $ROOT"
echo "排除清单   : $EXCLUDE"
echo "输出归档   : $OUT"
echo "-------------------------------------------"

# 归档内使用相对路径（./...），排除清单中的模式据此匹配。
# 先在仓库外的临时目录构建，避免 tar 因归档写入本目录而报
# "file changed as we read it"；tar 退出码 1 = 部分文件读取时变化（非致命警告），
# 仅 >=2 视为失败。
BUILD_TMP="$(mktemp -d)"
STAGE="$BUILD_TMP/package.tar.gz"
tar --exclude-from="$EXCLUDE" -czf "$STAGE" .
rc=$?
if [[ $rc -ge 2 ]]; then
  echo "打包失败 (tar exit=$rc)"
  rmdir "$BUILD_TMP" 2>/dev/null
  exit 1
fi
[[ $rc -eq 1 ]] && echo "提示: tar 报告有文件在读取时发生变化（非致命，已忽略）"

mv "$STAGE" "$OUT" || { echo "归档移入失败"; exit 1; }
rmdir "$BUILD_TMP" 2>/dev/null   # 仅能删空目录，安全

# 校验和必须写 **basename**（而非绝对路径），否则接收方在自己机器上
# 执行 sha256sum -c 会因路径不存在而失败。子 shell 中 cd 不影响当前目录。
(
  cd "$(dirname "$OUT")" &&
  sha256sum "$(basename "$OUT")" >"$(basename "$OUT").sha256"
) || { echo "校验和生成失败"; exit 1; }

SIZE=$(du -h "$OUT" | cut -f1)
COUNT=$(tar -tzf "$OUT" | wc -l)
SUM=$(awk '{print $1}' "$OUT.sha256")

echo "完成 ✓"
echo "  归档    : $OUT"
echo "  体积    : $SIZE"
echo "  条目数  : $COUNT"
echo "  SHA256  : $SUM"
echo "  校验文件: $OUT.sha256（已写 basename，可与归档同目录任意搬移）"
echo ""
echo "接收方校验与解压（两个文件放同一目录）:"
echo "  sha256sum -c $(basename "$OUT").sha256"
echo "  mkdir devsim_tcad && tar -xzf $(basename "$OUT") -C devsim_tcad"
