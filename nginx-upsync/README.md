### nginx 1.10.3 + upsync + lua

1. simple example
    
    docker run -d -p 80:80 -p 443:443 --name "nginx" nginx-upsync
   
2. env

   | env | 备注|
   | ----| ----|
   |host|     consul host addr, default 127.0.0.1|
   |port |    consul port number, default 8500
   |upsfile|  upstream config path, default /data/apps/config/nginx/conf.d/dyups.upstream.kefu.eaemob.com.conf|
   
3. reload
   
    docker exec -ti nginx /docker-entrypoint.py -O reload
> * get consul service and reload nginx。
