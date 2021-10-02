import pandas as pd
import re
import sys
import sqlite3


def main():
    if len(sys.argv) != 3:
        print("usage: python3 templategen.py [executorname] [ydk path]")
        exit(1)

    executorname = sys.argv[1]
    ydkfile = sys.argv[2]
    con = sqlite3.connect('cards.cdb')

    ids = set()
    with open(ydkfile, "r") as f:
        for line in f.readlines():
            if line == "!side":
                break
            if line.strip().isdigit():
                ids.add(int(line.strip()))

    df = pd.read_sql_query(
        f"SELECT * FROM texts WHERE id IN {tuple(ids)}", con)
    df = df.sort_values(by='name')

    def clean(varStr): return re.sub('\W|^(?=\d)', '', varStr)

    print(f"""
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
        {{""")
    for index, row in df.iterrows():
        print(
            f"            public const int {clean(row['name'])} = {row['id']};")
    print(f"""        }}
        public {executorname}Executor(GameAI ai, Duel duel) :
            base(ai, duel)
        {{            
        }}
    }}
}}
""")


if __name__ == '__main__':
    main()
