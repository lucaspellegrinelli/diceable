<br/>
<p align="center">
  <h1 align="center">Diceable</h1>

  <p align="center">
    A discord bot to roll dice with animation/effects with OBS integration
  </p>

  <p align="center">
    <a href="https://bot.togarashi.app/">Access diceable</a>
  </p>
</p>

## About The Project

https://github.com/lucaspellegrinelli/diceable/assets/19651296/76a50418-241b-4ecc-8e88-37667552a145

Diceable is a project I over engineered to help a friend that wanted to play a table top RPG with his friends.

He wanted a bot that he could add to his discord that would allow him or his players to roll dice throughout the game with rolling animations on discord. But he also wanted these dice rolls to show up on this OBS stream so it was easier to see and would allow the recording of the game to be better, so this project was born.

With time we also added a way to customize the way the dice for each player would look as well as adding a cool effect when rolling dice to make epic moments even more epic. 

## Running locally

### Prerequisites

* [Docker](https://www.docker.com/)

### Installation

You need to create a `.env` file in each of the subprojects [discordbot](https://github.com/lucaspellegrinelli/diceable/tree/main/discordbot), [frontend](https://github.com/lucaspellegrinelli/diceable/tree/main/frontend) and [pubsub](https://github.com/lucaspellegrinelli/diceable/tree/main/pubsub).

In each of the projects there's a `.env.example` to help you with that.

With all the `.env` files created and configured, you can run `docker compose up` to run the project.

## License

Distributed under the Apache License 2.0. See [LICENSE](https://github.com/lucaspellegrinelli/diceable/blob/main/LICENSE) for more information.
