from hbmqtt.plugins.topic_checking import BaseTopicPlugin

class AlfonsHBMQTTTopicPlugin(BaseTopicPlugin):
	def __init__(self, context):
		super().__init__(context)

	async def topic_filtering(self, *args, **kwargs):
		self.context.logger.debug("Topic checking - *args={} **kwargs={}".format(str(args), str(kwargs)))
		return True
