from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_handler
from mycroft.util.log import LOG

class InflacaoSkill(MycroftSkill):

    def __init__(self):
        super(InflacaoSkill, self).__init__(name='InflacaoSkill')

    # def initialize(self):
    #     self.register_intent_file('convert.intent', self.handle_ultimo_intent)

    @intent_handler(IntentBuilder('LaunchIntent').require('launch'))
    def handle_launch_intent(self, message):
        # LOG.debug(message)
        self.speak_dialog('launch')


    @intent_handler(IntentBuilder('UltimoIntent').require('ultimo'))
    def handle_ultimo_intent(self, message):

        LOG.debug('=== entrou no ultimo intent ===')
        self.speak('The type spoken is ' + type)

def create_skill():
    return InflacaoSkill()
