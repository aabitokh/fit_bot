docker build -t fit_bot_app .

docker run --rm -v "$(pwd):/app" fit_bot_app