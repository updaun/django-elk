import traceback
import logging.handlers
import logging
import json
from config.middleware import get_current_request, get_current_response


class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "time": self.formatTime(record, "%Y-%m-%dT%H:%M:%S"),
            "level": record.levelname,
            "module": record.module,
            "message": record.getMessage(),
            "name": record.name,
            "pathname": record.pathname,
            "filename": record.filename,
            "funcName": record.funcName,
            "lineno": record.lineno,
            "process": record.process,
            "thread": record.thread,
            "threadName": record.threadName,
        }

        # 예외 발생 시 스택 트레이스 추가
        if record.exc_info:
            log_record["exception"] = traceback.format_exc()

        # 요청 정보 추가 (RequestFilter가 설정된 경우)
        if hasattr(record, "method"):
            log_record["method"] = record.method
        if hasattr(record, "path"):
            log_record["path"] = record.path
        if hasattr(record, "status_code"):
            log_record["status_code"] = record.status_code
        if hasattr(record, "remote_addr"):
            log_record["remote_addr"] = record.remote_addr
        if hasattr(record, "user"):
            log_record["user"] = record.user
        if hasattr(record, "user_agent"):
            log_record["user_agent"] = record.user_agent

        return json.dumps(log_record, ensure_ascii=False)


class JSONSocketHandler(logging.handlers.SocketHandler):
    """JSON을 TCP로 전송하도록 설정 (Pickle 사용 금지)"""

    def makePickle(self, record):
        return (self.format(record) + "\n").encode("utf-8")


class RequestFilter(logging.Filter):
    """Django 요청 정보를 로그에 추가하는 필터"""

    def filter(self, record):
        request = get_current_request()
        response = get_current_response()
        if request:
            record.method = request.method  # HTTP 메서드
            record.path = request.get_full_path()  # 요청 경로
            record.remote_addr = request.META.get("REMOTE_ADDR", "")  # 클라이언트 IP
            record.user = (
                request.user.username if request.user.is_authenticated else "Anonymous"
            )
            record.user_agent = request.META.get("HTTP_USER_AGENT", "")  # 브라우저 정보

        if response:
            record.status_code = response.status_code
        return True
