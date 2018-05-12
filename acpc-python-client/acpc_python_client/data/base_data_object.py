class BaseDataObject(object):
    def __init__(self, wrapper):
        super().__init__()
        self._data_holder = wrapper.contents if hasattr(wrapper, 'contents') else wrapper
