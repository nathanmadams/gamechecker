# gamechecker

Things you'll need:

1. A Twilio account and phone number
2. A server with internet access running docker and git
3. Your sessionId cookie value from play.boardgamecore.net
4. A phone that can receive SMS messages

To run:

1. Clone the repo onto your server with `git clone git@github.com:nathanmadams/gamechecker.git`
2. `cd gamechecker`
3. `cp example-config.yaml config.yaml`
4. Edit `config.yaml` with your account information
5. Run `docker build -t gamechecker .`
6. Run `docker run -d --restart=always gamechecker`

You can just run `docker run gamechecker` to test it without running the container as a daemon.
