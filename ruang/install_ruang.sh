#!/usr/bin/env bash
# ==============================================================================
# Ruang 3D Virtual Office - Automated Installer Script
# Upstream Project: github.com/yugienugraha/ruang
# ==============================================================================

set -euo pipefail

echo "==========================================================="
echo "🏢 RUANG 3D VIRTUAL OFFICE INSTALLER FOR OMNI-AGENT OS"
echo "==========================================================="

INSTALL_DIR="${HOME}/.local/share/ruang"
BIN_DIR="${HOME}/.local/bin"

mkdir -p "${BIN_DIR}"
export PATH="${BIN_DIR}:${PATH}"

# Check Node.js >= 20
if ! command -v node >/dev/null 2>&1 || [ "$(node -v | cut -d'v' -f2 | cut -d'.' -f1)" -lt 20 ]; then
    echo "⚠️  Node.js 20+ tidak ditemukan. Mengunduh installer resmi Ruang..."
    curl -fsSL https://raw.githubusercontent.com/yugienugraha/ruang/main/install.sh | bash -s -- --service
else
    echo "✔ Node.js terdeteksi: $(node -v)"
    curl -fsSL https://raw.githubusercontent.com/yugienugraha/ruang/main/install.sh | bash -s -- --service
fi

echo ""
echo "🎉 Ruang 3D Virtual Office berhasil dipasang!"
echo "Akses kantor virtual Anda di: http://127.0.0.1:3001"
