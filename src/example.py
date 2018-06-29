import logging


RESET = -1
OFFLINE = 0
EVENT_LOG = []


class Hub(object):
  __ITEM__ = {}

  def __init__(self):
    self.ident = None

  @staticmethod
  def get(ident):
    return Hub.get(ident)

  def update(self, **kwargs):
    for k, v in kwargs.items():
      setattr(self, k, v)


def remove(ident):
  if ident in Hub.__ITEM__:
    del Hub.__ITEM__[ident]


def _write(ident, topic, value):
  EVENT_LOG.append((ident, topic, value))


def _send_offline_message(hub_id):
  _write(hub_id, 'offline', {'hub_id': hub_id})


def update_value(hub_id, key, value):  # TODO: handle notify=True/False
  # TODO: CHECK
  logging.info("#HUB #UPDATE edge_id: %s, key:%s, value:%s",
               hub_id, key, value)
  _hub = Hub.get(hub_id)

  if _hub:
    yield _write(hub_id, 'update_value',
                 {'hub_id': hub_id, 'key': key, 'value': value})
    if key == 'status':
      if value == RESET:
        remove(hub_id)
        return True
      elif value == OFFLINE:
        _send_offline_message(hub_id)
        return True
    kwargs = {key: value}
    _hub.update(**kwargs)
  return True
