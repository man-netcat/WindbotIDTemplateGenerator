import pandas as pd
import re
import sys


def main():
    if len(sys.argv) != 3:
        print("usage: python3 templategen.py [executorname] [ydk path]")
        exit(1)

    executorname = sys.argv[1]

    ydkfile = sys.argv[2]

    sheet_id = "1LmaojiWWhDxuKO8kFNfGH7tCOO5fuy4hjAC5WNDN4gg"
    sheet_name = "Sheet1"
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
    df = pd.read_csv(url)

    ids = set()
    with open(ydkfile, "r") as f:
        for line in f.readlines():
            if line.strip().isdigit():
                ids.add(int(line.strip()))

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
        public {executorname}Executor(GameAI ai, Duel duel) :
            base(ai, duel)
        {{
""")
    for id in ids:
        cardname = df[df['Omega id'] == id]['name.1']
        namestring = cardname.to_string(index=False)
        print(f"            public const int {clean(namestring)} = {id};")
    print(f"""
        }}
    }}
}}
""")


if __name__ == '__main__':
    main()
