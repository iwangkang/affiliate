#! -*- coding:utf-8 -*-

"""
@author:Conner
@version:1.0
@date:13-8-19
@description:服务入口，启动监听
"""
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from tornado import ioloop, web
from tornado import options
from tornado import process

from affiliate.config import settings
from affiliate.views.tracking import CPCHandler, CPSHandler

SETTINGS = dict(
    template_path=os.path.join(os.path.dirname(sys.argv[0]), "templates"),
    static_path=os.path.join(os.path.dirname(sys.argv[0]), "static")
)


urls = [
    (r'/cpc', CPCHandler),
    (r'/cps', CPSHandler),
]


options.define('port', default=9897, type=int)
options.define('fork', default=1, type=int)


def main():
    options.parse_command_line()
    port = options.options.port
    fork = options.options.fork

    settings.configure('PROCESS', fork)
    settings.configure('PORT_GROUP', range(port, port + fork))

    process.fork_processes(fork, max_restarts=10)

    settings.configure('PORT', port + process.task_id())
    # settings.configure('PORT', port)

    app = web.Application(
        handlers=urls,  #逻辑指定
        **SETTINGS      #路径指定
    )
    app.listen(settings.port, xheaders=True)
    loop = ioloop.IOLoop.instance()
    loop.start()


if __name__ == '__main__':
    print('Development server running on "http://localhost:9897"')
    print('Quit the server with Control+C')
    main()


