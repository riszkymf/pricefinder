




class DataTable(object):
    raw_data = None
    table_head = None
    table_data = None

    def __init__(self):
        self.raw_data = dict()
        self.table_data = dict()
        self.table_head = list()

    def append_headers(self,head):
        if head not in self.table_head:
            self.table_data[head] = list()
            self.table_head.append(head)
        
    def add_data(self,head,data):
        self.table_data[head].append(data)
