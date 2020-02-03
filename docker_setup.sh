docker build . -t base-coder-bot
docker run -d --restart always --name base-coder-bot base-coder-bot
