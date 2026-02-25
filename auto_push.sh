#!/bin/bash

# 1. 本地生成静态文件
echo "正在构建 Hugo 站点..."
hugo --minify

# 2. 定义变量
REMOTE_USER="root"
REMOTE_IP="154.44.21.204"
REMOTE_PORT="30405"
REMOTE_DIR="/var/www/zbw_site"

# 3. 同步文件到 VPS
# -e "ssh -p $REMOTE_PORT" 用于指定非标准 SSH 端口
echo "正在通过端口 $REMOTE_PORT 同步文件到 VPS..."
rsync -avz --delete -e "ssh -p $REMOTE_PORT" public/ ${REMOTE_USER}@${REMOTE_IP}:${REMOTE_DIR}/

echo "部署完成！"