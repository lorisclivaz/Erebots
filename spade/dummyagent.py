import time
import os
import datetime
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, PeriodicBehaviour
from spade.message import Message

LOCAL = os.environ.get("XMPP_SERVER_ADDRESS", "localhost")


class PeriodicSenderAgent(Agent):
    class InformBehaviour(PeriodicBehaviour):
        def __init__(self, period, start_at=None):
            super().__init__(period, start_at=None)
            self.counter = 0

        async def run(self):
            print(f"PeriodicSenderBehaviour running at {datetime.datetime.now().time()}: {self.counter}")
            msg = Message(to="receiver@{}".format(LOCAL))  # Instantiate the message
            msg.body = "Hello World"  # Set the message content

            await self.send(msg)
            print("Message sent!")

            if self.counter == 60:
                self.kill()
            self.counter += 1

        async def on_end(self):
            # stop agent from behaviour
            await self.agent.stop()

        async def on_start(self):
            pass

    async def setup(self):
        print(f"PeriodicSenderAgent started at {datetime.datetime.now().time()}")
        start_at = datetime.datetime.now() + datetime.timedelta(seconds=5)
        b = self.InformBehaviour(period=4, start_at=start_at)
        self.add_behaviour(b)


class ReceiverAgent(Agent):
    class RecvBehaviour(CyclicBehaviour):
        async def run(self):
            print("RecvBehaviour running")
            msg = await self.receive(timeout=10)  # wait for a message for 10 seconds
            if msg:
                print("Message received with content: {}".format(msg.body))
            else:
                print("Did not received any message after 120 seconds")
                self.kill()

        async def on_end(self):
            await self.agent.stop()

    async def setup(self):
        print("ReceiverAgent started")
        b = self.RecvBehaviour()
        self.add_behaviour(b)


if __name__ == "__main__":
    receiver_agent = ReceiverAgent("receiver@{}".format(LOCAL), "receiver")
    future = receiver_agent.start()
    future.result()  # wait for receiver agent to be prepared.
    sender_agent = PeriodicSenderAgent("sender@{}".format(LOCAL), "sender")
    sender_agent.start()

    while receiver_agent.is_alive():
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            sender_agent.stop()
            receiver_agent.stop()
            break
    print("Agents finished")
