const { Character } = require("./Character");

const resolvers = {
  Query: {
    characters: () => Character.all(),
  },
};

module.exports = {
  resolvers,
}
