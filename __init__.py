from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_handler
from mycroft.util.parse import extract_datetime
from .utils import get_request_json
from mycroft.util.log import LOG

class InflacaoSkill(MycroftSkill):

    def __init__(self):
        super(InflacaoSkill, self).__init__(name='InflacaoSkill')

    # def initialize(self):
    #     self.register_intent_file('convert.intent', self.handle_ultimo_intent)

    @intent_handler(IntentBuilder('LaunchIntent').require('launch'))
    def handle_launch_intent(self, message):
        LOG.debug('==== entered LOG ====')
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
        when = extract_datetime(utt)

        self.speak('when', str(when))

        LOG


def create_skill():
    return InflacaoSkill()
