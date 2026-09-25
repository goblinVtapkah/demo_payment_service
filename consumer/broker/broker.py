from faststream.rabbit import RabbitBroker, Channel
from core.config import get_settings

settings = get_settings()

broker = RabbitBroker(
	settings.rabbitmq_url,
	default_channel=Channel(prefetch_count=1),
)