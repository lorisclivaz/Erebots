import json


class WebSocketMessageUtils:

    @staticmethod
    def preprocess_for_websocket(some_json_payload: dict) -> bytes:
        """
        Utility function to preprocess a dictionary and transform it to a string suitable to be
        sent through a websocket
        """
        return json.dumps(some_json_payload, ensure_ascii=False).encode('utf8')
