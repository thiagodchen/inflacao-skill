# from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_file_handler
# from mycroft.util.parse import extract_datetime
from .utils import get_request_json
# from mycroft.util.log import LOG

ACCUMULATE_CODES = {
    'anual': '69',
    '3': '2263',
    '6': '2264',
    '12': '2265',
}

ACCUMULATE_SYN = {
    'três': '3',
    'três meses': '3',
    'seis': '6',
    'seis meses': '6',
    'doze': '12',
    'doze meses': '12',
    'trimestral': '3',
    'semestral': '6',
    'anual': 'anual',
    'um ano': 'anual',
    'no ano': 'anual',
    '3': '3',
    '6': '6',
    '12': '12',
}

MONTH_INTTOLIT = {1:'janeiro',  2:'fevereiro', 3:u'março',    4:'abril',
               5:'maio',     6:'junho',    7:'julho',    8:'agosto',
               9:'setembro', 10:'outubro',  11:'novembro', 12:'dezembro'}

MONTH_LITTONUM = {'janeiro': '01',  'fevereiro': '02', u'março': '03',    'abril': '04',
               'maio': '05',     'junho': '06',     'julho': '07',     'agosto': '08',
               'setembro': '09', 'outubro': '10',  'novembro': '11', 'dezembro': '12'}

def literal_to_int(s):
    num = {
        "zero":0,
        "um":1,
        "dois":2,
        "três":3,
        "quatro":4,
        "cinco":5,
        "seis":6,
        "sete":7,
        "oito":8,
        "nove":9,
        "dez":10,
        "onze":11,
        "doze":12,
        "treze":13,
        "quatorze":14,
        "quinze":15,
        "dezesseis":16,
        "dezessete":17,
        "dezoito":18,
        "dezenove":19,
        "vinte":20,
        "trinta":30,
        "quarenta":40,
        "cinquenta":50,
        "sessenta":60,
        "setenta":70,
        "oitenta":80,
        "noventa":90,
        "cem":100,
        "cento":100,
        "duzentos":200,
        "trezentos":300,
        "quatrocentos":400,
        "quinhentos":500,
        "seiscentos":600,
        "setecentos":700,
        "oitocentos":800,
        "novecentos":900
    }

    thousands = {
        "mil":1000,
        "milhão":1000000,
        "milhões":1000000,
        "bilhão":1000000000,
        "bilhões":1000000000
    }

    res = 0
    g = 0

    for i in s.split():
        if i in num:
            g += num[i]
        elif i in thousands:
            res += thousands[i] * (1 if g == 0 else g)
            g = 0
    res += g
    return res

def parse_date(datetime):
    """
        Arg:
            datetime.datetime
    """

    date = datetime.date()

    dict = {
        'year': str(date.year),
        'month': MONTH_INTTOLIT[date.month],
        'day': str(date.day)
    }
    return dict



class InflacaoSkill(MycroftSkill):

    def __init__(self):
        super(InflacaoSkill, self).__init__(name='InflacaoSkill')

    @intent_file_handler('launch.intent')
    def handle_launch_intent(self, message):
        self.speak_dialog('launch')


    @intent_file_handler('ultimo.intent')
    def handle_ultimo_intent(self, message):

        url = 'http://api.sidra.ibge.gov.br/values/h/n/t/1737/p/last/n1/all/v/63'

        response = get_request_json(url)
        response = response[0]

        value = response['V']
        date = response['D1N']
        date = date.split(' ')

        speech_text = ('A última variação do IPCA é de ' + value
                        + ' porcento, no período ' + date[0] + ' de ' + date[1] + '.')

        self.speak(speech_text)

    @intent_file_handler('mensal.intent')
    def handle_mensal_intent(self, message):
        # TODO: remove
        # utt = message.data.get('utterance').lower()

        month = message.data.get('month')
        year = message.data.get('year')
        # when = extract_datetime(utt, lang='pt-br') # https://mycroft-core.readthedocs.io/en/stable/source/mycroft.util.html
        # LOG.debug('==== entered LOG ====')
        # LOG.debug('datetime' + str(datetime))

        if len(month) != 2 and len(month) != 1:
            month = MONTH_LITTONUM[month]
        if len(year) != 4:
            year = literal_to_int(year)

        date = str(year) + month

        url = 'http://api.sidra.ibge.gov.br/values/h/n/t/1737/p/' + date + '/n1/all/v/63'

        response = get_request_json(url)
        response = response[0]

        value = response['V']
        date = response['D1N']
        date = date.split(' ')

        speech_text = ('A variação do IPCA é de ' + value
                        + ' porcento, no período ' + date[0] + ' de ' + date[1] + '.')

        self.speak(speech_text)


    @intent_file_handler('acumulado.intent')
    def handle_acumulado_intent(self, message):
        accumulate_time = message.data.get('accumulate_time')
        accumulate_code = ACCUMULATE_CODES[ACCUMULATE_SYN[accumulate_time]]

        url = 'http://api.sidra.ibge.gov.br/values/h/n/t/1737/p/last/n1/all/v/' + accumulate_code

        response = get_request_json(url)
        response = response[0]

        value = response['V']
        date = response['D1N']
        date = date.split(' ')

        speech_text = 'O IPCA acumulado nos últimos ' + accumulate_time + ' meses até ' + date[0] + ' de ' + date[1] + ' é '
        speech_text += value + ' porcento. ';

        self.speak(speech_text)

def create_skill():
    return InflacaoSkill()
