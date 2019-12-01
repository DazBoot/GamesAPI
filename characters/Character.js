const { characters } = require("./data");

class Character {
  static all() {
    return characters;
  }
}

module.exports = {
  Character,
};
