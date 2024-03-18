const { Client, GatewayIntentBits } = require("discord.js");
const axios = require("axios");
require("dotenv").config();

const client = new Client({ intents: [GatewayIntentBits.Guilds] });
const endpoint = (query) => `http://localhost:5000/ask?query=${query}`;

client.once("ready", () => {
  console.log("CPSync is online!");
});

client.on("interactionCreate", async (interaction) => {
  if (!interaction.isCommand()) return;

  const { commandName } = interaction;

  if (commandName === "ask") {
    const query = interaction.options.getString("query");
    await interaction.deferReply();
    axios
      .get(endpoint(query))
      .then((response) => interaction.editReply(response.data.answer))
      .catch((error) => interaction.editReply(`Error: ${error.message}`));
  }
});

client.login(process.env.DISCORD_TOKEN);
