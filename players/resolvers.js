const { Player } = require("./Player");

const resolvers = {
  Query: {
    players: () => Player.all(),
    player: (args) =>  {
      var players = Player.all()
      var output = [];
      for (var i = 0; i < players.length; i++) {
        if(players[i].names == args.name)
          output.push(players[i]);
      }
      return output;
    }
  },
};

module.exports = {
  resolvers,
}
