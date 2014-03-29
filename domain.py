from coopy.decorators import readonly

class UserRepo(object):
    def __init__(self, *args, **kwargs):
        self.users = {}
        self.relations = []

    def add_user_relation(self, user_id, screen_name, followers):
        if user_id in self.users.keys():
            self.users['user_id'] = None

        self.user[user_id]['screen_name'] = screen_name
        self.user[user_id]['followers'] = followers

        for saved_user in self.users:
            if user_id in saved_user['followers']:
                self.relations.append((user_id, saved_user))

    @readonly
    def retrieve_as_graph(self):
        response = {}
        response['nodes'] = []
        for user, content in self.users.iteritems():
            response['nodes'].append({
                'name': content['screen_name'],
                'id': user
            })

        response['edges'] = []
        for source, target in self.relations:
            response['edges'].append({
                'source': source,
                'target': target
            })

        return response

