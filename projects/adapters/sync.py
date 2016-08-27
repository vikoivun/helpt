class ModelSyncher(object):

    def __init__(self, queryset, generate_obj_id, delete_func=None,
                 delete_limit=0.4):
        d = {}
        self.generate_obj_id = generate_obj_id
        # Generate a list of all objects
        for obj in queryset:
            d[generate_obj_id(obj)] = obj
            obj._found = False
            obj._changed = False

        self.obj_dict = d
        self.delete_limit = delete_limit
        self.delete_func = delete_func

    def mark(self, obj):
        if getattr(obj, '_found', False):
            raise Exception("Object %s (%s) already marked" % (obj, self.generate_obj_id(obj)))

        obj._found = True
        obj_id = self.generate_obj_id(obj)
        if obj_id not in self.obj_dict:
            self.obj_dict[obj_id] = obj
        assert self.obj_dict[obj_id] == obj

    def get(self, obj_id):
        return self.obj_dict.get(obj_id, None)

    def finish(self):
        delete_list = []
        for obj_id, obj in self.obj_dict.items():
            if not obj._found:
                delete_list.append(obj)

        max_delete_count = len(self.obj_dict) * self.delete_limit
        if len(delete_list) > 5 and len(delete_list) > max_delete_count:
            raise Exception("Attempting to delete more than %d%% of total items" % int(self.delete_limit * 100))

        for obj in delete_list:
            if self.delete_func:
                self.delete_func(obj)
            else:
                print("Deleting object %s" % obj)
                obj.delete()
