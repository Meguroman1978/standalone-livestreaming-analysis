FROM nginx:1.25-alpine

# デフォルトのNginx設定を削除
RUN rm /etc/nginx/conf.d/default.conf

# カスタム設定をコピー
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 静的ファイルをNginxの公開ディレクトリへコピー
COPY index.html /usr/share/nginx/html/index.html
COPY README.md  /usr/share/nginx/html/README.md

EXPOSE 8080

CMD ["nginx", "-g", "daemon off;"]
