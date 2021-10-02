import os
import re
import sqlite3
import sys

import pandas as pd


def ydk_to_idlist(ydkfile):
    idlist = set()

    with open(ydkfile, "r") as f:
        for line in f.readlines():
            if "!side" in line:
                break
            if line.strip().isdigit():
                idlist.add(int(line.strip()))

    return idlist


def clean_cardname(cardname):
    cardname = re.sub('\W|^(?=\d)', '', cardname)
    if cardname[0].isdigit():
        cardname = "_" + cardname
    return cardname


def main():
    if len(sys.argv) != 3:
        print("usage: python3 templategen.py [executorname] [ydk path]")
        exit(1)

    executorname = sys.argv[1]
    ydkfile = sys.argv[2]

    if not os.path.exists(ydkfile):
        print("YDK file not found.")
        exit(1)

    if not os.path.exists('./cards.cdb'):
        print("Put cards.cdb next to this script.")
        exit(1)

    con = sqlite3.connect('cards.cdb')
    idlist = ydk_to_idlist(ydkfile)

    df = pd.read_sql_query(
        f"SELECT id, name FROM texts WHERE id IN {tuple(idlist)}", con)
    df = df.sort_values(by='name')

    with open(f"{executorname}Executor.cs", "w") as f:
        f.write(f"""
using System.Collections.Generic;
using System.Linq;
using WindBot;
using WindBot.Game;
using WindBot.Game.AI;
using YGOSharp.OCGWrapper.Enums;

namespace WindBot.Game.AI.Decks
{{
    [Deck("{executorname}", "AI_{executorname}")]
    public class {executorname}Executor : DefaultExecutor
    {{
        public class CardId
        {{\n""")
        for _, card in df.iterrows():
            f.write(
                f"            public const int {clean_cardname(card['name'])} = {card['id']};\n")
        f.write(f"""        }}
        public {executorname}Executor(GameAI ai, Duel duel) :
            base(ai, duel)
        {{            
        }}
    }}
}}
""")


if __name__ == '__main__':
    main()
