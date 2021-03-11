# TS Front-end

## Get started
1. Bash `curl -sL https://deb.nodesource.com/setup_12.x | bash - `
2. Bash `sudo apt-get install nodejs`
3. Bash `npm install -g @vue/cli  # choose typescript and unchoose babel`
4. Bash `npm install`
5. Bash `npm install --save echarts`

## How to use

1. Edit `./src/components/Test.vue`
2. Bash `npm run fe-serve`
3. Launch [backend](../backend/README.md)
4. Open `http://localhost:8001`

## How to develop

1. Build apache2: `https://blog.csdn.net/qq_16166591/article/details/93797976`
2. Bash `npm run fe-build`
3. Bash `sudo rm -rf /var/www/html`
4. Bash `sudo mv ./dist /var/www/html`
5. Bash `sudo service apache2 restart`
6. Launch [backend](../backend/README.md)
7. Open `http://localhost:8001`

## blog about <a-button>
https://blog.csdn.net/weixin_43583693/article/details/101296700
