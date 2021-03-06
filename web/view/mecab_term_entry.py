import os
import re
import jctconv
from lib import misc

re_katakana = re.compile('^[ァ-ヺー]+$')
re_symbol = re.compile("[（）＜＞＊「」、。＝〜!！\?？…・\s]")
katakana = {chr(i) for i in range(12449, 12449 + 90)}
hiragana = {chr(i) for i in range(12353, 12353 + 86)}

PARTS_OF_SPEECH = (
    '名詞,一般名詞',
    '名詞,サ変',
    '名詞,固有名詞',
    '名詞,姓',
    '名詞,名',
    '名詞,人名一般',
    '名詞,組織',
    '名詞,地域',
    '名詞,形容動詞語幹',
    '名詞,接尾-一般',
    '名詞,接尾-人名',
    '名詞,接尾-助数詞',
    '名詞,接尾-形容動詞語幹',
    '名詞,代名詞',
    '名詞,数',
    '記号,一般',
    '感動詞',
    '副詞,一般',
    '副詞,助詞類接続',
    '形容詞,アウオ基本形',
    '接頭詞,名詞接続',
    '接頭詞,形容詞接続',
    '連体詞',
    '動詞,五段ラ行基本',
    'フィラー',
    '動詞',
    '〜しい',
)
DIC_POS = (
    ["", "1285", "1285", "", "名詞", "一般", "*",
        "*", "*", "*", "", "", "", "", ""],
    ["", "1283", "1283", "", "名詞", "サ変接続", "*",
        "*", "*", "*", "", "", "", "", ""],
    ["", "1288", "1288", "", "名詞", "固有名詞", "一般",
        "*", "*", "*", "", "", "", "", ""],
    ["", "1290", "1290", "", "名詞", "固有名詞", "人名",
        "姓", "*", "*", "", "", "", "", ""],
    ["", "1291", "1291", "", "名詞", "固有名詞", "人名",
        "名", "*", "*", "", "", "", "", ""],
    ["", "1289", "1289", "", "名詞", "固有名詞", "人名",
        "一般", "*", "*", "", "", "", "", ""],
    ["", "1292", "1292", "", "名詞", "固有名詞", "組織",
        "*", "*", "*", "", "", "", "", ""],
    ["", "1293", "1293", "", "名詞", "固有名詞", "地域",
        "一般", "*", "*", "", "", "", "", ""],
    ["", "1287", "1287", "", "名詞", "形容動詞語幹",
        "*", "*", "*", "*", "", "", "", "", ""],
    ["", "1298", "1298", "", "名詞", "接尾", "一般",
        "*", "*", "*", "", "", "", "", ""],
    ["", "1302", "1302", "", "名詞", "接尾", "人名",
        "*", "*", "*", "", "", "", "", ""],
    ["", "1300", "1300", "", "名詞", "接尾", "助数詞",
        "*", "*", "*", "", "", "", "", ""],
    ["", "1301", "1301", "", "名詞", "接尾", "形容動詞語幹",
        "*", "*", "*", "", "", "", "", ""],
    ["", "1306", "1306", "", "名詞", "代名詞", "一般",
        "*", "*", "*", "", "", "", "", ""],
    ["", "1295", "1295", "", "名詞", "数", "*",
        "*", "*", "*", "", "", "", "", ""],
    ["", "5", "5", "", "記号", "一般", "*", "*", "*", "*", "", "", "", "", ""],
    ["", "3", "3", "", "感動詞", "*", "*", "*", "*", "*", "", "", "", "", ""],
    ["", "1281", "1281", "", "副詞", "一般", "*",
        "*", "*", "*", "", "", "", "", ""],
    ["", "1282", "1282", "", "副詞", "助詞類接続",
        "*", "*", "*", "*", "", "", "", "", ""],
    ["", "19", "19", "", "形容詞", "自立", "*", "*",
        "形容詞・アウオ段", "基本形", "", "", "", "", ""],
    ["", "560", "560", "", "接頭詞", "名詞接続", "*",
        "*", "*", "*", "", "", "", "", ""],
    ["", "557", "557", "", "接頭詞", "形容詞接続", "*",
        "*", "*", "*", "", "", "", "", ""],
    ["", "1315", "1315", "", "連体詞", "*", "*",
        "*", "*", "*", "", "", "", "", ""],
    ["", "772", "772", "", "動詞", "自立", "*", "*",
        "五段・ラ行", "基本形", "", "", "", "", ""],
    ["", "2", "2", "", "フィラー", "*", "*", "*", "*", "*", "", "", "", "", ""],
)

GODAN_WAONBIN = (
    ["", "814", "814", "", "動詞", "動詞", "*", "*",
        "五段・ワ行促音便", "仮定形", "", "", "", "", ""],
    ["", "817", "817", "", "動詞", "動詞", "*", "*",
        "五段・ワ行促音便", "基本形", "", "", "", "", ""],
    ["", "820", "820", "", "動詞", "動詞", "*", "*",
        "五段・ワ行促音便", "未然ウ接続", "", "", "", "", ""],
    ["", "823", "823", "", "動詞", "動詞", "*", "*",
        "五段・ワ行促音便", "未然形", "", "", "", "", ""],
    ["", "826", "826", "", "動詞", "動詞", "*", "*",
        "五段・ワ行促音便", "命令e", "", "", "", "", ""],
    ["", "829", "829", "", "動詞", "動詞", "*", "*",
        "五段・ワ行促音便", "連用タ接続", "", "", "", "", ""],
    ["", "832", "832", "", "動詞", "動詞", "*", "*",
        "五段・ワ行促音便", "連用形", "", "", "", "", ""],
)
GODAN_SUFFIXES = ('えうおわえっい', 'れるろられっり')

SHII = (
    ('い',
        ["", "43", "43", "", "形容詞", "自立", "*", "*", "形容詞・イ段", "基本形", "", "", "", "", ""]),
    ('',
        ["", "45", "45", "", "形容詞", "自立", "*", "*", "形容詞・イ段", "文語基本形", "", "", "", "", ""]),
    ('から',
        ["", "47", "47", "", "形容詞", "自立", "*", "*", "形容詞・イ段", "未然ヌ接続", "", "", "", "", ""]),
    ('かろ',
        ["", "46", "46", "", "形容詞", "自立", "*", "*", "形容詞・イ段", "未然ウ接続", "", "", "", "", ""]),
    ('かっ',
        ["", "50", "50", "", "形容詞", "自立", "*", "*", "形容詞・イ段", "連用タ接続", "", "", "", "", ""]),
    ('く',
        ["", "51", "51", "", "形容詞", "自立", "*", "*", "形容詞・イ段", "連用テ接続", "", "", "", "", ""]),
    ('くっ',
        ["", "51", "51", "", "形容詞", "自立", "*", "*", "形容詞・イ段", "連用テ接続", "", "", "", "", ""]),
    ('ゅう',
        ["", "49", "49", "", "形容詞", "自立", "*", "*", "形容詞・イ段", "連用ゴザイ接続", "", "", "", "", ""]),
    ('ゅぅ',
        ["", "49", "49", "", "形容詞", "自立", "*", "*", "形容詞・イ段", "連用ゴザイ接続", "", "", "", "", ""]),
    ('う',
        ["", "49", "49", "", "形容詞", "自立", "*", "*", "形容詞・イ段", "連用ゴザイ接続", "", "", "", "", ""]),
    ('き',
        ["", "44", "44", "", "形容詞", "自立", "*", "*", "形容詞・イ段", "体言接続", "", "", "", "", ""]),
    ('けれ',
        ["", "40", "40", "", "形容詞", "自立", "*", "*", "形容詞・イ段", "仮定形", "", "", "", "", ""]),
    ('かれ',
        ["", "48", "48", "", "形容詞", "自立", "*", "*", "形容詞・イ段", "命令e", "", "", "", "", ""]),
    ('けりゃ',
        ["", "41", "41", "", "形容詞", "自立", "*", "*", "形容詞・イ段", "仮定縮約1", "", "", "", "", ""]),
    ('きゃ',
        ["", "42", "42", "", "形容詞", "自立", "*", "*", "形容詞・イ段", "仮定縮約2", "", "", "", "", ""]),
    ('',
        ["", "39", "39", "", "形容詞", "自立", "*", "*", "形容詞・イ段", "ガル接続", "", "", "", "", ""]),
)
GODAN_MA = (
    ('め',
        ["", "760", "760", "", "動詞", "自立", "*", "*", "五段・マ行", "仮定形", "", "", "", "", ""]),
    ('みゃ',
        ["", "761", "761", "", "動詞", "自立", "*", "*", "五段・マ行", "仮定縮約1", "", "", "", "", ""]),
    ('む',
        ["", "762", "762", "", "動詞", "自立", "*", "*", "五段・マ行", "基本形", "", "", "", "", ""]),
    ('も',
        ["", "763", "763", "", "動詞", "自立", "*", "*", "五段・マ行", "未然ウ接続", "", "", "", "", ""]),
    ('ま',
        ["", "764", "764", "", "動詞", "自立", "*", "*", "五段・マ行", "未然形", "", "", "", "", ""]),
    ('め',
        ["", "765", "765", "", "動詞", "自立", "*", "*", "五段・マ行", "命令e", "", "", "", "", ""]),
    ('ん',
        ["", "766", "766", "", "動詞", "自立", "*", "*", "五段・マ行", "連用タ接続", "", "", "", "", ""]),
    ('み',
        ["", "767", "767", "", "動詞", "自立", "*", "*", "五段・マ行", "連用形", "", "", "", "", ""]),
)


def get_dicdir():
    result = misc.command('mecab-config --dicdir', True)
    return os.path.join(result[1].strip(), 'original')


def write_dic(pos, term, lemma, yomi):
    pos[0] = term
    pos[10] = lemma
    pos[3] = 0
    pos[11] = pos[12] = yomi
    if pos[-1] != 'MA':
        pos.append('MA')
    pos = map(str, pos)
    entry = ','.join(pos)
    dicpath = os.path.join(get_dicdir(), 'manual.csv')
    with open(dicpath, 'a+', encoding='utf8') as fd:
        fd.write(entry + '\n')
    return entry


def is_godan_waonbin(lemma):
    return lemma.endswith(('う', 'る'))


def is_godan_magyou(lemma):
    return lemma.endswith(('込む', 'こむ'))


def add_verb(term, lemma, yomi):
    if is_godan_waonbin(lemma):
        suffixes = GODAN_SUFFIXES[0] if lemma.endswith('う') else GODAN_SUFFIXES[1]
        for (pos, suffix) in zip(GODAN_WAONBIN, suffixes):
            term = term[:-1] + suffix
            yomi = yomi[:-1] + jctconv.hira2kata(suffix)
            yield write_dic(pos, term, lemma, yomi)
    elif is_godan_magyou(lemma):
        term = lemma[:-1]
        yomi = yomi[:-1]
        for (suffix, pos) in GODAN_MA:
            new_term = term + suffix
            new_yomi = yomi + jctconv.hira2kata(suffix)
            yield write_dic(pos, new_term, lemma, new_yomi)


def add_shii(term, lemma, yomi):
    if term.endswith('しい'):
        term = term[:-1]
    elif not term.endswith('し'):
        term += 'し'
    if yomi.endswith('シイ'):
        yomi = yomi[:-1]
    elif not yomi.endswith('シ'):
        yomi += 'シ'
    for (suffix, pos) in SHII:
        new_term = term + suffix
        new_yomi = yomi + jctconv.hira2kata(suffix)
        yield write_dic(pos, new_term, lemma, new_yomi)


def add_term(input_pos, term, lemma, yomi):
    term_added_message = ''
    if input_pos == '動詞':
        for added_entry in add_verb(term, lemma, yomi):
            term_added_message += 'Added %s\n' % added_entry
    elif input_pos == '〜しい':
        for added_entry in add_shii(term, lemma, yomi):
            term_added_message += 'Added %s\n' % added_entry
    else:
        for (i, pos_idx) in enumerate(PARTS_OF_SPEECH):
            if pos_idx == input_pos:
                added_entry = write_dic(DIC_POS[i], term, lemma, yomi)
                term_added_message = 'Added %s' % added_entry
                break
    return term_added_message
