FROM oven/bun:1

WORKDIR /app

COPY package.json /app

RUN bun install

COPY . /app

RUN bun run build

CMD ["bun", ".output/server/index.mjs"] 