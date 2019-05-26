import requests


class ExecuteAPICall:
    """
    The Generic Class for ALl API call and related helper function needs in the ROBOT File.
    """
    def api_call(self, url, device_id):
        """
        :param :
               url : REST API url for unique device id of the speaker
        :return:
               response : response body of the API which is the Domain and the Role
        """

        try:
            response = requests.get(url+device_id)

        except Exception as e:
            logger.info("Exception {} occurred while calling API".format(e))

        return response

