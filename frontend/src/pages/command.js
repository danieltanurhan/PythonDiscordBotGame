import React from "react";

const Commands = () => {
  const commandData = [
    {
      title: "Basic Commands",
      commands: [
        {
          name: "/help",
          description: "Get this list of commands using the bot.",
        },
        {
          name: "/fish",
          description: "Catch some fish! This is the main command of the bot.",
        },
        {
          name: "/shop",
          description: "Shop for upgrades to buy using the /buy command.",
        },
        {
          name: "/profile",
          description: "View you or another user's profile.",
        },
        {
          name: "/sell",
          description: "Sell fish you've caught for virtual money.",
        },
        { name: "/daily", description: "Get your daily reward." },
        {
          name: "/coinflip",
          description: "Flip a coin to have a chance at doubling your money.",
        },
      ],
    },
    {
      title: "Progression",
      commands: [
        {
          name: "/color",
          description:
            "Sets the color of the embeds the bot responds to you with.",
        },
        { name: "/pos", description: "See your position on leaderboards." },
        { name: "/top", description: "Check out the leaderboards." },
        {
          name: "/servertop",
          description: "Shows a leaderboard for the current server you're in.",
        },
        {
          name: "/prestige",
          description: "Reset your progress for permanent powerful buffs.",
        },
        {
          name: "/pets",
          description: "View current pets you own or select a pet to use.",
        },
      ],
    },
    {
      title: "Information",
      commands: [
        {
          name: "/clan",
          description:
            "If you are clanless, it displays a help command for clans. If you are in a clan, you will see your clan menu.",
        },
        {
          name: "/info",
          description:
            "Information about the bot. This shows things such as total servers and who made the bot.",
        },
        {
          name: "/invite",
          description:
            "Get a link to the official server, and a link to invite the bot to your servers.",
        },
        { name: "/vote", description: "Get a voting link." },
        {
          name: "/donate",
          description:
            "Support the development of the bot and receive donator perks.",
        },
      ],
    },
    {
      title: "Extra",
      commands: [
        {
          name: "/biome",
          description:
            "Switch biomes, or view a list of biomes you have unlocked.",
        },
        {
          name: "/bait",
          description:
            "Select your bait. You can buy different types of bait with /shop bait.",
        },
        {
          name: "/rod",
          description:
            "Select a different rod to use. You can buy different rods with /shop rods.",
        },
        {
          name: "/quests",
          description: "List of quests. Quests reset daily at midnight GMT.",
        },
        {
          name: "/buffs",
          description:
            "See your current multipliers. This is affected by things such as bait and upgrades.",
        },
        { name: "/balance", description: "Check your balance." },
        {
          name: "/boosts",
          description:
            "Check your currently active boosts. This also shows the duration left on global boosts, if there is any.",
        },
        {
          name: "/boosters",
          description: "Check how many personal and global boosters you have.",
        },
        {
          name: "/charms",
          description:
            "Charms increase many different stats and are found in chests when you are above level 20.",
        },
        {
          name: "/settings",
          description:
            "Allows you to customize various aspects of the bot to your liking.",
        },
        {
          name: "/badge",
          description:
            "View your currently owned badges, or switch to a different badge.",
        },
      ],
    },
  ];

  return (
    <div>
      {commandData.map((section) => (
        <div>
          <h2>{section.title}</h2>
          {section.commands.map((action) => (
            <p>
              <span>{action.name}</span> - {action.description}
            </p>
          ))}
        </div>
      ))}
    </div>
  );
};

export default Commands;
