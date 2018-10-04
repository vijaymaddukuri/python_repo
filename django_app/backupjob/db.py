from django_app.backupjob.messagebroker import MessageBroker

class DB(MessageBroker):
    """
    publish message to the DB.
    :param message: message.
    :return:
    """
    # This will change in Future.
    def publish_message(self, message):
        return "%s - %s" % ("DB", message)
