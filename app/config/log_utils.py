import logging
import logging.handlers
import json


class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "time": self.formatTime(record, "%Y-%m-%dT%H:%M:%S"),
            "level": record.levelname,
            "module": record.module,
            "message": record.getMessage(),
        }
        return json.dumps(log_record, ensure_ascii=False)


class JSONSocketHandler(logging.handlers.SocketHandler):
    """JSON을 TCP로 전송하도록 설정 (Pickle 사용 금지)"""

    def makePickle(self, record):
        return (self.format(record) + "\n").encode("utf-8")
