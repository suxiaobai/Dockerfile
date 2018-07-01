FROM docker-registry.easemob.com/kefu/centos:7.3
COPY ./docker-entrypoint.py /
RUN chmod +x /docker-entrypoint.py && groupadd -g 500 easemob && useradd -u 500 -g easemob easemob && \
    yum install -y unzip wget make gcc pcre-devel openssl-devel GeoIP-devel && \
    mkdir /usr/local/nginx && cd /usr/local/nginx && \
    wget https://github.com/weibocom/nginx-upsync-module/archive/master.zip && \
    wget https://nginx.org/download/nginx-1.10.3.tar.gz && \
    wget http://luajit.org/download/LuaJIT-2.0.5.tar.gz && \
    wget https://github.com/openresty/lua-nginx-module/archive/v0.10.2.tar.gz && \
    tar zxf nginx-1.10.3.tar.gz && unzip master.zip && \
    tar -xzvf v0.10.2.tar.gz && \
    tar zxf LuaJIT-2.0.5.tar.gz && \
    cd LuaJIT-2.0.5 && make PREFIX=/usr/local/luajit && make install PREFIX=/usr/local/luajit && cd .. && \
    echo "export LUAJIT_LIB=/usr/local/luajit/lib" >> /etc/profile && \
    echo "export LUAJIT_INC=/usr/local/luajit/include/luajit-2.0" >> /etc/profile && \
    . /etc/profile && cd nginx-1.10.3 && \
        ./configure \
        --prefix=/home/easemob/apps/opt/nginx \
        --conf-path=/home/easemob/apps/config/nginx/nginx.conf \
        --user=easemob \
        --group=easemob \
        --pid-path=/home/easemob/apps/var/nginx/nginx.pid \
        --error-log-path=/home/easemob/apps/log/nginx/error.log \
        --http-log-path=/home/easemob/apps/log/nginx/access.log \
        --sbin-path=/home/easemob/apps/opt/nginx/sbin/nginx \
        --lock-path=/home/easemob/apps/var/nginx/nginx.lock \
        --http-client-body-temp-path=/home/easemob/apps/var/nginx/client_temp \
        --http-proxy-temp-path=/home/easemob/apps/var/nginx/proxy_temp \
        --http-fastcgi-temp-path=/home/easemob/apps/var/nginx/fastcgi_temp \
        --http-uwsgi-temp-path=/home/easemob/apps/var/nginx/uwsgi_temp \
        --http-scgi-temp-path=/home/easemob/apps/var/nginx/scgi_temp \
        --with-http_geoip_module \
        --with-http_ssl_module \
        --with-http_realip_module \
        --with-http_addition_module \
        --with-http_sub_module \
        --with-http_dav_module \
        --with-http_flv_module \
        --with-http_mp4_module \
        --with-http_gunzip_module \
        --with-http_gzip_static_module \
        --with-http_random_index_module \
        --with-http_secure_link_module \
        --with-http_stub_status_module \
        --with-stream \
        --with-stream_ssl_module \
        --with-file-aio \
        --without-mail_pop3_module \
        --without-mail_imap_module \
        --without-mail_smtp_module \
        --with-ld-opt="-Wl,-rpath,/usr/local/luajit/lib" \
        --add-module=/usr/local/nginx/lua-nginx-module-0.10.2 \
        --add-module=/usr/local/nginx/nginx-upsync-module-master && \
        make && make install &&  mkdir /data && ln -s /home/easemob/apps /data/apps && \
    mkdir /home/easemob/apps/config/nginx/conf.d && \
    echo "export PATH=$PATH:/data/apps/opt/nginx/sbin" >> /etc/profile

EXPOSE 80 443
ENTRYPOINT ["/docker-entrypoint.py"]
CMD ["-O","start"]