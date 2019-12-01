const { players } = require("./data");

class Player {
  static all() {
    return players;
  }
}

module.exports = {
  Player,
};
