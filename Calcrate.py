import sys
import pandas
import math
import traceback
import numpy as np
import codecs
from FEMUtils import FEMUtils

class Calcrate:

    def __init__(self):

        self.入力シート名1 = "入力"
        self.入力シート名2 = "入力2"
        self.出力シート名 = "計算・出力"

        self.配列上限 = 1285200
        self.MAX節点 = 1000
        self.MAX材料 = 1000
        self.MAX要素 = 1000
        self.MAX集中荷重 = 6000
        self.MAX分布荷重 = 1000
        self.MAX拘束条件 = 1000

        self.節点数       = 0
        self.節点X        = np.zeros( self.MAX節点,         dtype=float)
        self.節点Y        = np.zeros( self.MAX節点,         dtype=float)
        self.節点Z        = np.zeros( self.MAX節点,         dtype=float)

        self.材料数       = 0
        self.弾性係数     = np.zeros( self.MAX材料,         dtype=float)
        self.gk           = np.zeros( self.MAX材料,         dtype=float)
        self.断面積       = np.zeros( self.MAX材料,         dtype=float)
        self.yi           = np.zeros( self.MAX材料,         dtype=float)
        self.zi           = np.zeros( self.MAX材料,         dtype=float)

        self.要素数       = 0
        self.要素節点     = np.zeros((self.MAX要素, 2),     dtype=int)
        self.要素材料     = np.zeros( self.MAX要素,         dtype=int)
        self.fai          = np.zeros( self.MAX要素,         dtype=float)

        self.集中荷重数   = 0
        self.集中荷重節点 = np.zeros( self.MAX集中荷重,     dtype=int)
        self.fx           = np.zeros( self.MAX集中荷重,     dtype=float)
        self.fy           = np.zeros( self.MAX集中荷重,     dtype=float)
        self.fz           = np.zeros( self.MAX集中荷重,     dtype=float)
        self.fmx          = np.zeros( self.MAX集中荷重,     dtype=float)
        self.fmy          = np.zeros( self.MAX集中荷重,     dtype=float)
        self.fmz          = np.zeros( self.MAX集中荷重,     dtype=float)

        self.拘束条件数   = 0
        self.拘束条件節点 = np.zeros( self.MAX拘束条件,     dtype=int)
        self.nxfx         = np.zeros( self.MAX拘束条件,     dtype=int)
        self.nyfx         = np.zeros( self.MAX拘束条件,     dtype=int)
        self.nzfx         = np.zeros( self.MAX拘束条件,     dtype=int)
        self.mxfx         = np.zeros( self.MAX拘束条件,     dtype=int)
        self.myfx         = np.zeros( self.MAX拘束条件,     dtype=int)
        self.mzfx         = np.zeros( self.MAX拘束条件,     dtype=int)

        self.分布荷重数   = 0
        self.分布荷重節点 = np.zeros((self.MAX分布荷重, 2), dtype=int)
        self.wx           = np.zeros( self.MAX分布荷重,     dtype=float)
        self.wy           = np.zeros( self.MAX分布荷重,     dtype=float)
        self.wz           = np.zeros( self.MAX分布荷重,     dtype=float)

        self.iD           = np.zeros((6, self.MAX節点),     dtype=int) 
        self.SE           = np.zeros( 78,                   dtype=float)
        self.AjCB         = np.zeros( self.配列上限,        dtype=float)
        self.変位         = np.zeros((self.MAX節点, 6),     dtype=float)
        self.FORCE        = np.zeros( 6 * self.MAX節点,     dtype=float)
        self.MHT          = np.zeros( 6 * self.MAX節点,     dtype=int)
        self.MAXA         = np.zeros( 6 * self.MAX節点 + 1, dtype=int)
        self.Ek           = np.zeros((12, 12),              dtype=float) 
        self.kTR1         = np.zeros( self.MAX要素,         dtype=str)
        self.kTR2         = np.zeros( self.MAX要素,         dtype=str)

        self.N   = np.zeros((self.MAX要素, 2), dtype=float)  
        self.Qy  = np.zeros((self.MAX要素, 2), dtype=float)  
        self.Qz  = np.zeros((self.MAX要素, 2), dtype=float)  
        self.Mx  = np.zeros((self.MAX要素, 2), dtype=float)  
        self.My  = np.zeros((self.MAX要素, 2), dtype=float)  
        self.Mz  = np.zeros((self.MAX要素, 2), dtype=float)  

    ############################################################
    ##     ３次元　手動入力作成データよりデータを読み込む     ##
    ##          　　　  ** iNPUTX.for **                      ##
    ############################################################
    def データ入力(self):

        try:
            filename = self.入力シート名1+'.xlsx'
            data = pandas.read_excel(filename, header=None)
            Range = data.values
        except:
            traceback.print_exc()
            sys.exit(self.入力シート名1+".xlsx の読み込みに失敗しました。")

        self.節点数 = int(Range[2][1])
        self.材料数 = int(Range[2][5])
        self.要素数 = int(Range[2][11])

        for i in range(self.節点数):
            self.節点X[i]       = float(Range[5+i][0])
            self.節点Y[i]       = float(Range[5+i][1])
            self.節点Z[i]       = float(Range[5+i][2])

        for i in range(self.材料数):
            self.弾性係数[i]    = float(Range[5+i][4])
            self.gk[i]          = float(Range[5+i][5])
            self.断面積[i]      = float(Range[5+i][6])
            self.yi[i]          = float(Range[5+i][7])
            self.zi[i]          = float(Range[5+i][8])

        for i in range(self.要素数):
            self.要素節点[i][0] = int(Range[5+i][10])
            self.要素節点[i][1] = int(Range[5+i][11])
            self.要素材料[i]    = int(Range[5+i][12])
            k1x = int(Range[5+i][13])
            k1y = int(Range[5+i][14])
            k1z = int(Range[5+i][15])
            k2x = int(Range[5+i][16])
            k2y = int(Range[5+i][17])
            k2z = int(Range[5+i][18])
            self.fai[i]         = float(Range[5+i][19])

            k1 = k1x + k1y + k1z
            k2 = k2x + k2y + k2z

            if   k1 == 0:
                self.kTR1[i] = "0"
            elif k1 == 1:
                if k1x == 1: self.kTR1[i] = "1"
                if k1y == 1: self.kTR1[i] = "2"
                if k1z == 1: self.kTR1[i] = "3"
            elif k1 == 2:
                if k1x == 1 and k1y == 1: self.kTR1[i] = "4"
                if k1y == 1 and k1z == 1: self.kTR1[i] = "5"
                if k1z == 1 and k1x == 1: self.kTR1[i] = "6"
            elif k1 == 3:
                self.kTR1[i] = "7"

            if   k2 == 0:
                self.kTR2[i] = "0"
            elif k2 == 1:
                if k2x == 1: self.kTR2[i] = "1"
                if k2y == 1: self.kTR2[i] = "2"
                if k2z == 1: self.kTR2[i] = "3"
            elif k2 == 2:
                if k2x == 1 and k2y == 1: self.kTR2[i] = "4"
                if k2y == 1 and k2z == 1: self.kTR2[i] = "5"
                if k2z == 1 and k2x == 1: self.kTR2[i] = "6"
            elif k2 == 3:
                self.kTR2[i] = "7"

        self.拘束条件数 = int(Range[2][22])
        self.集中荷重数 = int(Range[2][30])
        self.分布荷重数 = int(Range[2][38])

        for i in range(self.拘束条件数):
            self.拘束条件節点[i]    = int(Range[6+i][21])
            self.nxfx[i]            = int(Range[6+i][22])
            self.nyfx[i]            = int(Range[6+i][23])
            self.nzfx[i]            = int(Range[6+i][24])
            self.mxfx[i]            = int(Range[6+i][25])
            self.myfx[i]            = int(Range[6+i][26])
            self.mzfx[i]            = int(Range[6+i][27])

        for i in range(self.集中荷重数):
            self.集中荷重節点[i]    =   int(Range[6+i][29])
            self.fx[i]              = float(Range[6+i][30])
            self.fy[i]              = float(Range[6+i][31])
            self.fz[i]              = float(Range[6+i][32])
            self.fmx[i]             = float(Range[6+i][33])
            self.fmy[i]             = float(Range[6+i][34])
            self.fmz[i]             = float(Range[6+i][35])

        for i in range(self.分布荷重数):
            self.分布荷重節点[i][0] =   int(Range[6+i][37])
            self.分布荷重節点[i][1] =   int(Range[6+i][38])
            self.wx[i]              = float(Range[6+i][39])
            self.wy[i]              = float(Range[6+i][40])
            self.wz[i]              = float(Range[6+i][41])

    ##################################
    ##     ３次元　外力を加える     ##
    ##       ** ADDFW.for **        ##
    ##################################
    def 外力add(self):

        for i in range(self.集中荷重数):

            j = self.集中荷重節点[i] - 1

            if self.fx[i] != 0:
                ii = self.iD[0][j] - 1 
                self.FORCE[ii] += self.fx[i]

            if self.fy[i] != 0:
                ii = self.iD[1][j] - 1
                self.FORCE[ii] += self.fy[i]

            if self.fz[i] != 0:
                ii = self.iD[2][j] - 1
                self.FORCE[ii] += self.fz[i]

            if self.fmx[i] != 0:
                ii = self.iD[3][j] - 1
                self.FORCE[ii] += self.fmx[i]

            if self.fmy[i] != 0:
                ii = self.iD[4][j] - 1
                self.FORCE[ii] += self.fmy[i]

            if self.fmz[i] != 0:
                ii = self.iD[5][j] - 1
                self.FORCE[ii] += self.fmz[i]

    ####################################################
    ##     トラス（０）　ラーメン（１）の結合状態     ##
    ##        self.kTR1[i] - self.kTR2[j)             ##
    ##                    x,y,z - x,y,z               ##
    ##             jj=4  (0,1,1 - 1,1,1)              ##
    ##             jj=5  (1,0,1 - 1,1,1)              ##
    ##     ３次元  jj=6  (1,1,0 - 1,1,1)              ##
    ##             jj=10 (1,1,1 - 0,1,1)              ##
    ##             jj=11 (1,1,1 - 1,0,1)              ##
    ##             jj=12 (1,1,1 - 1,1,0)              ##
    ##                ** ELkA1.for **                 ##
    ####################################################
    def elka1(self, jj):
        b = self.Ek[jj, :12] / self.Ek[jj, jj]  # 1x12 vector
        ek_col = self.Ek[:12, jj].reshape(12, 1)  # 12x1 vector
        self.Ek[:12, :12] -= ek_col * b  # broadcasting: (12x1) * (1x12) = (12x12)

    ####################################################
    ##     トラス（０）　ラーメン（１）の結合状態     ##
    ##        self.kTR1[i] - self.kTR2[j)             ##
    ##                    x,y,z - x,y,z               ##
    ##             j1=4  (0,1,1 - 0,1,1)              ##
    ##     ３次元  j1=5  (1,0,1 - 1,0,1)              ##
    ##             j1=6  (1,1,0 - 1,1,0)              ##
    ##                ** ELkA2.for **                 ##
    ####################################################
    def elka2(self, j1):
        j2 = j1 + 6

        bunbo1 = self.Ek[j1, j1] * self.Ek[j2, j2] - self.Ek[j2, j1] * self.Ek[j1, j2]
        bunbo2 = -bunbo1

        row_j1 = self.Ek[j1, :12]
        row_j2 = self.Ek[j2, :12]

        b1 = (self.Ek[j1, j2] * row_j2 - self.Ek[j2, j2] * row_j1) / bunbo1
        b2 = (self.Ek[j1, j1] * row_j2 - self.Ek[j2, j1] * row_j1) / bunbo2

        ek1 = self.Ek[:12, j1].reshape(-1, 1)  # shape (12,1)
        ek2 = self.Ek[:12, j2].reshape(-1, 1)  # shape (12,1)

        # Cộng từng hàng vector hóa cùng lúc
        self.Ek[:12, :12] += ek1 * b1 + ek2 * b2

    ####################################################
    ##     トラス（０）　ラーメン（１）の結合状態     ##
    ##        self.kTR1[i] - self.kTR2[j)             ##
    ##                    x,y,z - x,y,z               ##
    ##             jj=6  (0,0,1 - 1,1,1)              ##
    ##             jj=5  (0,1,0 - 1,1,1)              ##
    ##             jj=4  (1,0,0 - 1,1,1)              ##
    ##     ３次元  jj=12 (1,1,1 - 0,0,1)              ##
    ##             jj=11 (1,1,1 - 0,1,0)              ##
    ##             jj=10 (1,1,1 - 1,0,0)              ##
    ##                ** ELkA3.for **                 ##
    ####################################################
    def elka3(self, jj):
        # Bảng ánh xạ jj sang (j1, j2)
        mapping = {
            5:  (3, 4),
            4:  (3, 5),
            3:  (4, 5),
            11: (9, 10),
            10: (9, 11),
            9:  (10, 11)
        }
        if jj not in mapping:
            return
        j1, j2 = mapping[jj]

        bunbo1 = self.Ek[j1, j1] * self.Ek[j2, j2] - self.Ek[j2, j1] * self.Ek[j1, j2]
        bunbo2 = -bunbo1

        # Lấy các hàng tương ứng j1, j2
        row_j1 = self.Ek[j1, :12]
        row_j2 = self.Ek[j2, :12]

        b1 = (self.Ek[j1, j2] * row_j2 - self.Ek[j2, j2] * row_j1) / bunbo1
        b2 = (self.Ek[j1, j1] * row_j2 - self.Ek[j2, j1] * row_j1) / bunbo2

        ek1 = self.Ek[:12, j1].reshape(-1, 1)  # (12,1)
        ek2 = self.Ek[:12, j2].reshape(-1, 1)  # (12,1)

        self.Ek[:12, :12] += ek1 * b1 + ek2 * b2

    ####################################################
    ##     トラス（０）　ラーメン（１）の結合状態     ##
    ##        self.kTR1[i] - self.kTR2[j)             ##
    ##                    x,y,z - x,y,z               ##
    ##     ３次元  j=4   (0,0,0 - 1,1,1)              ##
    ##             j=10  (1,1,1 - 0,0,0)              ##
    ##                ** ELkA4.for **                 ##
    ####################################################
    def elka4(self, j):
        j1  = j
        j2  = j + 1
        j3  = j + 2
        A = self.Ek[np.ix_([j1, j2, j3], [j1, j2, j3])]
        B = self.Ek[np.ix_([j1, j2, j3], range(12))]

        # Phân tích giá trị
        b1, b2, b3 = A[0]
        b4, b5, b6 = A[1]
        b7, b8, b9 = A[2]

        bb1 = 1 / b9
        am1 = b1 - b3 * b7 * bb1
        am2 = b2 - b3 * b8 * bb1
        am3 = b4 - b6 * b7 * bb1
        am4 = b5 - b6 * b8 * bb1
        am  = 1 / (am1 * am4 - am3 * am2)
        s1  = -am4 * am
        s2  = am2 * am
        s3  = (b3 * am4 * bb1 - b6 * am2 * bb1) * am

        am  = 1 / (am2 * am3 - am4 * am1)
        t1  = -am3 * am
        t2  = am1 * am
        t3  = (b3 * am3 * bb1 - b6 * am1 * bb1) * am

        bm  = -am
        r1 = (b8 * am3 * bb1 + b7 * am4 * bb1 * bm)
        r2 = (-b7 * am2 * bb1 * bm - b8 * am1 * bb1 * am)
        bb2 = bb1 / b9
        rr1 = bb1 + b3 * b7 * bb2 * am4 * bm
        rr2 = b6 * b7 * bb2 * am2 * bm
        rr3 = b3 * b8 * bb2 * am3 * am
        rr4 = b6 * b8 * bb2 * am1 * am
        r3 = -rr1 + rr2 - rr3 + rr4

        # Tính hàng ma trận B đã nhân hệ số (s1, s2, s3) → bx, by, bz
        coeffs = np.array([
            [s1, s2, s3],
            [t1, t2, t3],
            [r1, r2, r3]
        ])
        result = coeffs @ B  # (3,3) @ (3,12) → (3,12)
        Ei_j = self.Ek[:12, [j1, j2, j3]]  # (12, 3)
        self.Ek[:12, :12] += Ei_j @ result  # (12,3) @ (3,12) = (12,12)

    ####################################################
    ##     トラス（０）　ラーメン（１）の結合状態     ##
    ##        self.kTR1[i] - self.kTR2[j)             ##
    ##                    x,y,z - x,y,z               ##
    ##     ３次元   j=1  (0,0,1 - 0,0,1)              ##
    ##              j=2  (0,1,0 - 0,1,0)              ##
    ##              j=3  (1,0,0 - 1,0,0)              ##
    ##                ** ELkA5.for **                 ##
    ####################################################
    def elka5(self, j):
        Ek = self.Ek
        indices = {
            0: (0, 1, 7, 8, 5, 11),
            1: (1, 2, 8, 9, 4, 10),
            2: (0, 2, 6, 9, 3, 9)
        }
        j1, j2, j3, j4, idx8, idx12 = indices[j]

        # Số lượng phần tử cần xử lý
        indices_base = [0, 1, 2, idx8, 6, 7, 8, idx12]

        # Tính toán hệ số s1
        s1 = 1.0 / (Ek[j1, j1] * Ek[j2, j2] - Ek[j2, j1] * Ek[j1, j2])

        # Tính các vector t5~t12 và v5~v12 một cách vector hóa
        t = (Ek[j1, j2] * Ek[j2, indices_base] - Ek[j2, j2] * Ek[j1, indices_base]) * s1
        v = (Ek[j2, j1] * Ek[j1, indices_base] - Ek[j1, j1] * Ek[j2, indices_base]) * s1

        # Tính smx, smy
        smx = Ek[j3, indices_base] + Ek[j3, j1] * t + Ek[j3, j2] * v
        smy = Ek[j4, indices_base] + Ek[j4, j1] * t + Ek[j4, j2] * v

        # Tính các hệ số phụ
        c2 = (-Ek[j2, j2] * Ek[j1, j3] + Ek[j1, j2] * Ek[j2, j3]) * s1
        c3 = (-Ek[j2, j2] * Ek[j1, j4] + Ek[j1, j2] * Ek[j2, j4]) * s1
        d2 = ( Ek[j2, j1] * Ek[j1, j3] - Ek[j1, j1] * Ek[j2, j3]) * s1
        d3 = ( Ek[j2, j1] * Ek[j1, j4] - Ek[j1, j1] * Ek[j2, j4]) * s1

        # Phần tử phụ
        sk11 = Ek[j3, j1]*c2 + Ek[j3, j2]*d2 + Ek[j3, j3]
        sk12 = Ek[j3, j1]*c3 + Ek[j3, j2]*d3 + Ek[j3, j4]
        sk21 = Ek[j4, j1]*c2 + Ek[j4, j2]*d2 + Ek[j4, j3]
        sk22 = Ek[j4, j1]*c3 + Ek[j4, j2]*d3 + Ek[j4, j4]

        skk = 1.0 / (sk11 * sk22 - sk21 * sk12)

        # Tính x3 và x4 (x35 ~ x312 và x45 ~ x412)
        x3 = (sk12 * smy - sk22 * smx) * skk
        x4 = (sk21 * smx - sk11 * smy) * skk

        # Tính x1 (x15~x112) và x2 (x25~x212)
        x1 = t + c2 * x3 + c3 * x4
        x2 = v + d2 * x3 + d3 * x4

        # Các vị trí cần gán
        skip = {
            0: {3, 4, 9, 10},
            1: {3, 5, 9, 11},
            2: {4, 5, 10, 11}
        }

        rows = [i for i in range(12) if i not in skip[j]]
        Ek_sub = Ek[np.ix_(rows, [j1, j2, j3, j4])]  # shape (len(rows), 4)

        update = (
            Ek_sub[:, 0:1] * x1 +
            Ek_sub[:, 1:2] * x2 +
            Ek_sub[:, 2:3] * x3 +
            Ek_sub[:, 3:4] * x4
        )
        Ek[np.ix_(rows, indices_base)] += update

        for k in (j1, j2, j3, j4):
            Ek[k, :] = 0
            Ek[:, k] = 0

    ##############################################################
    ##     ３次元　小軸力｛ｆ’｝＝［Ｋ’］＊［Ｔ］＊｛ｕ｝           ##
    ##                 　 ** FBUZAi.for **                      ##
    ##############################################################
    def fbuzai(self, jEL):

        ts  = np.zeros(( 3, 3), dtype=float)
        tf  = np.zeros(( 3, 3), dtype=float)
        te  = np.zeros(( 3, 3), dtype=float)
        t   = np.zeros((12,12), dtype=float)
        ek2 = np.zeros((12,12), dtype=float)

        i    = self.要素節点[jEL][0] - 1
        j    = self.要素節点[jEL][1] - 1
        M    = self.要素材料[jEL] - 1
        FAii = self.fai[jEL]
        DX   = self.節点X[j] - self.節点X[i]
        DY   = self.節点Y[j] - self.節点Y[i]
        DZ   = self.節点Z[j] - self.節点Z[i]
        EL   = math.sqrt(DX * DX + DY * DY + DZ * DZ)

        if DX == 0 and DY == 0:
            te[0][0] = 0
            te[0][1] = 0
            te[0][2] = 1
            te[1][0] = math.cos(FAii)
            te[1][1] = math.sin(FAii)
            te[1][2] = 0
            te[2][0] = -math.sin(FAii)
            te[2][1] = math.cos(FAii)
            te[2][2] = 0
        else:
            xl = DX / EL
            XM = DY / EL
            XN = DZ / EL
            xlm = math.sqrt(xl * xl + XM * XM)
            ts[0][0] = xl
            ts[0][1] = XM
            ts[0][2] = XN
            ts[1][0] = -XM / xlm
            ts[1][1] = xl / xlm
            ts[1][2] = 0
            ts[2][0] = -XN * xl / xlm
            ts[2][1] = -XM * XN / xlm
            ts[2][2] = xlm
            tf[0][0] = 1
            tf[0][1] = 0
            tf[0][2] = 0
            tf[1][0] = 0
            tf[1][1] = math.cos(FAii)
            tf[1][2] = math.sin(FAii)
            tf[2][0] = 0
            tf[2][1] = -math.sin(FAii)
            tf[2][2] = math.cos(FAii)

            for i in range(3):
                for j in range(3):
                    S = 0
                    for k in range(3):
                        S = S + tf[i][k] * ts[k][j]
                    te[i][j] = S

        G = self.弾性係数[M] * self.断面積[M] / EL
        YYi = self.yi[M]
        ZZi = self.zi[M]
        if self.kTR1[jEL] == "0" and self.kTR2[jEL] == "0":
            YYi = 0
            ZZi = 0

        EE  = self.弾性係数[M]
        EL2 = EL * EL
        EL3 = EL * EL2
        Z6  = 6 * EE * ZZi / EL2
        Z12 = 2 * Z6 / EL
        Y6  = 6 * EE * YYi / EL2
        Y12 = 2 * Y6 / EL
        GkL = self.gk[M] / EL
        Y2  = 2 * EE * YYi / EL
        Y4  = 2 * Y2
        Z2  = 2 * EE * ZZi / EL
        Z4  = 2 * Z2
        for i in range(12):
            for j in range(i, 12):
                ek2[i][j] = 0
        
        ek2[0][0]   = G
        ek2[0][6]   = -G
        ek2[1][1]   = Z12
        ek2[1][5]   = Z6
        ek2[1][7]   = -Z12
        ek2[1][11]  = Z6
        ek2[2][2]   = Y12
        ek2[2][4]   = -Y6
        ek2[2][8]   = -Y12
        ek2[2][10]  = -Y6
        ek2[3][3]   = GkL
        ek2[3][9]   = -GkL
        ek2[4][4]   = Y4
        ek2[4][8]   = Y6
        ek2[4][10]  = Y2
        ek2[5][5]   = Z4
        ek2[5][7]   = -Z6
        ek2[5][11]  = Z2
        ek2[6][6]   = G
        ek2[7][7]   = Z12
        ek2[7][11]  = -Z6
        ek2[8][8]   = Y12
        ek2[8][10]  = Y6
        ek2[9][9]   = GkL
        ek2[10][10] = Y4
        ek2[11][11] = Z4

        i_lower = np.tril_indices(12, -1)
        ek2[i_lower] = ek2.T[i_lower]
        
        t[:, :] = 0

        for offset in [0, 3, 6, 9]:
            t[offset:offset+3, offset:offset+3] = te

        np.dot(ek2, t, out = self.Ek)

    ####################################
    ##     ３次元　変 位 の 計 算     ##
    ##        ** HENikS.for **        ##
    ####################################
    def 変位計算(self):

        FLOAD = np.zeros(6, dtype=float)

        for i in range(self.節点数):
            for j in range(6):
                k = self.iD[j, i]
                if k != 0:
                    FLOAD[j] = self.FORCE[k - 1]
                else:
                    FLOAD[j] = 0  # đảm bảo gán 0 nếu k==0

            self.変位[i, :] = FLOAD  # gán nguyên 6 phần tử cùng lúc
        
        for i in range(self.拘束条件数):
            j = self.拘束条件節点[i] - 1
            if 1 == self.nxfx[i]: self.変位[j][0] = 0
            if 1 == self.nyfx[i]: self.変位[j][1] = 0
            if 1 == self.nzfx[i]: self.変位[j][2] = 0
            if 1 == self.mxfx[i]: self.変位[j][3] = 0
            if 1 == self.myfx[i]: self.変位[j][4] = 0
            if 1 == self.mzfx[i]: self.変位[j][5] = 0

    ##########################################################
    ##     ３次元の軸力，せん断力，曲げモーメントの計算         ##
    ##                 ** POWER2.for **                     ##
    ##########################################################
    def 結果出力(self):
        gforce = np.zeros(12, dtype=float)
        gdisp  = np.zeros(12, dtype=float)

        encodings_to_try = ['utf-8', 'shift_jis']

        # ===== 1) Tạo tiêu đề =====
        csvlist = [
            ",Node Displacement,,,,,,, , Reactions,,,,,,, , Element Internal Forces,,,,,,",
            ",Node, UX, UY, UZ, RX, RY, RZ, , Node, FX, FY, FZ, MX, MY, MZ, , Elem, Node, FX, FY, FZ, MX, MY, MZ",
            "======================================================================================================================",
            "", "", ""
        ]

        # ===== 2) Xuất biến dạng =====
        csv変位list = []
        for i in range(self.節点数):
            csv変位list.append(",{},{},{},{},{},{},{}".format(
                i+1,
                *[FEMUtils.zero_if_small(d) for d in self.変位[i][:6]]
            ))

        # ===== 3) Reset phản lực =====
        self.FORCE[:] = 0.0
        csv要素list = []

        # ===== 4) Tính nội lực phần tử =====
        for k in range(self.要素数):
            self.小剛性マトリックス作成(k)

            i, j = self.要素節点[k][0]-1, self.要素節点[k][1]-1
            gdisp[0:6]  = self.変位[i]
            gdisp[6:12] = self.変位[j]

            gforce = self.Ek @ gdisp

            # --- Ma trận chuyển hướng te ---
            xi, yi, zi = self.節点X[i], self.節点Y[i], self.節点Z[i]
            xj, yj, zj = self.節点X[j], self.節点Y[j], self.節点Z[j]
            DX, DY, DZ = xj - xi, yj - yi, zj - zi
            L = math.sqrt(DX*DX + DY*DY + DZ*DZ)
            FAii = self.fai[k]

            if DX == 0 and DY == 0:
                te = np.array([
                    [0, 0, 1],
                    [math.cos(FAii), math.sin(FAii), 0],
                    [-math.sin(FAii), math.cos(FAii), 0]
                ])
            else:
                xl, XM, XN = DX/L, DY/L, DZ/L
                xlm = math.sqrt(xl*xl + XM*XM)
                ts = np.array([
                    [xl, XM, XN],
                    [-XM/xlm, xl/xlm, 0],
                    [-XN*xl/xlm, -XM*XN/xlm, xlm]
                ])
                tf = np.array([
                    [1,0,0],
                    [0,math.cos(FAii), math.sin(FAii)],
                    [0,-math.sin(FAii), math.cos(FAii)]
                ])
                te = tf @ ts

            T = np.zeros((12,12))
            for off in (0,3,6,9):
                T[off:off+3, off:off+3] = te

            # --- Gom UDL nếu có ---
            wxg = wyg = wzg = 0.0
            for m in range(getattr(self,'分布荷重数',0)):
                a,b = self.分布荷重節点[m]
                if (a==i+1 and b==j+1) or (a==j+1 and b==i+1):
                    wxg += self.wx[m]
                    wyg += self.wy[m]
                    wzg += self.wz[m]

            if (wxg!=0 or wyg!=0 or wzg!=0):
                w_loc = te @ np.array([wxg,wyg,wzg])
                wx, wy, wz = w_loc
                fe_loc = np.array([
                    0.5*L*wx, 0.5*L*wy, 0.5*L*wz, 0.0, -wz*L**2/12.0, wy*L**2/12.0,
                    0.5*L*wx, 0.5*L*wy, 0.5*L*wz, 0.0, wz*L**2/12.0, -wy*L**2/12.0
                ])
                fe_glo = T.T @ fe_loc
                gforce -= fe_glo

            # --- Cập nhật phản lực ---
            self.FORCE[i*6:i*6+6] += gforce[0:6]
            self.FORCE[j*6:j*6+6] += gforce[6:12]

            # --- Xuất nội lực phần tử ---
            # Node đầu: xử lý moment và lực cắt theo quy ước dương
            gforce_head = gforce[0:6].copy()
            gforce_head[1] *= -1  # Fy (lực cắt)
            gforce_head[2] *= -1  # Fz (lực cắt)
            gforce_head[4] *= -1  # My (moment uốn)
            gforce_head[5] *= -1  # Mz (moment uốn)

            csv要素list.append("{},{},{},{},{},{},{},{}".format(
                k+1, i+1, *[FEMUtils.zero_if_small(g) for g in gforce_head]
            ))

            # Node cuối: giữ nguyên (theo FEM local)
            csv要素list.append(",{},{},{},{},{},{},{}".format(
                j+1, *[FEMUtils.zero_if_small(g) for g in gforce[6:12]]
            ))

        # ===== 5) Xuất phản lực =====
        csv反力list = []
        for i in range(self.節点数):
            start = i*6
            csv反力list.append("{},{},{},{},{},{},{}".format(
                i+1, *[FEMUtils.zero_if_small(self.FORCE[start+j]) for j in range(6)]
            ))

        # ===== 6) Gom tất cả vào csvlist =====
        row = max(len(csv変位list), len(csv反力list), len(csv要素list))
        for r in range(row):
            line = ""
            line += (csv変位list[r]+",,") if r<len(csv変位list) else ",,,,,,,,,"
            line += (csv反力list[r]+",,") if r<len(csv反力list) else ",,,,,,,,"
            line += csv要素list[r] if r<len(csv要素list) else ",,,,,,,"
            csvlist.append(line)

        # ===== 7) Ghi file chỉ 1 lần =====
        written = False
        for enc in encodings_to_try:
            try:
                with codecs.open(self.出力シート名+'.csv', "w", encoding=enc) as f:
                    for line in csvlist:
                        f.write(line + "\r\n")
                written = True
                break
            except Exception as e:
                print(f"Ghi file với {enc} thất bại: {e}")
        
        if not written:
            traceback.print_exc()
            sys.exit(self.出力シート名 + ".csv の書き込みに失敗しました。")

    #########################################
    ##     ３次元　skyline  of  matrix     ##
    ##          ** SkYMAT.for **           ##
    #########################################
    def SkYマトリックス(self, NEQ):

        NBC = 0
        NBC = (
            np.sum(self.nxfx != 0) + 
            np.sum(self.nyfx != 0) + 
            np.sum(self.nzfx != 0) + 
            np.sum(self.mxfx != 0) + 
            np.sum(self.myfx != 0) + 
            np.sum(self.mzfx != 0)
        )
        
        NEQ = 6 * self.節点数 - NBC

        self.iD = np.ones((6, self.節点数), dtype=int)
        
        idx_nodes = self.拘束条件節点 - 1
        self.iD[0, idx_nodes[self.nxfx == 1]] = 0
        self.iD[1, idx_nodes[self.nyfx == 1]] = 0
        self.iD[2, idx_nodes[self.nzfx == 1]] = 0
        self.iD[3, idx_nodes[self.mxfx == 1]] = 0
        self.iD[4, idx_nodes[self.myfx == 1]] = 0
        self.iD[5, idx_nodes[self.mzfx == 1]] = 0

        flat = self.iD.flatten()
        indices = np.where(flat == 1)[0]            # vị trí phần tử bằng 1
        numbers = np.arange(1, len(indices) + 1)    # Tạo mảng số thứ tự cho các phần tử ==1
        flat[indices] = numbers                     # Gán lại các phần tử này
        self.iD = flat.reshape(self.iD.shape)       # reshape lại về kích thước cũ

        ND = 12
        self.MHT = np.zeros(NEQ, dtype=int)

        LM = np.zeros(ND, dtype=int)
        for jEL in range( self.要素数):
            j1 = self.要素節点[jEL][0] - 1
            j2 = self.要素節点[jEL][1] - 1
            LM[:6] = self.iD[:, j1]
            LM[6:] = self.iD[:, j2]

            LS = np.min(LM[LM != 0])
            for ii in LM[LM != 0]:
                MEE = ii - LS
                idx = ii - 1
                self.MHT[idx] = max(self.MHT[idx], MEE)

        self.MAXA = np.zeros(NEQ + 2, dtype=int)
        self.MAXA[0] = 1
        self.MAXA[1] = 2

        for i in range(1, NEQ):
            self.MAXA[i + 1] = self.MAXA[i] + self.MHT[i] + 1
        
        if self.MAXA[NEQ + 1] - self.MAXA[0] > self.配列上限:
            sys.exit("メモリオーバーしました：SkYマトリックス()")


        for jEL in range(self.要素数):
            self.小剛性マトリックス作成(jEL)

            for i in range(ND):
                LM[i] = 0
            
            j = self.要素節点[jEL][0] - 1
            LM[0]  = self.iD[0][j]
            LM[1]  = self.iD[1][j]
            LM[2]  = self.iD[2][j]
            LM[3]  = self.iD[3][j]
            LM[4]  = self.iD[4][j]
            LM[5]  = self.iD[5][j]
            j = self.要素節点[jEL][1] - 1
            LM[6]  = self.iD[0][j]
            LM[7]  = self.iD[1][j]
            LM[8]  = self.iD[2][j]
            LM[9]  = self.iD[3][j]
            LM[10] = self.iD[4][j]
            LM[11] = self.iD[5][j]

            NDi = 0
            for i in range(ND):
                ii = LM[i]
                if ii > 0:
                    kS = i
                    for j in range(ND):
                        jj = LM[j]
                        if jj > 0:
                            ij = ii - jj
                            if ij >= 0:
                                NEC = self.MAXA[ii - 1] + ij - 1
                                kSS = kS
                                if j >= i: kSS = j + NDi
                                self.AjCB[NEC] = self.AjCB[NEC] + self.SE[kSS]

                        kS = kS + ND - j - 1
                NDi = NDi + ND - i - 1

        return NEQ

    ############################################
    ##     ３次元　小剛性マトリックス作成     ##
    ##        selm(12,12)---> se(78)          ##
    ##            ** STiMAS.for **            ##
    ############################################
    def 小剛性マトリックス作成(self, jEL, return_T=False):

        ts  = np.zeros(( 3, 3),dtype=float)
        tf  = np.zeros(( 3, 3),dtype=float)
        te  = np.zeros(( 3, 3),dtype=float)
        t   = np.zeros((12,12),dtype=float)
        ek2 = np.zeros((12,12),dtype=float)

        M    = self.要素材料[jEL] -1
        FAii = self.fai[jEL]
        i = self.要素節点[jEL][0] - 1
        j = self.要素節点[jEL][1] - 1
        DX   = self.節点X[j] - self.節点X[i]
        DY   = self.節点Y[j] - self.節点Y[i]
        DZ   = self.節点Z[j] - self.節点Z[i]
        EL   = math.sqrt(DX * DX + DY * DY + DZ * DZ)

        if DX == 0 and DY == 0:
            te[0][0] = 0
            te[0][1] = 0
            te[0][2] = 1
            te[1][0] = math.cos(FAii)
            te[1][1] = math.sin(FAii)
            te[1][2] = 0
            te[2][0] = -math.sin(FAii)
            te[2][1] = math.cos(FAii)
            te[2][2] = 0
        else:
            xl = DX / EL
            XM = DY / EL
            XN = DZ / EL
            xlm = math.sqrt(xl * xl + XM * XM)
            ts[0][0] = xl
            ts[0][1] = XM
            ts[0][2] = XN
            ts[1][0] = -XM / xlm
            ts[1][1] = xl / xlm
            ts[1][2] = 0
            ts[2][0] = -XN * xl / xlm
            ts[2][1] = -XM * XN / xlm
            ts[2][2] = xlm
            tf[0][0] = 1
            tf[0][1] = 0
            tf[0][2] = 0
            tf[1][0] = 0
            tf[1][1] = math.cos(FAii)
            tf[1][2] = math.sin(FAii)
            tf[2][0] = 0
            tf[2][1] = -math.sin(FAii)
            tf[2][2] = math.cos(FAii)

            np.dot(tf, ts, out = te)

        G = self.弾性係数[M] * self.断面積[M] / EL
        YYi = self.yi[M]
        ZZi = self.zi[M]
        if self.kTR1[jEL] == "0" and self.kTR2[jEL] == "0": YYi = 0
        if self.kTR1[jEL] == "0" and self.kTR2[jEL] == "0": ZZi = 0

        EE  = self.弾性係数[M]
        EL2 = EL * EL
        EL3 = EL * EL2
        Z6  = 6 * EE * ZZi / EL2
        Z12 = 12 * EE * ZZi / EL3
        Y6  = 6 * EE * YYi / EL2
        Y12 = 12 * EE * YYi / EL3
        GkL = self.gk[M] / EL
        Y2  = 2 * EE * YYi / EL
        Y4  = 2 * Y2
        Z2  = 2 * EE * ZZi / EL
        Z4  = 2 * Z2

        for i in range(12):
            for j  in range(12):
                self.Ek[i][j] = 0
        
        self.Ek[0] [0]  =  G        # Lực dọc (axial) EA/L
        self.Ek[0] [6]  = -G        # Lực dọc (axial) EA/L
        self.Ek[1] [1]  =  Z12      # Uốn theo trục Y (Iz)
        self.Ek[1] [5]  =  Z6       # Uốn theo trục Y (Iz)
        self.Ek[1] [7]  = -Z12      # Uốn theo trục Y (Iz)
        self.Ek[1] [11] =  Z6       # Uốn theo trục Y (Iz)
        self.Ek[2] [2]  =  Y12      # Uốn theo trục Z (Iy)
        self.Ek[2] [4]  = -Y6       # Uốn theo trục Z (Iy)
        self.Ek[2] [8]  = -Y12      # Uốn theo trục Z (Iy)
        self.Ek[2] [10] = -Y6       # Uốn theo trục Z (Iy)
        self.Ek[3] [3]  =  GkL      # Xoắn (torsion) GJ/L
        self.Ek[3] [9]  = -GkL      # Xoắn (torsion) GJ/L
        self.Ek[4] [4]  =  Y4       # Uốn theo trục Z (Iy)
        self.Ek[4] [8]  =  Y6       # Uốn theo trục Z (Iy)
        self.Ek[4] [10] =  Y2       # Uốn theo trục Z (Iy)
        self.Ek[5] [5]  =  Z4       # Uốn theo trục Y (Iz)
        self.Ek[5] [7]  = -Z6       # Uốn theo trục Y (Iz)
        self.Ek[5] [11] =  Z2       # Uốn theo trục Y (Iz)
        self.Ek[6] [6]  =  G        # Lực dọc (axial) EA/L
        self.Ek[7] [7]  =  Z12      # Uốn theo trục Y (Iz)
        self.Ek[7] [11] = -Z6       # Uốn theo trục Y (Iz)
        self.Ek[8] [8]  =  Y12      # Uốn theo trục Z (Iy)
        self.Ek[8] [10] =  Y6       # Uốn theo trục Z (Iy)
        self.Ek[9] [9]  =  GkL      # Xoắn (torsion) GJ/L
        self.Ek[10][10] =  Y4       # Uốn theo trục Z (Iy)
        self.Ek[11][11] =  Z4       # Uốn theo trục Y (Iz)

        i_lower = np.tril_indices(12, -1)
        self.Ek[i_lower] = self.Ek.T[i_lower]
        
        t[:, :] = 0
        
        for offset in [0, 3, 6, 9]:
            t[offset:offset+3, offset:offset+3] = te

        T = np.array(t)                   # ← convert list → ndarray
        Ek = np.array(self.Ek)

        np.dot(T.T, Ek, out = ek2) 
        t = np.array(t)
        self.Ek = np.dot(ek2, t, out = self.Ek)

        if self.kTR1[jEL] == "5" and self.kTR2[jEL] == "7": self.elka1(3)
        if self.kTR1[jEL] == "6" and self.kTR2[jEL] == "7": self.elka1(4)
        if self.kTR1[jEL] == "4" and self.kTR2[jEL] == "7": self.elka1(5)
        if self.kTR1[jEL] == "7" and self.kTR2[jEL] == "5": self.elka1(9)
        if self.kTR1[jEL] == "7" and self.kTR2[jEL] == "6": self.elka1(10)
        if self.kTR1[jEL] == "7" and self.kTR2[jEL] == "4": self.elka1(11)

        if self.kTR1[jEL] == "5" and self.kTR2[jEL] == "5": self.elka2(3)
        if self.kTR1[jEL] == "6" and self.kTR2[jEL] == "6": self.elka2(4)
        if self.kTR1[jEL] == "4" and self.kTR2[jEL] == "4": self.elka2(5)

        if self.kTR1[jEL] == "3" and self.kTR2[jEL] == "7": self.elka3(5)
        if self.kTR1[jEL] == "2" and self.kTR2[jEL] == "7": self.elka3(4)
        if self.kTR1[jEL] == "1" and self.kTR2[jEL] == "7": self.elka3(3)
        if self.kTR1[jEL] == "7" and self.kTR2[jEL] == "3": self.elka3(11)
        if self.kTR1[jEL] == "7" and self.kTR2[jEL] == "2": self.elka3(10)
        if self.kTR1[jEL] == "7" and self.kTR2[jEL] == "1": self.elka3(9)

        if self.kTR1[jEL] == "0" and self.kTR2[jEL] == "7": self.elka4(3)
        if self.kTR1[jEL] == "7" and self.kTR2[jEL] == "0": self.elka4(9)

        if self.kTR1[jEL] == "3" and self.kTR2[jEL] == "3": self.elka5(0)
        if self.kTR1[jEL] == "2" and self.kTR2[jEL] == "2": self.elka5(1)
        if self.kTR1[jEL] == "1" and self.kTR2[jEL] == "1": self.elka5(2)

        k = 0
        for i in range(12):
            for j in range(i, 12):
                self.SE[k] = self.Ek[i][j]
                k = k + 1

        # Tính Ek global
        self.Ek = T.T @ self.Ek @ T
        if return_T:
            return self.Ek, T
        else:
            return self.Ek
    ###########################################
    ##    ３次元  [A] ----> [L]*[D]*[L]t     ##
    ##           ** SUBDEC.for **            ##
    ###########################################
    def decomp(self, NN):

        for N in range(NN):
            kN = self.MAXA[N]          # vị trí phần tử đường chéo của cột N
            kL = kN + 1                # phần tử ngay dưới đường chéo
            kU = self.MAXA[N + 1] - 1  # phần tử cuối cùng trong cột
            kH = kU - kL               # số phần tử phía dưới đường chéo (chiều cao profile)

            # Khử Gauss theo cấu trúc Skyline
            if kH > 0:
                k = N - kH 
                for j in range(kH):
                    kLT = kU - 1 - j                # địa chỉ phần tử phía dưới đường chéo
                    ki = self.MAXA[k]               # địa chỉ đường chéo của cột nhỏ hơn k
                    ND = self.MAXA[k + 1] - ki - 1  # số phần tử profile cột k
                    kk = min(j + 1, ND)             # số phần tử giao nhau giữa 2 profile
                    if kk > 0:
                        C = np.dot(self.AjCB[ki : ki + kk], self.AjCB[kLT : kLT + kk])
                        self.AjCB[kLT - 1] -= C
                    k += 1

            # Tính hệ số chia (Lij)
            if kH >= 0:
                k = N
                B = 0
                for kk in range(kL-1, kU):
                    k -= 1
                    ki = self.MAXA[k] - 1
                    C = self.AjCB[kk] / self.AjCB[ki]   # c là hệ số chia Lik
                    if abs(C) >= 1e7:
                        sys.exit("計算エラー：decomp(),")

                    B += C * self.AjCB[kk]
                    self.AjCB[kk] = C

                # Cập nhật phần tử đường chéo
                self.AjCB[kN - 1] -= B

            if self.AjCB[kN - 1] == 0: self.AjCB[kN - 1] = -1E-16

    ################################################################
    ##    ３次元　reduce and back-substitute iteration vectors    ##
    ##                    ** SUBRED.for **                        ##
    ################################################################
    def redbak(self, NN):
        # forward_substitution – Giải Ly=f
        for N in range(NN):

            kL = self.MAXA[N] + 1
            kU = self.MAXA[N + 1] - 1
            if kU - kL >= 0:
                k = N
                C = 0
                for kk in range(kL-1, kU):
                    k = k - 1
                    C = C + self.AjCB[kk] * self.FORCE[k]

                self.FORCE[N] -= C
        # backward_substitution - Giải Ux=y
        for N in range(NN):
            k = self.MAXA[N] - 1
            self.FORCE[N] = self.FORCE[N] / self.AjCB[k]

        N = NN - 1
        for L in range(1, NN):
            kL = self.MAXA[N] + 1
            kU = self.MAXA[N + 1] - 1
            if kU - kL >= 0:
                k = N
                for kk in range(kL-1, kU):
                    k = k - 1
                    self.FORCE[k] -= (self.AjCB[kk] * self.FORCE[N])

            N = N - 1

    ##################################################################
    #      ３次元 節点に分布荷重を集中荷重とモーメントに等価する     #
    #                     ** WBUNPU.for **                           #
    ##################################################################
    def 分布荷重振り分け(self):
        for i in range(self.分布荷重数):
            N1 = self.分布荷重節点[i][0]
            N2 = self.分布荷重節点[i][1]

            for j in range(self.要素数):
                M1 = self.要素節点[j][0]
                M2 = self.要素節点[j][1]

                if (N1 == M1 and N2 == M2) or (N1 == M2 and N2 == M1):
                    # Lấy toạ độ
                    x1, y1, z1 = self.節点X[N1-1], self.節点Y[N1-1], self.節点Z[N1-1]
                    x2, y2, z2 = self.節点X[N2-1], self.節点Y[N2-1], self.節点Z[N2-1]

                    # Vector định hướng local
                    dx, dy, dz = x2 - x1, y2 - y1, z2 - z1
                    L = math.sqrt(dx**2 + dy**2 + dz**2)
                    lx, ly, lz = dx / L, dy / L, dz / L

                    # Tải local
                    wx, wy, wz = self.wx[i], self.wy[i], self.wz[i]

                    # Vector lực local dạng [Fx, Fy, Fz, Mx, My, Mz]
                    F_local_1 = [0.5*L*wx, 0.5*L*wy, 0.5*L*wz,
                                0, -wz*L**2/12,  wy*L**2/12]
                    F_local_2 = [0.5*L*wx, 0.5*L*wy, 0.5*L*wz,
                                0,  wz*L**2/12, -wy*L**2/12]

                    # Không xoay lực tại đây (nếu wx, wy, wz đã được nhập theo global)
                    # Nếu muốn xoay thì phải viết thêm T = ma trận 12x12

                    # === Nút đầu
                    self.集中荷重節点[self.集中荷重数] = N1
                    self.fx [self.集中荷重数] = F_local_1[0]
                    self.fy [self.集中荷重数] = F_local_1[1]
                    self.fz [self.集中荷重数] = F_local_1[2]
                    self.fmx[self.集中荷重数] = 0
                    self.fmy[self.集中荷重数] = F_local_1[4] if self.iD[4][N1-1] != 0 else 0
                    self.fmz[self.集中荷重数] = F_local_1[5] if self.iD[5][N1-1] != 0 else 0
                    self.集中荷重数 += 1

                    # === Nút cuối
                    self.集中荷重節点[self.集中荷重数] = N2
                    self.fx [self.集中荷重数] = F_local_2[0]
                    self.fy [self.集中荷重数] = F_local_2[1]
                    self.fz [self.集中荷重数] = F_local_2[2]
                    self.fmx[self.集中荷重数] = 0
                    self.fmy[self.集中荷重数] = F_local_2[4] if self.iD[4][N2-1] != 0 else 0
                    self.fmz[self.集中荷重数] = F_local_2[5] if self.iD[5][N2-1] != 0 else 0
                    self.集中荷重数 += 1

    def prepare_element_for_gui(self):
        """
        Tính nội lực phần tử để hiển thị GUI, tận dụng logic trong 結果出力().
        Kết quả lưu vào self.N, self.Qy, self.Qz, self.Mx, self.My, self.Mz
        """
        ND = 12
        gdisp  = np.zeros(ND)
        gforce = np.zeros(ND)

        # Reset mảng nội lực
        self.N[:]  = 0
        self.Qy[:] = 0
        self.Qz[:] = 0
        self.Mx[:] = 0
        self.My[:] = 0
        self.Mz[:] = 0

        for k in range(self.要素数):
            # Tạo ma trận cứng local 12x12
            self.小剛性マトリックス作成(k)

            # Chỉ số hai đầu nút (0-based)
            i, j = self.要素節点[k][0]-1, self.要素節点[k][1]-1
            gdisp[0:6]  = self.変位[i]
            gdisp[6:12] = self.変位[j]

            # Nội lực local
            gforce = self.Ek @ gdisp

            # --- Ma trận chuyển hướng te ---
            DX = self.節点X[j] - self.節点X[i]
            DY = self.節点Y[j] - self.節点Y[i]
            DZ = self.節点Z[j] - self.節点Z[i]
            L = math.sqrt(DX*DX + DY*DY + DZ*DZ)
            FAii = self.fai[k]

            if DX==0 and DY==0:
                te = np.array([[0,0,1],
                            [math.cos(FAii), math.sin(FAii), 0],
                            [-math.sin(FAii), math.cos(FAii), 0]])
            else:
                xl, XM, XN = DX/L, DY/L, DZ/L
                xlm = math.sqrt(xl*xl + XM*XM)
                ts = np.array([[xl, XM, XN],
                            [-XM/xlm, xl/xlm, 0],
                            [-XN*xl/xlm, -XM*XN/xlm, xlm]])
                tf = np.array([[1,0,0],
                            [0,math.cos(FAii), math.sin(FAii)],
                            [0,-math.sin(FAii), math.cos(FAii)]])
                te = tf @ ts

            T = np.zeros((12,12))
            for off in (0,3,6,9):
                T[off:off+3, off:off+3] = te

            # --- Gom UDL nếu có ---
            wxg = wyg = wzg = 0.0
            for m in range(getattr(self,'分布荷重数',0)):
                a,b = self.分布荷重節点[m]
                if (a==i+1 and b==j+1) or (a==j+1 and b==i+1):
                    wxg += self.wx[m]
                    wyg += self.wy[m]
                    wzg += self.wz[m]

            if (wxg!=0 or wyg!=0 or wzg!=0):
                w_loc = te @ np.array([wxg,wyg,wzg])
                wx, wy, wz = w_loc
                fe_loc = np.array([0.5*L*wx, 0.5*L*wy, 0.5*L*wz, 0.0, -wz*L**2/12.0, wy*L**2/12.0,
                                0.5*L*wx, 0.5*L*wy, 0.5*L*wz, 0.0, wz*L**2/12.0, -wy*L**2/12.0])
                fe_glo = T.T @ fe_loc
                gforce -= fe_glo

            # --- Gán nội lực vào mảng GUI ---
            self.N[k,0]  = gforce[0]
            self.Qy[k,0] = -gforce[1]
            self.Qz[k,0] = -gforce[2]
            self.Mx[k,0] = gforce[3]
            self.My[k,0] = -gforce[4]
            self.Mz[k,0] = -gforce[5]

            self.N[k,1]  = gforce[6]
            self.Qy[k,1] = gforce[7]
            self.Qz[k,1] = gforce[8]
            self.Mx[k,1] = gforce[9]
            self.My[k,1] = gforce[10]
            self.Mz[k,1] = gforce[11]
