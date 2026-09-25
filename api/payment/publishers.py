from broker.broker import broker

async def payments_new_publish(message):
	await broker.publish(message, queue="payments.new")