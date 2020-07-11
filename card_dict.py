from functools import reduce
import math

CARD_POOL = {
    '万': list(range(1, 10)),
    '筒': list(range(11, 20)),
    '条': list(range(21, 30)),
    '风': [31, 32, 33, 34],  # 东西南北
    '老头': [1, 9, 11, 19, 21, 29],
    '三元': [35, 36, 37],  # 中发白
    '绿': [22, 23, 24, 25, 26, 27, 28, 36],
    '幺九': [],
    '役满': ['大三元', '四暗刻', '字一色', '绿一色', '清老头', '国士无双', '小四喜', '大四喜']
}
CARD_POOL['字'] = CARD_POOL['三元'] + CARD_POOL['风']
CARD_POOL['幺九'] = CARD_POOL['老头'] + CARD_POOL['字']
CARD_POOL['老头顺'] = [[x, x + 1, x + 2] if str(x).endswith('1') else [x - 2, x - 1, x] for x in CARD_POOL['老头']]
CARD_POOL['字刻'] = [[x] * 3 for x in CARD_POOL['字']]
CARD_POOL['老头刻'] = [[x] * 3 for x in CARD_POOL['老头']]
CARD_POOL['幺九刻'] = CARD_POOL['字刻'] + CARD_POOL['老头刻']
CARD_POOL['三元刻'] = [[x] * 3 for x in CARD_POOL['三元']]
CARD_POOL['风刻'] = [[x] * 3 for x in CARD_POOL['风']]

SHOW_DICT = {
    31: '东风',
    32: '西风',
    33: '南风',
    34: '北风',
    35: '中',
    36: '发',
    37: '白',
}

PAIRS = reduce(lambda x, y: x + y, CARD_POOL.values())

CARD_FU_DICT = {
    "自摸": 2 * 0,
    "七对": 0,
    "门清荣和": 10 * 0,
    "幺九明刻": 4 * 0,
    "幺九暗刻": 8 * 0,
    "幺九明杠": 16 * 0,
    "幺九暗杠": 32 * 0,
    "中张明刻": 2 * 0,
    "中张暗刻": 4 * 0,
    "中张明杠": 8 * 0,
    "中张暗杠": 16 * 0,
    "雀头场风、自风、三元牌": 2 * 0,
    "雀头双风牌": 4 * 0,
    "单骑、边张、欠张": 2 * 0
}


def is_flush(l):
    l = sorted(list(l))
    if l[1] == l[0] + 1 and l[2] == l[1] + 1:
        return True
    else:
        return False


def is_triple(l):
    l = list(l)
    if l.count(l[0]) == 3:
        return True
    else:
        return False


class CheckCard(object):
    def __init__(self, input_list,
                 home="",
                 zimo="",
                 mq="",
                 baopai=0,
                 my_wind="",
                 last_ting="",
                 peng_ke="",
                 gang=0,
                 court_wind=31,
                 input_fu=0,
                 lingshangkaihua="",  # 岭上开花
                 yifa=""  # 一发
                 ):
        self.input_list = sorted(input_list)
        self.input_list_set = set(input_list)
        self.fu = input_fu
        self.mq = mq
        self.home = home
        self.fan = baopai
        if zimo and mq:
            self.fan = self.fan + 1
        if lingshangkaihua:
            self.fan = self.fan + 1
        if yifa:
            self.fan = self.fan + 1
        self.card_group = []
        self.my_wind = my_wind
        self.court_wind = court_wind
        self.last_ting = last_ting
        self.peng_ke = peng_ke
        self.success = []
        if gang == 3:
            self.fan = self.fan + 2

    def check_lz(self):  # 立直
        if self.mq:
            print("立直")
            self.success.append("立直")
            self.fan = self.fan + 1
            return True

    def check_gsws(self):  # 检查国士无双
        gsws = set(CARD_POOL['幺九'])
        if set(self.input_list) == gsws:
            print('国土无双，十三幺！')
            self.success.append("国土无双")
            self.fan = self.fan + 13
            return True

    def check_ph(self):  # 检查平和
        if not self.mq:
            return False
        if not self.last_ting:
            return False
        if self.card_group[0][0] not in CARD_POOL['三元'] + [self.court_wind, self.my_wind, self.last_ting]:
            flush_list = [item for item in self.card_group[1:] if is_flush(item)]
            if len(flush_list) == 4 and self.last_ting in reduce(
                    lambda x, y: x + y,
                    [[item[0], item[2]] for item in flush_list]):
                print("平和")
                self.success.append("平和")
                self.fan = self.fan + 1
                return True
        return False

    def check_qys(self):  # 清一色
        if self.input_list_set.issubset(set(CARD_POOL['万'])) or \
                self.input_list_set.issubset(set(CARD_POOL['筒'])) or \
                self.input_list_set.issubset(set(CARD_POOL['条'])):
            print("和牌：清一色")
            self.success.append("清一色")
            self.fan = self.fan + 5
            return True
        return False

    def check_hys(self):  # 混一色
        join_set = self.input_list_set & set(CARD_POOL['字'])
        if len(join_set) != 0:
            left_set = self.input_list_set - join_set
            if left_set.issubset(set(CARD_POOL['万'])) or \
                    left_set.issubset(set(CARD_POOL['筒'])) or \
                    left_set.issubset(set(CARD_POOL['条'])):
                print("和牌：混一色")
                self.success.append("混一色")
                self.fan = self.fan + 2
                return True

    def check_7_pairs(self):
        for x in self.input_list_set:
            if self.input_list.count(x) not in [2, 4]:
                return False
        self.fan = self.fan + 2
        print("七对")
        self.success.append("七对")
        return True

    def check_ddh(self):  # 对对胡
        card_group = self.card_group[1:]
        if all([is_triple(x) for x in card_group]):
            print("和牌：对对和")
            self.success.append("对对和")
            self.fan = self.fan + 2
            return True

    def check_dy(self):  # 断幺
        if len(self.input_list_set & set(CARD_POOL['幺九'])) == 0:
            self.fan = self.fan + 1
            print("断幺")
            self.success.append("断幺")
            return True

    def check_zi(self):  # 检查字牌刻
        card_group = self.card_group[1:]
        for item in [x[0] for x in card_group if is_triple(x)]:
            if item in [self.court_wind, self.my_wind, 35, 36, 37]:
                self.fan = self.fan + 1
                print("役牌 {}".format(SHOW_DICT[item]))
                self.success.append("役牌 {}".format(SHOW_DICT[item]))

    def check_hlt(self):  # 混老头
        if self.input_list_set.issubset(set(CARD_POOL['幺九'])):
            print("混老头")
            self.fan = self.fan + 2
            self.success.append("混老头")
            return True
        return False

    def check_ybk(self):  # 一杯口
        if not self.mq:
            return False
        flush_list = [item[0] for item in self.card_group[1:] if is_flush(item)]
        if len(flush_list) >= 2:
            for item in set(flush_list):
                if flush_list.count(item) >= 2:
                    print("一杯口")
                    self.success.append("一杯口")
                    self.fan = self.fan + 1
                    return True
        return False

    def check_ebk(self):  # 二杯口
        if not self.mq:
            return False
        flush_list = [item[0] for item in self.card_group[1:] if is_flush(item)]

        if len(flush_list) == 4:
            items = list(set(flush_list))
            if len(items) == 2:
                for item in items:
                    if items.count(item) != 2:
                        return False
                print("二杯口")
                self.success.append("二杯口")
                self.fan = self.fan + 3
                return True
        return False

    def check_yqtg(self):  # 一气通贯
        flush_list = [item for item in self.card_group[1:] if is_flush(item)]
        if len(flush_list) >= 3:
            flush_total = reduce(lambda x, y: x + y, flush_list)
            if set(CARD_POOL['万']).issubset(set(flush_total)) or \
                    set(CARD_POOL['筒']).issubset(set(flush_total)) or \
                    set(CARD_POOL['条']).issubset(set(flush_total)):
                print("一气通贯")
                self.success.append("一气通贯")
                self.fan = self.fan + 1
                return True
        return False

    def check_ssts(self):  # 三色同顺
        flush_list = [item for item in self.card_group[1:] if is_flush(item)]
        if len(flush_list) >= 3:
            type_list = [str(item[0])[-1] for item in flush_list]
            for t in set(type_list):
                if type_list.count(t) >= 3:
                    print("三色同顺")
                    self.success.append("三色同顺")
                    self.fan = self.fan + 1
                    return True
            return False

    def check_sstk(self):  # 三色同刻
        triple_list = [item for item in self.card_group[1:] if is_triple(item)]
        if len(triple_list) >= 3:
            type_list = [str(item[0])[-1] for item in triple_list]
            for t in set(type_list):
                if type_list.count(t) >= 3:
                    self.fan = self.fan + 2
                    print("三色同刻")
                    self.success.append("三色同刻")
                    return True
            return False

    def check_hqdyj(self):  # 混全带幺九
        if set(self.card_group[0]).issubset(set(CARD_POOL['幺九'])):
            for item in self.card_group[1:]:
                if item not in CARD_POOL['幺九刻'] + CARD_POOL['老头顺']:
                    return False
            print('混全带幺九')
            self.success.append("混全带幺九")
            self.fan = self.fan + 1
            return True

    def check_cqdyj(self):  # 纯全带幺九
        if set(self.card_group[0]).issubset(set(CARD_POOL['老头'])):
            for item in self.card_group[1:]:
                if item not in CARD_POOL['老头刻'] + CARD_POOL['老头顺']:
                    return False
            print('纯全带幺九')
            self.success.append("纯全带幺九")
            self.fan = self.fan + 2
            return True

    def check_lys(self):  # 绿一色
        if self.input_list_set.issubset(set(CARD_POOL['绿'])):
            print('绿一色')
            self.success.append("绿一色")
            self.fan = self.fan + 13
            return True

    def check_zys(self):  # 字一色
        if self.input_list_set.issubset(set(CARD_POOL['字'])):
            print('字一色')
            self.success.append("字一色")
            self.fan = self.fan + 13
            return True

    def check_sak(self):  # 三暗刻 四暗刻 清老头 大四喜
        triple_list = [item for item in self.card_group[1:] if is_triple(item)]
        if len(triple_list) == 3 and not self.peng_ke:
            self.fan = self.fan + 2
            print("三暗刻")
            self.success.append("三暗刻")
            return True
        elif len(triple_list) == 4:
            if self.input_list_set.issubset(CARD_POOL['老头']):
                print('清老头')
                self.success.append("清老头")
                self.fan = self.fan + 13
            elif len([item for item in triple_list if set(item) in CARD_POOL['风']]) == 4:
                print('大四喜')
                self.success.append("大四喜")
                self.fan = self.fan + 13 * 2
            elif self.mq and not self.peng_ke:
                print('四暗刻')
                self.success.append("四暗刻")
                self.fan = self.fan + 13
            return True

    def check_xsx(self):  # 小四喜
        triple_list = [item for item in self.card_group[1:] if is_triple(item) and item in CARD_POOL['风刻']]
        if len(triple_list) == 3 and set(self.card_group[0]) in CARD_POOL['风']:
            print('小四喜')
            self.success.append("小四喜")
            self.fan = self.fan + 13
            return True

    def check_dsy(self):  # 大三元
        triple_list = [item for item in self.card_group[1:] if is_triple(item)]
        if len(triple_list) >= 3:
            cnt = 0
            for item in triple_list:
                if item in CARD_POOL['三元刻']:
                    cnt = cnt + 1
            if cnt != 3:
                return False
            self.fan = self.fan + 13
            print("大三元")
            self.success.append("大三元")
            return True

    def check_xsy(self):
        triple_list = [item for item in self.card_group[1:] if is_triple(item)]
        if len(triple_list) >= 2:
            cnt = 0
            for item in triple_list:
                if item in CARD_POOL['三元刻']:
                    cnt = cnt + 1
            if cnt != 2:
                return False
            if set(self.card_group[0]) not in CARD_POOL['三元']:
                return False
            self.fan = self.fan + 2
            print("小三元")
            self.success.append("小三元")
            return True

    def check_normal(self):
        # 牌面检查，是否属于本函数规定的范围内。
        from functools import reduce
        pairs = reduce(lambda x, y: x + y, CARD_POOL.values())
        #     print(pais)
        for x in set(self.input_list):
            if self.input_list.count(x) > 4:  # 某张牌的数量超过了4，是不正确的。
                return False
            if x not in pairs:
                print('参数错误：输入的牌型{}不在范围内。\n万：1-9，条：11-19，饼：21-29，东西南北风：31,33,35,37，中发白：41,43,45。'.format(x))
                return False
        # 牌数检查。
        if len(self.input_list) != 14:
            print('和牌失败：牌数不正确。')
            return False

        # 是否有对子检查。
        double = []
        for x in set(self.input_list):
            if self.input_list.count(x) >= 2:
                double.append(x)
        print(double)
        if len(double) == 0:
            # print('和牌失败：无对子')
            return False

        # 常规和牌检测。
        a1 = self.input_list.copy()
        a2 = []  # a2用来存放和牌后分组的结果。
        for x in double:
            # print('double', x)
            a1.remove(x)
            a1.remove(x)
            a2.append((x, x))
            for i in range(int(len(a1) / 3)):
                # print('i-', i)
                # print(a1)
                if a1.count(a1[0]) == 3:
                    # 列表移除，可以使用remove,pop，和切片，这里切片更加实用。
                    a2.append([a1[0]] * 3)
                    a1 = a1[3:]
                    # print(a1)
                elif a1[0] in a1 and a1[0] + 1 in a1 \
                        and a1[0] + 2 in a1:  # 这里注意，11,2222,33，和牌结果22,123,123，则连续的3个可能不是相邻的。
                    a2.append([a1[0], a1[0] + 1, a1[0] + 2])
                    a1.remove(a1[0] + 2)
                    a1.remove(a1[0] + 1)
                    a1.remove(a1[0])
                    # print(a1)

                else:
                    a1 = self.input_list.copy()
                    a2 = []
                    # print('重置')
                    break
            else:
                print('和牌成功,结果：', a2)
                self.card_group = a2
                return True

        # 如果上述没有返回和牌成功，这里需要返回和牌失败。
        else:
            # print('和牌失败：遍历完成。')
            return False

    def process(self):
        if not self.check_normal():
            self.check_gsws()
            if self.check_7_pairs():
                if not self.check_zys() or not self.check_lys():
                    self.check_hlt()
                    self.check_hys()
                    self.check_qys()
        else:
            self.check_sak()
            self.check_xsx()
            self.check_dsy()
            self.check_lys()
            self.check_zys()

            if not set(self.success) & set(CARD_POOL['役满']):
                self.check_lz()
                self.check_ph()
                self.check_qys()
                self.check_hys()
                self.check_ddh()
                self.check_dy()
                self.check_zi()
                if not self.check_hlt():
                    self.check_hqdyj()
                if not self.check_ebk():
                    if not self.check_7_pairs():
                        self.check_ybk()
                self.check_yqtg()
                self.check_ssts()
                self.check_sstk()
                self.check_cqdyj()
                self.check_xsy()
        print(self.fan)
        print(self.success)
        print(self.calculate())

    def caculate_fu(self):

        pass

    def calculate(self):
        if 1 <= self.fan <= 4:  # 满贯
            base = self.fu * 2 ** (self.fan + 2)
        elif self.fan == 5:
            base = 2000
        elif self.fan in [6, 7]:  # 跳满
            base = 3000
        elif self.fan in [8, 9, 10]:  # 倍满:
            base = 4000
        elif self.fan in [11, 12]:  # 三倍满
            base = 6000
        elif self.fan > 13:  # 役满
            base = 8000
        else:
            return "invalid fan"
        if self.home:
            score = 6 * base
        else:
            score = 4 * base
        return score


def calculate_fu(card_type_dict=CARD_FU_DICT):
    if card_type_dict.get("七对", 0):
        return 25
    base_fu = 20
    return math.ceil((base_fu + sum(card_type_dict.values())) / 10) * 10


if __name__ == '__main__':
    c = CheckCard(
        # [35, 35, 35, 36, 36, 36, 21, 21, 21, 31, 31, 34, 34, 34],
        [1, 1, 1, 2, 3, 7, 7, 7, 8, 8, 8, 9, 9, 9],
        # [2, 2, 3, 3, 4, 4, 6, 6, 17, 7,18, 8, 19, 9],
        # [1, 1, 9, 9, 31, 31, 32, 32, 35, 35, 36, 36, 33, 33],
        # [1, 1, 2, 2, 3, 3, 11, 11, 12, 12, 14, 14, 36, 36],
        last_ting=1, mq=1,
        my_wind=34,
        input_fu=40)

    c.process()
