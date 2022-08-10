
class MeshUser:
    def __init__(self, app, user_id, network_number_property_id):
        self._app = app
        self.user_id = user_id
        self._fetched = False
        self._network_number_property_id = network_number_property_id

    def _fetch_profile(self):
        if self._fetched:
            return

        resp = self._app.client.users_profile_get(user=self.user_id)
        self._profile = resp.data['profile']


        self.fetched = True

    @property
    def email(self):
        self._fetch_profile()
        return self._profile['email']

    @property
    def network_number(self):
        self._fetch_profile()
        custom_field = self._profile.get('fields', {}).get(self._network_number_property_id, None)
        return custom_field['value'] if custom_field else None

