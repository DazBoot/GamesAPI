const { gql } = require("apollo-server");

const typeDef = gql`
  type Player {
    name: String
    region: String
    characters: [String]
  }

  extend type Query {
    players: [Player]
    player: Player
  }
`;

module.exports = {
  typeDef
};
