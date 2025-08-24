import sys
from Calcrate import Calcrate

if __name__ == "__main__":

    cal = Calcrate()

    cal.データ入力()
    NEQ = cal.SkYマトリックス(0)
    cal.分布荷重振り分け()
    cal.外力add()
    cal.decomp(NEQ)
    cal.redbak(NEQ)
    cal.変位計算()

    cal.結果出力()

    print("解析が終わりました")