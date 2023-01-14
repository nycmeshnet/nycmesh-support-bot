
# NYC Mesh Support Bot
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]

Slack chatbot to help with NYC Mesh support requests

## Usage

Use the included CLI to run the server like so:
```shell
supportbot-server
```

The server connects to the Slack API via websockets, bypassing the need for a public IP / port.

## Getting Started

### Running with Docker

- install [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- start Docker Desktop
- clone the repo and open a shell in the root folder
- ensure you have a .env file with all required credentials
- run the following commands:
```shell
docker build . -t supportbot
docker run --name nycmesh-support-bot --rm -v "$PWD/.env:/app/.env" supportbot
```

### Testing with Docker
 
- follow the directions above for running
- run the following commands:
```shell
docker build . -t supportbot
docker run -v "$PWD/.env:/app/.env" --rm nycmesh-support-bot-test pytest
```

### Prerequisites
You'll need `python` and `pip` to install this client. Confirm these are available with:
```shell
python3 --version
python3 -m pip --version
```

If not, install them using the appropriate instructions for your OS [here](https://www.python.org/downloads/)

### Installation

To install the `supportbot-server` command, do the following:

```shell
git clone https://github.com/andybaumgar/nycmesh-support-bot.git
cd nycmesh-support-bot/
```

A virtual environment is optional but recommended:
```shell
python3 -m venv venv
source venv/bin/activate
```

Finally, install this package with
```shell
pip install -e .
```

### Credentials

The bot needs Slack API credentials to operate. They are supplied in the .env file.

You can obtain credentials for a Slack workspace by creating a socket-mode app following
[these instructions](https://api.slack.com/apis/connections/socket).

### Usage

```shell
> supportbot-server
Starting bolt app...
Bolt app is running!
```

## Autoreload (Linux and Mac)
- install [entr](https://github.com/eradman/entr)
- `find . -name \*.py -print | entr -r supportbot-server`

### CLI Arguments

The `supportbot-server` command is configurable via a few CLI arguments. Use 
`supportbot-server --help` to learn more about the available options.

## Deploy Process

The supportbot uses GitHub Actions Docker and DockerHub for CI/CD. The [GitHub Actions workflow file](/.github/workflows/ci.yml) describes the process.

### Dockerhub
Dockerhub is used as an image registry to store our built code before deployment.

## Secrets

Secrets are stored in GitHub Secrets, and locally in a `.env` file. In production a [script](env_json_to_dotenv.py) is used to convert the GitHub Secrets to `.env`.

### GitHub Actions/Runner setup

[Github Actions Self Hosted Runner setup description](https://docs.github.com/en/actions/hosting-your-own-runners/adding-self-hosted-runners)

#### Starting and Stopping the Runner
An extra command is used to setup the runner as a service:
```
cd /home/supportbot/actions-runner
sudo ./svc.sh start
```



## Built With

* [Python](https://python.org)
* [Click](https://click.palletsprojects.com/)
* [Slack Bolt for Python](https://slack.dev/bolt-python/concepts)

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See the `LICENSE` file for more information.

## Contact
 - Andrew Dickinson - andrew.dickinson.0216@gmail.com
 - Andy Baumgar - andybaumgar@gmail.com
 - Daniel Heredia - daniel@nycmesh.net
 - Marg Suarez - margsuarez@gmail.com

Project Link: [https://github.com/andybaumgar/nycmesh-support-bot](https://github.com/andybaumgar/nycmesh-support-bot)

## Acknowledgments

* [The Best README Template](https://github.com/othneildrew/Best-README-Template)

[contributors-shield]: https://img.shields.io/github/contributors/andybaumgar/nycmesh-support-bot.svg
[contributors-url]: https://github.com/andybaumgar/nycmesh-support-bot/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/andybaumgar/nycmesh-support-bot.svg
[forks-url]: https://github.com/andybaumgar/nycmesh-support-bot/network/members
[stars-shield]: https://img.shields.io/github/stars/andybaumgar/nycmesh-support-bot.svg
[stars-url]: https://github.com/andybaumgar/nycmesh-support-bot/stargazers
[issues-shield]: https://img.shields.io/github/issues/andybaumgar/nycmesh-support-bot.svg
[issues-url]: https://github.com/andybaumgar/nycmesh-support-bot/issues
[license-shield]: https://img.shields.io/github/license/andybaumgar/nycmesh-support-bot.svg
[license-url]: https://github.com/andybaumgar/nycmesh-support-bot/blob/master/LICENSE.txt
