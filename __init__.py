from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_handler
from mycroft.util.parse import extract_datetime
from .utils import get_request_json
from mycroft.util.log import LOG

MONTH = {1:'janeiro',  2:'fevereiro', 3:u'março',    4:'abril',
               5:'maio',     6:'junho',    7:'julho',    8:'agosto',
               9:'setembro', 10:'outubro',  11:'novembro', 12:'dezembro'}

def parse_date(datetime):
    """
        Arg:
            datetime.datetime
    """

    date = datetime.date()

    dict = {
        'year': str(date.year),
        'month': MONTH[date.month],
        'day': str(date.day)
    }
    return dict

class InflacaoSkill(MycroftSkill):

    def __init__(self):
        super(InflacaoSkill, self).__init__(name='InflacaoSkill')

    # def initialize(self):
    #     self.register_intent_file('convert.intent', self.handle_ultimo_intent)

    @intent_handler(IntentBuilder('LaunchIntent').require('launch'))
    def handle_launch_intent(self, message):
        self.speak_dialog('launch')


    @intent_handler(IntentBuilder('UltimoIntent').require('ultimo').require('ipca'))
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

    @intent_handler(IntentBuilder('MensalIntent').require('ipca'))
    def handle_mensal_intent(self, message):
        utt = message.data.get('utterance').lower()
        when = extract_datetime(utt, lang='pt-br') # https://mycroft-core.readthedocs.io/en/stable/source/mycroft.util.html

        datetime = when[0]

        date_pt = parse_date(datetime)

        # LOG.debug('==== entered LOG ====')
        # LOG.debug('datetime' + str(datetime))

        speech_text = utt + ' ' + date_pt['year'] +  date_pt['month'] +  date_pt['day'] + ' ' + when[1]
        self.speak(speech_text)

def create_skill():
    return InflacaoSkill()
