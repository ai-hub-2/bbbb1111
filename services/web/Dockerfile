FROM alpine:3.20 AS build
RUN apk add --no-cache imagemagick
WORKDIR /work
COPY /web /work
# Generate icons if missing
RUN mkdir -p /work/icons && \
	if [ ! -f /work/icons/icon-192.png ]; then \
	echo 'convert -size 192x192 xc:\#0d9488 -gravity center -pointsize 72 -fill white -annotate 0 "A" icon-192.png' > /tmp/mk.sh && sh /tmp/mk.sh && mv icon-192.png /work/icons/icon-192.png; \
	fi && \
	if [ ! -f /work/icons/icon-512.png ]; then \
	echo 'convert -size 512x512 xc:\#0d9488 -gravity center -pointsize 192 -fill white -annotate 0 "A" icon-512.png' > /tmp/mk2.sh && sh /tmp/mk2.sh && mv icon-512.png /work/icons/icon-512.png; \
	fi

FROM nginx:1.27-alpine
COPY /services/web/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /work /usr/share/nginx/html
EXPOSE 8080
CMD ["nginx", "-g", "daemon off;"]