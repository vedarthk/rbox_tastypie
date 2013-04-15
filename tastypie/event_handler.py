from tastypie.exceptions import TastypieError, Unauthorized
from django.utils import importlib


class EventHandler(object):
    """
    A base class that provides basic structure of what events are raised
    """

    def __get__(self, instance, owner):
        """
        Makes ``EventManager`` a descriptor of ``ResourceOptions`` and creates
        a reference to the ``ResourceOptions`` object that may be used by
        methods of ``BasicEventManager``.
        """
        self.resource_meta = instance
        return self

    #Get method handlers
    def pre_read_list(self, object_list, bundle):
        """
        Called before get_list is executed.
        object_list: list of authorized objects that can be read by the user
        bundle: plain bundle - does not have obj or data populated
        """
        pass

    def post_read_list(self, object_list, bundle):
        """
        Called after get_list is executed.
        object_list: list of authorized objects that can be read by the user
        bundle: plain bundle - does not have obj or data populated
        """
        pass

    def pre_read_detail(self, object_list, bundle):
        """
        Called before dehydrate object is executed.
        object_list: list of authorized objects that can be read by the user
        bundle: bundle - bundle.obj is the object being requested. dehydration is not yet called
        """

        pass

    def post_read_detail(self, object_list, bundle):
        """
        Called after dehydrate object is executed.
        object_list: list of authorized objects that can be read by the user
        bundle: bundle - bundle.obj is the object being requested. dehydration is already 
        executed and bundle.data has dehydrated data
        """
        pass


    #Post method handlers
    '''
    #Not implemented currently
    def pre_create_list(self, object_list, bundle):
        pass

    def post_create_list(self, object_list, bundle):
        pass
    '''

    def pre_create_detail(self, object_list, bundle):
        pass

    def post_create_detail(self, object_list, bundle):
        pass

    #put method handlers
    def pre_update_detail(self, object_list, bundle):
        pass

    def post_update_detail(self, object_list, bundle):
        pass

    def pre_update_list(self, object_list, bundle):
        pass

    def post_update_list(self, object_list, bundle):
        pass


    #delete method handlers
    def pre_delete_list(self, object_list, bundle):
        pass

    def post_delete_list(self, object_list, bundle):
        pass

    def pre_delete_detail(self, object_list, bundle):
        pass

    def post_delete_detail(self, object_list, bundle):
        pass


class MultiEventHandler(EventHandler):

    def __init__(self, event_handlers=[], *args, **kwargs):
        self.event_handlers = event_handlers
        self._event_handlers = None
        super(MultiEventHandler,self).__init__(*args, **kwargs)

    def resolve_class_by_name(self, cls_path):
        if not isinstance(cls_path , basestring):
            return cls_path
        # It's a string. Let's figure it out.
        if '.' in cls_path:
            # Try to import.
            module_bits = cls_path.split('.')
            module_path, class_name = '.'.join(module_bits[:-1]), module_bits[-1]
            module = importlib.import_module(module_path)
        else:
            # We've got a bare class name here, which won't work (No AppCache
            # to rely on). Try to throw a useful error.
            raise ImportError("Tastypie requires a Python-style path (<module.module.Class>) to lazy load event handlers. Only given '%s'." % self.to)

        cls = getattr(module, class_name, None)

        if cls is None:
            raise ImportError("Module '%s' does not appear to have a class called '%s'." % (module_path, class_name))
        return cls

    def get_event_handlers(self):
        if not self._event_handlers:
            self._event_handlers =  [self.resolve_class_by_name(cls) for cls in self.event_handlers]
        return self._event_handlers

    def read_list_handlers(self):
        return self.get_event_handlers()

    def read_detail_handlers(self):
        return self.get_event_handlers()

    def create_detail_handlers(self):
        return self.get_event_handlers()

    def update_detail_handlers(self):
        return self.get_event_handlers()

    def update_list_handlers(self):
        return self.get_event_handlers()

    def delete_list_handlers(self):
        return self.get_event_handlers()

    def delete_detail_handlers(self):
        return self.get_event_handlers()


    def pre_read_list(self, object_list, bundle):
        for event_handler in self.read_list_handlers():
            event_handler.pre_read_list(object_list, bundle)

    def post_read_list(self, object_list, bundle):
        for event_handler in self.read_list_handlers():
            event_handler.post_read_list(object_list, bundle)

    def pre_read_detail(self, object_list, bundle):
        for event_handler in self.read_detail_handlers():
            event_handler.pre_read_detail(object_list, bundle)

    def post_read_detail(self, object_list, bundle):
        for event_handler in self.read_detail_handlers():
            event_handler.post_read_detail(object_list, bundle)

    #Post method handlers
    def pre_create_detail(self, object_list, bundle):
        for ev in self.create_detail_handlers():
            ev.pre_create_detail(object_list, bundle)

    def post_create_detail(self, object_list, bundle):
        for ev in self.create_detail_handlers():
            ev.post_create_detail(object_list, bundle)

    #put method handlers
    def pre_update_detail(self, object_list, bundle):
        for ev in self.update_detail_handlers():
            ev.pre_update_detail(object_list, bundle)

    def post_update_detail(self, object_list, bundle):
        for ev in self.update_detail_handlers():
            ev.post_update_detail(object_list, bundle)

    def pre_update_list(self, object_list, bundle):
        for ev in self.update_list_handlers():
            ev.pre_update_list(object_list, bundle)

    def post_update_list(self, object_list, bundle):
        for ev in self.update_list_handlers():
            ev.post_update_list(object_list, bundle)


    #delete method handlers
    def pre_delete_list(self, object_list, bundle):
        for ev in self.delete_list_handlers():
            ev.pre_delete_list(object_list, bundle)

    def post_delete_list(self, object_list, bundle):
        for ev in self.delete_list_handlers():
            ev.post_delete_list(object_list, bundle)

    def pre_delete_detail(self, object_list, bundle):
        for ev in self.delete_detail_handlers():
            ev.pre_delete_detail(object_list, bundle)

    def post_delete_detail(self, object_list, bundle):
        for ev in self.delete_detail_handlers():
            ev.post_delete_detail(object_list, bundle)


